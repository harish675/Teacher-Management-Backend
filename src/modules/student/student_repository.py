from typing import List, Optional
from pymongo.database import Database
from bson import ObjectId
from datetime import datetime, timezone
import logging

from .student_model import Student

logger = logging.getLogger(__name__)


class StudentRepository:
    """Repository for Student database operations"""
    
    def __init__(self, db: Database):
        self.db = db
        self.collection = db["students"]
    
    def create_student(self, student_data: dict) -> dict:
        """
        Create a new student in the database
        
        Args:
            student_data: Dictionary containing student information
            
        Returns:
            Created student document
        """
        try:
            student_data["created_date"] = datetime.now(timezone.utc)
            student_data["updated_date"] = datetime.now(timezone.utc)
            student_data["is_active"] = True
            
            result = self.collection.insert_one(student_data)
            student_data["_id"] = str(result.inserted_id)
            
            logger.info(f"Created student with ID: {student_data['_id']}")
            return student_data
        except Exception as e:
            logger.error(f"Error creating student: {e}")
            raise
    
    def get_all_students(self, skip: int = 0, limit: int = 100) -> List[dict]:
        """
        Get all active students
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of student documents
        """
        try:
            students = list(
                self.collection.find({"is_active": True})
                .skip(skip)
                .limit(limit)
            )
            
            # Convert ObjectId to string
            for student in students:
                student["_id"] = str(student["_id"])
            
            return students
        except Exception as e:
            logger.error(f"Error fetching students: {e}")
            raise
    
    def get_student_by_id(self, student_id: str) -> Optional[dict]:
        """
        Get a student by ID
        
        Args:
            student_id: Student's unique identifier
            
        Returns:
            Student document or None if not found
        """
        try:
            # Assuming student_id is already a string representation of ObjectId
            # No need for ObjectId.is_valid if we're treating _id as a string in the DB
            # if not ObjectId.is_valid(student_id):
            #     return None
            
            student = self.collection.find_one({
                "_id": student_id,
                "is_active": True
            })
            
            if student:
                student["_id"] = str(student["_id"])
            
            return student
        except Exception as e:
            logger.error(f"Error fetching student by ID {student_id}: {e}")
            raise
    
    def get_student_by_email(self, email: str) -> Optional[dict]:
        """
        Get a student by email
        
        Args:
            email: Student's email address
            
        Returns:
            Student document or None if not found
        """
        try:
            student = self.collection.find_one({
                "email": email,
                "is_active": True
            })
            
            if student:
                student["_id"] = str(student["_id"])
            
            return student
        except Exception as e:
            logger.error(f"Error fetching student by email {email}: {e}")
            raise
    
    def update_student(self, student_id: str, update_data: dict) -> Optional[dict]:
        """
        Update a student's information
        
        Args:
            student_id: Student's unique identifier
            update_data: Dictionary containing fields to update
            
        Returns:
            Updated student document or None if not found
        """
        try:
            # Assuming student_id is already a string representation of ObjectId
            # if not ObjectId.is_valid(student_id):
            #     return None
            
            update_data["updated_date"] = datetime.now(timezone.utc)
            
            result = self.collection.find_one_and_update(
                {"_id": student_id, "is_active": True},
                {"$set": update_data},
                return_document=True
            )
            
            if result:
                result["_id"] = str(result["_id"])
                logger.info(f"Updated student with ID: {student_id}")
            
            return result
        except Exception as e:
            logger.error(f"Error updating student {student_id}: {e}")
            raise
    
    def delete_student(self, student_id: str) -> bool:
        """
        Soft delete a student (set is_active to False)
        
        Args:
            student_id: Student's unique identifier
            
        Returns:
            True if deleted, False otherwise
        """
        try:
            # Assuming student_id is already a string representation of ObjectId
            # if not ObjectId.is_valid(student_id):
            #     return False
            
            result = self.collection.update_one(
                {"_id": student_id},
                {"$set": {"is_active": False, "updated_date": datetime.now(timezone.utc)}}
            )
            
            if result.modified_count > 0:
                logger.info(f"Deleted student with ID: {student_id}")
                return True
            
            return False
        except Exception as e:
            logger.error(f"Error deleting student {student_id}: {e}")
            raise
    
    def get_students_by_ids(self, student_ids: List[str]) -> List[dict]:
        """
        Get multiple students by their IDs
        
        Args:
            student_ids: List of student IDs
            
        Returns:
            List of student documents
        """
        try:
            # Filter out any empty strings if necessary, but assume valid string IDs
            valid_ids = [sid for sid in student_ids if sid]
            if not valid_ids:
                return []
            
            students = list(
                self.collection.find({
                    "_id": {"$in": valid_ids},
                    "is_active": True
                })
            )
            
            for student in students:
                student["_id"] = str(student["_id"])
            
            return students
        except Exception as e:
            logger.error(f"Error fetching students by IDs: {e}")
            raise
