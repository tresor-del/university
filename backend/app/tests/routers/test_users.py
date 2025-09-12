from sqlalchemy import select

from app.crud import users
from app.models.users import User
from app.schemas.users import UserCreate, UserUpdate, UpdatePassword
from app.tests.utils.users import create_random_user, random_lower_string
from app.core.settings import settings
from app.core.security import verify_password

def test_retrieve_users(client, db, superuser_token_headers):
    """
    Test la reception de la liste de tous les utilisateurs
    """
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
    """
    Vérifie que l'admin courant peut créer un utilisateur
    """
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
    """
    S'assure qu'un utilisateur courant ne peux pas créer un utilisateur
    """
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
    """
    Test la reception des données de l'admin courant
    """
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=superuser_token_headers)
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"] is True
    assert current_user["username"] == settings.FIRST_SUPERUSER

def test_get_users_normal_user_me(client, db, normal_user_token_headers):
    """
    Test la reception des données de l'utilisateur courant
    """
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    current_user = r.json()
    print(current_user)
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"] is False
    assert current_user["username"] == settings.USERNAME_TEST_USER

def test_get_existing_user(client, db, superuser_token_headers):
    """
    Vérifie que l'utilisateur créé existe
    """
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

def test_get_existing_user_current_user(client, db):
    """
    Verifie que l'utilisateur connecté existe
    """
    username = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(password=password, username=username)
    user = users.create_user(db=db, user_data=user_in)
    print(user)
    
    data = user_in.model_dump()
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=data)
    token_data = r.json()
    access_token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    
    res = client.get(f"{settings.API_V1_STR}/users/{user.id}", headers=headers)
    assert 200 <= r.status_code < 300
    api_user = res.json()
    print("api_user: ", api_user)
    existing_user = users.get_user_by_username(db=db, username=username) 
    assert existing_user
    assert existing_user.username == api_user["username"]
    
def test_get_existing_user_permissions_error(client, db, normal_user_token_headers):
    username = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(password=password, username=username)
    user = users.create_user(db=db, user_data=user_in)
    id = user.id
    r = client.get(f"{settings.API_V1_STR}/users/{id}", headers=normal_user_token_headers)
    assert r.status_code == 403 
    print(r.json())

def test_update_user(client, superuser_token_headers, db):
    username = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(username=username, password=password)    
    user = users.create_user(db=db, user_data=user_in)
    
    print(user)
    data = {"full_name": "updated_full_name"}
    r = client.patch(
        f"{settings.API_V1_STR}/users/{user.id}",
        json=data,
        headers=superuser_token_headers
    )

    assert r.status_code == 200
    updated_user = r.json()
    assert updated_user["full_name"] == "updated_full_name"
    
    user_query = select(User).where(User.username==username)
    user_db = db.execute(user_query).scalar_one()
    db.refresh(user_db)
    assert user_db
    assert user_db.full_name ==  "updated_full_name"

def test_update_user_not_exists(client, superuser_token_headers):
    data = {
        "full_name": "updated_full_name"
    }
    id = "24"
    r = client.patch(
        f"{settings.API_V1_STR}/users/{id}",
        headers=superuser_token_headers,
        json=data
    )
    assert r.status_code == 404
    assert r.json()["detail"] == "Cet utilisateur n'est pas enrégistré sur le systeme"
    
def test_update_user_username_exists(client, superuser_token_headers, db):
    username = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(username=username, password=password)
    user = users.create_user(db=db, user_data=user_in)

    username2 = random_lower_string()
    password2 = random_lower_string()
    user_in2 = UserCreate(username=username2, password=password2)
    user2 = users.create_user(db=db, user_data=user_in2)
    
    data = {"username": user.username}
    r = client.patch(
        f"{settings.API_V1_STR}/users/{user2.id}",
        headers=superuser_token_headers,
        json=data
    )
    assert r.status_code == 409
    assert r.json()["detail"] == "Un utilisateur avec ce nom existe déjà"

def test_update_user_me(client, db, normal_user_token_headers):
    """
    Test la mise à jour de l'utilisateur courant
    """
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
    """
    Test la mise à jour du mot de passe de l'utilisateur courant
    
    Et verifie que l'utilisateur a le mm mot de passe dans la bd
    """
    new_password = random_lower_string()
    body_in = UpdatePassword(
        current_password=settings.FIRST_SUPERUSER_PASSWORD, 
        new_password=new_password
    )
    body = body_in.model_dump()
    r = client.patch(
        f"{settings.API_V1_STR}/users/me/password",
        headers=superuser_token_headers,
        json=body
    )
    assert r.status_code == 200
    updated_user = r.json()
    print("u: ", updated_user)
    assert updated_user["message"] == "Mot de passe mis à jour avec succès"
    
    user_query = select(User).where(User.username==settings.FIRST_SUPERUSER)
    
    user_db = db.execute(user_query).scalar_one()
    assert user_db
    assert user_db.username == settings.FIRST_SUPERUSER
    assert verify_password(new_password, user_db.hashed_password)

    # Remettre le mot de passe pour garder la cohérence du code
    old_data = UpdatePassword(
        current_password=new_password, 
        new_password=settings.FIRST_SUPERUSER_PASSWORD
    )
    old_data = old_data.model_dump()
    # print(old_data)
    r = client.patch(
        f"{settings.API_V1_STR}/users/me/password",
        headers=superuser_token_headers,
        json=old_data
    )
    print("1: ", r.json())
    assert r.status_code == 200
    assert verify_password(settings.FIRST_SUPERUSER_PASSWORD, user_db.hashed_password)
    
