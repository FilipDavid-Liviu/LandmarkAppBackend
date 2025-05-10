from sqlalchemy.orm import Session
from models import User
from repositories.landmark_repository import get_landmark_by_id, update_landmark_image
from utils.photo_utils import process_image, delete_photo_with_landmark_id
from exceptions.exceptions import UnauthorizedError, LandmarkNotFoundError, InvalidFileTypeError, FileProcessingError

def upload_photo_service(db: Session, user: User, landmark_id: int, file, base_url: str) -> str:
    if not user.is_admin:
        raise UnauthorizedError("User does not have admin privileges")

    landmark = get_landmark_by_id(db, landmark_id)
    if not landmark:
        raise LandmarkNotFoundError(f"Landmark with id {landmark_id} not found")

    if not file.content_type.startswith("image/"):
        raise InvalidFileTypeError("File must be an image")

    try:
        delete_photo_with_landmark_id(landmark_id)
        filename = process_image(file, landmark_id)
        image_url = base_url.rstrip("/") + f"/static/photos/{filename}"
        update_landmark_image(db, landmark, image_url)
        return image_url
    except Exception as e:
        raise FileProcessingError(f"Error processing image: {str(e)}")

def delete_photo_service(db: Session, user: User, landmark_id: int):
    if not user.is_admin:
        raise UnauthorizedError("User does not have admin privileges")

    landmark = get_landmark_by_id(db, landmark_id)
    if not landmark:
        raise LandmarkNotFoundError(f"Landmark with id {landmark_id} not found")

    try:
        delete_photo_with_landmark_id(landmark_id)
        update_landmark_image(db, landmark, None)
    except Exception as e:
        raise FileProcessingError(f"Error deleting image: {str(e)}")
