import os, io, shutil

from fastapi.routing import APIRouter
from fastapi import UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse

from app.core.security import encrypt_file, decrypt_file
from app.models.media import Media
from app.schemas.message import Message
from app.schemas.media import MediaCreate, MediaResponse, MediumResponse
from app.core import settings
from app.core.security import save_encrypted_file, read_encrypted_file
from app.deps import SessionDeps
from app.crud import media


router = APIRouter(prefix="/media", tags=["media"])

@router.post("/", response_model=MediaResponse)
def upload_media(db: SessionDeps, student_id: int = None, teacher_id: int = None, file: UploadFile = File(...)):
    file_location = save_encrypted_file(file, file.filename)
    media_data = MediaCreate(
        file_path=file_location,
        file_type="photo", 
        mime_type=file.content_type,
        student_id=student_id,
        teacher_id=teacher_id
    )
    return media.create_media(db=db, media=media_data)

@router.get("/download/{media_id}")
def download_media(media_id: int, db: SessionDeps):
    media = db.query(Media).filter(Media.id == media_id).first()
    if not media:
        raise HTTPException(status_code=404, detail="Fichier introuvable")
    
    content = read_encrypted_file(media.file_path)
    return StreamingResponse(io.BytesIO(content), media_type=media.mime_type)
