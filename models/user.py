from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from passlib.context import CryptContext
from .base import Base
from .saved_landmarks import saved_landmarks

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)

    saved_landmarks = relationship(
        "Landmark",
        secondary=saved_landmarks,
        back_populates="saved_by"
    )
    
    log_entries = relationship(
        "LogEntry",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.password_hash)

    def set_password(self, password: str):
        self.password_hash = pwd_context.hash(password)
        