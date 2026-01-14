from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from fastapi import Request

import secrets


import models
import crud
from database import engine, SessionLocal
from schemas import ProfileCreate, ProfileUpdate
from logger import logger

# ---------------- APP INIT ----------------
app = FastAPI(title="TrackA-Me API")

models.Base.metadata.create_all(bind=engine)

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- RATE LIMIT ----------------
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={"detail": "Too many requests"}
    )

# ---------------- AUTH ----------------
security = HTTPBasic()

def verify_user(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "admin")
    correct_password = secrets.compare_digest(credentials.password, "trackame123")

    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

    return credentials.username

# ---------------- DB DEP ----------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- ROUTES ----------------
@app.get("/health")
def health():
    return {"status": "ok"}

# -------- CREATE (AUTH + RATE LIMITED) --------
@app.post("/profile")
@limiter.limit("5/minute")
def create_profile(
    request: Request,   # ✅ REQUIRED by slowapi
    profile: ProfileCreate,
    db: Session = Depends(get_db),
    user=Depends(verify_user)
):

    logger.info("Creating profile for %s", profile.email)
    p = crud.create_profile(db, profile)
    return {"id": p.id, "message": "Profile created successfully"}

# -------- UPDATE (AUTH) --------
@app.put("/profile/{profile_id}")
def update_profile(
    profile_id: int,
    profile: ProfileUpdate,
    db: Session = Depends(get_db),
    user=Depends(verify_user)
):
    logger.info("Updating profile %s", profile_id)
    updated = crud.update_profile(db, profile_id, profile)
    if not updated:
        raise HTTPException(status_code=404, detail="Profile not found")
    return {"message": "Profile updated"}

# -------- PREFILL EDIT --------
@app.get("/profile/{profile_id}/edit")
def get_profile_for_edit(profile_id: int, db: Session = Depends(get_db)):
    profile = crud.get_profile_for_update(db, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

# -------- LIST PROFILES (PAGINATED) --------
@app.get("/profiles")
def list_profiles(
    page: int = 1,
    size: int = 10,
    db: Session = Depends(get_db)
):
    offset = (page - 1) * size
    profiles = db.query(models.Profile).offset(offset).limit(size).all()

    return [
        {
            "id": p.id,
            "name": p.name,
            "skills": [s.name for s in p.skills]
        }
        for p in profiles
    ]

# -------- SEARCH --------
@app.get("/profiles/search")
def search_profiles(skill: str, db: Session = Depends(get_db)):
    profiles = crud.search_profiles_by_skill(db, skill)
    return [
        {
            "id": p.id,
            "name": p.name,
            "skills": [s.name for s in p.skills]
        }
        for p in profiles
    ]
