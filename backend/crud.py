"""
This file contains all database interaction logic.

Separating CRUD logic from API routes:
- Keeps code clean
- Improves maintainability
- Follows service-layer architecture
"""

from sqlalchemy.orm import Session
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from models import Profile, Skill, Project
from schemas import ProfileCreate
from fallbacks import FaLLBACKS


# ---------------- SKILL HELPERS ---------------- #

def normalize_skill_name(skill: str) -> str:
    """
    Converts a skill input into its canonical form
    using predefined aliases.
    """
    if not skill:
        return ""

    skill_clean = skill.strip().lower()

    for canonical, aliases in FaLLBACKS.items():
        if skill_clean == canonical:
            return canonical
        if skill_clean in aliases:
            return canonical

    return skill_clean


def extract_skills_from_text(text: str) -> set[str]:
    """
    Extracts skills from free text like tech stack or description
    using keyword matching.
    """
    if not text:
        return set()

    text = text.lower()
    detected_skills = set()

    for canonical, keywords in FaLLBACKS.items():
        for keyword in keywords:
            if keyword in text:
                detected_skills.add(canonical)

    return detected_skills


def get_or_create_skill(db: Session, name: str):
    """
    Normalizes skill names before storing to avoid duplicates
    like 'AI', 'ai', 'Artificial Intelligence'.
    """
    canonical_name = normalize_skill_name(name)
    if not canonical_name:
        return None

    skill = db.query(Skill).filter(Skill.name == canonical_name).first()

    if not skill:
        skill = Skill(name=canonical_name)
        db.add(skill)
        db.commit()
        db.refresh(skill)

    return skill


# ---------------- CREATE PROFILE ---------------- #

def create_profile(db: Session, data: ProfileCreate):
    """
    Creates a new profile with:
    - explicit skills
    - inferred skills from projects
    - proper integrity handling
    """

    # Backend-level validation (never trust frontend)
    if not data.email or not data.email.strip():
        raise HTTPException(
            status_code=400,
            detail="Email is required and must be unique"
        )

    profile = Profile(
        name=data.name,
        email=data.email.strip(),
        education=data.education,
        work=data.work,
        links=data.links
    )

    # 1. Explicit skills
    explicit_skills = {
        normalize_skill_name(skill)
        for skill in data.skills
        if skill
    }

    # 2. Inferred skills from projects
    inferred_skills = set()
    for proj in data.projects:
        inferred_skills |= extract_skills_from_text(proj.tech_stack)
        inferred_skills |= extract_skills_from_text(proj.description)

    all_skills = explicit_skills | inferred_skills

    for skill_name in all_skills:
        skill = get_or_create_skill(db, skill_name)
        if skill:
            profile.skills.append(skill)

    # 3. Attach projects
    for proj in data.projects:
        project = Project(
            title=proj.title,
            description=proj.description,
            tech_stack=proj.tech_stack
        )
        profile.projects.append(project)

    db.add(profile)

    try:
        db.commit()
        db.refresh(profile)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Profile with this email already exists"
        )

    return profile


# ---------------- READ OPS ---------------- #

def get_all_profiles(db: Session):
    """Returns all profiles stored in the system."""
    return db.query(Profile).all()


def search_profiles_by_skill(db: Session, skill: str):
    """
    Searches profiles using skill aliases and canonical names.
    """
    normalized = normalize_skill_name(skill)
    possible_terms = {normalized}

    for canonical, aliases in FaLLBACKS.items():
        if canonical == normalized:
            possible_terms.update(aliases)

    query = db.query(Profile).join(Profile.skills)

    filters = [
        Skill.name.ilike(f"%{term}%")
        for term in possible_terms
        if term
    ]

    return query.filter(or_(*filters)).all()


# ---------------- UPDATE PROFILE ---------------- #

def update_profile(db: Session, profile_id: int, data):
    profile = db.query(Profile).filter(Profile.id == profile_id).first()

    if not profile:
        return None

    # 1. Update basic fields (email intentionally NOT editable)
    for field in ["name", "education", "work", "links"]:
        value = getattr(data, field)
        if value is not None:
            setattr(profile, field, value)

    # 2. Update projects (replace strategy)
    if data.projects is not None:
        profile.projects.clear()
        for proj in data.projects:
            project = Project(
                title=proj.title,
                description=proj.description,
                tech_stack=proj.tech_stack
            )
            profile.projects.append(project)

    # 3. Recompute skills
    if data.skills is not None or data.projects is not None:
        profile.skills.clear()

        explicit_skills = set()
        if data.skills:
            explicit_skills = {
                normalize_skill_name(skill)
                for skill in data.skills
                if skill
            }

        inferred_skills = set()
        for proj in profile.projects:
            inferred_skills |= extract_skills_from_text(proj.tech_stack)
            inferred_skills |= extract_skills_from_text(proj.description)

        all_skills = explicit_skills | inferred_skills

        for skill_name in all_skills:
            skill = get_or_create_skill(db, skill_name)
            if skill:
                profile.skills.append(skill)

    db.commit()
    db.refresh(profile)
    return profile


# ---------------- EDIT PREFILL ---------------- #

def get_profile_for_update(db: Session, profile_id: int):
    profile = db.query(Profile).filter(Profile.id == profile_id).first()

    if not profile:
        return None

    return {
        "name": profile.name,
        "education": profile.education,
        "work": profile.work,
        "links": profile.links,
        "skills": [s.name for s in profile.skills],
        "projects": [
            {
                "title": p.title,
                "description": p.description,
                "tech_stack": p.tech_stack
            }
            for p in profile.projects
        ]
    }
