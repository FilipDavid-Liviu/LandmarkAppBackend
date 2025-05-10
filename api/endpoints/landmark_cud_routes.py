from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import LandmarkCreate, Landmark
from api.core.deps import get_db
from api.core.auth import get_current_user
from services.landmark_service import (
    add_landmark_service,
    update_landmark_service,
    delete_landmark_service
)
from exceptions.exceptions import LandmarkNotFoundError, UnauthorizedError

router = APIRouter(prefix="/landmarks", tags=["Landmarks"])


@router.post("/add", response_model=Landmark)
def add_landmark(
    landmark_data: LandmarkCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        data = landmark_data.model_dump()
        data.pop("id", None)
        return add_landmark_service(db, current_user, data)
    except UnauthorizedError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.patch("/update/{landmark_id}", response_model=Landmark)
def update_landmark(
    landmark_id: int,
    updated: LandmarkCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        data = updated.model_dump()
        data.pop("id", None)
        return update_landmark_service(db, current_user, landmark_id, data)
    except UnauthorizedError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except LandmarkNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/delete/{landmark_id}")
def delete_landmark(
    landmark_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        return delete_landmark_service(db, current_user, landmark_id)
    except UnauthorizedError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except LandmarkNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
