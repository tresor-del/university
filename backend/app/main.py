from fastapi import FastAPI
from .routers import students
from app.middlewares import setup_middleware



app = FastAPI()

setup_middleware(app)

app.include_router(students.router)

@app.get(
    "/",
    tags=["health"]
)
async def root():
    return {"message": "L'application tourne avec succès"}