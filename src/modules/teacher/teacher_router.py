from fastapi import APIRouter, Depends, Query
from typing import List
from pymongo.database import Database

from ...lib.database import mongo_connection
from .teacher_controller import TeacherController
from .teacher_schema import CreateTeacherRequest, UpdateTeacherRequest, TeacherResponse

router = APIRouter(prefix="/teachers", tags=["Teachers"])


def get_db() -> Database:
    """Dependency to get database connection"""
    return mongo_connection.db


@router.post("", response_model=TeacherResponse, status_code=201)
async def create_teacher(
    request: CreateTeacherRequest,
    db: Database = Depends(get_db)
):
    """
    Create a new teacher
    
    Args:
        request: Teacher creation data
        db: Database connection
        
    Returns:
        Created teacher data
    """
    controller = TeacherController(db)
    return controller.create_teacher(request)


@router.get("", response_model=List[TeacherResponse])
async def get_all_teachers(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of records to return"),
    db: Database = Depends(get_db)
):
    """
    Get all teachers
    
    Args:
        skip: Number of records to skip for pagination
        limit: Maximum number of records to return
        db: Database connection
        
    Returns:
        List of teachers
    """
    controller = TeacherController(db)
    return controller.get_all_teachers(skip, limit)


@router.get("/{teacher_id}", response_model=TeacherResponse)
async def get_teacher_by_id(
    teacher_id: str,
    db: Database = Depends(get_db)
):
    """
    Get a teacher by ID
    
    Args:
        teacher_id: Teacher's unique identifier
        db: Database connection
        
    Returns:
        Teacher data
    """
    controller = TeacherController(db)
    return controller.get_teacher_by_id(teacher_id)


@router.put("/{teacher_id}", response_model=TeacherResponse)
async def update_teacher(
    teacher_id: str,
    request: UpdateTeacherRequest,
    db: Database = Depends(get_db)
):
    """
    Update a teacher's information
    
    Args:
        teacher_id: Teacher's unique identifier
        request: Teacher update data
        db: Database connection
        
    Returns:
        Updated teacher data
    """
    controller = TeacherController(db)
    return controller.update_teacher(teacher_id, request)


@router.delete("/{teacher_id}")
async def delete_teacher(
    teacher_id: str,
    db: Database = Depends(get_db)
):
    """
    Delete a teacher
    
    Args:
        teacher_id: Teacher's unique identifier
        db: Database connection
        
    Returns:
        Success message
    """
    controller = TeacherController(db)
    return controller.delete_teacher(teacher_id)
