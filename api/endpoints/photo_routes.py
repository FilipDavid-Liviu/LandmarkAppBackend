from fastapi import APIRouter, UploadFile, File, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from api.core.deps import get_db
from api.core.auth import get_current_user
from models import User
from services.photo_service import upload_photo_service, delete_photo_service
from exceptions.exceptions import (
    UnauthorizedError,
    LandmarkNotFoundError,
    InvalidFileTypeError,
    FileProcessingError
)

router = APIRouter(prefix="/photos", tags=["Photos"])

@router.post("/upload/{landmark_id}")
def upload_photo(
    landmark_id: int,
    file: UploadFile = File(...),
    request: Request = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        image_url = upload_photo_service(db, current_user, landmark_id, file, request.base_url._url)
        return JSONResponse(content={"image": image_url})
    except UnauthorizedError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except LandmarkNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except InvalidFileTypeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except FileProcessingError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete/{landmark_id}")
def delete_photo(
    landmark_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        delete_photo_service(db, current_user, landmark_id)
        return {"message": "Photo deleted"}
    except UnauthorizedError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except LandmarkNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except FileProcessingError as e:
        raise HTTPException(status_code=500, detail=str(e))