from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import time
import logging

from models import Landmark as LandmarkModel
from database import get_db
from schemas import Landmark
from utils import normalize_search_text, normalize_column, abs_column

router = APIRouter()

@router.get("/get_all", response_model=List[Landmark])
def get_all(db: Session = Depends(get_db)):
    landmarks = db.query(LandmarkModel).order_by(LandmarkModel.id).all()
    return landmarks


@router.get("/get_all_name_type_sort", response_model=List[Landmark])
def get_all_name_type_sort(search: Optional[str] = None, sort: Optional[int] = None, db: Session = Depends(get_db)):
    start = time.time()
    query = db.query(LandmarkModel)
    if search:
        normalized_search = normalize_search_text(search)
        name_type = normalize_column(LandmarkModel.name + LandmarkModel.type)
        type_name = normalize_column(LandmarkModel.type + LandmarkModel.name)
        query = query.filter(
            name_type.ilike(f"%{normalized_search}%") |
            type_name.ilike(f"%{normalized_search}%")
        )

    if sort == 1:
        query = query.order_by(LandmarkModel.lat.desc())
    elif sort == 2:
        query = query.order_by(abs_column(LandmarkModel.lat).desc())

    results = query.order_by(LandmarkModel.id).all()
    end = time.time()

    logging.info(f"Query time with search='{search}', sort='{sort}': {end - start:.4f} seconds | Results: {len(results)}")
    return results


@router.get("/get_all_name", response_model=List[Landmark])
def get_all_name(search: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(LandmarkModel)

    if search:
        normalized_search = normalize_search_text(search)
        normalized_name = normalize_column(LandmarkModel.name)

        query = query.filter(normalized_name.ilike(f"%{normalized_search}%"))

    return query.order_by(LandmarkModel.id).all()


@router.get("/get_by_id/{landmark_id}", response_model=Landmark)
def get_by_id(landmark_id: int, db: Session = Depends(get_db)):
    db_landmark = db.query(LandmarkModel).filter(LandmarkModel.id == landmark_id).first()
    if db_landmark is None:
        raise HTTPException(status_code=404, detail="Landmark not found")
    return db_landmark
