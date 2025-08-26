from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import students

app = FastAPI(
    title="Application de Gestion Scolaire"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(students.router)