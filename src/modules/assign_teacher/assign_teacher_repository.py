from typing import List, Optional
from pymongo.database import Database
from bson import ObjectId
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)


class AssignTeacherRepository:
    """Repository for Teacher-Course assignment operations"""
    
    def __init__(self, db: Database):
        self.db = db
        self.courses_collection = db["courses"]
        self.teachers_collection = db["teachers"]
    
    def assign_courses_to_teacher(self, teacher_id: str, course_ids: List[str]) -> dict:
        """
        Assign multiple courses to a teacher
        
        Args:
            teacher_id: Teacher's unique identifier
            course_ids: List of course IDs to assign
            
        Returns:
            Dictionary with assignment results
        """
        try:
            assigned_courses = []
            already_assigned = []
            
            for course_id in course_ids:
                if not ObjectId.is_valid(course_id):
                    continue
                
                # Check if teacher is already assigned to this course
                course = self.courses_collection.find_one({
                    "_id": course_id,
                    "is_active": True
                })
                
                if not course:
                    continue
                
                if teacher_id in course.get("teacher_ids", []):
                    already_assigned.append(course_id)
                    continue
                
                # Add teacher to course
                result = self.courses_collection.update_one(
                    {"_id": course_id, "is_active": True},
                    {
                        "$addToSet": {"teacher_ids": teacher_id},
                        "$set": {"updated_date": datetime.now(timezone.utc)}
                    }
                )
                
                if result.modified_count > 0:
                    assigned_courses.append(course_id)
                    logger.info(f"Assigned teacher {teacher_id} to course {course_id}")
            
            return {
                "teacher_id": teacher_id,
                "assigned_courses": assigned_courses,
                "already_assigned": already_assigned,
                "total_assigned": len(assigned_courses)
            }
        except Exception as e:
            logger.error(f"Error assigning courses to teacher: {e}")
            raise
    
    def unassign_courses_from_teacher(self, teacher_id: str, course_ids: List[str]) -> dict:
        """
        Unassign multiple courses from a teacher
        
        Args:
            teacher_id: Teacher's unique identifier
            course_ids: List of course IDs to unassign
            
        Returns:
            Dictionary with unassignment results
        """
        try:
            unassigned_courses = []
            
            for course_id in course_ids:
                if not course_id:
                    continue
                
                result = self.courses_collection.update_one(
                    {"_id": course_id, "is_active": True},
                    {
                        "$pull": {"teacher_ids": teacher_id},
                        "$set": {"updated_date": datetime.now(timezone.utc)}
                    }
                )
                
                if result.modified_count > 0:
                    unassigned_courses.append(course_id)
                    logger.info(f"Unassigned teacher {teacher_id} from course {course_id}")
            
            return {
                "teacher_id": teacher_id,
                "unassigned_courses": unassigned_courses,
                "total_unassigned": len(unassigned_courses)
            }
        except Exception as e:
            logger.error(f"Error unassigning courses from teacher: {e}")
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
                self.courses_collection.find({
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
    
    def get_teachers_by_course(self, course_id: str) -> List[str]:
        """
        Get all teacher IDs assigned to a course
        
        Args:
            course_id: Course's unique identifier
            
        Returns:
            List of teacher IDs
        """
        try:
            if not ObjectId.is_valid(course_id):
                return []
            
            course = self.courses_collection.find_one({
                "_id": ObjectId(course_id),
                "is_active": True
            })
            
            if course:
                return course.get("teacher_ids", [])
            
            return []
        except Exception as e:
            logger.error(f"Error fetching teachers by course {course_id}: {e}")
            raise
