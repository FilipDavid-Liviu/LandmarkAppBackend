from pathlib import Path
from io import BytesIO
from PIL import Image
from fastapi import UploadFile
import os
from dotenv import load_dotenv
from api.core.config import settings
from exceptions.exceptions import FileProcessingError

load_dotenv()

UPLOAD_DIR = Path(settings.PHOTO_UPLOAD_DIR)
MAX_WIDTH = settings.MAX_PHOTO_WIDTH
MAX_HEIGHT = settings.MAX_PHOTO_HEIGHT
PHOTO_QUALITY = settings.PHOTO_QUALITY

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

def delete_photo_with_landmark_id(landmark_id: int):
    for file in UPLOAD_DIR.glob(f"{landmark_id}.*"):
        file.unlink()

def process_image(file: UploadFile, landmark_id: int) -> str:
    try:
        image_bytes = BytesIO(file.file.read())
        with Image.open(image_bytes) as img:
            img = img.convert("RGB")
            img.thumbnail((MAX_WIDTH, MAX_HEIGHT))

            filename = f"{landmark_id}.jpg"
            file_path = UPLOAD_DIR / filename
            img.save(file_path, format="JPEG", quality=PHOTO_QUALITY)
        
        return filename
    except Exception as e:
        raise FileProcessingError(f"Error processing image: {str(e)}")
