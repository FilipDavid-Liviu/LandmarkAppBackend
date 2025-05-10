import os
from dotenv import load_dotenv
import logging
from pathlib import Path

load_dotenv()

class Settings:
    # Security settings
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    
    # CORS settings
    CORS_ORIGINS: list = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list = ["*"]
    CORS_ALLOW_HEADERS: list = ["*"]
    
    # Static files
    STATIC_DIR: str = "static"
    
    # Logging
    LOG_FILE: str = "performance_log.txt"
    LOG_FORMAT: str = "%(asctime)s - %(message)s"
    LOG_LEVEL: int = logging.INFO
    
    # Photo settings
    PHOTO_UPLOAD_DIR: str = os.getenv("PHOTO_UPLOAD_DIR")
    MAX_PHOTO_WIDTH: int = int(os.getenv("MAX_PHOTO_WIDTH"))
    MAX_PHOTO_HEIGHT: int = int(os.getenv("MAX_PHOTO_HEIGHT"))
    PHOTO_QUALITY: int = int(os.getenv("PHOTO_QUALITY"))
    
    # Fake data
    DEFAULT_FAKE_LANDMARKS: int = 10000
    FAKE_BATCH_SIZE: int = 1000

    def setup_logging(self):
        logging.basicConfig(
            filename=self.LOG_FILE,
            level=self.LOG_LEVEL,
            format=self.LOG_FORMAT
        )

settings = Settings()
settings.setup_logging()
