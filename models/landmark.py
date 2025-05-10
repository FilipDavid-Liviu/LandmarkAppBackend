from sqlalchemy import Column, Integer, Float, String, Text
from sqlalchemy.orm import relationship
from .base import Base
from .saved_landmarks import saved_landmarks

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
