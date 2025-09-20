import io

from sqlalchemy import select

from fastapi import UploadFile

from app.models.media import Media
from app.models.teachers import Teacher
from app.models.students import Student

def create_fake_media(filename: str = "photo.png"):
    fake_png = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR"
    file = io.BytesIO(fake_png)
    file = UploadFile(filename=filename, file=file)
    return file

def check_principal_photo(*,db, entity, principal_media, is_teacher:bool = False):
    assert principal_media
    assert isinstance(principal_media, Media)
    assert principal_media.is_principal 

    # Vérifier que l'entité a le média principal
    entity_query = select(type(entity)).where(type(entity).id == entity.id)
    entity_db = db.execute(entity_query).scalar_one_or_none()
    assert entity_db.medias
    assert principal_media in entity_db.medias
    
    # Vérifier que le média existe dans la bdd
    conditions = [Media.file_path == principal_media.file_path]
    if is_teacher:
        conditions.append(Media.teacher_id == entity.id)
    else:
        conditions.append(Media.student_id == entity.id)
    media_query = select(Media).where(*conditions)
    media_db = db.execute(media_query).scalar_one_or_none()
    assert media_db
    assert media_db.file_path == principal_media.file_path

    
    
def check_add_media(*, db, entity, media, is_teacher: bool = False):
    
    # vérifier que l'entité de la base de donnée est relié au media
    entity_query = select(type(entity)).where(type(entity).id == entity.id)

    entity = db.execute(entity_query).scalar_one_or_none()
    assert len(entity.medias) >= 1

    # vérifier que le média rélié a l'entité
    assert hasattr(entity, "medias")
    assert isinstance(media, Media)

    if is_teacher:
        assert media.teacher_id == entity.id
        assert media.student_id is None
    else:
        assert media.student_id == entity.id
        assert media.teacher_id is None
    
    assert media.file_type == "photo"
    
    # Vérifider la relation côté entité
    assert isinstance(entity.medias, list)
    assert len(entity.medias) >= 1
    assert media in entity.medias 
    
def check_read_media(*, db, entity, media1, media2, data, count, is_teacher: bool = False):
    entity_query = select(type(entity)).where(
            type(entity).id == entity.id
        )
    entity = db.execute(entity_query).scalar_one_or_none()
    print(entity.medias)
    assert len(entity.medias) >= 2
    
    assert isinstance(data, list)
    assert count == 2
    assert len(data) >= 2  
    
    # Vérifier que tous les médias appartiennent au bon entité
    for m in data:
        if is_teacher:
            assert m.teacher_id == entity.id
            assert m.student_id is None
        else:
            assert m.student_id == entity.id
            assert m.teacher_id is None
    
    # Vérifier que nos médias sont dans la liste
    media_ids = [m.id for m in data]
    assert media1.id in media_ids
    assert media2.id in media_ids

    # Vérifier que l'entité a les médias
    assert entity.medias
    for media in data:
        assert media in entity.medias