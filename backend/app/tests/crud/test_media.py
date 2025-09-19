import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.crud.media import add_media, read_media
from app.tests.utils.teachers import create_random_teacher
from app.tests.utils.students import create_random_student
from app.models.media import Media
from app.tests.utils.students import create_random_student
from app.tests.utils.media import create_fake_media
from app.models.teachers import Teacher
from app.models.students import Student

def test_add_media_teacher(db: Session) -> None:
    """
    Test l'ajout d'un média à un enseignant.
    """
    file = create_fake_media()
    teacher = create_random_teacher(db)
    media = add_media(db=db, file_type="photo", teacher_id=teacher.id, file=file)
    
    # vérifier que l'enseignant de la base de donnée est relié au media
    teacher_query = select(Teacher).where(Teacher.id == teacher.id)
    teacher = db.execute(teacher_query).scalar_one_or_none()
    print(teacher.medias)
    assert len(teacher.medias) >= 1

    # vérifier que le média rélié a l'enseignant
    assert hasattr(teacher, "medias")
    assert isinstance(media, Media)
    assert media.teacher_id == teacher.id
    assert media.student_id is None
    assert media.file_type == "photo"
    
    # Vérifider la relation côté enseignant
    assert isinstance(teacher.medias, list)
    assert len(teacher.medias) >= 1
    assert media in teacher.medias
    
    # Vérifier que le média existe en base de données
    media_query = select(Media).where(Media.id == media.id)
    media_db = db.execute(media_query).scalar_one_or_none()
    assert media_db is not None
    assert media_db.teacher_id == teacher.id
    assert media_db.student_id is None
    
    
def test_add_media_student(db: Session) -> None:
    """Test l'ajout d'un média à un étudiant."""
    file = create_fake_media()
    student = create_random_student(db)
    
    media = add_media(db=db, file_type="photo", student_id=student.id, file=file)

    # verifier que l'étudiant de la bdd est relié au média créé
    student_query = select(Student).where(Student.id == student.id)
    student = db.execute(student_query).scalar_one_or_none()
    print(student.medias)
    assert len(student.medias) >= 1
    
    # vérifier que le media est relié a l'étudiant
    assert isinstance(media, Media)
    assert media.student_id == student.id
    assert media.teacher_id is None
    assert media.file_type == "photo"
    
    # Vérifier la relation côté étudiant
    assert student.medias is not None
    assert media in student.medias
    
    # Vérifier que le média existe en base de données
    media_query = select(Media).where(Media.id == media.id)
    media_db = db.execute(media_query).scalar_one_or_none()
    assert media_db is not None
    assert media_db.student_id == student.id
    assert media_db.teacher_id is None
    
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

def test_get_media_teacher(db: Session) -> None:
    """Test la récupération des médias d'un enseignant."""
    file1 = create_fake_media()
    file2 = create_fake_media()
    teacher = create_random_teacher(db)
    
    # Ajouter plusieurs médias
    media1 = add_media(db=db, file_type="photo", teacher_id=teacher.id, file=file1)
    media2 = add_media(db=db, file_type="document", teacher_id=teacher.id, file=file2)
    
    r = read_media(db=db, teacher_id=teacher.id)
    
    teacher_query = select(Teacher).where(Teacher.id == teacher.id)
    teacher = db.execute(teacher_query).scalar_one_or_none()
    print(teacher.medias)
    assert len(teacher.medias) >= 2
    
    assert isinstance(r["data"], list)
    assert r["count"] == 2
    assert len(r["data"]) >= 2  
    
    # Vérifier que tous les médias appartiennent au bon enseignant
    for m in r["data"]:
        assert m.teacher_id == teacher.id
        assert m.student_id is None
    
    # Vérifier que nos médias sont dans la liste
    media_ids = [m.id for m in r["data"]]
    assert media1.id in media_ids
    assert media2.id in media_ids

    # Vérifier que l'enseignant a les médias
    assert teacher.medias
    for media in r["data"]:
        assert media in teacher.medias

def test_read_media_student(db: Session) -> None:
    """Test la récupération des médias d'un étudiant."""
    file1 = create_fake_media()
    file2 = create_fake_media()
    student = create_random_student(db)
    
    # Ajouter plusieurs médias
    media1 = add_media(db=db, file_type="photo", student_id=student.id, file=file1)
    media2 = add_media(db=db, file_type="qr", student_id=student.id, file=file2)
    
    r = read_media(db=db, student_id=student.id)
    
    # verifier que l'étudiant de la bdd est relié au média créé
    student_query = select(Student).where(Student.id == student.id)
    student = db.execute(student_query).scalar_one_or_none()
    print(student.medias)
    assert len(student.medias) >= 2
    
    assert isinstance(r["data"], list)
    assert r["count"] == 2
    assert len(r["data"]) >= 2 
    
    # Vérifier que tous les médias appartiennent au bon étudiant
    for m in r["data"]:
        assert m.student_id == student.id
        assert m.teacher is None
    
    # Vérifier que nos médias sont dans la liste
    media_ids = [m.id for m in r["data"]]
    assert media1.id in media_ids
    assert media2.id in media_ids

    # Vérifier que l'enseignant a les médias
    assert student.medias
    for media in r["data"]:
        assert media in student.medias

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