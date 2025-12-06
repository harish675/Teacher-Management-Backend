from typing import List
from fastapi import HTTPException, status
from pymongo.database import Database
import logging

from .assign_teacher_repository import AssignTeacherRepository
from .assign_teacher_schema import AssignTeacherCourseRequest, TeacherCourseResponse
from ..teacher.teacher_repository import TeacherRepository
from ..course.course_repository import CourseRepository

logger = logging.getLogger(__name__)


class AssignTeacherController:
    """Controller for Teacher-Course assignment business logic"""
    
    def __init__(self, db: Database):
        self.repository = AssignTeacherRepository(db)
        self.teacher_repository = TeacherRepository(db)
        self.course_repository = CourseRepository(db)
    
    def assign_courses_to_teacher(self, request: AssignTeacherCourseRequest) -> TeacherCourseResponse:
        """
        Assign multiple courses to a teacher
        
        Args:
            request: AssignTeacherCourseRequest with teacher_id and course_ids
            
        Returns:
            TeacherCourseResponse with assignment details
            
        Raises:
            HTTPException: If teacher or courses not found
        """
        try:
            # Validate teacher exists
            teacher = self.teacher_repository.get_teacher_by_id(request.teacher_id)
            if not teacher:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Teacher with ID {request.teacher_id} not found"
                )
            
            # Validate all courses exist
            courses = self.course_repository.get_courses_by_ids(request.course_ids)
            if len(courses) != len(request.course_ids):
                found_ids = [c["_id"] for c in courses]
                missing_ids = [cid for cid in request.course_ids if cid not in found_ids]
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Courses not found: {', '.join(missing_ids)}"
                )
            
            # Assign courses to teacher
            result = self.repository.assign_courses_to_teacher(
                request.teacher_id,
                request.course_ids
            )
            
            # Get updated course list for teacher
            teacher_courses = self.repository.get_courses_by_teacher(request.teacher_id)
            
            return TeacherCourseResponse(
                teacher_id=request.teacher_id,
                teacher_name=teacher["name"],
                courses=teacher_courses,
                total_courses=len(teacher_courses)
            )
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error in assign_courses_to_teacher controller: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to assign courses to teacher"
            )
    
    def get_courses_by_teacher(self, teacher_id: str) -> TeacherCourseResponse:
        """
        Get all courses assigned to a teacher
        
        Args:
            teacher_id: Teacher's unique identifier
            
        Returns:
            TeacherCourseResponse with teacher's courses
            
        Raises:
            HTTPException: If teacher not found
        """
        try:
            # Validate teacher exists
            teacher = self.teacher_repository.get_teacher_by_id(teacher_id)
            if not teacher:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Teacher with ID {teacher_id} not found"
                )
            
            # Get courses for teacher
            courses = self.repository.get_courses_by_teacher(teacher_id)
            
            return TeacherCourseResponse(
                teacher_id=teacher_id,
                teacher_name=teacher["name"],
                courses=courses,
                total_courses=len(courses)
            )
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error in get_courses_by_teacher controller: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to fetch courses for teacher"
            )
