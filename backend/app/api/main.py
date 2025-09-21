from fastapi import APIRouter

from app.api.routes import users, students, login, teachers, courses, departements, programs, media

api_router = APIRouter()
api_router.include_router(users.router)
api_router.include_router(students.router)
api_router.include_router(login.router)
api_router.include_router(teachers.router)
api_router.include_router(courses.router)
api_router.include_router(departements.router)
api_router.include_router(programs.router)
api_router.include_router(media.router)

