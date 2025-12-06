from pydantic import BaseModel

class User(BaseModel):
    id: str
    name: str
    email: str



class CourseStudentEnrollment(BaseModel):
    course_id: str
    student_id: str
    enrolled_by: User
