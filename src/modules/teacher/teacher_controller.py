from typing import List, Optional
from fastapi import HTTPException, status
from pymongo.database import Database
import logging

from .teacher_repository import TeacherRepository
from .teacher_schema import CreateTeacherRequest, UpdateTeacherRequest, TeacherResponse

logger = logging.getLogger(__name__)


class TeacherController:
    """Controller for Teacher business logic"""
    
    def __init__(self, db: Database):
        self.repository = TeacherRepository(db)
    
    def create_teacher(self, request: CreateTeacherRequest) -> TeacherResponse:
        """
        Create a new teacher
        
        Args:
            request: CreateTeacherRequest with teacher data
            
        Returns:
            TeacherResponse with created teacher data
            
        Raises:
            HTTPException: If email already exists
        """
        try:
            # Check if email already exists
            existing_teacher = self.repository.get_teacher_by_email(request.email)
            if existing_teacher:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Teacher with email {request.email} already exists"
                )
            
            # Create teacher
            teacher_data = request.model_dump()
            created_teacher = self.repository.create_teacher(teacher_data)
            
            return TeacherResponse(**created_teacher)
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error in create_teacher controller: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create teacher"
            )
    
    def get_all_teachers(self, skip: int = 0, limit: int = 100) -> List[TeacherResponse]:
        """
        Get all teachers
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of TeacherResponse objects
        """
        try:
            teachers = self.repository.get_all_teachers(skip, limit)
            return [TeacherResponse(**teacher) for teacher in teachers]
        except Exception as e:
            logger.error(f"Error in get_all_teachers controller: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to fetch teachers"
            )
    
    def get_teacher_by_id(self, teacher_id: str) -> TeacherResponse:
        """
        Get a teacher by ID
        
        Args:
            teacher_id: Teacher's unique identifier
            
        Returns:
            TeacherResponse with teacher data
            
        Raises:
            HTTPException: If teacher not found
        """
        try:
            teacher = self.repository.get_teacher_by_id(teacher_id)
            if not teacher:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Teacher with ID {teacher_id} not found"
                )
            
            return TeacherResponse(**teacher)
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error in get_teacher_by_id controller: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to fetch teacher"
            )
    
    def update_teacher(self, teacher_id: str, request: UpdateTeacherRequest) -> TeacherResponse:
        """
        Update a teacher's information
        
        Args:
            teacher_id: Teacher's unique identifier
            request: UpdateTeacherRequest with fields to update
            
        Returns:
            TeacherResponse with updated teacher data
            
        Raises:
            HTTPException: If teacher not found or email already exists
        """
        try:
            # Check if teacher exists
            existing_teacher = self.repository.get_teacher_by_id(teacher_id)
            if not existing_teacher:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Teacher with ID {teacher_id} not found"
                )
            
            # Check if email is being updated and if it already exists
            if request.email and request.email != existing_teacher.get("email"):
                email_exists = self.repository.get_teacher_by_email(request.email)
                if email_exists:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Teacher with email {request.email} already exists"
                    )
            
            # Update teacher
            update_data = request.model_dump(exclude_unset=True)
            updated_teacher = self.repository.update_teacher(teacher_id, update_data)
            
            if not updated_teacher:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Teacher with ID {teacher_id} not found"
                )
            
            return TeacherResponse(**updated_teacher)
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error in update_teacher controller: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update teacher"
            )
    
    def delete_teacher(self, teacher_id: str) -> dict:
        """
        Delete a teacher
        
        Args:
            teacher_id: Teacher's unique identifier
            
        Returns:
            Success message
            
        Raises:
            HTTPException: If teacher not found
        """
        try:
            deleted = self.repository.delete_teacher(teacher_id)
            if not deleted:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Teacher with ID {teacher_id} not found"
                )
            
            return {"message": "Teacher deleted successfully"}
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error in delete_teacher controller: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete teacher"
            )
