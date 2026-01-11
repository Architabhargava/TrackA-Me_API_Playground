"""
Main application entry point.

This file:
- Initializes FastAPI
- Registers routes
- Manages DB sessions
"""
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from schemas import ProfileUpdate
from fastapi import HTTPException


import models
from database import engine, SessionLocal
import crud
from schemas import ProfileCreate

# Create database tables on app startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Profile Playground API")

def get_db():
    """
    Dependency that provides a database session
    for each request and ensures cleanup.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health")
def health_check():
    """
    Health check endpoint used for monitoring
    and deployment validation.
    """
    return {"status": "ok"}

@app.post("/profile")
def create_profile(profile: ProfileCreate, db: Session = Depends(get_db)):
    """
    Creates a new profile with skills and projects.
    """
    return crud.create_profile(db, profile)

@app.get("/profile/{profile_id}/edit")
def get_profile_for_edit(
    profile_id: int,
    db: Session = Depends(get_db)
):
    profile = crud.get_profile_for_update(db, profile_id)

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    return profile

@app.put("/profile/{profile_id}")
def update_profile_api(
    profile_id: int,
    profile: ProfileUpdate,
    db: Session = Depends(get_db)
):
    updated = crud.update_profile(db, profile_id, profile)

    if not updated:
        raise HTTPException(status_code=404, detail="Profile not found")

    return {
        "message": "Profile updated successfully",
        "id": updated.id,
        "skills": [s.name for s in updated.skills],
        "projects": [p.title for p in updated.projects]
    }


@app.get("/profiles")
def list_profiles(db: Session = Depends(get_db)):
    """
    Returns a summarized view of all profiles.
    """
    profiles = crud.get_all_profiles(db)
    return [
        {
            "id": p.id,
            "name": p.name,
            "skills": [s.name for s in p.skills],
            "projects": [proj.title for proj in p.projects]
        }
        for p in profiles
    ]

@app.get("/profiles/search")
def search_profiles(skill: str, db: Session = Depends(get_db)):
    """
    Searches profiles based on a skill keyword.
    """
    profiles = crud.search_profiles_by_skill(db, skill)
    return [
        {
            "name": p.name,
            "email": p.email,
            "skills": [s.name for s in p.skills]
        }
        for p in profiles
    ]
