from sqlalchemy import Column, Integer, ForeignKey, Table
from .base import Base

saved_landmarks = Table(
    "saved_landmarks", Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("landmark_id", Integer, ForeignKey("landmarks.id", ondelete="CASCADE"), primary_key=True),
)
