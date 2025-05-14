from fastapi import Depends
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from typing import Optional
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from exceptions.exceptions import AuthenticationError
from models import User
from api.core.deps import get_db
from api.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(tz=timezone.utc) + expires_delta
    print(f"Token expiration time: {expire}")
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise AuthenticationError("Could not validate credentials")
        
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise AuthenticationError("User not found")
        
        return user
    except JWTError:
        raise AuthenticationError("Could not validate credentials")
