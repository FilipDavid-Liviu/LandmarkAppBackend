from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import asyncio


from fake import populate_db_fakes
from db import seed_all, engine
from api.core.deps import get_db
from api.endpoints import (
    landmark_cud_routes,
    landmark_get_routes,
    photo_routes,
    user_routes,
    saved_landmarks_routes,
    admin_routes,
    utils_routes
)
from models import Base
from exceptions.exceptions import DatabaseError
from api.core.config import settings
from services.monitoring_service import monitoring_loop
from exceptions.exceptions import AuthenticationError

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        Base.metadata.create_all(bind=engine)
        seed_all()
        monitoring_task = asyncio.create_task(monitoring_loop(check_interval=30))
        yield
    except Exception as e:
        raise DatabaseError(f"Error during application startup: {str(e)}")
    finally:
        monitoring_task.cancel()
        try:
            await monitoring_task
        except asyncio.CancelledError:
            pass

app = FastAPI(lifespan=lifespan)
app.include_router(user_routes.router)
app.include_router(landmark_get_routes.router)
app.include_router(saved_landmarks_routes.router)
app.include_router(landmark_cud_routes.router)
app.include_router(photo_routes.router)
app.include_router(admin_routes.router)
app.include_router(utils_routes.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

app.mount("/static", StaticFiles(directory=settings.STATIC_DIR), name="static")

@app.exception_handler(AuthenticationError)
async def authentication_error_handler(request: Request, exc: AuthenticationError):
    return JSONResponse(
        status_code=403,
        content={"message": str(exc)},
    )
