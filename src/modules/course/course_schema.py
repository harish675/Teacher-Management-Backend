from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class CreateCourseRequest(BaseModel):
    """Request schema for creating a new course"""
    course_name: str = Field(..., min_length=1, max_length=200, description="Course name")
    description: Optional[str] = Field(None, max_length=1000, description="Course description")


class UpdateCourseRequest(BaseModel):
    """Request schema for updating course information"""
    course_name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)


class CourseResponse(BaseModel):
    """Response schema for course data"""
    id: str = Field(..., alias="_id", description="Course's unique identifier")
    course_name: str
    description: Optional[str] = None
    teacher_ids: List[str] = Field(default_factory=list, description="List of teacher IDs assigned to this course")
    enrolled_student_ids: List[str] = Field(default_factory=list, description="List of student IDs enrolled in this course")
    created_date: datetime
    updated_date: datetime
    is_active: bool

    class Config:
        populate_by_name = True
        from_attributes = True


class CourseWithDetailsResponse(BaseModel):
    """Response schema for course data with teacher and student details"""
    id: str = Field(..., alias="_id")
    course_name: str
    description: Optional[str] = None
    teachers: List[dict] = Field(default_factory=list, description="List of teachers assigned to this course")
    students: List[dict] = Field(default_factory=list, description="List of students enrolled in this course")
    created_date: datetime
    updated_date: datetime
    is_active: bool

    class Config:
        populate_by_name = True
        from_attributes = True
