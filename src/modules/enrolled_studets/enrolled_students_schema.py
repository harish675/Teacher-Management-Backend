from pydantic import BaseModel, Field
from typing import List


class EnrollStudentCourseRequest(BaseModel):
    """Request schema for enrolling a student in courses"""
    student_id: str = Field(..., description="Student's unique identifier")
    course_ids: List[str] = Field(..., min_length=1, description="List of course IDs to enroll the student in")


class UnenrollStudentCourseRequest(BaseModel):
    """Request schema for unenrolling a student from courses"""
    student_id: str = Field(..., description="Student's unique identifier")
    course_ids: List[str] = Field(..., min_length=1, description="List of course IDs to unenroll the student from")


class StudentCourseResponse(BaseModel):
    """Response schema for student-course enrollment"""
    student_id: str
    student_name: str
    courses: List[dict] = Field(default_factory=list, description="List of courses the student is enrolled in")
    total_courses: int = Field(..., description="Total number of courses enrolled")

    class Config:
        populate_by_name = True
        from_attributes = True


class CourseStudentsResponse(BaseModel):
    """Response schema for students enrolled in a course"""
    course_id: str
    course_name: str
    students: List[dict] = Field(default_factory=list, description="List of students enrolled in this course")
    total_students: int = Field(..., description="Total number of students enrolled")

    class Config:
        populate_by_name = True
        from_attributes = True
