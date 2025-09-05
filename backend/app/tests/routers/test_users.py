from fastapi import status

from app.crud import users
from app.schemas.users import UserCreate, UserUpdate, UpdatePassword
from app.tests.utils.users import create_random_user, random_lower_string
from app.core.settings import settings

def test_retrieve_users(client, db, superuser_token_headers):
    user1 = create_random_user(db)
    user2 = create_random_user(db)
    response = client.get(
        f"{settings.API_V1_STR}/users",
        headers=superuser_token_headers                          
    )
    assert response.status_code == 200
    all_users = response.json()
    assert len(all_users["data"]) > 1
    assert "count" in all_users
    for item in all_users["data"]:
        assert "username" in item
    
def test_create_user_by_superuser(client, db, superuser_token_headers):
    username = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(username=username, password=password)
    user = user_in.model_dump()
    response = client.post(
        f"{settings.API_V1_STR}/users/",
        json=user,
        headers=superuser_token_headers
    )
    assert response.status_code == 200

def test_create_user_by_normal_user(client, db, normal_user_token_headers):
    username = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(username=username, password=password)
    user = user_in.model_dump()
    response = client.post(
        f"{settings.API_V1_STR}/users/",
        json=user,
        headers=normal_user_token_headers
    )
    assert response.status_code == 403

def test_get_users_superuser_me(client, superuser_token_headers):
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=superuser_token_headers)
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"] is True
    assert current_user["username"] == settings.FIRST_SUPERUSER

def test_get_users_normal_user_me(client, db, normal_user_token_headers):
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"] is False
    assert current_user["username"] == settings.USERNAME_TEST_USER

def test_get_existing_user(client, db, superuser_token_headers):
    username = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(username=username, password=password)
    
    user = users.create_user(db=db, user_data=user_in)
    id = user.id
    r = client.get(f"{settings.API_V1_STR}/users/{id}", headers=superuser_token_headers)
    
    assert 200 <= r.status_code < 300
    api_user = r.json()
    existing_user = users.get_user_by_username(db=db, username=username) 
    assert existing_user.username == api_user["username"]

def test_update_user_me(client, db, normal_user_token_headers):
    full_name = random_lower_string()
    username = random_lower_string()
    user_in = UserUpdate(full_name=full_name, username=username)
    user = user_in.model_dump()
    response = client.patch(
        f"{settings.API_V1_STR}/users/me",  
        headers=normal_user_token_headers,
        json=user,
    )
    assert response.status_code == 200

def test_update_password_me(client, db, superuser_token_headers):
    new_password = random_lower_string()
    body_in = UpdatePassword(current_password=settings.FIRST_SUPERUSER_PASSWORD, new_password=new_password)
    body = body_in.model_dump()
    r = client.patch(
        f"{settings.API_V1_STR}/users/me/password",
        headers=superuser_token_headers,
        json=body
    )
    assert r.status_code == 200