def test_update_password_me_incorrect_password(client, superuser_token_headers, db):
    new_password = random_lower_string()
    data = UpdatePassword(current_password=new_password, new_password=new_password)
    data = data.model_dump()
    r = client.patch(
        f"{settings.API_V1_STR}/users/me/password",
        headers=superuser_token_headers,
        json=data
    )
    assert r.status_code ==  400
    updated_user = r.json()
    assert updated_user["detail"] == "Mot de passe Incorrect"
    
def test_update_user_me_username_exits(client, normal_user_token_headers, db):
    """
    Test pour verifier que les usernames sont unique
    """
    username = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(username=username, password=password)
    user = users.create_user(db=db, user_data=user_in)
    
    data = {"username": username}
    r = client.patch(
        f'{settings.API_V1_STR}/users/me',
        headers=normal_user_token_headers,
        json=data
    )
    assert r.status_code == 409 
    assert r.json()["detail"] == "Un utilisateur avec ce nom existe déjà"
    
def test_update_password_me_same_password_error(client, db, superuser_token_headers):
    data = {
        "current_password": settings.FIRST_SUPERUSER_PASSWORD,
        "new_password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.patch(
        f"{settings.API_V1_STR}/users/me/password",
        headers=superuser_token_headers,
        json=data,
    )
    assert r.status_code == 400
    updated_user = r.json()
    assert (
        updated_user["detail"] == "Le nouveau mot de passe doit être différent de l'ancien"
    )
    
def test_register_user(client, db):
    username = random_lower_string()
    password = random_lower_string()
    full_name = random_lower_string()
    data = {"username": username, "password": password, "full_name": full_name}
    r = client.post(
        f"{settings.API_V1_STR}/users/signup",
        json=data
    )
    assert r.status_code == 200
    created_user = r.json()
    assert created_user["username"] == username
    assert created_user["full_name"] == full_name
    
    user_query = select(User).where(User.username==username)
    user_db = db.execute(user_query).scalar_one()
    assert user_db
    assert user_db.username == username
    assert user_db.full_name == full_name
    assert verify_password(password, user_db.hashed_password)
    
def test_register_user_already_exist_error(client):
    password = random_lower_string()
    full_name = random_lower_string()
    data = {
        "username": settings.FIRST_SUPERUSER,
        "password": password,
        "full_name": full_name
    }
    r = client.post(
        f"{settings.API_V1_STR}/users/signup",
        json=data
    )
    assert r.status_code == 400
    assert r.json()["detail"] == "Un utilisateur avec ce username existe déjà"
    
def test_delete_user_me(client, db):
    username = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(username=username, password=password)
    user = users.create_user(db=db, user_data=user_in)
    
    login_data = {
        "username": username,
        "password": password
    }
    r = client.post(
        f"{settings.API_V1_STR}/login/access-token",
        data=login_data
    )
    token_data = r.json()
    access_token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    print(headers)
    r = client.delete(
        f"{settings.API_V1_STR}/users/me",
        headers=headers
    )
    assert r.status_code == 200
    assert r.json()["message"] == "Utilisateur supprimé avec succes"
    
    user_query = select(User).where(User.id == user.id)
    user_db = db.execute(user_query).first()
    assert user_db is None
    
def test_delete_user_as_me_superuser(client, db, superuser_token_headers):
    r = client.delete(
        f"{settings.API_V1_STR}/users/me",
        headers=superuser_token_headers
    )
    assert r.status_code == 400
    assert r.json()["detail"] == "Les admins n'ont pas l'autorisation de se supprimer"

def delete_user_super_user(client, db, superuser_token_headers):
    username = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(username=username, password=password)
    user = users.create_user(db=db, user_data=user_in)

    r = client.delete(
        f"{settings.API_V1_STR}/users/{user.id}",
        headers=superuser_token_headers
    )
    assert r.status_code == 200
    assert r.json()["message"] == "Utilisateur supprimer avec succès"
    userdb = db.execute(select(User).where(User.id==user.id)).first()
    assert userdb is None

def test_delete_user_not_found(client, db, superuser_token_headers):
    r = client.delete(
        f"{settings.API_V1_STR}/users/456",
        headers=superuser_token_headers
    )
    assert r.status_code == 404
    assert r.json()["detail"] == "Utilisateur non trouvé"
    
def test_delete_user_without_privileges(client, db, normal_user_token_headers):
    username = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(username=username, password=password)
    user = users.create_user(db=db, user_data=user_in)

    r = client.delete(
        f"{settings.API_V1_STR}/users/{user.id}",
        headers=normal_user_token_headers
    )
    assert r.status_code == 403
    assert r.json()["detail"] == "User have not enougth privileges"
    