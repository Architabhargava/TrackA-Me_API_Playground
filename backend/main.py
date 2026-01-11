from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import models
import crud
from database import engine, SessionLocal
from schemas import ProfileCreate, ProfileUpdate

# Create database tables
models.Base.metadata.create_all(bind=engine)

# ✅ CREATE APP FIRST
app = FastAPI(title="TrackA-Me API")

# ✅ THEN ADD MIDDLEWARE
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/profile")
def create_profile(profile: ProfileCreate, db: Session = Depends(get_db)):
    return crud.create_profile(db, profile)

@app.get("/profile/{profile_id}/edit")
def get_profile_for_edit(profile_id: int, db: Session = Depends(get_db)):
    profile = crud.get_profile_for_update(db, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@app.put("/profile/{profile_id}")
def update_profile(
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
    profiles = crud.search_profiles_by_skill(db, skill)
    return [
        {
            "name": p.name,
            "email": p.email,
            "skills": [s.name for s in p.skills]
        }
        for p in profiles
    ]
