from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.users import User
from app.schemas.users import UserBase, UserInDB, UserRead, UpdateUser
from app.core.security import verify_password

def create_user(*, db: Session, user_data: UserInDB) -> UserRead | None:
    db_user = User(**user_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(*, db: Session, id: int, data: UpdateUser) -> UserRead | None:
    user = db.query(User).filter(User.id==id).first()
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data:
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_username(*, db: Session, username: str) -> UserRead | None:
    statement = select(User).where(User.username==username)
    user = db.execute(statement=statement).first()
    return user

def authenticate_user(*, db: Session, username: str, password: str) -> UserRead | None:
    db_user = db.query(User).filter(User.username==username).first()
    if not db_user:
        return None
    if not verify_password(password, hashed_password=db_user.password):
        return None
    return db_user