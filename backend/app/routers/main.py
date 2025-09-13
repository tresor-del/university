from fastapi import APIRouter

from app.routers import users, students, login, teachers, courses, departements, programs

api_router = APIRouter()
api_router.include_router(users.router)
api_router.include_router(students.router)
api_router.include_router(login.router)
api_router.include_router(teachers.router)
api_router.include_router(courses.router)
api_router.include_router(departements.router)
api_router.include_router(programs.router)
