from typing import Annotated

import jwt
from jwt.exceptions import InvalidTokenError

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session
from sqlalchemy import select

from pydantic import ValidationError

from app.core.config import sessionLocal, engine
from app.core.config import Base
from app.core.settings import settings
from app.core import security
from app.models.users import User
from app.models.students import Student
from app.schemas.users import UserPublic
from app.models.token import Token


reusable_oauth2 = OAuth2PasswordBearer (
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)
TokenDeps = Annotated [str, Depends(reusable_oauth2)]

Base.metadata.create_all(bind=engine)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()     

SessionDeps = Annotated [Session, Depends(get_db)]


def get_current_user(db: SessionDeps, token: TokenDeps) -> UserPublic:
    """
    Fonction de dépendance. Retourne l'utilisateur actuel
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = payload.get("sub")
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        ) 
        
    # corrigé: recevoir le user par le username pas l'id
    user = db.execute(
        select(User).where(User.username == token_data)
    ).scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="User is not active")
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]

def get_current_active_admin(current_user: CurrentUser):
    """
    Retourne le superuser
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="User have not enougth privileges"
        )
    return current_user
