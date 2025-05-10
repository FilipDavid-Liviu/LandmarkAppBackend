from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from models import Landmark as LandmarkModel, User
from database import get_db
from utils.photo_utils import process_image, delete_photo_with_landmark_id
from auth import get_current_user

router = APIRouter()

@router.post("/upload_photo/{landmark_id}")
def upload_photo(landmark_id: int, file: UploadFile = File(...), db: Session = Depends(get_db), request: Request = None, current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="You don't have enough privileges")
    db_landmark = db.query(LandmarkModel).filter(LandmarkModel.id == landmark_id).first()
    if not db_landmark:
        raise HTTPException(status_code=404, detail="Landmark not found")
    
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    delete_photo_with_landmark_id(landmark_id)

    filename = process_image(file, landmark_id)

    image_url = request.base_url._url.rstrip("/") + f"/static/photos/{filename}"
    db_landmark.image = image_url
    db.commit()
    db.refresh(db_landmark)

    return JSONResponse(content={"image": image_url})


@router.delete("/delete_photo/{landmark_id}")
def delete_photo(landmark_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="You don't have enough privileges")
    db_landmark = db.query(LandmarkModel).filter(LandmarkModel.id == landmark_id).first()
    if not db_landmark:
        raise HTTPException(status_code=404, detail="Landmark not found")
    
    delete_photo_with_landmark_id(landmark_id)
    db_landmark.image = None
    db.commit()
    return {"message": "Photo deleted"}

