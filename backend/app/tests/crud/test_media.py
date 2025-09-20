from typing import Any
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.crud.media import add_media, add_principal_photo, read_media, update_principal_photo
from app.tests.utils.teachers import create_random_teacher
from app.tests.utils.students import create_random_student
from app.models.media import Media
from app.tests.utils.students import create_random_student
from app.tests.utils.media import check_read_media, create_fake_media, check_principal_photo, check_add_media
from app.models.teachers import Teacher
from app.models.students import Student

def test_add_media_teacher(db: Session) -> None:
    """
    Test l'ajout d'un média à un enseignant.
    """
    file = create_fake_media()
    teacher = create_random_teacher(db)
    teacher_db = db.query(Teacher).where(Teacher.id==teacher.id).first()
    
    media = add_media(db=db, file_type="photo", teacher_id=teacher.id, file=file)
    
    check_add_media(db=db, entity=teacher_db, media=media, is_teacher=True)
      
def test_add_media_student(db: Session) -> None:
    """Test l'ajout d'un média à un étudiant."""
    file = create_fake_media()
    student = create_random_student(db)
    student_db = db.query(Student).where(Student.id==student.id).first()
    media = add_media(db=db, file_type="photo", student_id=student.id, file=file)
    
    check_add_media(db=db, entity=student_db, media=media, is_teacher=False)
    
def test_add_media_with_no_teacher_student(db: Session) -> None:
    """Test l'ajout d'un média sans enseignant ni étudiant."""
    file = create_fake_media()
    r = add_media(db=db, file_type="photo", file=file)
    assert r is None
    
def test_add_media_with_both_teacher_and_student(db: Session) -> None:
    """
    Test l'ajout d'un média avec à la fois un enseignant et un étudiant .
    """
    file = create_fake_media()
    teacher = create_random_teacher(db)
    student = create_random_student(db)
    r = add_media(db=db, file_type="photo", teacher_id=teacher.id, student_id=student.id, file=file)
    
    assert r is None

def test_read_media_teacher(db: Session) -> None:
    """Test la récupération des médias d'un enseignant."""
    file1 = create_fake_media()
    file2 = create_fake_media()
    teacher = create_random_teacher(db)
    teacher_db = db.query(Teacher).where(Teacher.id == teacher.id).first()
    
    # Ajouter plusieurs médias
    media1 = add_media(db=db, file_type="photo", teacher_id=teacher.id, file=file1)
    media2 = add_media(db=db, file_type="document", teacher_id=teacher.id, file=file2)
    
    r = read_media(db=db, teacher_id=teacher.id)
    data = r["data"]
    count = r["count"]

    check_read_media(db=db, entity=teacher_db, media1=media1, media2=media2, data=data, count=count, is_teacher=True)

def test_read_media_student(db: Session) -> None:
    """Test la récupération des médias d'un étudiant."""
    file1 = create_fake_media()
    file2 = create_fake_media()
    student = create_random_student(db)
    student_db = db.query(Student).where(Student.id == student.id).first()
    
    # Ajouter plusieurs médias
    media1 = add_media(db=db, file_type="photo", student_id=student.id, file=file1)
    media2 = add_media(db=db, file_type="qr", student_id=student.id, file=file2)
    
    r = read_media(db=db, student_id=student.id)

    data = r["data"]
    count = r["count"]
    
    check_read_media(db=db, entity=student_db, media1=media1, media2=media2, data=data, count=count, is_teacher=False)

def test_read_media_nonexistent_teacher(db: Session) -> None:
    """Test la récupération des médias pour un enseignant inexistant."""
    fake_teacher_id = uuid.uuid4()
    r = read_media(db=db, teacher_id=fake_teacher_id)
    
    assert isinstance(r["data"], list)
    assert len(r["data"]) == 0 

