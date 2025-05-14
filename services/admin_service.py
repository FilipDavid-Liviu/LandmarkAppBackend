from sqlalchemy.orm import Session
from models import User
from services.monitoring_service import suspicious_users
from repositories.user_repository import get_user_by_id
from exceptions.exceptions import UnauthorizedError

def get_monitored_users_service(db: Session, current_user: User) -> list[dict]:

    if not current_user.is_admin:
        raise UnauthorizedError("Only admins can view monitored users")

    monitored_users = []
    for user_id in suspicious_users:
        user = get_user_by_id(db, user_id)
        if not user:
            continue
        if user:
            monitored_users.append({
                "id": user.id,
                "username": user.username,
                "is_admin": user.is_admin
            })

    return monitored_users
