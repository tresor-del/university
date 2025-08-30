from typing import Annotated

from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.core.config import sessionLocal, engine
from app.core.config import Base

API_V1_STR = "api/v1"

reusable_oauth2 = OAuth2PasswordBearer (
    tokenUrl=f"{API_V1_STR}/login/access-token"
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