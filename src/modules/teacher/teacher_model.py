from typing import Optional, List
from bson import ObjectId
from pydantic import BaseModel, Field
from datetime import datetime, timezone



class Teacher(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    name: str
    email: str
    subject_expertise: Optional[str] = None
    experience_years: Optional[int] = None
    created_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_active: bool = True