from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from schemas import UserCreate
from services.user_service import register_user_service, login_user_service
from api.core.deps import get_db
from exceptions.exceptions import UserAlreadyExistsError, InvalidCredentialsError

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register/")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        return register_user_service(db, user)
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login/")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        return login_user_service(db, form_data)
    except InvalidCredentialsError as e:
        raise HTTPException(status_code=400, detail=str(e))
