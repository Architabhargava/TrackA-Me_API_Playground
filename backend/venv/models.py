"""
This file defines the database schema using SQLAlchemy models.

The design is normalized to follow real-world practices:
- Profile can have multiple skills
- Skills can belong to multiple profiles (many-to-many)
- Profile can own multiple projects
"""

from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

# Association table for many-to-many relationship
# between profiles and skills
profile_skills = Table(
    "profile_skills",
    Base.metadata,
    Column("profile_id", ForeignKey("profiles.id")),
    Column("skill_id", ForeignKey("skills.id")),
)

class Profile(Base):
    """
    Stores basic user information.
    Acts as the central entity of the system.
    """
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    education = Column(Text)
    work = Column(Text)
    links = Column(Text)

    # Relationship mappings
    skills = relationship(
        "Skill",
        secondary=profile_skills,
        back_populates="profiles"
    )

    projects = relationship(
        "Project",
        back_populates="owner"
    )

class Skill(Base):
    """
    Stores unique skills.
    Shared across multiple profiles.
    """
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    profiles = relationship(
        "Profile",
        secondary=profile_skills,
        back_populates="skills"
    )

class Project(Base):
    """
    Stores project details linked to a profile.
    """
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    tech_stack = Column(Text)

    profile_id = Column(Integer, ForeignKey("profiles.id"))
    owner = relationship("Profile", back_populates="projects")
from datetime import datetime
from sqlalchemy import DateTime

