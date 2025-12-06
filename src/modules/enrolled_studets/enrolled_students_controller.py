from typing import List
from fastapi import HTTPException, status
from pymongo.database import Database
import logging

from .enrolled_students_repository import EnrolledStudentsRepository
from .enrolled_students_schema import (
    EnrollStudentCourseRequest,
    StudentCourseResponse,
    CourseStudentsResponse
)
from ..student.student_repository import StudentRepository
from ..course.course_repository import CourseRepository

logger = logging.getLogger(__name__)


class EnrolledStudentsController:
    """Controller for Student-Course enrollment business logic"""
    
    def __init__(self, db: Database):
        self.repository = EnrolledStudentsRepository(db)
        self.student_repository = StudentRepository(db)
        self.course_repository = CourseRepository(db)
    
    def enroll_student_in_courses(self, request: EnrollStudentCourseRequest) -> StudentCourseResponse:
        """
        Enroll a student in multiple courses
        
        Args:
            request: EnrollStudentCourseRequest with student_id and course_ids
            
        Returns:
            StudentCourseResponse with enrollment details
            
        Raises:
            HTTPException: If student or courses not found
        """
        try:
            # Validate student exists
            student = self.student_repository.get_student_by_id(request.student_id)
            if not student:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Student with ID {request.student_id} not found"
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
            
            # Enroll student in courses
            result = self.repository.enroll_student_in_courses(
                request.student_id,
                request.course_ids
            )
            
            # Get updated course list for student
            student_courses = self.repository.get_courses_by_student(request.student_id)
            
            return StudentCourseResponse(
                student_id=request.student_id,
                student_name=student["name"],
                courses=student_courses,
                total_courses=len(student_courses)
            )
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error in enroll_student_in_courses controller: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to enroll student in courses"
            )
    
    def get_students_by_course(self, course_id: str) -> CourseStudentsResponse:
        """
        Get all students enrolled in a course
        
        Args:
            course_id: Course's unique identifier
            
        Returns:
            CourseStudentsResponse with enrolled students
            
        Raises:
            HTTPException: If course not found
        """
        try:
            # Validate course exists
            course = self.course_repository.get_course_by_id(course_id)
            if not course:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Course with ID {course_id} not found"
                )
            
            # Get student IDs enrolled in course
            student_ids = self.repository.get_students_by_course(course_id)
            
            # Get student details
            students = self.student_repository.get_students_by_ids(student_ids) if student_ids else []
            
            return CourseStudentsResponse(
                course_id=course_id,
                course_name=course["course_name"],
                students=students,
                total_students=len(students)
            )
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error in get_students_by_course controller: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to fetch students for course"
            )
    
    def get_courses_by_student(self, student_id: str) -> StudentCourseResponse:
        """
        Get all courses a student is enrolled in
        
        Args:
            student_id: Student's unique identifier
            
        Returns:
            StudentCourseResponse with student's courses
            
        Raises:
            HTTPException: If student not found
        """
        try:
            # Validate student exists
            student = self.student_repository.get_student_by_id(student_id)
            if not student:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Student with ID {student_id} not found"
                )
            
            # Get courses for student
            courses = self.repository.get_courses_by_student(student_id)
            
            return StudentCourseResponse(
                student_id=student_id,
                student_name=student["name"],
                courses=courses,
                total_courses=len(courses)
            )
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error in get_courses_by_student controller: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to fetch courses for student"
            )
    
    def get_all_enrollments(self) -> List[CourseStudentsResponse]:
        """
        Get all course enrollments
        
        Returns:
            List of CourseStudentsResponse with all enrollments
        """
        try:
            enrollments = self.repository.get_all_enrollments()
            
            result = []
            for enrollment in enrollments:
                # Get student details for each course
                student_ids = enrollment.get("enrolled_student_ids", [])
                students = self.student_repository.get_students_by_ids(student_ids) if student_ids else []
                
                result.append(CourseStudentsResponse(
                    course_id=enrollment["course_id"],
                    course_name=enrollment["course_name"],
                    students=students,
                    total_students=len(students)
                ))
            
            return result
        except Exception as e:
            logger.error(f"Error in get_all_enrollments controller: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to fetch enrollments"
            )
