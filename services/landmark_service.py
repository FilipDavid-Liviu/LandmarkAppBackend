import logging
import time
from sqlalchemy.orm import Session
from models import User
from repositories.landmark_repository import (
    create_landmark,
    update_landmark,
    delete_landmark,
    get_all_landmarks,
    get_landmark_by_id,
    get_landmarks_by_name,
    get_landmarks_by_name_type_sorted,
)
from utils.photo_utils import delete_photo_with_landmark_id
from exceptions.exceptions import LandmarkNotFoundError, UnauthorizedError


def add_landmark_service(db: Session, user: User, landmark_data: dict):
    if not user.is_admin:
        raise UnauthorizedError("User does not have admin privileges")
    return create_landmark(db, landmark_data)


def update_landmark_service(db: Session, user: User, landmark_id: int, data: dict):
    if not user.is_admin:
        raise UnauthorizedError("User does not have admin privileges")
    
    landmark = get_landmark_by_id(db, landmark_id)
    if not landmark:
        raise LandmarkNotFoundError(f"Landmark with id {landmark_id} not found")

    return update_landmark(db, landmark, data)


def delete_landmark_service(db: Session, user: User, landmark_id: int):
    if not user.is_admin:
        raise UnauthorizedError("User does not have admin privileges")
    
    landmark = get_landmark_by_id(db, landmark_id)
    if not landmark:
        raise LandmarkNotFoundError(f"Landmark with id {landmark_id} not found")

    delete_photo_with_landmark_id(landmark_id)
    delete_landmark(db, landmark)


def get_all_landmarks_service(db: Session):
    return get_all_landmarks(db)


def get_landmark_by_id_service(db: Session, landmark_id: int):
    landmark = get_landmark_by_id(db, landmark_id)
    if not landmark:
        raise LandmarkNotFoundError(f"Landmark with id {landmark_id} not found")
    return landmark


def get_landmarks_name_service(db: Session, search: str | None):
    return get_landmarks_by_name(db, search)


def get_landmarks_name_type_sort_service(db: Session, search: str | None, sort: int | None):
    start = time.time()
    results = get_landmarks_by_name_type_sorted(db, search, sort)
    end = time.time()
    logging.info(f"Query time with search='{search}', sort='{sort}': {end - start:.4f} seconds | Results: {len(results)}")
    return results
