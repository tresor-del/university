from fastapi.testclient import TestClient

from sqlalchemy.orm import Session

from app.tests.utils.utils import random_lower_string
from app.schemas.users import UserCreate
from app.crud import users


def test_create_user(db: Session):
    username = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(username=username, password=password)
    user = users.create_user(db=db, user_data=user_in)
    assert user.username == username
    assert hasattr(user, "hashed_password")