from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class UserBase(BaseModel):
    """
    Schemas de base pour les users
    """
    username: str = Field(
        max_length=255, 
        json_schema_extra={"unique":True, "index":True}
    )
    full_name: str  | None = Field(default=None, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    
    model_config = ConfigDict(from_attributes=True) 

class UserCreate(UserBase):
    """
    Schemas pour la création des users
    """
    password: str = Field(min_length=8, max_length=40)
    
class UserRegister(UserBase):
    """
    Schemas pour l'enrégistrement de l'utilisaeur
    """
    username: str = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)
    is_active: bool = True

class UserUpdate(UserBase):
    """
    Schemas pour la mise à jour de l'utilisateur 
    """
    username: str | None = Field(default=None, max_length=255)
    is_active: bool = True 
    password: str | None = Field(default=None, min_length=8, max_length=40)

class UserUpdateMe(BaseModel):
    """
    Schemas pour la mise à jour de son propre compte utilisateur
    """
    full_name: str | None = Field(default=None, max_length=255)
    is_active: bool = True
    username: str | None = Field(default=None, max_length=255)
    is_active: bool = True

    model_config = ConfigDict(from_attributes=True) 

class UserPublic(UserBase):
    """
    Schemas publique des utilisateurs
    """
    id: int

class UsersPublic(BaseModel):
    """
    Schemas publique de la liste de tous les utilisateurs
    """
    data: list[UserPublic]
    count: int
    
    model_config = ConfigDict(from_attributes=True)

class Message(BaseModel):
    """
    Schemas d'envoie de message
    """
    message: str
    
class UpdatePassword(BaseModel):
    """
    Schemas pour mettre à jour le mot de passe
    """
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)

class NewPassword(BaseModel):
    """
    Schemas pour prendre un nouveau mot de passe
    """
    token: str
    new_password: str = Field(min_length=8, max_length=40)
    
    
    model_config = ConfigDict(from_attributes=True) 
