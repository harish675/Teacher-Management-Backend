
from typing import Optional, List
from bson import ObjectId
from pydantic import BaseModel, Field
from datetime import datetime, timezone


class Course(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    course_name: str
    description: Optional[str] = None
    teacher_ids: List[str] = Field(default_factory=list)
    enrolled_student_ids: List[str] = Field(default_factory=list)
    created_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_active: bool = True