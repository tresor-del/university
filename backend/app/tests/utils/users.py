from fastapi.testclient import TestClient

from sqlalchemy.orm import Session

from app.crud import users
from app.schemas.users import UserCreate
from app.tests.utils.utils import random_lower_string

def user_authentication_headers(
    *, 
    client: TestClient, 
    username: str, 
    password: str
) -> dict [str: str]:
    data = {"username": username, "password": password}
    r = client.post("/login/access-token", data=data)
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