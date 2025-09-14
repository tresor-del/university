from uuid import UUID
from sqlalchemy.orm import Session

from app.models.media import Media
from app.schemas.media import MediaCreate

def create_media(*,db: Session, media: MediaCreate):
    db_media = Media(**media.model_dump())
    db.add(db_media)
    db.commit()
    db.refresh(db_media)
    return db_media

def get_student_media(*, db: Session, student_id: UUID):
    return db.query(Media).filter(Media.id==student_id).all()

def get_teacher_media(*, db: Session, teacher_id: UUID):
    return db.query(Media).filter(Media.id==teacher_id).all()
