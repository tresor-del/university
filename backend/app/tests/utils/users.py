from fastapi.exceptions import HTTPException
from fastapi.testclient import TestClient

from sqlalchemy.orm import Session

from app.core.settings import settings
from app.crud import users
from app.schemas.users import UserCreate, UserUpdate
from app.tests.utils.utils import random_lower_string

def user_authentication_headers(
    *, 
    client: TestClient, 
    username: str, 
    password: str,
    db: Session
) -> dict [str: str]:
    data = {"username": username, "password": password}
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers

def create_random_user(db: Session) -> UserCreate:
    username = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(username=username, password=password)
    user = users.create_user(db=db, user_data=user_in)
    return user

def authenticate_user_from_username(
    *,
    client: TestClient,
    username: str,
    db: Session
) -> dict[str, str]:
    """
    Retourne le token de l'utilisateur avec le username donné
    
    Si l'utilisateur n'existe pas, il le crée d'abord
    """
    password = random_lower_string()
    # print(password)
    user = users.get_user_by_username(db=db, username=username)
    if not user:
        print("user not found")
        user_in_create = UserCreate(username=username, password=password)
        user = users.create_user(db=db, user_data=user_in_create)
    else:
        print("user found")
        user_in_update = UserUpdate(password=password)
        if not user.id:
            raise Exception("User not set")
        user = users.update_user(db=db, data=user_in_update, id=user.id)
    return user_authentication_headers(db=db,client=client, username=username, password=password)
