# Student CRUD

**Module:** 5 — FastAPI Development
**Estimated time:** 50 minutes

## Objective

Build a full CRUD (Create, Read, Update, Delete) API for student records with a SQLite database, including both PUT (full replace) and PATCH (partial update) operations.

## What You'll Do

1. In `app/database.py`, set up the SQLAlchemy engine, `SessionLocal`, and `get_db()` dependency.
2. In `app/models/student.py`, define the `Student` ORM model with columns: id, name, email (unique), major, gpa.
3. In `app/schemas/student.py`, define four schemas:
   - `StudentCreate` — required fields for creation (with email validation).
   - `StudentUpdate` — all fields for PUT (full replacement).
   - `StudentPatch` — all optional fields for PATCH (partial update).
   - `StudentResponse` — adds id and `from_attributes` config.
4. In `app/routers/students.py`, implement all six endpoints:
   - `POST /` — create a student, handle duplicate email with 409.
   - `GET /` — list students with optional major and min_gpa query filters.
   - `GET /{student_id}` — get one student or 404.
   - `PUT /{student_id}` — fully replace a student record.
   - `PATCH /{student_id}` — partially update using `model_dump(exclude_unset=True)`.
   - `DELETE /{student_id}` — delete a student or 404.
5. In `app/main.py`, create tables and include the students router.

## Starter Code

```
app/
  __init__.py
  main.py              — FastAPI app; needs table creation and router inclusion
  database.py          — Engine and session stubs
  models/
    __init__.py
    student.py         — ORM model stub
  schemas/
    __init__.py
    student.py         — Four schema stubs (Create, Update, Patch, Response)
  routers/
    __init__.py
    students.py        — Six endpoint stubs with signatures and docstrings
```

## Running

```bash
uvicorn app.main:app --reload
```

## Deliverable

A complete student management API with all CRUD operations, duplicate email detection, query filtering, and correct use of PUT vs PATCH semantics.
