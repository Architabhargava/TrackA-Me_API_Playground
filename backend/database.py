"""
This file is responsible for setting up the database connection.

We use SQLite because:
- It requires zero setup
- It is lightweight
- Perfect for assignments and prototypes

SQLAlchemy is used as the ORM to interact with the database
using Python objects instead of raw SQL.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite database stored locally as profile.db
DATABASE_URL = "sqlite:///./profile.db"

# Engine is the core interface to the database
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # Required for SQLite with FastAPI
)

# Each request will get its own database session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for all ORM models
Base = declarative_base()
