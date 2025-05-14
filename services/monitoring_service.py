from datetime import datetime, timedelta, UTC
from sqlalchemy.orm import Session
from db import SessionLocal
from repositories.log_repository import get_suspicious_users

suspicious_users = set()

async def monitoring_loop(check_interval: int = 60):
    from asyncio import sleep
    print("[Monitoring] Background monitoring started.")
    while True:
        try:
            check_suspicious_activity()
        except Exception as e:
            print(f"[Monitoring] Error in monitoring loop: {str(e)}")
        print(f"[Monitoring] Sleeping for {check_interval} seconds.")
        await sleep(check_interval)

def check_suspicious_activity():
    global suspicious_users
    db: Session = SessionLocal()
    try:
        last_10_minutes = datetime.now(UTC) - timedelta(minutes=40)
        print(f"[Monitoring] Checking for suspicious activity since {last_10_minutes.isoformat()}")
        suspicious = get_suspicious_users(db, last_10_minutes, threshold=20)

        new_suspicious_users = {user_id for user_id, count in suspicious}
        if new_suspicious_users:
            print(f"[Monitoring] Suspicious users detected: {new_suspicious_users}")

        suspicious_users.clear()
        suspicious_users.update(new_suspicious_users)
    finally:
        db.close()
        