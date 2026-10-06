from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Optional

from app.schemas.student import( 
    StudentCreate, 
    StudentUpdate, 
    StudentPatch, 
    StudentResponse,
)

from app.models.student import Student
from app.database import get_db

router = APIRouter()

#Helper function
def get_student_or_404(student_id: int, db: Session):
    student = db.get(Student, student_id)

    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Student not found"
        )
    return student

#POST /students — create a student (handle duplicate email with 409)
@router.post(
    "/", 
    response_model=StudentResponse, 
    status_code=status.HTTP_201_CREATED
)
def create_student(
    student: StudentCreate, 
    db: Session = Depends(get_db)
):
    existing_student = db.scalar(
        select(Student).where(Student.email == student.email)
    )
    if existing_student:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists"
        )
    new_student = Student(
        name=student.name,
        email=student.email,
        major=student.major,
        gpa=student.gpa
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student

#GET /students — list students with optional filters
@router.get("/", response_model=list[StudentResponse])
def list_students(
    major: Optional[str] = Query(None),
    min_gpa: Optional[float] = Query(
        None, 
        ge=0.0, 
        le=4.0
    ),
    db: Session = Depends(get_db),
):
    stmt = select(Student)

    if major is not None:
        stmt = stmt.where(Student.major == major)

    if min_gpa is not None:
        stmt = stmt.where(Student.gpa >= min_gpa)

    return db.scalars(stmt).all()

#Returns a single student by ID.
@router.get("/{student_id}", response_model=StudentResponse)
def get_student(
    student_id: int, 
    db: Session = Depends(get_db)
):
    return get_student_or_404(student_id, db)

#Fully replaces a student record (all fields required).
@router.put("/{student_id}", response_model=StudentResponse)
def replace_student(
    student_id: int, 
    student: StudentUpdate, 
    db: Session = Depends(get_db)
):
    student_record = get_student_or_404(student_id, db)

    existing_email = db.scalar(
        select(Student).where(
            Student.email == student.email,
            Student.id != student_id
        )
    )
    if existing_email: 
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists"
        )

    student_record.name = student.name
    student_record.email = student.email
    student_record.major = student.major
    student_record.gpa = student.gpa

    db.commit()
    db.refresh(student_record)

    return student_record

#Partially updates a student (only fields sent are changed)
@router.patch("/{student_id}", response_model=StudentResponse)
def patch_student(student_id: int, 
                  student: StudentPatch, 
                  db: Session = Depends(get_db)
):
    student_record = get_student_or_404(student_id, db)

    update_data = student.model_dump(exclude_unset=True)

    if "email" in update_data:
        existing_email = db.scalar(
            select(Student).where(
                Student.email == update_data["email"],
                Student.id != student_id
            )
        )
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already exists"
            )

    for field, value in update_data.items():
        setattr(student_record, field, value)
    db.commit()
    db.refresh(student_record)

    return student_record

#DELETE delete a student and return confirmation
@router.delete("/{student_id}")
def delete_student(
    student_id: int, 
    db: Session = Depends(get_db)
):
    student_record = get_student_or_404(student_id, db)

    db.delete(student_record)
    db.commit()

    return {"message": "Student deleted successfully"
    }