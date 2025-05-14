from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Session
from models import LogEntry

def create_log_entry(db: Session, user_id: int, action: str):
    log_entry = LogEntry(user_id=user_id, action=action)
    db.add(log_entry)
    db.commit()
    return log_entry

def log_landmark_creation(db: Session, user_id: int, landmark_id: int):
    return create_log_entry(db, user_id, f"Created landmark {landmark_id}")

def log_landmark_update(db: Session, user_id: int, landmark_id: int):
    return create_log_entry(db, user_id, f"Updated landmark {landmark_id}")

def log_landmark_deletion(db: Session, user_id: int, landmark_id: int):
    return create_log_entry(db, user_id, f"Deleted landmark {landmark_id}")

def log_landmark_save(db: Session, user_id: int, landmark_id: int):
    return create_log_entry(db, user_id, f"Saved landmark {landmark_id}")

def log_landmark_unsave(db: Session, user_id: int, landmark_id: int):
    return create_log_entry(db, user_id, f"Unsaved landmark {landmark_id}")

def log_user_registration(db: Session, user_id: int):
    return create_log_entry(db, user_id, "User registered")

def log_user_login(db: Session, user_id: int):
    return create_log_entry(db, user_id, "User logged in")

def get_suspicious_users(db: Session, since: datetime, threshold: int = 20):
    suspicious = db.query(
        LogEntry.user_id,
        func.count(LogEntry.id).label('count')
    ).filter(
        LogEntry.timestamp >= since
    ).group_by(LogEntry.user_id).having(
        func.count(LogEntry.id) >= threshold
    ).all()
    print(f"[Monitoring] Found suspicious users: {suspicious}")
    return suspicious