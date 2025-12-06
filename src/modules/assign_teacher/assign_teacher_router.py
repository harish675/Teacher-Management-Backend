from fastapi import APIRouter, Depends
from pymongo.database import Database

from ...lib.database import mongo_connection
from .assign_teacher_controller import AssignTeacherController
from .assign_teacher_schema import AssignTeacherCourseRequest, TeacherCourseResponse

router = APIRouter(prefix="/teacher-course", tags=["Teacher-Course Assignment"])


def get_db() -> Database:
    """Dependency to get database connection"""
    return mongo_connection.db


@router.post("/assign", response_model=TeacherCourseResponse, status_code=201)
async def assign_courses_to_teacher(
    request: AssignTeacherCourseRequest,
    db: Database = Depends(get_db)
):
    """
    Assign multiple courses to a teacher
    
    Args:
        request: Assignment data with teacher_id and course_ids
        db: Database connection
        
    Returns:
        Teacher course assignment details
    """
    controller = AssignTeacherController(db)
    return controller.assign_courses_to_teacher(request)


@router.get("/{teacher_id}", response_model=TeacherCourseResponse)
async def get_courses_by_teacher(
    teacher_id: str,
    db: Database = Depends(get_db)
):
    """
    Get all courses assigned to a teacher
    
    Args:
        teacher_id: Teacher's unique identifier
        db: Database connection
        
    Returns:
        List of courses assigned to the teacher
    """
    controller = AssignTeacherController(db)
    return controller.get_courses_by_teacher(teacher_id)
