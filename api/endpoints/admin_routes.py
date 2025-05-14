from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.core.deps import get_db
from api.core.auth import get_current_user
from models import User
from services.admin_service import get_monitored_users_service
from exceptions.exceptions import UnauthorizedError
router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/monitored-users")
def get_monitored_users(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        monitored_users = get_monitored_users_service(db, current_user)
        return {"monitored_users": monitored_users}
    except UnauthorizedError as e:
        raise HTTPException(status_code=403, detail=str(e))