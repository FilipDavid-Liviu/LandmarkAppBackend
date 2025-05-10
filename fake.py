from faker import Faker
from sqlalchemy.orm import Session
from models import Landmark
from exceptions.exceptions import DatabaseError
from api.core.config import settings

fake = Faker()

def populate_db_fakes(
    db: Session,
    num_landmarks: int = settings.DEFAULT_FAKE_LANDMARKS,
    batch_size: int = settings.FAKE_BATCH_SIZE
):
    try:
        for i in range(0, num_landmarks, batch_size):
            batch = []
            current_batch_size = min(batch_size, num_landmarks - i)
            
            for _ in range(current_batch_size):
                landmark = Landmark(
                    lat=fake.latitude(),
                    lng=fake.longitude(),
                    name=fake.company(),
                    type=fake.word(),
                    description=fake.paragraph(),
                    image=fake.image_url()
                )
                batch.append(landmark)
            
            db.bulk_save_objects(batch)
            db.commit()
            
    except Exception as e:
        db.rollback()
        raise DatabaseError(f"Error populating fake data: {str(e)}")
    