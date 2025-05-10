from sqlalchemy.orm import Session
from models import User
from repositories.user_repository import save_landmark_for_user, unsave_landmark_for_user, get_user_saved_landmarks
from repositories.landmark_repository import get_landmark_by_id
from exceptions.exceptions import (
    LandmarkNotFoundError, 
    SavedLandmarkError,
    LandmarkAlreadySavedError,
    LandmarkNotSavedError
)

def save_landmark_service(db: Session, user: User, landmark_id: int):
    landmark = get_landmark_by_id(db, landmark_id)
    if not landmark:
        raise LandmarkNotFoundError(f"Landmark with id {landmark_id} not found")

    if landmark in user.saved_landmarks:
        raise LandmarkAlreadySavedError(f"Landmark with id {landmark_id} is already saved")

    try:
        save_landmark_for_user(db, user, landmark)
        return {"message": "Landmark saved successfully"}
    except Exception as e:
        raise SavedLandmarkError(f"Error saving landmark: {str(e)}")


def unsave_landmark_service(db: Session, user: User, landmark_id: int):
    landmark = get_landmark_by_id(db, landmark_id)
    if not landmark:
        raise LandmarkNotFoundError(f"Landmark with id {landmark_id} not found")

    if landmark not in user.saved_landmarks:
        raise LandmarkNotSavedError(f"Landmark with id {landmark_id} is not saved")

    try:
        unsave_landmark_for_user(db, user, landmark)
        return {"message": "Landmark unsaved successfully"}
    except Exception as e:
        raise SavedLandmarkError(f"Error unsaving landmark: {str(e)}")


def get_saved_landmarks_service(user: User):
    saved_landmarks = get_user_saved_landmarks(user)
    return {"saved_landmarks": saved_landmarks}
