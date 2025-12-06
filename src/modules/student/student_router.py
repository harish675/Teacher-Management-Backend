from fastapi import APIRouter, Depends, Query
from typing import List
from pymongo.database import Database

from ...lib.database import mongo_connection
from .student_controller import StudentController
from .student_schema import CreateStudentRequest, UpdateStudentRequest, StudentResponse

router = APIRouter(prefix="/students", tags=["Students"])


def get_db() -> Database:
    """Dependency to get database connection"""
    return mongo_connection.db


@router.post("", response_model=StudentResponse, status_code=201)
async def create_student(
    request: CreateStudentRequest,
    db: Database = Depends(get_db)
):
    """
    Create a new student
    
    Args:
        request: Student creation data
        db: Database connection
        
    Returns:
        Created student data
    """
    controller = StudentController(db)
    return controller.create_student(request)


@router.get("", response_model=List[StudentResponse])
async def get_all_students(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of records to return"),
    db: Database = Depends(get_db)
):
    """
    Get all students
    
    Args:
        skip: Number of records to skip for pagination
        limit: Maximum number of records to return
        db: Database connection
        
    Returns:
        List of students
    """
    controller = StudentController(db)
    return controller.get_all_students(skip, limit)


@router.get("/{student_id}", response_model=StudentResponse)
async def get_student_by_id(
    student_id: str,
    db: Database = Depends(get_db)
):
    """
    Get a student by ID
    
    Args:
        student_id: Student's unique identifier
        db: Database connection
        
    Returns:
        Student data
    """
    controller = StudentController(db)
    return controller.get_student_by_id(student_id)


@router.put("/{student_id}", response_model=StudentResponse)
async def update_student(
    student_id: str,
    request: UpdateStudentRequest,
    db: Database = Depends(get_db)
):
    """
    Update a student's information
    
    Args:
        student_id: Student's unique identifier
        request: Student update data
        db: Database connection
        
    Returns:
        Updated student data
    """
    controller = StudentController(db)
    return controller.update_student(student_id, request)


@router.delete("/{student_id}")
async def delete_student(
    student_id: str,
    db: Database = Depends(get_db)
):
    """
    Delete a student
    
    Args:
        student_id: Student's unique identifier
        db: Database connection
        
    Returns:
        Success message
    """
    controller = StudentController(db)
    return controller.delete_student(student_id)
