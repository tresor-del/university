from sqlalchemy import func, select

from fastapi import Depends
from fastapi.routing import APIRoute

from app.models.users import User
from app.deps import (
    SessionDeps,
    get_current_active_admin
)
from app.schemas.users import (
    UserBase,
    UserPublic
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