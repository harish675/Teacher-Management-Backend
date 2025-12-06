from typing import List, Optional
from pymongo.database import Database
from bson import ObjectId
from datetime import datetime, timezone
import logging

from .teacher_model import Teacher

logger = logging.getLogger(__name__)


class TeacherRepository:
    """Repository for Teacher database operations"""
    
    def __init__(self, db: Database):
        self.db = db
        self.collection = db["teachers"]
    
    def create_teacher(self, teacher_data: dict) -> dict:
        """
        Create a new teacher in the database
        
        Args:
            teacher_data: Dictionary containing teacher information
            
        Returns:
            Created teacher document
        """
        try:
            teacher_data["created_date"] = datetime.now(timezone.utc)
            teacher_data["updated_date"] = datetime.now(timezone.utc)
            teacher_data["is_active"] = True
            
            result = self.collection.insert_one(teacher_data)
            teacher_data["_id"] = str(result.inserted_id)
            
            logger.info(f"Created teacher with ID: {teacher_data['_id']}")
            return teacher_data
        except Exception as e:
            logger.error(f"Error creating teacher: {e}")
            raise
    
    def get_all_teachers(self, skip: int = 0, limit: int = 100) -> List[dict]:
        """
        Get all active teachers
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of teacher documents
        """
        try:
            teachers = list(
                self.collection.find({"is_active": True})
                .skip(skip)
                .limit(limit)
            )
            
            # Convert ObjectId to string
            for teacher in teachers:
                teacher["_id"] = str(teacher["_id"])
            
            return teachers
        except Exception as e:
            logger.error(f"Error fetching teachers: {e}")
            raise
    
    def get_teacher_by_id(self, teacher_id: str) -> Optional[dict]:
        """
        Get a teacher by ID
        
        Args:
            teacher_id: Teacher's unique identifier
            
        Returns:
            Teacher document or None if not found
        """
        try:
            teacher = self.collection.find_one({
                "_id": teacher_id,
                "is_active": True
            })
            
            if teacher:
                teacher["_id"] = str(teacher["_id"])
            
            return teacher
        except Exception as e:
            logger.error(f"Error fetching teacher by ID {teacher_id}: {e}")
            raise
    
    def get_teacher_by_email(self, email: str) -> Optional[dict]:
        """
        Get a teacher by email
        
        Args:
            email: Teacher's email address
            
        Returns:
            Teacher document or None if not found
        """
        try:
            teacher = self.collection.find_one({
                "email": email,
                "is_active": True
            })
            
            if teacher:
                teacher["_id"] = str(teacher["_id"])
            
            return teacher
        except Exception as e:
            logger.error(f"Error fetching teacher by email {email}: {e}")
            raise
    
    def update_teacher(self, teacher_id: str, update_data: dict) -> Optional[dict]:
        """
        Update a teacher's information
        
        Args:
            teacher_id: Teacher's unique identifier
            update_data: Dictionary containing fields to update
            
        Returns:
            Updated teacher document or None if not found
        """
        try:
            update_data["updated_date"] = datetime.now(timezone.utc)
            
            result = self.collection.find_one_and_update(
                {"_id": teacher_id, "is_active": True},
                {"$set": update_data},
                return_document=True
            )
            
            if result:
                result["_id"] = str(result["_id"])
                logger.info(f"Updated teacher with ID: {teacher_id}")
            
            return result
        except Exception as e:
            logger.error(f"Error updating teacher {teacher_id}: {e}")
            raise
    
    def delete_teacher(self, teacher_id: str) -> bool:
        """
        Soft delete a teacher (set is_active to False)
        
        Args:
            teacher_id: Teacher's unique identifier
            
        Returns:
            True if deleted, False otherwise
        """
        try:
            result = self.collection.update_one(
                {"_id": teacher_id},
                {"$set": {"is_active": False, "updated_date": datetime.now(timezone.utc)}}
            )
            
            if result.modified_count > 0:
                logger.info(f"Deleted teacher with ID: {teacher_id}")
                return True
            
            return False
        except Exception as e:
            logger.error(f"Error deleting teacher {teacher_id}: {e}")
            raise
    
    def get_teachers_by_ids(self, teacher_ids: List[str]) -> List[dict]:
        """
        Get multiple teachers by their IDs
        
        Args:
            teacher_ids: List of teacher IDs
            
        Returns:
            List of teacher documents
        """
        try:
            valid_ids = [tid for tid in teacher_ids if tid]
            if not valid_ids:
                return []
            
            teachers = list(
                self.collection.find({
                    "_id": {"$in": valid_ids},
                    "is_active": True
                })
            )
            
            for teacher in teachers:
                teacher["_id"] = str(teacher["_id"])
            
            return teachers
        except Exception as e:
            logger.error(f"Error fetching teachers by IDs: {e}")
            raise
