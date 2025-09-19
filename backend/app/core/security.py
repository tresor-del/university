import jwt , os

from typing import Any
from datetime import datetime, timezone, timedelta
from passlib.context import CryptContext
from cryptography.fernet import Fernet

from app.core.settings import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"

SECRET_KEY = Fernet.generate_key()
fernet = Fernet(SECRET_KEY)
UPLOAD_DIR = settings.MEDIA_UPLOAD_DIRE

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else: 
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def save_encrypted_file(file, filename):
    file_location = os.path.join(UPLOAD_DIR, filename)
    os.makedirs(os.path.dirname(file_location), exist_ok=True)
    # lecture du contenu
    content = file.file.read()
    # chiffrement
    encrypted_content = fernet.encrypt(content)
    # stockage sur le disque
    with open(file_location, "wb") as f:
        f.write(encrypted_content)
    return file_location


def read_encrypted_file(path):
    with open(path, "rb") as f:
        encrypted_content = f.read()
    return fernet.decrypt(encrypted_content)

