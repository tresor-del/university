from fastapi import dependencies, Depends
from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException

from app.deps import get_current_active_admin, SessionDeps
from app.models.university import Course
from app.schemas.message import Message
from app.schemas.university import CourseCreate, CourseUpdate, CourseResponse, CoursesResponse
from app.crud.courses import (
    read_courses,
    create_course,
    update_course,
    delete_course,
    get_course
)

router = APIRouter(prefix="/courses", tags=["courses"])



@router.get("/", dependencies=[Depends(get_current_active_admin)], response_model=CoursesResponse)
def read_courses_route(db: SessionDeps, skip: int = 0, limit: int = 100) -> CoursesResponse:
    """
    Récupérer la liste de toutes les cours
    """
    courses = read_courses(db=db, skip=skip, limit=limit)
    return courses

@router.post("/", dependencies=[Depends(get_current_active_admin)], response_model=CourseResponse)
def create_course_route(db: SessionDeps, data: CourseCreate) -> CourseResponse:
    """
    creéer un cours
    """
    course = create_course(db=db, course_data=data)
    return course

@router.patch("/{course_id}", dependencies=[Depends(get_current_active_admin)], response_model=CourseResponse)
def update_course_route(db: SessionDeps, course_id: int, data: CourseUpdate) -> CourseResponse:
    """
    Mets à jour un cours
    """
    course = db.get(Course, course_id)
    if not course:
        raise HTTPException(
            status_code=404,
            detail="Cours non trouvé sur le système"
        )
    course_updated = update_course(db=db, course_id=course_id, data=data)
    return course_updated

@router.delete("/{course_id}", dependencies=[Depends(get_current_active_admin)], response_model=Message)
def delete_course_route(db: SessionDeps, course_id: int) -> Message:
    """
    Supprime un cours
    """
    result = delete_course(db=db, course_id=course_id)
    if result:
        return Message("Cours supprimé avec succès")
    raise HTTPException(
            status_code=404,
            detail="Cours non trouvé sur le système"
        )

@router.get("/{course_id}", dependencies=[Depends(get_current_active_admin)], response_model=CourseResponse)
def get_course_route(db: SessionDeps, course_id: int) -> CourseResponse:
    """
    Récupérer un cours
    """
    course = get_course(db=db, course_id=course_id)
    if course:
        return course
    raise HTTPException(
        status_code=404,
        detail="Cours non trouvé sur le système"
    )
