from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from fake import populate_db_fakes
from db import seed_all, engine
from api.core.deps import get_db
from api.endpoints import (
    landmark_cud_routes,
    landmark_get_routes,
    photo_routes,
    user_routes,
    saved_landmarks_routes
)
from models import Base
from exceptions.exceptions import DatabaseError
from api.core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        Base.metadata.create_all(bind=engine)
        seed_all()
        yield
    except Exception as e:
        raise DatabaseError(f"Error during application startup: {str(e)}")

app = FastAPI(lifespan=lifespan)
app.include_router(user_routes.router)
app.include_router(landmark_get_routes.router)
app.include_router(saved_landmarks_routes.router)
app.include_router(landmark_cud_routes.router)
app.include_router(photo_routes.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

app.mount("/static", StaticFiles(directory=settings.STATIC_DIR), name="static")

@app.get("/health")
def health_check():
    return {"status": "OK"}

@app.post("/populate_fake_data")
def populate_fake_data(
    db: Session = Depends(get_db),
    num_landmarks: int = settings.DEFAULT_FAKE_LANDMARKS
):
    try:
        populate_db_fakes(db, num_landmarks, settings.FAKE_BATCH_SIZE)
        return {"message": "Database populated with fake data"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        