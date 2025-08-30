from typing import Annotated

import jwt
from jwt.exceptions import InvalidTokenError

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from pydantic import ValidationError

from app.core.config import sessionLocal, engine
from app.core.config import Base
from app.core.settings import settings
from app.core import security
from app.models.users import User
from app.schemas.users import UserRead
from app.models.token import Token


reusable_oauth2 = OAuth2PasswordBearer (
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)

Base.metadata.create_all(bind=engine)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()     

SessionDeps = Annotated [Session, Depends(get_db)]
TokenDeps = Annotated [str, Depends(reusable_oauth2)]


def get_current_user(db: SessionDeps, token: TokenDeps) -> UserRead:
    
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = Token(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        ) 
    
    user = db.get(User, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="User is not active")
    return user

Current_user = Annotated[User, Depends(get_current_user)]
