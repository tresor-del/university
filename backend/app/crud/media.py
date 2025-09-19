from uuid import UUID
from fastapi import File, UploadFile
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.media import Media
from app.models.students import Student
from app.schemas.media import MediaCreate, MediaResponse
from app.core.security import save_encrypted_file

def add_media(*,db: Session,file_type: str, student_id: UUID = None, teacher_id: UUID = None, file: UploadFile = File(...)) -> Media | None:
    if student_id and teacher_id:
        return None
    elif student_id or teacher_id:
        file_location = save_encrypted_file(file, file.filename)
        media_data = MediaCreate(
            file_path=file_location,
            file_type=file_type, 
            mime_type=file.content_type,
            student_id=student_id,
            teacher_id=teacher_id
        )
        db_media = Media(**media_data.model_dump())
        db.add(db_media)
        db.commit()
        db.refresh(db_media)
        return db_media
    else:
        return None

def read_media(*, db: Session, student_id: UUID = None, teacher_id: UUID = None) -> dict | None:
    if student_id and teacher_id:
        return None
    
    elif student_id or teacher_id:
        count_stm = select(func.count()).select_from(Media).where(
            Media.student_id==student_id, 
            Media.teacher_id==teacher_id
        )
        count = db.execute(count_stm).scalar()
        medias = db.query(Media).filter(
            Media.student_id==student_id,
            Media.teacher_id==teacher_id
        ).all()
        return {"data": medias, "count": count}
    return None
 
def add_principal_photo(*, db: Session, student_id: UUID = None, teacher_id: UUID = None, file: UploadFile = File(...)) -> Media | None:
    if student_id and teacher_id:
        return None
    
    elif student_id or teacher_id:
        file_location = save_encrypted_file(file, file.filename)
        media_data = MediaCreate(
            file_path=file_location,
            file_type="photo", 
            mime_type=file.content_type,
            student_id=student_id,
            teacher_id=teacher_id,
            is_principal=True
        )
        db_media = Media(**media_data.model_dump())
        db.add(db_media)
        db.commit()
        db.refresh(db_media)
        return db_media
    return None

def change_principal_photo(*, db: Session, student_id: UUID = None, teacher_id: UUID = None, new_file: UploadFile = None) -> Media | None:
    if student_id and teacher_id:
        return None
    elif student_id or teacher_id:
        old_principal_media = db.query(Media).filter(
            Media.student_id==student_id,
            Media.teacher_id==teacher_id,
            Media.is_principal==True
        ).first()
        if old_principal_media:
            old_principal_media.is_principal == False
            db.commit()
            db.refresh(old_principal_media)
        else: 
            if new_file:
                file_location = save_encrypted_file(new_file, new_file.filename)
                media_data = MediaCreate(
                    file_path=file_location,
                    file_type="photo",
                    mime_type=new_file.content_type,
                    student_id=student_id,
                    teacher_id=teacher_id,
                    is_princpal=True
                )
                db_media = Media(**media_data.model_dump())
                db.add(db_media)
                db.commit()
                db.refresh(db_media)
                return db_media
            return None

def delete_media(*, db: Session, file_path: str, student_id: UUID = None, teacher_id: UUID = None) -> bool | None:
    if student_id and teacher_id:
        return None
    elif student_id or teacher_id:
        if file_path:
            media = db.query(Media).where(
                Media.student_id==student_id,
                Media.teacher_id==teacher_id,
                Media.file_path==file_path
            ).first()
            db.delete(media)
            db.commit()
            return True
        return None
    return None