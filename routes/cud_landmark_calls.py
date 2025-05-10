from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models import Landmark as LandmarkModel, User
from database import get_db
from schemas import Landmark, LandmarkCreate
from utils.photo_utils import delete_photo_with_landmark_id
from auth import get_current_user

router = APIRouter()

@router.post("/add", response_model=Landmark)
def add_landmark(landmark_data: LandmarkCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="You don't have enough privileges")
    data = landmark_data.model_dump()
    data.pop('id', None) 
    db_landmark = LandmarkModel(**data)
    db.add(db_landmark)
    db.commit()
    db.refresh(db_landmark)
    return db_landmark


@router.patch("/update/{landmark_id}", response_model=Landmark)
def update_landmark(landmark_id: int, updated: LandmarkCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="You don't have enough privileges")

    db_landmark = db.query(LandmarkModel).filter(LandmarkModel.id == landmark_id).first()
    if db_landmark is None:
        raise HTTPException(status_code=404, detail="Landmark not found")
    
    data = updated.model_dump()
    data.pop('id', None)

    for key, value in data.items():
        setattr(db_landmark, key, value)

    db.commit()
    db.refresh(db_landmark)
    return db_landmark


@router.delete("/delete/{landmark_id}")
def delete_landmark(landmark_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="You don't have enough privileges")
    
    db_landmark = db.query(LandmarkModel).filter(LandmarkModel.id == landmark_id).first()
    if db_landmark is None:
        raise HTTPException(status_code=404, detail="Landmark not found")
    
    delete_photo_with_landmark_id(landmark_id)
    db.delete(db_landmark)
    db.commit()
    return {"message": "Deleted"}
