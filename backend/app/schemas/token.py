from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenRead(BaseModel):
    sub: str | None = None

  
    model_config = ConfigDict(from_attributes=True) 
