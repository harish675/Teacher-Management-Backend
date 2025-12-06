from fastapi import APIRouter, Depends

from .modules.student.student_router import router as student_router
from .modules.teacher.teacher_router import router as teacher_router
from .modules.course.course_router import router as course_router
from .modules.assign_teacher.assign_teacher_router import router as assign_teacher_router
from .modules.enrolled_studets.enrolled_students_router import router as enrolled_students_router

router = APIRouter()

# Include all module routers
router.include_router(student_router)
router.include_router(teacher_router)
router.include_router(course_router)
router.include_router(assign_teacher_router)
router.include_router(enrolled_students_router)


@router.get("/health")
async def root():
    return {"message": "Hello World"}

