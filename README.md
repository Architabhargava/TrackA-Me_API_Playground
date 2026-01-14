# TrackA-Me-API-Playground -

# (End-to-End Profile Management System)

TrackA-Me is a deliberately engineered
full-stack application built to demonstrate how I approach real software
engineering problems - not just making something work, but making it clean,
explainable, debuggable, deployable, and testable.

This project goes beyond basic CRUD by intentionally incorporating:-

**authentication, rate limiting, database integrity, search with fallbacks,
CI/CD, deployment, and frontend–backend integration.**

This README is intentionally long and explicit so that anyone reviewing the
project can understand what exists, why it exists, how it works, and how to use
it without external explanation.

## Live URLs

Frontend (Netlify):
[https://archita-me-api-playground.netlify.app]([https://archita-me-api-playground.netlify.app]() "frontend")

Backend (Render): [https://tracka-me-api-playground.onrender.com]([https://archita-me-api-playground.netlify.app]() "Backend - to check logs")

Swagger / OpenAPI Docs: [https://tracka-me-api-playground.onrender.com/docs](https://archita-me-api-playground.netlify.app "Fast API Swagger UI")

## Problem Statement

The goal was to build a profile management
system where profiles can be **created, viewed, updated, and searched by skill**. The
project intentionally focuses not just on functionality, but on engineering
concerns such as validation, security, reliability, and maintainability.

## High-Level Architecture

The system follows a simple client–server
architecture:

• **Frontend**: Static HTML, CSS, Vanilla JavaScript (Netlify)

• **Backend**: FastAPI application (Render)

• **Database**: SQLite managed via SQLAlchemy ORM

This separation keeps responsibilities clear and avoids unnecessary coupling.

## Repository Structure

backend/

  ├── main.py        → API routes, auth, middleware, rate
limiting

  ├── crud.py        → All database interaction logic

  ├── models.py      → SQLAlchemy models

  ├── schemas.py     → Pydantic schemas

  ├── database.py   → DB engine & session management

  ├── fallbacks.py  → Skill aliases and normalization

  ├── tests/        → Pytest test cases

frontend/

  ├── index.html    → UI structure

  ├── script.js     → API calls & auth handling

  └── styles.css

  │
  ├── .github/workflows/
  │   └── ci.yml          → GitHub Actions CI pipeline
  │
  └── README.md

  └── Engineering_Decisions.md

## Backend Flow (End-to-End)

### 1. Request enters `main.py`

* Route is matched
* Auth is checked (for write operations)
* Rate limit is enforced (for profile creation)

### 2. Request is validated

* Using Pydantic schemas (`schemas.py`)
* Invalid input is rejected early

### 3. Business logic is delegated

* `main.py` **never touches DB directly**
* All DB operations go through `crud.py`

### 4. Database interaction

* SQLAlchemy models (`models.py`)
* Integrity constraints enforced at DB level
* Errors handled cleanly (no crashes)

### 5. Response returned

* Clean JSON
* Appropriate HTTP status codes

## Core Features

### Profile Management

* Create profile
* View all profiles
* Edit/update profiles using prefilled data
* Pagination support

### Skill Handling

* Skills are normalized (`AI`, `ai`, `Artificial Intelligence` → `ai`)
* Skill aliases defined in `fallbacks.py`
* Auto-tagging from project descriptions and tech stack

### Search

* Search profiles by skill
* Alias-aware matching
* Case-insensitive search

## Authentication & Authorization

Write operations are protected using HTTP
Basic Authentication.

Credentials (IMPORTANT):

**User ID: Predusk**

**Password: tracka**

Only create and update operations require authentication. Read operations are
intentionally public.

## Rate Limiting

Profile creation is rate limited to 5
requests per minute per IP. Exceeding this limit returns HTTP 429 (Too Many
Requests).

## Database Design & Integrity

### Relationships

* Profiles ↔ Skills → many-to-many
* Profiles ↔ Projects → one-to-many

### Important Constraint

* **Email is UNIQUE**

Why?

* Ensures real-world data integrity
* Prevents duplicate profiles

### Handling Errors

* Empty email → rejected
* Duplicate email → HTTP 400 with clean message
* No unhandled crashes

## Testing Strategy

* Tests written using **pytest**
* Focused on core API behavior
* Designed to catch:
  * schema issues
  * route failures
  * configuration errors

## CI Pipeline (GitHub Actions)

* Runs on every push to `main`
* Steps:
  * install dependencies
  * run tests in clean environment

**CI ensures:**

* no hidden local dependencies
* reproducible builds
* confidence in changes

## Logging

* Backend logs important operations
* Logs visible in Render dashboard
* Used during debugging and validation

## Known Limitations

• SQLite is not designed for high concurrency

• No role-based access control

• HTTP Basic Auth is minimal and not production-grade

• UI is functional rather than polished

## Future Improvements

* JWT authentication
* PostgreSQL database
* Role-based permissions
* React frontend
* Fuzzy search & ranking
* Monitoring & metrics

## References

FastAPI: https://fastapi.tiangolo.com/

SQLAlchemy: https://docs.sqlalchemy.org/

Pydantic: https://docs.pydantic.dev/

SlowAPI: https://slowapi.readthedocs.io/

pytest: https://docs.pytest.org/

HTTP Basic Auth RFC: https://datatracker.ietf.org/doc/html/rfc7617

GitHub Actions: https://docs.github.com/en/actions

Render: https://render.com/docs

Netlify: https://docs.netlify.com/
