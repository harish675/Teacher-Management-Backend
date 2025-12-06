from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime


class CreateStudentRequest(BaseModel):
    """Request schema for creating a new student"""
    name: str = Field(..., min_length=1, max_length=100, description="Student's full name")
    email: EmailStr = Field(..., description="Student's email address")
    age: Optional[int] = Field(None, ge=5, le=100, description="Student's age")


class UpdateStudentRequest(BaseModel):
    """Request schema for updating student information"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    age: Optional[int] = Field(None, ge=5, le=100)


class StudentResponse(BaseModel):
    """Response schema for student data"""
    id: str = Field(..., alias="_id", description="Student's unique identifier")
    name: str
    email: str
    age: Optional[int] = None
    created_date: datetime
    updated_date: datetime
    is_active: bool

    class Config:
        populate_by_name = True
        from_attributes = True
