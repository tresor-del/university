from uuid import UUID
from fastapi import BackgroundTasks, File, UploadFile
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.media import Media
from app.models.students import Student
from app.schemas.media import MediaCreate, MediaResponse
from app.background_tasks.media import encrypt_and_store
from app.utils.media import save_temp_file

def add_media(
    *,
    db: Session,
    file_type: str,
    file: UploadFile = File(...),
    student_id: UUID = None,
    teacher_id: UUID = None,
    background_tasks: BackgroundTasks,
    is_principal: bool = False
) -> Media | None:
    """
    Ajoute un nouveau média avec traitement en arrière-plan
    """
    
    if student_id and teacher_id:
        return None
    elif not (student_id or teacher_id):
        return None
    
    print(file)
    
    temp_media_data = MediaCreate(
        file_path="",  # Sera mis à jour par la background task
        file_type=file_type,
        mime_type = None, # juste pour que les test de crud marchent
        status="processing",
        student_id=student_id,
        teacher_id=teacher_id,
        is_principal=is_principal,
        file_size=0,  # Sera calculé
        storage_location="local"
    )
    
    temp_path, media = save_temp_file(
        db=db, 
        temp_file=temp_media_data, 
        file=file,
        file_type=file_type
    )
    
    encrypt_and_store(db=db, media_id=media.id, temp_path=temp_path, file_type=file_type) # parceque bg_tasks ne marche que dans les routes
    
    # background_tasks.add_task(
    #     encrypt_and_store,
    #     db,
    #     media.id,
    #     temp_path,
    #     file_type,
    # )
    
    media = db.execute(select(Media).where(Media.id==media.id)).scalar_one_or_none()
    return media if media else None

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

def update_principal_photo(*, db: Session,background_tasks: BackgroundTasks, student_id: UUID = None, teacher_id: UUID = None, new_file: UploadFile = None) -> Media | None:
    if student_id and teacher_id:
        return None
    elif student_id or teacher_id:
        old_principal_medias = db.query(Media).filter(
            Media.student_id==student_id,
            Media.teacher_id==teacher_id,
            Media.is_principal==True
        ).all()
        for media in old_principal_medias:
            media.is_principal = False
        db.commit()
        for media in old_principal_medias:
            db.refresh(media)
        if not new_file:
            return None
        if new_file:
            media = add_media(db=db, file_type="photo", file=new_file, student_id=student_id, teacher_id=teacher_id, background_tasks=background_tasks, is_principal=True)
            return media
        return None

def delete_media(*, db: Session, file_path: str, student_id: UUID = None, teacher_id: UUID = None) -> bool | None:
    if student_id and teacher_id:
        return None
    elif student_id or teacher_id:
        media = db.query(Media).where(
            Media.student_id==student_id,
             Media.teacher_id==teacher_id,
             Media.file_path==file_path
        ).first()
        if media:
            db.delete(media)
            db.commit()
            return True
        return None
    return None

def get_media(*, db: Session, file_path: str, student_id: UUID =None, teacher_id: UUID = None) -> Media | None:
    if student_id and teacher_id:
        return None
    elif student_id or teacher_id:
        media = db.query(Media).where(
            Media.student_id==student_id,
            Media.teacher_id==teacher_id,
            Media.file_path==file_path
        ).first()
        if media:
            return media
        return None
    return None
