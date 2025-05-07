from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import logging

from fake import populate_db_fakes
from database import engine, get_db
from models import Base
from seed import seed_landmarks
from routes import photo_calls, get_landmark_calls, cud_landmark_calls

logging.basicConfig(
    filename="performance_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)


app = FastAPI()
app.include_router(photo_calls.router)
app.include_router(get_landmark_calls.router)
app.include_router(cud_landmark_calls.router)
origins = [
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
seed_landmarks()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/health")
def health_check():
    return {"status": "OK"}


@app.post("/populate_fake_data")
def populate_fake_data(db: Session = Depends(get_db), num_landmarks: int = 10000):
    try:
        populate_db_fakes(db, num_landmarks)
        return {"message": "Database populated with fake data"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
        