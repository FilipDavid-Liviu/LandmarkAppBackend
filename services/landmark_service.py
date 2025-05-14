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
from repositories.log_repository import (
    log_landmark_creation,
    log_landmark_update,
    log_landmark_deletion
)
from utils.photo_utils import delete_photo_with_landmark_id
from exceptions.exceptions import LandmarkNotFoundError, UnauthorizedError


def add_landmark_service(db: Session, user: User, landmark_data: dict):
    if not user.is_admin:
        raise UnauthorizedError("User does not have admin privileges")
    landmark = create_landmark(db, landmark_data)
    log_landmark_creation(db, user.id, landmark.id)
    return landmark


def update_landmark_service(db: Session, user: User, landmark_id: int, data: dict):
    if not user.is_admin:
        raise UnauthorizedError("User does not have admin privileges")
    
    landmark = get_landmark_by_id(db, landmark_id)
    if not landmark:
        raise LandmarkNotFoundError(f"Landmark with id {landmark_id} not found")

    updated_landmark = update_landmark(db, landmark, data)
    log_landmark_update(db, user.id, landmark_id)
    return updated_landmark


def delete_landmark_service(db: Session, user: User, landmark_id: int):
    if not user.is_admin:
        raise UnauthorizedError("User does not have admin privileges")
    
    landmark = get_landmark_by_id(db, landmark_id)
    if not landmark:
        raise LandmarkNotFoundError(f"Landmark with id {landmark_id} not found")

    delete_photo_with_landmark_id(landmark_id)
    delete_landmark(db, landmark)
    log_landmark_deletion(db, user.id, landmark_id)


def get_all_landmarks_service(db: Session):
    return get_all_landmarks(db)


def get_landmark_by_id_service(db: Session, landmark_id: int):
    landmark = get_landmark_by_id(db, landmark_id)
    if not landmark:
        raise LandmarkNotFoundError(f"Landmark with id {landmark_id} not found")
    return landmark


def get_landmarks_name_service(db: Session, search: str | None, limit: int):
    return get_landmarks_by_name(db, search, limit)


def get_landmarks_name_type_sort_service(db: Session, search: str | None, sort: int | None):
    start = time.time()
    results = get_landmarks_by_name_type_sorted(db, search, sort)
    end = time.time()
    logging.info(f"Query time with search='{search}', sort='{sort}': {end - start:.4f} seconds | Results: {len(results)}")
    return results