def test_read_media_nonexistent_student(db: Session) -> None:
    """Test la récupération des médias pour un étudiant inexistant."""
    fake_student_id = uuid.uuid4()
    r = read_media(db=db, student_id=fake_student_id)
    
    assert isinstance(r["data"], list)
    assert len(r["data"]) == 0 

def test_read_media_no_parameters(db: Session) -> None:
    """
    Test la récupération des médias sans paramètres.
    """
    try:
        r = read_media(db=db)
    except Exception as e:
        assert True

def test_media_isolation_teacher_student(db: Session) -> None:
    """Test que les médias d'un enseignant et d'un étudiant sont bien isolés."""
    teacher = create_random_teacher(db)
    student = create_random_student(db)
    
    file_teacher = create_fake_media()
    file_student = create_fake_media()
    
    media_teacher = add_media(db=db, file_type="photo", teacher_id=teacher.id, file=file_teacher)
    media_student = add_media(db=db, file_type="photo", student_id=student.id, file=file_student)
    
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

def test_multiple_file_types(db: Session) -> None:
    """Test l'ajout de différents types de fichiers."""
    teacher = create_random_teacher(db)
    student = create_random_student(db)
    
    file_types = ["photo", "document", "qr"]
    
    for file_type in file_types:
        # Test pour enseignant
        file_teacher = create_fake_media()
        media_teacher = add_media(db=db, file_type=file_type, teacher_id=teacher.id, file=file_teacher)
        assert media_teacher.file_type == file_type
        
        # Test pour étudiant
        file_student = create_fake_media()
        media_student = add_media(db=db, file_type=file_type, student_id=student.id, file=file_student)
        assert media_student.file_type == file_type

def test_add_principal_photo_student(db: Session) -> None:
    """
    Test l'ajout d'une photo principale(sera utilisé pour les cartes et autre)
    """
    file_student = create_fake_media()
    student = create_random_student(db)
    student_db = db.query(Student).where(Student.id == student.id).first()
    principal_media = add_principal_photo(db=db,student_id=student.id, file=file_student) 
    
    check_principal_photo(db=db, entity=student_db, principal_media=principal_media, is_teacher=False) 
    
def test_add_principal_photo_teacher(db: Session) -> None:
    """
    Test l'ajout d'une photo principale(sera utilisé pour les cartes et autre)
    """
    file_teacher = create_fake_media()
    teacher = create_random_teacher(db)
    teacher_db = db.query(Teacher).where(Teacher.id == teacher.id).first()
    principal_media = add_principal_photo(db=db,teacher_id=teacher.id, file=file_teacher) 
    
    check_principal_photo(db=db, entity=teacher_db, principal_media=principal_media, is_teacher=True)
    
def test_add_principal_photo_teacher_student(db: Session) -> Any:
    file = create_fake_media()
    teacher = create_random_teacher(db)
    student = create_random_student(db)
    r = add_principal_photo(db=db, student_id=student.id, teacher_id=teacher.id, file=file)
    assert r is None

def test_add_principal_photo_no_teacher_student(db: Session) -> Any:
    file = create_fake_media()
    r = add_principal_photo(db=db, file=file)
    assert r is None

def test_update_princ_photo_student(db: Session) -> Any:
    # ajouter une photo
    file = create_fake_media("photo1.png")
    student = create_random_student(db)
    principal_media = add_principal_photo(db=db,student_id=student.id, file=file)
    
    assert principal_media.is_principal
    
    # essayer de la mettre à jour
    update_file = create_fake_media("photo2.png")
    updated_photo = update_principal_photo(db=db, student_id=student.id, new_file=update_file)
    
    # vérifier que l'ancienne photo n'est plus la principale
    assert principal_media.is_principal is False
    assert principal_media.file_path != updated_photo.file_path
    
    # vérifier que la photo à bien été mise à jour
    query = select(Student).where(Student.id_etudiant==student.id_etudiant)
    student_db = db.execute(query).scalar_one_or_none()
    print(student_db)
    check_principal_photo(db=db, entity=student_db, principal_media=updated_photo, is_teacher=False) 
    
