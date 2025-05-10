from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import User
from api.core.deps import get_db
from api.core.auth import get_current_user
from services.saved_landmarks_service import save_landmark_service, unsave_landmark_service, get_saved_landmarks_service
from exceptions.exceptions import (
    LandmarkNotFoundError, 
    SavedLandmarkError,
    LandmarkAlreadySavedError,
    LandmarkNotSavedError
)

router = APIRouter(prefix="/saved_landmarks", tags=["Saved Landmarks"])


@router.post("/save/{landmark_id}")
def save_landmark(landmark_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        return save_landmark_service(db, current_user, landmark_id)
    except LandmarkNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except LandmarkAlreadySavedError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except SavedLandmarkError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/unsave/{landmark_id}")
def unsave_landmark(landmark_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        return unsave_landmark_service(db, current_user, landmark_id)
    except LandmarkNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except LandmarkNotSavedError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except SavedLandmarkError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get_saved")
def get_saved_landmarks(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        return get_saved_landmarks_service(current_user)
    except SavedLandmarkError as e:
        raise HTTPException(status_code=500, detail=str(e))
