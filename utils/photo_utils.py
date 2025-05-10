from pathlib import Path
from io import BytesIO
from PIL import Image
from fastapi import UploadFile

UPLOAD_DIR = Path("static/photos")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
MAX_WIDTH = 1024
MAX_HEIGHT = 1024

def delete_photo_with_landmark_id(landmark_id: int):
    for file in UPLOAD_DIR.glob(f"{landmark_id}.*"):
        file.unlink()

def process_image(file: UploadFile, landmark_id: int) -> str:
    image_bytes = BytesIO(file.file.read())
    with Image.open(image_bytes) as img:
        img = img.convert("RGB")
        img.thumbnail((MAX_WIDTH, MAX_HEIGHT))

        filename = f"{landmark_id}.jpg"
        file_path = UPLOAD_DIR / filename
        img.save(file_path, format="JPEG", quality=85)
    
    return filename
