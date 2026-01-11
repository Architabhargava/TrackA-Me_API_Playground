"""
This file defines Pydantic schemas.

Schemas:
- Validate incoming API data
- Control the shape of API responses
- Act as a contract between frontend and backend
"""

from pydantic import BaseModel, Field
from typing import List

class ProjectBase(BaseModel):
    title: str = Field(
        example="Forest Fire Detection System",
        description="Title of the project"
    )
    description: str | None = Field(
        default=None,
        example="ML-based system to detect forest fires using IoT sensors"
    )
    tech_stack: str | None = Field(
        default=None,
        example="Python, FastAPI, Random Forest, Raspberry Pi"
    )

class ProfileCreate(BaseModel):
    name: str = Field(
        example="Enter your full name"
    )
    email: str = Field(
        example="Enter your email address"
    )
    education: str | None = Field(
        default=None,
        example="BTech CSE, 3rd Year"
    )
    work: str | None = Field(
        default=None,
        example="ML Intern at FUDR"
    )
    links: str | None = Field(
        default=None,
        example="GitHub: https://github.com/username | LinkedIn: https://linkedin.com/in/username"
    )

    skills: List[str] = Field(
        default=[],
        example=["Python", "Machine Learning", "FastAPI"]
    )

    projects: List[ProjectBase] = Field(
        default=[],
        example=[
            {
                "title": "Retail Shelf AI",
                "description": "Detects empty shelves using computer vision",
                "tech_stack": "Python, OpenCV, YOLO"
            }
        ]
    )

    
class ProfileOut(BaseModel):
    """
    Simplified output schema used for responses.
    """
    id: int
    name: str
    email: str
    skills: List[str]
    projects: List[str]

    class Config:
        from_attributes = True

from pydantic import BaseModel, Field
from typing import List, Optional

class ProfileUpdate(BaseModel):
    """
    Used for updating an existing profile.
    All fields are optional to support partial updates.
    """
    name: Optional[str] = None
    education: Optional[str] = None
    work: Optional[str] = None
    links: Optional[str] = None

    skills: Optional[List[str]] = None
    projects: Optional[List[ProjectBase]] = None

