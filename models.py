from sqlalchemy import Column, Integer, String, Float, Text, Boolean, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship
from passlib.context import CryptContext

Base = declarative_base()

saved_landmarks = Table(
    "saved_landmarks", Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("landmark_id", Integer, ForeignKey("landmarks.id", ondelete="CASCADE"), primary_key=True),
)

class Landmark(Base):
    __tablename__ = "landmarks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    name = Column(String(100), nullable=False, index=True)
    type = Column(String(100), nullable=False, index=True)
    description = Column(Text)
    image = Column(Text)

    saved_by = relationship(
        "User",
        secondary=saved_landmarks,
        back_populates="saved_landmarks"
    )

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

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.password_hash)

    def set_password(self, password: str):
        self.password_hash = pwd_context.hash(password)
