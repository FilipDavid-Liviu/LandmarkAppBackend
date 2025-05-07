from sqlalchemy import Column, Integer, String, Float, Text, Boolean, ForeignKey, Table, Index
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

saved_landmarks = Table(
    "saved_landmarks", Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("landmark_id", Integer, ForeignKey("landmarks.id", ondelete="CASCADE"), primary_key=True),
)

# class Landmark(Base):
#     __tablename__ = "landmarks"

#     id = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     lat = Column(Float, nullable=False)
#     lng = Column(Float, nullable=False)
#     name = Column(String(100), nullable=False)
#     type = Column(String(100), nullable=False)
#     description = Column(Text)
#     image = Column(Text)

#     saved_by = relationship(
#         "User",
#         secondary=saved_landmarks,
#         back_populates="saved_landmarks"
#     )

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

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False)
    is_admin = Column(Boolean, default=False)
    saved_landmarks = relationship(
        "Landmark",
        secondary=saved_landmarks,
        back_populates="saved_by"
    )
