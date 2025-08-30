from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class UserBase(BaseModel):
    id: Optional[int] = None
    username: str
    full_name: str
    is_active: bool
    is_superuser: bool
    
    model_config = ConfigDict(from_attributes=True)

class UserInDB(UserBase):
    password: str = Field(min_length=8, max_length=40)

class UserRead(UserBase):
    pass