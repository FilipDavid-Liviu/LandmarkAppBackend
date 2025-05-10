from sqlalchemy.orm import Session
from models import User, Landmark
from schemas import UserCreate
from exceptions.exceptions import DatabaseError

def create_user(db: Session, user: UserCreate):
    try:
        new_user = User(username=user.username)
        new_user.set_password(user.password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        db.rollback()
        raise DatabaseError(f"Error creating user: {str(e)}")


def get_user_by_username(db: Session, username: str):
    try:
        return db.query(User).filter(User.username == username).first()
    except Exception as e:
        raise DatabaseError(f"Error fetching user: {str(e)}")


def get_user_by_id(db: Session, user_id: int):
    try:
        return db.query(User).filter(User.id == user_id).first()
    except Exception as e:
        raise DatabaseError(f"Error fetching user: {str(e)}")


def save_landmark_for_user(db: Session, user: User, landmark: Landmark):
    try:
        if landmark not in user.saved_landmarks:
            user.saved_landmarks.append(landmark)
            db.commit()
            db.refresh(user)
    except Exception as e:
        db.rollback()
        raise DatabaseError(f"Error saving landmark for user: {str(e)}")


def unsave_landmark_for_user(db: Session, user: User, landmark: Landmark):
    try:
        if landmark in user.saved_landmarks:
            user.saved_landmarks.remove(landmark)
            db.commit()
            db.refresh(user)
    except Exception as e:
        db.rollback()
        raise DatabaseError(f"Error unsaving landmark for user: {str(e)}")


def get_user_saved_landmarks(user: User):
    try:
        return [landmark.id for landmark in user.saved_landmarks]
    except Exception as e:
        raise DatabaseError(f"Error fetching saved landmarks: {str(e)}")
