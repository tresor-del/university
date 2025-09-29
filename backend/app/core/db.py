from app.core.settings import settings

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.engine import create_engine

from app.models.users import User
from app.schemas.users import UserCreate
from app.crud import users
from app.core.security import get_password_hash

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))

def init_db(db: Session) -> None:
    user = db.execute(
        select(User).where(User.username==settings.FIRST_SUPERUSER)
    ).first()
    if not user:
        # Bcrypt a une limite de 72 octets pour les mots de passe.
        # On tronque pour s'assurer que la limite n'est jamais dépassée.
        # passlib gère automatiquement la troncature pour bcrypt,
        # il n'est donc pas nécessaire de le faire manuellement ici.
        user_in = UserCreate(
            username=settings.FIRST_SUPERUSER,
            # Le mot de passe sera haché avant d'être passé à create_user
            password=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
            is_superuser=True
        )
        user = users.create_user(db=db, user_data=user_in)