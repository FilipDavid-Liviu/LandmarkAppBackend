from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models import Landmark as LandmarkModel, User
from api.core.deps import get_db
from api.core.auth import get_current_user

router = APIRouter()

@router.post("/save_landmark/{landmark_id}")
def save_landmark(
    landmark_id: int, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    landmark = db.query(LandmarkModel).filter(LandmarkModel.id == landmark_id).first()
    if not landmark:
        raise HTTPException(status_code=404, detail="Landmark not found")
    
    if landmark in current_user.saved_landmarks:
        raise HTTPException(status_code=400, detail="Landmark already saved")
    
    current_user.saved_landmarks.append(landmark)
    db.commit()
    db.refresh(current_user)

    return {"message": "Landmark saved successfully"}

@router.post("/unsave_landmark/{landmark_id}")
def unsave_landmark(
    landmark_id: int, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    landmark = db.query(LandmarkModel).filter(LandmarkModel.id == landmark_id).first()
    if not landmark:
        raise HTTPException(status_code=404, detail="Landmark not found")
    
    if landmark not in current_user.saved_landmarks:
        raise HTTPException(status_code=400, detail="Landmark not saved by user")
    
    current_user.saved_landmarks.remove(landmark)
    db.commit()
    db.refresh(current_user)

    return {"message": "Landmark unsaved successfully"}


@router.get("/get_saved_landmarks")
def get_saved_landmarks(
    current_user: User = Depends(get_current_user), 
    _: Session = Depends(get_db)
):
    saved_landmark_ids = [landmark.id for landmark in current_user.saved_landmarks]
    
    return {"saved_landmarks": saved_landmark_ids}
