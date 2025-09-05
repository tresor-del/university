from fastapi.testclient import TestClient

from sqlalchemy.orm import Session

from app.tests.utils.utils import random_lower_string
from app.tests.utils.users import create_random_user
from app.schemas.users import UserCreate, UserUpdate, UserPublic
from app.crud import users
from app.models.users import User


def test_create_user(db: Session):
    user = create_random_user(db)
    assert user.username == user.username

def test_if_user_is_active(db: Session):
    user = create_random_user(db)
    assert user.is_active is True

def test_if_user_is_superuser(db: Session):
    username = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(username=username, password=password, is_superuser=True)
    user = users.create_user(db=db, user_data=user_in)
    assert user.is_superuser is True
    
def test_update_user(db: Session):
    user = create_random_user(db)
    full_name = random_lower_string()
    update_user = UserUpdate(full_name=full_name, is_active=False, is_superuser=True)
    response = users.update_user(db=db, id=user.id, data=update_user)
    assert isinstance(response, UserPublic)
    assert response.full_name == full_name
    assert response.is_active == False
    assert response.is_superuser == True


def test_get_user_by_username(db: Session):
    user = create_random_user(db)
    response = users.get_user_by_username(db=db, username=user.username)
    assert isinstance(response, UserPublic)
    assert response.full_name == user.full_name
    
def test_authenticate_user(db: Session):
    username = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(username=username, password=password)
    db_user = users.create_user(db=db, user_data=user_in)
    response = users.authenticate_user(db=db, username=username, password=password)
    assert isinstance(response, UserPublic)
    assert response.username == db_user.username
    
def test_not_authenticate_user(db: Session):
    username = random_lower_string()
    password = random_lower_string()
    response = users.authenticate_user(db=db, username=username, password=password)
    assert response is None

    