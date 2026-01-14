# Engineering Decisions & Detailed Iteration Log ->

**TrackA-Me-API-Playground**

This document captures the engineering thought process behind TrackA‑Me. It explains what decisions were made, what alternatives existed, what failed during development, and how those failures improved the final system.

## Initial Design Phase

The project began as a simple CRUD API. As development progressed, additional non‑functional requirements such as
authentication, rate limiting, testing, CI, and deployment were added incrementally.

## Technology Trade-offs

Several technology choices were evaluated:

• Flask vs FastAPI → FastAPI chosen for typing and docs

• SQLite vs PostgreSQL → SQLite chosen for simplicity

• Vanilla JS vs React → Vanilla JS chosen to focus on backend logic

Each decision favored clarity and correctness over scale.


## Why These Technology Choices?

### FastAPI

Chosen over Flask/Django because:-

* built-in request validation (Pydantic)
* automatic Swagger documentation

* explicit dependency injection
* clean async-ready design

### SQLAlchemy

Used to:-

* define clear models
* enforce relationships

* maintain explicit database control
* avoid raw SQL scattered across code

### SQLite

Chosen intentionally because:-

* simple to set up
* reproducible across environments

* sufficient for a take-home / demo project

(PostgreSQL was considered but rejected to avoid unnecessary infra complexity.)

### Vanilla JavaScript Frontend

Chosen over React/Vue because:-

* focus remains on backend engineering
* no framework overhead

* easier for reviewers to follow logic


## Authentication Design (Why Basic Auth?)

Alternatives considered:

• JWT → unnecessary token complexity

• OAuth → out of scope

Basic Auth was chosen because:

• explicit

• stateless

• easy to reason about

• clearly demonstrates protected routes


## Authentication Visibility Issue

Authentication initially worked but was not visible in Swagger.

Cause:

• Security scheme not explicitly declared

Fix:

• Switched from Depends() to Security() so Swagger could expose the Authorize button


## Dependency & Environment Failures

Early CI failures revealed dependency conflicts caused by a polluted virtual environment.

Resolution:

• Minimal requirements.txt

• Fresh dependency installation in CI


## Rate Limiting Behavior

While testing, creating a 6th profile caused failures. This was intentional due to rate limiting and helped validate
protective behavior.

## Database Integrity Errors

Unique constraint violations occurred when empty or duplicate emails were submitted.

Fix:

• Frontend validation

• Backend IntegrityError handling

• Clear HTTP 400 responses

## Testing & CI Learnings

CI surfaced hidden assumptions such as missing PYTHONPATH and middleware requirements. Fixing these improved system robustness.

## Final Reflection

TrackA‑Me reflects a realistic engineering journey. The final system is intentionally simple but robust, explainable, and
defensible.
