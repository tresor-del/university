from typing import Any
import uuid

from fastapi import BackgroundTasks
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.crud.public.media import add_media, delete_media, get_media, read_media, update_principal_photo
from app.tests.utils.teachers import create_random_teacher
from app.tests.utils.students import create_random_student
from app.models.media import Media
from app.tests.utils.students import create_random_student
from app.tests.utils.media import check_read_media, create_fake_media, check_principal_photo, check_add_media
from app.models.teachers import Teacher
from app.models.students import Student

def test_add_media_teacher(db: Session, bgtasks: BackgroundTasks) -> None:
    """
    Test l'ajout d'un média à un enseignant.
    """
    file = create_fake_media()
    
    teacher = create_random_teacher(db)
    teacher_db = db.query(Teacher).where(Teacher.id==teacher.id).first()
    
    media = add_media(db=db, file_type="photo", teacher_id=teacher.id, file=file, background_tasks=bgtasks)
    
    print(media.status)
    assert media.file_path != ''
    
    check_add_media(db=db, entity=teacher_db, media=media, is_teacher=True)
      
def test_add_media_student(db: Session, bgtasks: BackgroundTasks) -> None:
    """
    Test l'ajout d'un média à un étudiant.
    """
    file = create_fake_media()
    
    student = create_random_student(db)
    student_db = db.query(Student).where(Student.id==student.id).first()
    media = add_media(db=db, file_type="photo", student_id=student.id, file=file , background_tasks=bgtasks)
    
    check_add_media(db=db, entity=student_db, media=media, is_teacher=False)
    
def test_add_media_with_no_teacher_student(db: Session, bgtasks: BackgroundTasks) -> None:
    """Test l'ajout d'un média sans enseignant ni étudiant."""
    file = create_fake_media()
    r = add_media(db=db, file_type="photo", file=file, background_tasks=bgtasks)
    assert r is None
    
def test_add_media_with_both_teacher_and_student(db: Session, bgtasks: BackgroundTasks) -> None:
    """
    Test l'ajout d'un média avec à la fois un enseignant et un étudiant .
    """
    file = create_fake_media()
    teacher = create_random_teacher(db)
    student = create_random_student(db)
    r = add_media(db=db, file_type="photo", teacher_id=teacher.id, student_id=student.id, file=file, background_tasks=bgtasks)
    
    assert r is None

def test_read_media_teacher(db: Session, bgtasks: BackgroundTasks) -> None:
    """Test la récupération des médias d'un enseignant."""
    file1 = create_fake_media()
    file2 = create_fake_media()
    teacher = create_random_teacher(db)
    teacher_db = db.query(Teacher).where(Teacher.id == teacher.id).first()
    
    # Ajouter plusieurs médias
    media1 = add_media(db=db, file_type="photo", teacher_id=teacher.id, file=file1, background_tasks=bgtasks)
    media2 = add_media(db=db, file_type="document", teacher_id=teacher.id, file=file2, background_tasks=bgtasks)
    
    r = read_media(db=db, teacher_id=teacher.id)
    data = r["data"]
    count = r["count"]

    check_read_media(db=db, entity=teacher_db, media1=media1, media2=media2, data=data, count=count, is_teacher=True)

def test_read_media_student(db: Session, bgtasks: BackgroundTasks) -> None:
    """Test la récupération des médias d'un étudiant."""
    file1 = create_fake_media()
    file2 = create_fake_media()
    student = create_random_student(db)
    student_db = db.query(Student).where(Student.id == student.id).first()
    
    # Ajouter plusieurs médias
    media1 = add_media(db=db, file_type="photo", student_id=student.id, file=file1, background_tasks=bgtasks)
    media2 = add_media(db=db, file_type="qr", student_id=student.id, file=file2, background_tasks=bgtasks)
    
    r = read_media(db=db, student_id=student.id)

    data = r["data"]
    count = r["count"]
    
    check_read_media(db=db, entity=student_db, media1=media1, media2=media2, data=data, count=count, is_teacher=False)

def test_read_media_nonexistent_teacher(db: Session, bgtasks: BackgroundTasks) -> None:
    """Test la récupération des médias pour un enseignant inexistant."""
    fake_teacher_id = uuid.uuid4()
    r = read_media(db=db, teacher_id=fake_teacher_id)
    
    assert isinstance(r["data"], list)
    assert len(r["data"]) == 0 

def test_read_media_nonexistent_student(db: Session, bgtasks: BackgroundTasks) -> None:
    """Test la récupération des médias pour un étudiant inexistant."""
    fake_student_id = uuid.uuid4()
    r = read_media(db=db, student_id=fake_student_id)
    
    assert isinstance(r["data"], list)
    assert len(r["data"]) == 0 

