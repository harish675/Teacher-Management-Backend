
from .mock_data import students_mock_data, teachers_mock_data, courses_mock_data

from ..assign_teacher.assign_teacher_model import CourseTeacherAssignment
from ..course.course_model import Course
from ..enrolled_studets.enrolled_students_model import CourseStudentEnrollment
from ..student.student_model import Student
from ..teacher.teacher_model import Teacher



class SeedData:
    
    def __init__(self):
        from ...lib.database import mongo_connection
        from bson import ObjectId
        db = mongo_connection.db

        def add_string_id(data_list):
            for item in data_list:
                if '_id' not in item:
                    item['_id'] = str(ObjectId())
            return data_list

        # Seed Teachers
        if db.teachers.count_documents({}) == 0:
            db.teachers.insert_many(add_string_id(teachers_mock_data))

        # Seed Students
        if db.students.count_documents({}) == 0:
            db.students.insert_many(add_string_id(students_mock_data))

        # Seed Courses
        if db.courses.count_documents({}) == 0:
            db.courses.insert_many(add_string_id(courses_mock_data))


       