from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional

#Schema for creating a student.
class StudentCreate(BaseModel):
    name: str 
    email: str 
    major: Optional[str] = None
    gpa: Optional[float] = Field(
        default=None,
        ge=0,
        le=4
    )

    @field_validator('email')
    @classmethod
    def validate_email(cls, value):
        if '@' not in value:
            raise ValueError('Email must contain @')
        return value

#StudentUpdate — used for fully replacing a student (PUT)
class StudentUpdate(BaseModel):
    name: str
    email: str
    major: Optional[str] = None
    gpa: Optional[float] = Field(
        default=None,
        ge=0,
        le=4
    )
    @field_validator('email')
    @classmethod
    def validate_email(cls, value):
        if '@' not in value:
            raise ValueError('Email must contain @')
        return value
    
#partially updating a student (PATCH).
class StudentPatch(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    major: Optional[str] = None
    gpa: Optional[float] = Field(
        default=None,
        ge=0,
        le=4
    )
    @field_validator('email')
    @classmethod
    def validate_email(cls, value):
        if value is not None and '@' not in value:
            raise ValueError('Email must contain @')
        return value
    
#Schema for returning student data.
class StudentResponse(StudentCreate):
    id: int
    model_config = ConfigDict(
        from_attributes=True
    )

