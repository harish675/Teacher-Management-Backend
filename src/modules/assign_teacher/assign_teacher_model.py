from pydantic import BaseModel
from datetime import datetime, timezone
from pydantic import Field 

class User(BaseModel):
    id: str
    name: str
    email: str
    

class CourseTeacherAssignment(BaseModel):
    course_id: str
    teacher_id: str
    assigned_by: User
    assigned_date: str
    created_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_active: bool = True
