from typing import List, Optional
from pymongo.database import Database
from bson import ObjectId
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)


class EnrolledStudentsRepository:
    """Repository for Student-Course enrollment operations"""
    
    def __init__(self, db: Database):
        self.db = db
        self.courses_collection = db["courses"]
        self.students_collection = db["students"]
    
    def enroll_student_in_courses(self, student_id: str, course_ids: List[str]) -> dict:
        """
        Enroll a student in multiple courses
        
        Args:
            student_id: Student's unique identifier
            course_ids: List of course IDs to enroll in
            
        Returns:
            Dictionary with enrollment results
        """
        try:
            enrolled_courses = []
            already_enrolled = []
            
            for course_id in course_ids:
                if not ObjectId.is_valid(course_id):
                    continue
                
                # Check if student is already enrolled in this course
                course = self.courses_collection.find_one({
                    "_id": course_id,
                    "is_active": True
                })
                
                if not course:
                    continue
                
                if student_id in course.get("enrolled_student_ids", []):
                    already_enrolled.append(course_id)
                    continue
                
                # Add student to course
                result = self.courses_collection.update_one(
                    {"_id": course_id, "is_active": True},
                    {
                        "$addToSet": {"enrolled_student_ids": student_id},
                        "$set": {"updated_date": datetime.now(timezone.utc)}
                    }
                )
                
                if result.modified_count > 0:
                    enrolled_courses.append(course_id)
                    logger.info(f"Enrolled student {student_id} in course {course_id}")
            
            return {
                "student_id": student_id,
                "enrolled_courses": enrolled_courses,
                "already_enrolled": already_enrolled,
                "total_enrolled": len(enrolled_courses)
            }
        except Exception as e:
            logger.error(f"Error enrolling student in courses: {e}")
            raise
    
    def unenroll_student_from_courses(self, student_id: str, course_ids: List[str]) -> dict:
        """
        Unenroll a student from multiple courses
        
        Args:
            student_id: Student's unique identifier
            course_ids: List of course IDs to unenroll from
            
        Returns:
            Dictionary with unenrollment results
        """
        try:
            unenrolled_courses = []
            
            for course_id in course_ids:
                if not course_id:
                    continue
                
                result = self.courses_collection.update_one(
                    {"_id": course_id, "is_active": True},
                    {
                        "$pull": {"enrolled_student_ids": student_id},
                        "$set": {"updated_date": datetime.now(timezone.utc)}
                    }
                )
                
                if result.modified_count > 0:
                    unenrolled_courses.append(course_id)
                    logger.info(f"Unenrolled student {student_id} from course {course_id}")
            
            return {
                "student_id": student_id,
                "unenrolled_courses": unenrolled_courses,
                "total_unenrolled": len(unenrolled_courses)
            }
        except Exception as e:
            logger.error(f"Error unenrolling student from courses: {e}")
            raise
    
    def get_students_by_course(self, course_id: str) -> List[str]:
        """
        Get all student IDs enrolled in a course
        
        Args:
            course_id: Course's unique identifier
            
        Returns:
            List of student IDs
        """
        try:
            if not ObjectId.is_valid(course_id):
                return []
            
            course = self.courses_collection.find_one({
                "_id": ObjectId(course_id),
                "is_active": True
            })
            
            if course:
                return course.get("enrolled_student_ids", [])
            
            return []
        except Exception as e:
            logger.error(f"Error fetching students by course {course_id}: {e}")
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
                self.courses_collection.find({
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
    
    def get_all_enrollments(self) -> List[dict]:
        """
        Get all course enrollments with student details
        
        Returns:
            List of courses with enrolled students
        """
        try:
            courses = list(
                self.courses_collection.find({"is_active": True})
            )
            
            enrollments = []
            for course in courses:
                course["_id"] = str(course["_id"])
                enrollments.append({
                    "course_id": course["_id"],
                    "course_name": course.get("course_name", ""),
                    "enrolled_student_ids": course.get("enrolled_student_ids", []),
                    "total_students": len(course.get("enrolled_student_ids", []))
                })
            
            return enrollments
        except Exception as e:
            logger.error(f"Error fetching all enrollments: {e}")
            raise
