from fastapi import APIRouter

from app.routers import users, students, login

api_router = APIRouter()
api_router.include_router(users.router)
api_router.include_router(students.router)
api_router.include_router(login.router)