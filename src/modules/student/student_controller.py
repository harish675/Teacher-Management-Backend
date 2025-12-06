from typing import List, Optional
from fastapi import HTTPException, status
from pymongo.database import Database
import logging

from .student_repository import StudentRepository
from .student_schema import CreateStudentRequest, UpdateStudentRequest, StudentResponse

logger = logging.getLogger(__name__)


class StudentController:
    """Controller for Student business logic"""
    
    def __init__(self, db: Database):
        self.repository = StudentRepository(db)
    
    def create_student(self, request: CreateStudentRequest) -> StudentResponse:
        """
        Create a new student
        
        Args:
            request: CreateStudentRequest with student data
            
        Returns:
            StudentResponse with created student data
            
        Raises:
            HTTPException: If email already exists
        """
        try:
            # Check if email already exists
            existing_student = self.repository.get_student_by_email(request.email)
            if existing_student:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Student with email {request.email} already exists"
                )
            
            # Create student
            student_data = request.model_dump()
            created_student = self.repository.create_student(student_data)
            
            return StudentResponse(**created_student)
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error in create_student controller: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create student"
            )
    
    def get_all_students(self, skip: int = 0, limit: int = 100) -> List[StudentResponse]:
        """
        Get all students
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of StudentResponse objects
        """
        try:
            students = self.repository.get_all_students(skip, limit)
            return [StudentResponse(**student) for student in students]
        except Exception as e:
            logger.error(f"Error in get_all_students controller: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to fetch students"
            )
    
    def get_student_by_id(self, student_id: str) -> StudentResponse:
        """
        Get a student by ID
        
        Args:
            student_id: Student's unique identifier
            
        Returns:
            StudentResponse with student data
            
        Raises:
            HTTPException: If student not found
        """
        try:
            student = self.repository.get_student_by_id(student_id)
            if not student:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Student with ID {student_id} not found"
                )
            
            return StudentResponse(**student)
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error in get_student_by_id controller: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to fetch student"
            )
    
    def update_student(self, student_id: str, request: UpdateStudentRequest) -> StudentResponse:
        """
        Update a student's information
        
        Args:
            student_id: Student's unique identifier
            request: UpdateStudentRequest with fields to update
            
        Returns:
            StudentResponse with updated student data
            
        Raises:
            HTTPException: If student not found or email already exists
        """
        try:
            # Check if student exists
            existing_student = self.repository.get_student_by_id(student_id)
            if not existing_student:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Student with ID {student_id} not found"
                )
            
            # Check if email is being updated and if it already exists
            if request.email and request.email != existing_student.get("email"):
                email_exists = self.repository.get_student_by_email(request.email)
                if email_exists:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Student with email {request.email} already exists"
                    )
            
            # Update student
            update_data = request.model_dump(exclude_unset=True)
            updated_student = self.repository.update_student(student_id, update_data)
            
            if not updated_student:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Student with ID {student_id} not found"
                )
            
            return StudentResponse(**updated_student)
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error in update_student controller: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update student"
            )
    
    def delete_student(self, student_id: str) -> dict:
        """
        Delete a student
        
        Args:
            student_id: Student's unique identifier
            
        Returns:
            Success message
            
        Raises:
            HTTPException: If student not found
        """
        try:
            deleted = self.repository.delete_student(student_id)
            if not deleted:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Student with ID {student_id} not found"
                )
            
            return {"message": "Student deleted successfully"}
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error in delete_student controller: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete student"
            )
