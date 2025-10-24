from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends,HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.token import Token
from app.api.deps import SessionDeps
from app.crud import users
from app.core.settings import settings
from app.core import security

router = APIRouter(tags=["login"])

@router.post("/login/access-token")
def login_for_access_token(
    db: SessionDeps, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    user = users.authenticate_user(
        db=db, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expire = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token_data = {
        "sub": user.username,
    }
    return Token(
        access_token=security.create_access_token(
            data=token_data, expires_delta=access_token_expire
        )
    )