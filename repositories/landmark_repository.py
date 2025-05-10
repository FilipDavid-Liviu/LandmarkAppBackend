from sqlalchemy.orm import Session
from models import Landmark as LandmarkModel
from utils.utils import normalize_search_text, normalize_column, abs_column
from exceptions.exceptions import DatabaseError


def create_landmark(db: Session, data: dict):
    try:
        landmark = LandmarkModel(**data)
        db.add(landmark)
        db.commit()
        db.refresh(landmark)
        return landmark
    except Exception as e:
        db.rollback()
        raise DatabaseError(f"Error creating landmark: {str(e)}")


def update_landmark(db: Session, landmark: LandmarkModel, data: dict):
    try:
        for key, value in data.items():
            setattr(landmark, key, value)
        db.commit()
        db.refresh(landmark)
        return landmark
    except Exception as e:
        db.rollback()
        raise DatabaseError(f"Error updating landmark: {str(e)}")


def delete_landmark(db: Session, landmark: LandmarkModel):
    try:
        db.delete(landmark)
        db.commit()
    except Exception as e:
        db.rollback()
        raise DatabaseError(f"Error deleting landmark: {str(e)}")


def get_all_landmarks(db: Session):
    try:
        return db.query(LandmarkModel).order_by(LandmarkModel.id).all()
    except Exception as e:
        raise DatabaseError(f"Error fetching landmarks: {str(e)}")


def get_landmark_by_id(db: Session, landmark_id: int):
    try:
        return db.query(LandmarkModel).filter(LandmarkModel.id == landmark_id).first()
    except Exception as e:
        raise DatabaseError(f"Error fetching landmark: {str(e)}")


def get_landmarks_by_name(db: Session, search: str | None):
    query = db.query(LandmarkModel)
    if search:
        normalized_search = normalize_search_text(search)
        normalized_name = normalize_column(LandmarkModel.name)
        query = query.filter(normalized_name.ilike(f"%{normalized_search}%"))
    return query.order_by(LandmarkModel.id).all()


def get_landmarks_by_name_type_sorted(db: Session, search: str | None, sort: int | None):
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

    return query.order_by(LandmarkModel.id).all()


def update_landmark_image(db: Session, landmark: LandmarkModel, image_url: str | None):
    try:
        landmark.image = image_url
        db.commit()
        db.refresh(landmark)
    except Exception as e:
        db.rollback()
        raise DatabaseError(f"Error updating landmark image: {str(e)}")
