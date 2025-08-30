from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends
from app.core.config import sessionLocal, engine
from app.models.students import Base


Base.metadata.create_all(bind=engine)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()     

SessionDeps = Annotated [Session, Depends(get_db)]