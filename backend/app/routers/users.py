from typing import Any

from sqlalchemy import func, select

from fastapi import Depends
from fastapi.routing import APIRoute
from fastapi.exceptions import HTTPException

from app.models.users import User
from app.core.security import verify_password, get_password_hash
from app.crud import users
from app.deps import (
    SessionDeps,
    CurrentUser,
    get_current_active_admin
)
from app.schemas.users import (
    UserPublic,
    UserCreate,
    UpdateUser,
    Message,
    UpdatePassword
)


router = APIRoute(prefix="/users", tags=["users"])


@router.get(
    "/",
    dependancies=[Depends(get_current_active_admin)],
    response_model=UserPublic
)
def read_users(db: SessionDeps, skip: int = 0, limit: int = 100):
    """
    Récupérer tous les utilisateurs
    """
    count_statement = select(func.count()).select_from(User)
    count = db.execute(count_statement).one()

    statement = select(User).offset(skip).limit(limit)
    users = db.execute(statement).all()
    
    return UserPublic(data=users, count=count)

@router.post(
    "/",
    dependencies=[Depends(get_current_active_admin)],
    response_model=UserPublic
)
def create_user(*, db: SessionDeps, user_in: UserCreate) -> Any:
    """
    Créer un utilisateur 
    """
    user = users.get_user_by_username(db=db, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=400, 
            detail="Un utilisateur avec ce username existe déjà"
        )
    user = users.create_user(db=db, user_data=user_in)
    return user


@router.patch("/me", response_model=UserPublic)
def update_user_me(
    *,
    db:SessionDeps,
    user_in: UpdateUser,
    current_user:CurrentUser,
) -> Any:
    """
    Mise à jour de son propre compte
    """
    if user_in.username:
        existing_user =  users.get_user_by_username(db=db, username=user_in.username)
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException (
                status_code=400,
                detail="Un utilisateur avec ce nom existe déjà"
            )
    user_data = user_in.model_dump(exclude_unset=True)
    for key, value in user_data:
        setattr(current_user, key, value)
    db.commit()
    db.refresh(current_user)
    return current_user

@router.patch("/me/password", response_model=Message)
def update_password_me(
    *,
    db: SessionDeps,
    body: UpdatePassword,
    current_user: CurrentUser
) -> Any:
    """
    Mise à jour de son propre mot de passe
    """
    if not verify_password(body.current_password, current_user.password):
        raise HTTPException(status_code=400, detail="Mot de passe Incorrect")
    if body.current_password == body.new_password:
        raise HTTPException(status_code=400, detail="Le nouveau mot de passe doit être différent de l'ancien")
    hashed_password = get_password_hash((body.new_password))
    current_user.hashed_password = hashed_password
    db.add(current_user)
    db.commit()
    return Message(message="Mot de passe mis à jour avec succes")


@router.get("/me", response_model=UserPublic)
def read_user_me(current_user: CurrentUser) -> Any:
    """
    Recevoir l'utilisateur actuel
    """
    return current_user

@router.delete("/me", response_model=Message)
def delete_user_me(db: SessionDeps, current_user: CurrentUser) -> Any:
    """
    Supprimer son propre compte
    """
    if current_user.is_superuser:
        raise HTTPException(
            status_code=400,
            detail="Les admins n'ont pas l'autorisation de se supprimer"
        )
    db.delete(current_user)
    db.commit()
    return Message(message="Utilisateur supprimé avec succes")

@router.post("/signup", response_model=UserPublic)
def register_user(db: SessionDeps, user_in: UserCreate) -> Any:
    """
    S'enrégistrer
    """
    user = users.get_user_by_username(db=db, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=400, 
            detail="Un utilisateur avec ce username existe déjà"
        )
    user_create = UserCreate.model_validate(user_in)
    user = users.create_user(db=db, create_user=user_create)
    return user

@router.get("/{user_id}", response_model=UserPublic)
def read_user_by_id(
    user_id: int,
    db: SessionDeps,
    current_user: CurrentUser
) -> Any:
    """
    Recevoire un utilisateur by id
    """
    user = db.get(User, user_id)
    if user == current_user:
        return user
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="The user doesn't have enough privilege"
        )
    return user

@router.patch(
    "/{user_id}",
    dependencies=[Depends(get_current_active_admin)],
    response_model=UserPublic,
)
def update_user(
    *,
    db: SessionDeps, 
    user_id: int, 
    user_in: UpdateUser
) -> Any:
    """
    Mettre à jour un utilisateur
    """
    db_user = db.get(User, user_id)
    if not db_user:
        raise HTTPException(
            status_code=404, 
            detail="Cet utilisateur n'existe pas"
        )
    if user_in.username:
        existing_user =  users.get_user_by_username(db=db, username=user_in.username)
        if existing_user and existing_user.id != user_id:
            raise HTTPException (
                status_code=400,
                detail="Un utilisateur avec ce nom existe déjà"
            )
    db_user = users.update_user(db=db, data=user_in)
    return db_user

@router.delete("/{user_id}", dependencies=[Depends(get_current_active_admin)])
def delete_user(
    db: SessionDeps, current_user: CurrentUser, user_id: int
) -> Message:
    """
    Supprimer un utilisateur
    """
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user == current_user:
        raise HTTPException(
            status_code=403, detail="Les admins n'ont pas le droit de se supprimer"
        )
    db.delete(user)
    db.commit()
    return Message(message="Utilisateur supprimer avec succès")