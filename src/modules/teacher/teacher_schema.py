from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime


class CreateTeacherRequest(BaseModel):
    """Request schema for creating a new teacher"""
    name: str = Field(..., min_length=1, max_length=100, description="Teacher's full name")
    email: EmailStr = Field(..., description="Teacher's email address")
    subject_expertise: Optional[str] = Field(None, max_length=100, description="Teacher's subject expertise")
    experience_years: Optional[int] = Field(None, ge=0, le=50, description="Years of teaching experience")


class UpdateTeacherRequest(BaseModel):
    """Request schema for updating teacher information"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    subject_expertise: Optional[str] = Field(None, max_length=100)
    experience_years: Optional[int] = Field(None, ge=0, le=50)


class TeacherResponse(BaseModel):
    """Response schema for teacher data"""
    id: str = Field(..., alias="_id", description="Teacher's unique identifier")
    name: str
    email: str
    subject_expertise: Optional[str] = None
    experience_years: Optional[int] = None
    created_date: datetime
    updated_date: datetime
    is_active: bool

    class Config:
        populate_by_name = True
        from_attributes = True
