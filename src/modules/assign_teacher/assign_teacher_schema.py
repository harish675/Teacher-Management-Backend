from pydantic import BaseModel, Field
from typing import List


class AssignTeacherCourseRequest(BaseModel):
    """Request schema for assigning courses to a teacher"""
    teacher_id: str = Field(..., description="Teacher's unique identifier")
    course_ids: List[str] = Field(..., min_length=1, description="List of course IDs to assign to the teacher")


class UnassignTeacherCourseRequest(BaseModel):
    """Request schema for unassigning courses from a teacher"""
    teacher_id: str = Field(..., description="Teacher's unique identifier")
    course_ids: List[str] = Field(..., min_length=1, description="List of course IDs to unassign from the teacher")


class TeacherCourseResponse(BaseModel):
    """Response schema for teacher-course assignment"""
    teacher_id: str
    teacher_name: str
    courses: List[dict] = Field(default_factory=list, description="List of courses assigned to this teacher")
    total_courses: int = Field(..., description="Total number of courses assigned")

    class Config:
        populate_by_name = True
        from_attributes = True
