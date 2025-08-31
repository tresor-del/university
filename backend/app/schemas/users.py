from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class UserBase(BaseModel):
    id: int
    username: str
    full_name: str
    is_active: bool
    is_superuser: bool
    
    model_config = ConfigDict(from_attributes=True)

class UserInDB(UserBase):
    hashed_password: str = Field(min_length=8, max_length=40)

class UserRead(UserBase):
    pass

class UserCreate(UserInDB):
    pass

class UpdateUser(BaseModel):
    username: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[str] = None
    is_superuser: Optional[str] = None
    password: Optional[str] = None

class UserPublic(UserBase):
    pass

class Message(BaseModel):
    message: str
    
class UpdatePassword(BaseModel):
    current_password: str
    new_password: str