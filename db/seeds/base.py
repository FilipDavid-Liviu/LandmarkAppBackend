from sqlalchemy.orm import Session
from db.session import SessionLocal
from exceptions.exceptions import DatabaseError

class BaseSeeder:
    def __init__(self):
        self.db: Session = SessionLocal()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()

    def seed(self):
        raise NotImplementedError("Subclasses must implement seed method")
