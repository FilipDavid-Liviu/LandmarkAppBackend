from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from fake import populate_db_fakes
from api.core.config import settings
from api.core.deps import get_db
from api.core.auth import get_current_user
from models import User

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "OK"}

@router.post("/populate_fake_data")
def populate_fake_data(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    num_landmarks: int = settings.DEFAULT_FAKE_LANDMARKS
):
    try:
        if not current_user.is_admin:
            raise HTTPException(status_code=403, detail="User does not have admin privileges")
        populate_db_fakes(db, num_landmarks, settings.FAKE_BATCH_SIZE)
        return {"message": "Database populated with fake data"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
