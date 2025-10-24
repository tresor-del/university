import io
from uuid import UUID
import qrcode

from fastapi import BackgroundTasks, status
from fastapi.routing import APIRouter
from fastapi import UploadFile, File, HTTPException, Depends
from fastapi.responses import StreamingResponse

from app.models.media import Media
from app.schemas.media import MediaCreate, MediaResponse
from app.schemas.message import Message
from app.core import settings
from app.api.deps import SessionDeps, get_current_active_admin
from app.crud.public.media import add_media, delete_media
from app.models.teachers import Teacher
from app.models.students import Student

router = APIRouter(prefix="/media", tags=["media"])

@router.post("/{file_type}")
def upload_media(
    db: SessionDeps,
    file_type: str,
    student_id: UUID | None = None,
    teacher_id: UUID | None = None,
    file: UploadFile = File(...),
) -> MediaResponse:
    
    if not student_id and not teacher_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You must provide either student_id or teacher_id"
        )

    m = add_media(
        db=db,
        file_type=file_type,
        student_id=student_id,
        teacher_id=teacher_id,
        file=file,
        background_tasks=BackgroundTasks,
    )

    return MediaResponse.model_validate(m)


@router.delete("/delete/")
def delete_media_route(db: SessionDeps, file_path: str, teacher_id: UUID = None, student_id: UUID = None) -> Message:
    media = delete_media(
        db=db,
        file_path=file_path,
        student_id=student_id,
        teacher_id=teacher_id,
    )
    if not media:
        raise HTTPException(status_code=404, detail="Fichier introuvable")
    return Message(message='Média supprimé avec succès')