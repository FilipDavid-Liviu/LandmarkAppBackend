from faker import Faker
from sqlalchemy.orm import Session
from models import User, Landmark, saved_landmarks

fake = Faker()

def populate_db_fakes(db: Session, num_landmarks: int = 10000):
    for _ in range(num_landmarks):
        landmark = Landmark(
            lat=fake.latitude(),
            lng=fake.longitude(),
            name=fake.company(),
            type=fake.word(),
            description=fake.paragraph(),
            image=fake.image_url()
        )
        db.add(landmark)

    db.commit()
    