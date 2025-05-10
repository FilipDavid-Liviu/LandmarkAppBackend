from .base import BaseSeeder
from models import User
from exceptions.exceptions import DatabaseError

class UserSeeder(BaseSeeder):
    def __init__(self):
        super().__init__()
        self.dummy_users = [
            {"username": "david", "password": "abc", "is_admin": True},
            {"username": "ami", "password": "aa", "is_admin": False},
        ]

    def seed(self):
        try:
            if self.db.query(User).count() == 0:
                for user_data in self.dummy_users:
                    user = User(
                        username=user_data["username"],
                        is_admin=user_data["is_admin"]
                    )
                    user.set_password(user_data["password"])
                    self.db.add(user)
                self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise DatabaseError(f"Error seeding users: {str(e)}")
