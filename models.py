from sqlalchemy import Column, Integer, String, Float, Text, Boolean, ForeignKey, Table
from sqlalchemy.orm import declarative_base

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
    name = Column(String(100), nullable=False)
    type = Column(String(100), nullable=False)
    description = Column(Text)
    photo_url = Column(Text)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    is_admin = Column(Boolean, default=False)
