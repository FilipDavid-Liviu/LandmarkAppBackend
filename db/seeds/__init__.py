from .landmarks import LandmarkSeeder
from .users import UserSeeder

def seed_all():
    with LandmarkSeeder() as landmark_seeder:
        landmark_seeder.seed()
    
    with UserSeeder() as user_seeder:
        user_seeder.seed()
