import io
from uuid import UUID
import qrcode

from fastapi.routing import APIRouter
from fastapi import UploadFile, File, HTTPException, Depends
from fastapi.responses import StreamingResponse

from app.models.media import Media
from app.schemas.media import MediaCreate, MediaResponse
from app.core import settings
from app.core.security import save_encrypted_file, read_encrypted_file
from app.deps import SessionDeps, get_current_active_admin
from app.crud import media

router = APIRouter(prefix="/media", tags=["media"])

@router.post("/", response_model=MediaResponse)
def upload_media(db: SessionDeps, file_type: str, student_id: UUID = None, teacher_id: UUID = None, file: UploadFile = File(...)):
    
    return media.create_media(
        db=db, 
        file_type=file_type, 
        student_id=student_id, 
        teacher_id=teacher_id, 
        file=file
    )

@router.get("/download/{media_id}")
def download_media(media_id: UUID, db: SessionDeps):
    media = db.query(Media).filter(Media.id == media_id).first()
    if not media:
        raise HTTPException(status_code=404, detail="Fichier introuvable")
    
    content = read_encrypted_file(media.file_path)
    return StreamingResponse(io.BytesIO(content), media_type=media.mime_type)

@router.post("/qr_code", dependencies=[Depends(get_current_active_admin)])
def create_qr_code(db: SessionDeps, media_in: MediaCreate, data: str, student_id: UUID = None, teacher_id: UUID = None):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    file = qr.make_image(fill_color="black", back_color="white")
    
    if student_id:
        filename = f"qr_{student_id}.png"
    elif teacher_id:
        filename = f"qr_{teacher_id}.png"
        
    file_location = save_encrypted_file(file, filename)
    media_data = MediaCreate(
        file_path=file_location,
        file_type="qr_code", 
        mime_type="image/png",
        student_id=student_id,
        teacher_id=teacher_id
    )
    return media.create_media(db=db, media=media_data)

@router.get("/qr_code/{qr_id}", dependencies=[Depends(get_current_active_admin)])
def get_qr_code(db: SessionDeps, qr_id: UUID ):
    media = db.query(Media).filter(Media.id == qr_id).first()
    if not media:
        raise HTTPException(status_code=404, detail="Qr_code introuvable")
    
    content = read_encrypted_file(media.file_path)
    return StreamingResponse(io.BytesIO(content), media_type=media.mime_type)