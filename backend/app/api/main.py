from app.api.routes.admins import courses, departements, faculties, programs, teachers
from app.api.routes.admins.services_inscription import new_students
from app.api.routes.auth import login
from app.api.routes.public import media, students as self_enrollment_students
from fastapi import APIRouter

from app.api.routes import users

api_router = APIRouter()
api_router.include_router(users.router)
api_router.include_router(new_students.router)
api_router.include_router(login.router)
api_router.include_router(teachers.router)
api_router.include_router(courses.router)
api_router.include_router(departements.router)
api_router.include_router(programs.router)
api_router.include_router(media.router)
api_router.include_router(faculties.router)
