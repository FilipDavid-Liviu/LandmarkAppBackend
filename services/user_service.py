from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from schemas import UserCreate
from repositories.user_repository import create_user, get_user_by_username
from api.core.auth import create_access_token
from exceptions.exceptions import UserAlreadyExistsError, InvalidCredentialsError

def register_user_service(db: Session, user: UserCreate):
    existing_user = get_user_by_username(db, user.username)
    if existing_user:
        raise UserAlreadyExistsError("Username already taken")
    
    create_user(db, user)
    return {"message": "User created successfully"}


def login_user_service(db: Session, form_data: OAuth2PasswordRequestForm):
    user = get_user_by_username(db, form_data.username)
    if not user or not user.verify_password(form_data.password):
        raise InvalidCredentialsError("Invalid username or password")
    
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}
