from fastapi import APIRouter, Depends, Query
from typing import List
from pymongo.database import Database

from src.lib.database import mongo_connection
from .course_controller import CourseController
from .course_schema import CreateCourseRequest, UpdateCourseRequest, CourseResponse, CourseWithDetailsResponse

router = APIRouter(prefix="/courses", tags=["Courses"])


def get_db() -> Database:
    """Dependency to get database connection"""
    return mongo_connection.db


@router.post("", response_model=CourseResponse, status_code=201)
async def create_course(
    request: CreateCourseRequest,
    db: Database = Depends(get_db)
):
    """
    Create a new course
    
    Args:
        request: Course creation data
        db: Database connection
        
    Returns:
        Created course data
    """
    controller = CourseController(db)
    return controller.create_course(request)


@router.get("", response_model=List[CourseResponse])
async def get_all_courses(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of records to return"),
    db: Database = Depends(get_db)
):
    """
    Get all courses
    
    Args:
        skip: Number of records to skip for pagination
        limit: Maximum number of records to return
        db: Database connection
        
    Returns:
        List of courses
    """
    controller = CourseController(db)
    return controller.get_all_courses(skip, limit)


@router.get("/{course_id}")
async def get_course_by_id(
    course_id: str,
    include_details: bool = Query(False, description="Include teacher and student details"),
    db: Database = Depends(get_db)
):
    """
    Get a course by ID
    
    Args:
        course_id: Course's unique identifier
        include_details: Whether to include teacher and student details
        db: Database connection
        
    Returns:
        Course data
    """
    controller = CourseController(db)
    return controller.get_course_by_id(course_id, include_details)


@router.put("/{course_id}", response_model=CourseResponse)
async def update_course(
    course_id: str,
    request: UpdateCourseRequest,
    db: Database = Depends(get_db)
):
    """
    Update a course's information
    
    Args:
        course_id: Course's unique identifier
        request: Course update data
        db: Database connection
        
    Returns:
        Updated course data
    """
    controller = CourseController(db)
    return controller.update_course(course_id, request)


@router.delete("/{course_id}")
async def delete_course(
    course_id: str,
    db: Database = Depends(get_db)
):
    """
    Delete a course
    
    Args:
        course_id: Course's unique identifier
        db: Database connection
        
    Returns:
        Success message
    """
    controller = CourseController(db)
    return controller.delete_course(course_id)