def test_read_media_no_parameters(db: Session, bgtasks: BackgroundTasks) -> None:
    """
    Test la récupération des médias sans paramètres.
    """
    try:
        r = read_media(db=db)
    except Exception as e:
        assert True

def test_media_isolation_teacher_student(db: Session, bgtasks: BackgroundTasks) -> None:
    """Test que les médias d'un enseignant et d'un étudiant sont bien isolés."""
    teacher = create_random_teacher(db)
    student = create_random_student(db)
    
    file_teacher = create_fake_media()
    file_student = create_fake_media()
    
    media_teacher = add_media(db=db, file_type="photo", teacher_id=teacher.id, file=file_teacher, background_tasks=bgtasks)
    media_student = add_media(db=db, file_type="photo", student_id=student.id, file=file_student, background_tasks=bgtasks)
    
    # Récupérer les médias de chaque entité
    teacher_medias = read_media(db=db, teacher_id=teacher.id)
    student_medias = read_media(db=db, student_id=student.id)
    
    # Vérifier l'isolation
    teacher_media_ids = [m.id for m in teacher_medias["data"]]
    student_media_ids = [m.id for m in student_medias["data"]]
    
    assert media_teacher.id in teacher_media_ids
    assert media_teacher.id not in student_media_ids
    assert media_student.id in student_media_ids
    assert media_student.id not in teacher_media_ids

def test_multiple_file_types(db: Session, bgtasks: BackgroundTasks) -> None:
    """Test l'ajout de différents types de fichiers."""
    teacher = create_random_teacher(db)
    student = create_random_student(db)
    
    file_types = ["photo", "document", "qr"]
    
    for file_type in file_types:
        # Test pour enseignant
        file_teacher = create_fake_media()
        media_teacher = add_media(db=db, file_type=file_type, teacher_id=teacher.id, file=file_teacher, background_tasks=bgtasks)
        assert media_teacher.file_type == file_type
        
        # Test pour étudiant
        file_student = create_fake_media()
        media_student = add_media(db=db, file_type=file_type, student_id=student.id, file=file_student, background_tasks=bgtasks)
        assert media_student.file_type == file_type

def test_add_principal_photo_student(db: Session, bgtasks: BackgroundTasks) -> None:
    """
    Test l'ajout d'une photo principale(sera utilisé pour les cartes et autre)
    """
    file_student = create_fake_media()
    student = create_random_student(db)
    student_db = db.query(Student).where(Student.id == student.id).first()
    principal_media = add_media(db=db,student_id=student.id, file=file_student, file_type="photo", background_tasks=bgtasks, is_principal=True) 
    
    check_principal_photo(db=db, entity=student_db, principal_media=principal_media, is_teacher=False) 
    
def test_add_principal_photo_teacher(db: Session, bgtasks: BackgroundTasks) -> None:
    """
    Test l'ajout d'une photo principale(sera utilisé pour les cartes et autre)
    """
    file_teacher = create_fake_media()
    teacher = create_random_teacher(db)
    teacher_db = db.query(Teacher).where(Teacher.id == teacher.id).first()
    principal_media = add_media(db=db,teacher_id=teacher.id, file=file_teacher,file_type="photo", background_tasks=bgtasks, is_principal=True) 
    
    check_principal_photo(db=db, entity=teacher_db, principal_media=principal_media, is_teacher=True)
    
def test_add_principal_photo_teacher_student(db: Session, bgtasks: BackgroundTasks) -> Any:
    file = create_fake_media()
    teacher = create_random_teacher(db)
    student = create_random_student(db)
    r = add_media(db=db, student_id=student.id, teacher_id=teacher.id, file=file, background_tasks=bgtasks, file_type="photo", is_principal=True)
    assert r is None

def test_add_principal_photo_no_teacher_student(db: Session, bgtasks: BackgroundTasks) -> Any:
    file = create_fake_media()
    r = add_media(db=db, file=file, background_tasks=bgtasks, file_type="photo", is_principal=True)
    assert r is None

def test_update_princ_photo_student(db: Session, bgtasks: BackgroundTasks) -> Any:
    # ajouter une photo
    file = create_fake_media("photo1.png")
    student = create_random_student(db)
    principal_photo = add_media(db=db,student_id=student.id, file=file, file_type="photo", background_tasks=bgtasks, is_principal=True)
    
    assert principal_photo.is_principal
    
    # essayer de la mettre à jour
    update_file = create_fake_media("photo2.png")
    updated_photo = update_principal_photo(db=db, student_id=student.id, new_file=update_file, background_tasks=bgtasks)
    
    # vérifier que l'ancienne photo n'est plus la principale
    assert principal_photo.is_principal is False
    
    # s'assurer que les deux fichiers ont des chemins différents
    assert principal_photo.file_path != updated_photo.file_path
    
    # vérifier que la photo à bien été mise à jour
    query = select(Student).where(Student.id_etudiant==student.id_etudiant)
    student_db = db.execute(query).scalar_one_or_none()
    print(student_db)
    check_principal_photo(db=db, entity=student_db, principal_media=updated_photo, is_teacher=False) 

