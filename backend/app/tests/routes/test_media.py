from typing import Any
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

from app.core.settings import settings
from app.tests.utils.media import create_fake_media_route
from app.tests.utils.students import create_random_student
from app.tests.utils.teachers import create_random_teacher

def test_add_media(db: Session, client: TestClient, superuser_token_headers: dict[str, str]) -> Any:
    file_student = create_fake_media_route("file_student.py")
    
    student = create_random_student(db)
    
    # data_student = {
    #     "file_type": "photo",
    #     "student_id": str(student.id)
    # }
    
    file_type = "photo"
    
    r_student = client.post(
        f"{settings.API_V1_STR}/media/{file_type}/{student.id}", 
        headers=superuser_token_headers,
        files=file_student
    )
    
    assert r_student.status_code == 200, r_student.text
