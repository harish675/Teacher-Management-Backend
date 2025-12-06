from typing import List, Optional
from fastapi import HTTPException, status
from pymongo.database import Database
import logging

from .course_repository import CourseRepository
from .course_schema import CreateCourseRequest, UpdateCourseRequest, CourseResponse, CourseWithDetailsResponse
from ..student.student_repository import StudentRepository
from ..teacher.teacher_repository import TeacherRepository

logger = logging.getLogger(__name__)


class CourseController:
    """Controller for Course business logic"""
    
    def __init__(self, db: Database):
        self.repository = CourseRepository(db)
        self.student_repository = StudentRepository(db)
        self.teacher_repository = TeacherRepository(db)
    
    def create_course(self, request: CreateCourseRequest) -> CourseResponse:
        """
        Create a new course
        
        Args:
            request: CreateCourseRequest with course data
            
        Returns:
            CourseResponse with created course data
            
        Raises:
            HTTPException: If course name already exists
        """
        try:
            # Check if course name already exists
            existing_course = self.repository.get_course_by_name(request.course_name)
            if existing_course:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Course with name '{request.course_name}' already exists"
                )
            
            # Create course
            course_data = request.model_dump()
            created_course = self.repository.create_course(course_data)
            
            return CourseResponse(**created_course)
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error in create_course controller: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create course"
            )
    
    def get_all_courses(self, skip: int = 0, limit: int = 100) -> List[CourseResponse]:
        """
        Get all courses
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of CourseResponse objects
        """
        try:
            courses = self.repository.get_all_courses(skip, limit)
            return [CourseResponse(**course) for course in courses]
        except Exception as e:
            logger.error(f"Error in get_all_courses controller: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to fetch courses"
            )
    
    def get_course_by_id(self, course_id: str, include_details: bool = False) -> CourseResponse:
        """
        Get a course by ID
        
        Args:
            course_id: Course's unique identifier
            include_details: Whether to include teacher and student details
            
        Returns:
            CourseResponse or CourseWithDetailsResponse with course data
            
        Raises:
            HTTPException: If course not found
        """
        try:
            course = self.repository.get_course_by_id(course_id)
            if not course:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Course with ID {course_id} not found"
                )
            
            if include_details:
                # Fetch teacher details
                teacher_ids = course.get("teacher_ids", [])
                teachers = self.teacher_repository.get_teachers_by_ids(teacher_ids) if teacher_ids else []
                
                # Fetch student details
                student_ids = course.get("enrolled_student_ids", [])
                students = self.student_repository.get_students_by_ids(student_ids) if student_ids else []
                
                course["teachers"] = teachers
                course["students"] = students
                
                return CourseWithDetailsResponse(**course)
            
            return CourseResponse(**course)
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error in get_course_by_id controller: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to fetch course"
            )
    
    def update_course(self, course_id: str, request: UpdateCourseRequest) -> CourseResponse:
        """
        Update a course's information
        
        Args:
            course_id: Course's unique identifier
            request: UpdateCourseRequest with fields to update
            
        Returns:
            CourseResponse with updated course data
            
        Raises:
            HTTPException: If course not found or name already exists
        """
        try:
            # Check if course exists
            existing_course = self.repository.get_course_by_id(course_id)
            if not existing_course:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Course with ID {course_id} not found"
                )
            
            # Check if course name is being updated and if it already exists
            if request.course_name and request.course_name != existing_course.get("course_name"):
                name_exists = self.repository.get_course_by_name(request.course_name)
                if name_exists:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Course with name '{request.course_name}' already exists"
                    )
            
            # Update course
            update_data = request.model_dump(exclude_unset=True)
            updated_course = self.repository.update_course(course_id, update_data)
            
            if not updated_course:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Course with ID {course_id} not found"
                )
            
            return CourseResponse(**updated_course)
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error in update_course controller: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update course"
            )
    
    def delete_course(self, course_id: str) -> dict:
        """
        Delete a course
        
        Args:
            course_id: Course's unique identifier
            
        Returns:
            Success message
            
        Raises:
            HTTPException: If course not found
        """
        try:
            deleted = self.repository.delete_course(course_id)
            if not deleted:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Course with ID {course_id} not found"
                )
            
            return {"message": "Course deleted successfully"}
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error in delete_course controller: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete course"
            )
