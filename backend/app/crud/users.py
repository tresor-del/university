
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.users import User
from app.schemas.users import UserUpdate, UserCreate, UserPublic, UserPublic
from app.core.security import verify_password, get_password_hash


def create_user(*, db: Session, user_data: UserCreate) -> UserPublic:
    hashed_password = get_password_hash(user_data.password)
    
    db_user = User(
        username=user_data.username,
        full_name=user_data.full_name,
        hashed_password=hashed_password,
        is_active=user_data.is_active,
        is_superuser=user_data.is_superuser,
        student_id=user_data.student_id if hasattr(user_data, "student_id") else None
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return UserPublic.model_validate(db_user)

def update_user(*, db: Session, id: UUID, data: UserUpdate) -> UserPublic | None:
    user = db.query(User).filter(User.id==id).first()
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return UserPublic.model_validate(user)

def get_user_by_username(*, db: Session, username: str) -> UserPublic | None:
    statement = select(User).where(User.username==username)
    user = db.execute(statement=statement).scalar_one_or_none()
    if user is None:
        return None
    return UserPublic.model_validate(user)

def authenticate_user(*, db: Session, username: str, password: str) -> UserPublic | None:
    db_user = db.query(User).filter(User.username==username).first()
    if not db_user:
        return None
    if not verify_password(password, hashed_password=db_user.hashed_password):
        return None
    return UserPublic.model_validate(db_user)