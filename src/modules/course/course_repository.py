from typing import List, Optional
from pymongo.database import Database
from bson import ObjectId
from datetime import datetime, timezone
import logging

from .course_model import Course

logger = logging.getLogger(__name__)


class CourseRepository:
    """Repository for Course database operations"""
    
    def __init__(self, db: Database):
        self.db = db
        self.collection = db["courses"]
    
    def create_course(self, course_data: dict) -> dict:
        """
        Create a new course in the database
        
        Args:
            course_data: Dictionary containing course information
            
        Returns:
            Created course document
        """
        try:
            course_data["created_date"] = datetime.now(timezone.utc)
            course_data["updated_date"] = datetime.now(timezone.utc)
            course_data["is_active"] = True
            course_data["teacher_ids"] = course_data.get("teacher_ids", [])
            course_data["enrolled_student_ids"] = course_data.get("enrolled_student_ids", [])
            
            result = self.collection.insert_one(course_data)
            course_data["_id"] = str(result.inserted_id)
            
            logger.info(f"Created course with ID: {course_data['_id']}")
            return course_data
        except Exception as e:
            logger.error(f"Error creating course: {e}")
            raise
    
    def get_all_courses(self, skip: int = 0, limit: int = 100) -> List[dict]:
        """
        Get all active courses
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of course documents
        """
        try:
            courses = list(
                self.collection.find({"is_active": True})
                .skip(skip)
                .limit(limit)
            )
            
            # Convert ObjectId to string
            for course in courses:
                course["_id"] = str(course["_id"])
            
            return courses
        except Exception as e:
            logger.error(f"Error fetching courses: {e}")
            raise
    
    def get_course_by_id(self, course_id: str) -> Optional[dict]:
        """
        Get a course by ID
        
        Args:
            course_id: Course's unique identifier
            
        Returns:
            Course document or None if not found
        """
        try:
            course = self.collection.find_one({
                "_id": course_id,
                "is_active": True
            })
            
            if course:
                course["_id"] = str(course["_id"])
            
            return course
        except Exception as e:
            logger.error(f"Error fetching course by ID {course_id}: {e}")
            raise
    
    def get_course_by_name(self, course_name: str) -> Optional[dict]:
        """
        Get a course by name
        
        Args:
            course_name: Course name
            
        Returns:
            Course document or None if not found
        """
        try:
            course = self.collection.find_one({
                "course_name": course_name,
                "is_active": True
            })
            
            if course:
                course["_id"] = str(course["_id"])
            
            return course
        except Exception as e:
            logger.error(f"Error fetching course by name {course_name}: {e}")
            raise
    
    def update_course(self, course_id: str, update_data: dict) -> Optional[dict]:
        """
        Update a course's information
        
        Args:
            course_id: Course's unique identifier
            update_data: Dictionary containing fields to update
            
        Returns:
            Updated course document or None if not found
        """
        try:
            update_data["updated_date"] = datetime.now(timezone.utc)
            
            result = self.collection.find_one_and_update(
                {"_id": course_id, "is_active": True},
                {"$set": update_data},
                return_document=True
            )
            
            if result:
                result["_id"] = str(result["_id"])
                logger.info(f"Updated course with ID: {course_id}")
            
            return result
        except Exception as e:
            logger.error(f"Error updating course {course_id}: {e}")
            raise
    
    def add_teacher_to_course(self, course_id: str, teacher_id: str) -> Optional[dict]:
        """
        Add a teacher to a course
        
        Args:
            course_id: Course's unique identifier
            teacher_id: Teacher's unique identifier
            
        Returns:
            Updated course document or None if not found
        """
        try:
            result = self.collection.find_one_and_update(
                {"_id": course_id, "is_active": True},
                {
                    "$addToSet": {"teacher_ids": teacher_id},
                    "$set": {"updated_date": datetime.now(timezone.utc)}
                },
                return_document=True
            )
            
            if result:
                result["_id"] = str(result["_id"])
                logger.info(f"Added teacher {teacher_id} to course {course_id}")
            
            return result
        except Exception as e:
            logger.error(f"Error adding teacher to course: {e}")
            raise
    
    def remove_teacher_from_course(self, course_id: str, teacher_id: str) -> Optional[dict]:
        """
        Remove a teacher from a course
        
        Args:
            course_id: Course's unique identifier
            teacher_id: Teacher's unique identifier
            
        Returns:
            Updated course document or None if not found
        """
        try:
            result = self.collection.find_one_and_update(
                {"_id": course_id, "is_active": True},
                {
                    "$pull": {"teacher_ids": teacher_id},
                    "$set": {"updated_date": datetime.now(timezone.utc)}
                },
                return_document=True
            )
            
            if result:
                result["_id"] = str(result["_id"])
                logger.info(f"Removed teacher {teacher_id} from course {course_id}")
            
            return result
        except Exception as e:
            logger.error(f"Error removing teacher from course: {e}")
            raise
    
    def add_student_to_course(self, course_id: str, student_id: str) -> Optional[dict]:
        """
        Add a student to a course
        
        Args:
            course_id: Course's unique identifier
            student_id: Student's unique identifier
            
        Returns:
            Updated course document or None if not found
        """
        try:
            result = self.collection.find_one_and_update(
                {"_id": course_id, "is_active": True},
                {
                    "$addToSet": {"enrolled_student_ids": student_id},
                    "$set": {"updated_date": datetime.now(timezone.utc)}
                },
                return_document=True
            )
            
            if result:
                result["_id"] = str(result["_id"])
                logger.info(f"Added student {student_id} to course {course_id}")
            
            return result
        except Exception as e:
            logger.error(f"Error adding student to course: {e}")
            raise
    
    def remove_student_from_course(self, course_id: str, student_id: str) -> Optional[dict]:
        """
        Remove a student from a course
        
        Args:
            course_id: Course's unique identifier
            student_id: Student's unique identifier
            
        Returns:
            Updated course document or None if not found
        """
        try:
            result = self.collection.find_one_and_update(
                {"_id": course_id, "is_active": True},
                {
                    "$pull": {"enrolled_student_ids": student_id},
                    "$set": {"updated_date": datetime.now(timezone.utc)}
                },
                return_document=True
            )
            
            if result:
                result["_id"] = str(result["_id"])
                logger.info(f"Removed student {student_id} from course {course_id}")
            
            return result
        except Exception as e:
            logger.error(f"Error removing student from course: {e}")
            raise
    
    def get_courses_by_teacher(self, teacher_id: str) -> List[dict]:
        """
        Get all courses assigned to a teacher
        
        Args:
            teacher_id: Teacher's unique identifier
            
        Returns:
            List of course documents
        """
        try:
            courses = list(
                self.collection.find({
                    "teacher_ids": teacher_id,
                    "is_active": True
                })
            )
            
            for course in courses:
                course["_id"] = str(course["_id"])
            
            return courses
        except Exception as e:
            logger.error(f"Error fetching courses by teacher {teacher_id}: {e}")
            raise
    
    def get_courses_by_student(self, student_id: str) -> List[dict]:
        """
        Get all courses a student is enrolled in
        
        Args:
            student_id: Student's unique identifier
            
        Returns:
            List of course documents
        """
        try:
            courses = list(
                self.collection.find({
                    "enrolled_student_ids": student_id,
                    "is_active": True
                })
            )
            
            for course in courses:
                course["_id"] = str(course["_id"])
            
            return courses
        except Exception as e:
            logger.error(f"Error fetching courses by student {student_id}: {e}")
            raise
    
    def get_courses_by_ids(self, course_ids: List[str]) -> List[dict]:
        """
        Get multiple courses by their IDs
        
        Args:
            course_ids: List of course IDs
            
        Returns:
            List of course documents
        """
        try:
            valid_ids = [cid for cid in course_ids if cid]
            if not valid_ids:
                return []
            
            courses = list(
                self.collection.find({
                    "_id": {"$in": valid_ids},
                    "is_active": True
                })
            )
            
            for course in courses:
                course["_id"] = str(course["_id"])
            
            return courses
        except Exception as e:
            logger.error(f"Error fetching courses by IDs: {e}")
            raise
    
    def delete_course(self, course_id: str) -> bool:
        """
        Soft delete a course (set is_active to False)
        
        Args:
            course_id: Course's unique identifier
            
        Returns:
            True if deleted, False otherwise
        """
        try:
            result = self.collection.update_one(
                {"_id": course_id},
                {"$set": {"is_active": False, "updated_date": datetime.now(timezone.utc)}}
            )
            
            if result.modified_count > 0:
                logger.info(f"Deleted course with ID: {course_id}")
                return True
            
            return False
        except Exception as e:
            logger.error(f"Error deleting course {course_id}: {e}")
            raise
