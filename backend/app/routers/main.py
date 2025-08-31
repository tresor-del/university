from fastapi import APIRouter

from app.routers import users, students

api_router = APIRouter()
api_router.include_router(users.router)
api_router.include_router(students.router)
