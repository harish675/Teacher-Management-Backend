from fastapi import APIRouter, Depends
from typing import List
from pymongo.database import Database

from ...lib.database import mongo_connection
from .enrolled_students_controller import EnrolledStudentsController
from .enrolled_students_schema import (
    EnrollStudentCourseRequest,
    StudentCourseResponse,
    CourseStudentsResponse
)

router = APIRouter(prefix="/student-course", tags=["Student-Course Enrollment"])


def get_db() -> Database:
    """Dependency to get database connection"""
    return mongo_connection.db


@router.post("/enroll", response_model=StudentCourseResponse, status_code=201)
async def enroll_student_in_courses(
    request: EnrollStudentCourseRequest,
    db: Database = Depends(get_db)
):
    """
    Enroll a student in multiple courses
    
    Args:
        request: Enrollment data with student_id and course_ids
        db: Database connection
        
    Returns:
        Student course enrollment details
    """
    controller = EnrolledStudentsController(db)
    return controller.enroll_student_in_courses(request)


@router.get("/{course_id}", response_model=CourseStudentsResponse)
async def get_students_by_course(
    course_id: str,
    db: Database = Depends(get_db)
):
    """
    Get all students enrolled in a course
    
    Args:
        course_id: Course's unique identifier
        db: Database connection
        
    Returns:
        List of students enrolled in the course
    """
    controller = EnrolledStudentsController(db)
    return controller.get_students_by_course(course_id)


@router.get("/student/{student_id}", response_model=StudentCourseResponse)
async def get_courses_by_student(
    student_id: str,
    db: Database = Depends(get_db)
):
    """
    Get all courses a student is enrolled in
    
    Args:
        student_id: Student's unique identifier
        db: Database connection
        
    Returns:
        List of courses the student is enrolled in
    """
    controller = EnrolledStudentsController(db)
    return controller.get_courses_by_student(student_id)


@router.get("/enrollments/all", response_model=List[CourseStudentsResponse])
async def get_all_enrollments(
    db: Database = Depends(get_db)
):
    """
    Get all course enrollments
    
    Args:
        db: Database connection
        
    Returns:
        List of all course enrollments with student details
    """
    controller = EnrolledStudentsController(db)
    return controller.get_all_enrollments()
