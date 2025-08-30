from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class TokenBase(BaseModel):
    token: str
    is_active: bool = True
    created_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    user_id: int


class TokenCreate(BaseModel):
    user_id: input


class TokenRead(TokenBase):
    id: int

  
    model_config = ConfigDict(from_attributes=True) 
