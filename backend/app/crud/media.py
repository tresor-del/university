from sqlalchemy.orm import Session

from app.models.media import Media
from app.schemas.media import MediaCreate

def create_media(*,db: Session, media: MediaCreate):
    db_media = Media(**media.model_dump())
    db.add(db_media)
    db.commit()
    db.refresh(db_media)
    return db_media

def get_student_media(*, db: Session, student_id: int):
    return db.query(Media).filter(Media.id==id).all()

def get_teacher_media(*, db: Session, teacher_id: int):
    return db.query(Media).filter(Media.id==id).all()