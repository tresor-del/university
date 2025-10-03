from typing import Any
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

from app.core.settings import settings
from app.models.media import Media
from app.tests.utils.media import create_fake_media_route
from app.tests.utils.students import create_random_student
from app.tests.utils.teachers import create_random_teacher

def test_add_media_student(db: Session, client: TestClient, superuser_token_headers: dict[str, str]) -> Any:
    file_student = create_fake_media_route("file_student.png")
    
    student = create_random_student(db)
    
    file_type = "photo"
    
    r_student = client.post(
        f"{settings.API_V1_STR}/media/{file_type}/?student_id={student.id}", 
        # data= {"student_id": str(student.id)},
        headers=superuser_token_headers,
        files=file_student
    )
    
    assert r_student.status_code == 200, r_student.text

def test_add_media_teacher(db: Session, client: TestClient, superuser_token_headers: dict[str, str]) -> Any:
    file_teacher = create_fake_media_route("file_teacher.png")
    
    teacher = create_random_teacher(db)
    file_type = "photo"
    
    r = client.post(
        f"{settings.API_V1_STR}/media/{file_type}/?teacher_id={teacher.id}", 
        # data= {"teacher_id": str(teacher.id)},
        headers=superuser_token_headers,
        files=file_teacher
    )
    
    assert r.status_code == 200

def test_delet_media(db: Session, client: TestClient, superuser_token_headers: dict[str, str]) -> Any:
    
    file_student = create_fake_media_route("file_student.png")
    student = create_random_student(db)
    file_type = "photo"
    r_student = client.post(
        f"{settings.API_V1_STR}/media/{file_type}/?student_id={student.id}", 
        # data= {"student_id": str(student.id)},
        headers=superuser_token_headers,
        files=file_student
    )
    
    file_path = str(r_student.json()["file_path"])
    
    media_db = db.query(Media).where(Media.file_path == file_path).first()
    assert media_db is not None
    
    response =  client.delete(
        f"{settings.API_V1_STR}/media/delete/?student_id={student.id}&file_path={file_path}",
        headers=superuser_token_headers
    )
    
    assert response.status_code == 200
    
    media_db = db.query(Media).where(Media.file_path == file_path).first()
    assert media_db is None