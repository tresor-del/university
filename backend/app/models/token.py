from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy import func
from datetime import datetime, timedelta
from app.core.config import Base

class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String(128), nullable=False, unique=True, index=True)
    is_active = Column(Boolean, default=True)  
    created_at = Column(DateTime, default=func.now)
    expires_at = Column(DateTime, default=lambda: func.now() + timedelta(days=7))

    user = relationship("User", back_populates="tokens")