def test_update_principal_photo_teacher(db: Session, bgtasks: BackgroundTasks) -> Any:
     # ajouter une photo
    file = create_fake_media("photo1.png")
    teacher = create_random_teacher(db)
    principal_photo = add_media(db=db,teacher_id=teacher.id, file=file, file_type="photo", background_tasks=bgtasks, is_principal=True)
    
    assert principal_photo.is_principal
    
    # essayer de la mettre à jour
    update_file = create_fake_media("photo2.png")
    updated_photo = update_principal_photo(db=db, teacher_id=teacher.id, new_file=update_file, background_tasks=bgtasks)
    
    # vérifier que l'ancienne photo n'est plus la principale
    assert principal_photo.is_principal is False
    
    # s'assurer que les deux fichiers ont des chemins différents
    assert principal_photo.file_path != updated_photo.file_path
    
    # vérifier que la photo à bien été mise à jour
    query = select(Teacher).where(Teacher.id==teacher.id)
    teacher_db = db.execute(query).scalar_one_or_none()
    check_principal_photo(db=db, entity=teacher_db, principal_media=updated_photo, is_teacher=True) 

def test_update_principal_photo_no_new_file(db: Session, bgtasks: BackgroundTasks) -> Any:
    teacher = create_random_teacher(db)
    file = create_fake_media("photo1.png")

    principal_photo = add_media(db=db,teacher_id=teacher.id, file=file, file_type="photo",background_tasks=bgtasks, is_principal=True)

    update_princ_photo = update_principal_photo(db=db, teacher_id=teacher.id, background_tasks=bgtasks)
    
    assert update_princ_photo is None
    assert principal_photo.is_principal is False
    
def test_delete_media_student(db: Session, bgtasks: BackgroundTasks) -> Any:
    teacher = create_random_teacher(db)
    student = create_random_student(db)

    file_teacher = create_fake_media("photo1.png")
    file_student = create_fake_media("photo2.png")

    media_teacher = add_media(db=db, file_type="photo", teacher_id=teacher.id, file=file_teacher, background_tasks=bgtasks)
    media_student = add_media(db=db, file_type="photo", student_id=student.id, file=file_student, background_tasks=bgtasks)

    delete_media_t = delete_media(db=db, file_path=media_teacher.file_path, teacher_id=teacher.id)
    delete_media_s = delete_media(db=db, file_path=media_student.file_path, student_id=student.id)
    
    assert delete_media_t
    assert delete_media_s

    student_media_query = select(Media).where(Media.id==media_student.id)
    student_media = db.execute(student_media_query).scalar_one_or_none()
    assert student_media is None
    
    teacher_media_query = select(Media).where(Media.id==media_teacher.id)
    teacher_media = db.execute(teacher_media_query).scalar_one_or_none()
    assert teacher_media is None
    
def test_delete_media_wrong_file_path(db: Session, bgtasks: BackgroundTasks) -> Any:
    teacher = create_random_teacher(db)
    student = create_random_student(db)
    
    delete_media_t = delete_media(db=db, file_path="fake/path.photo", teacher_id=teacher.id)
    delete_media_s = delete_media(db=db, file_path="fake/path.photo", student_id=student.id)
    
    assert delete_media_s is None
    assert delete_media_t is None
    
def test_get_media(db: Session, bgtasks: BackgroundTasks) -> Any:
    teacher = create_random_teacher(db)
    student = create_random_student(db)

    file_teacher = create_fake_media("photo1.png")
    file_student = create_fake_media("photo2.png")

    media_teacher = add_media(db=db, file_type="photo", teacher_id=teacher.id, file=file_teacher, background_tasks=bgtasks)
    media_student = add_media(db=db, file_type="photo", student_id=student.id, file=file_student, background_tasks=bgtasks)
    
    print(media_teacher.file_path)
    
    media_t = get_media(db=db, file_path=media_teacher.file_path, teacher_id=teacher.id)
    media_s = get_media(db=db, file_path=media_student.file_path, student_id=student.id)

    assert media_t
    assert isinstance(media_t, Media)
    assert media_s
    assert isinstance(media_s, Media)

def test_get_media_wrong_file_path(db: Session, bgtasks: BackgroundTasks) -> Any:
    teacher = create_random_teacher(db)
    student = create_random_student(db)

    media_t = get_media(db=db, file_path="fake/photo.png", teacher_id=teacher.id)
    media_s = get_media(db=db, file_path="fake/photo.png", student_id=student.id)
    
    assert media_t is None
    assert media_s is None
    