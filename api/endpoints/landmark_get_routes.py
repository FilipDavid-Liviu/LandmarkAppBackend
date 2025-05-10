from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from api.core.deps import get_db
from schemas import Landmark
from services.landmark_service import (
    get_all_landmarks_service,
    get_landmark_by_id_service,
    get_landmarks_name_service,
    get_landmarks_name_type_sort_service,
)
from exceptions.exceptions import LandmarkNotFoundError

router = APIRouter(prefix="/get_landmarks", tags=["Gets"])


@router.get("/get_all", response_model=List[Landmark])
def get_all(db: Session = Depends(get_db)):
    return get_all_landmarks_service(db)


@router.get("/get_all_name_type_sort", response_model=List[Landmark])
def get_all_name_type_sort(
    search: Optional[str] = None,
    sort: Optional[int] = None,
    db: Session = Depends(get_db)
):
    return get_landmarks_name_type_sort_service(db, search, sort)


@router.get("/get_all_name", response_model=List[Landmark])
def get_all_name(
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return get_landmarks_name_service(db, search)


@router.get("/get_by_id/{landmark_id}", response_model=Landmark)
def get_by_id(landmark_id: int, db: Session = Depends(get_db)):
    try:
        return get_landmark_by_id_service(db, landmark_id)
    except LandmarkNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
