from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class UserBase(BaseModel):
    username: str = Field(unique=True, index=True, max_length=255)
    full_name: str  | None = Field(default=None, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    
    model_config = ConfigDict(from_attributes=True) 

class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)
    
class UserRegister(UserBase):
    username: str = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)

class UserUpdate(UserBase):
    username: str | None = Field(default=None, max_length=255) 
    password: str | None = Field(default=None, min_length=8, max_length=40)

class UserUpdateMe(BaseModel):
    full_name: str | None = Field(default=None, max_length=255)
    username: str | None = Field(default=None, max_length=255)

    model_config = ConfigDict(from_attributes=True) 

class UserPublic(UserBase):
    id: int

class UsersPublic(UserBase):
    data: list[UserPublic]
    count: int

class Message(BaseModel):
    message: str
    
class UpdatePassword(BaseModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)

class NewPassword(BaseModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)
    
    
    model_config = ConfigDict(from_attributes=True) 
