from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from database import engine, get_db
from models import Base, Landmark as LandmarkModel
from schemas import Landmark, LandmarkCreate
from seed import seed_landmarks
from pathlib import Path
from fastapi.responses import JSONResponse
from uuid import uuid4
import os
from fastapi.staticfiles import StaticFiles
from fastapi.requests import Request

app = FastAPI()
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


@app.get("/get_all", response_model=List[Landmark])
def get_all(db: Session = Depends(get_db)):
    landmarks = db.query(LandmarkModel).order_by(LandmarkModel.id).all()
    return landmarks

@app.get("/get_all_name_type_sort", response_model=List[Landmark])
def get_all_name_type_sort(search: Optional[str] = None, sort: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(LandmarkModel)

    if search:
        query = query.filter(
            (LandmarkModel.name.ilike(f"%{search}%")) | (LandmarkModel.type.ilike(f"%{search}%"))
        )

    if sort == 1:
        query = query.order_by(LandmarkModel.lat.desc())
    elif sort == 2:
        query = query.order_by(LandmarkModel.lat.asc())

    return query.order_by(LandmarkModel.id).all()

@app.get("/get_all_name", response_model=List[Landmark])
def get_all_name(search: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(LandmarkModel)

    if search:
        query = query.filter(LandmarkModel.name.ilike(f"%{search}%"))

    return query.order_by(LandmarkModel.id).all()

@app.post("/add", response_model=Landmark)
def add_landmark(landmark_data: LandmarkCreate, db: Session = Depends(get_db)):
    data = landmark_data.model_dump()
    data.pop('id', None) 
    db_landmark = LandmarkModel(**data)
    db.add(db_landmark)
    db.commit()
    db.refresh(db_landmark)
    return db_landmark

@app.delete("/delete/{landmark_id}")
def delete_landmark(landmark_id: int, db: Session = Depends(get_db)):
    db_landmark = db.query(LandmarkModel).filter(LandmarkModel.id == landmark_id).first()
    if db_landmark is None:
        raise HTTPException(status_code=404, detail="Landmark not found")
    
    delete_landmark_photo(landmark_id)
    db.delete(db_landmark)
    db.commit()
    return {"message": "Deleted"}

@app.patch("/update/{landmark_id}", response_model=Landmark)
def update_landmark(landmark_id: int, updated: LandmarkCreate, db: Session = Depends(get_db)):
    db_landmark = db.query(LandmarkModel).filter(LandmarkModel.id == landmark_id).first()
    if db_landmark is None:
        raise HTTPException(status_code=404, detail="Landmark not found")
    
    data = updated.model_dump()
    data.pop('id', None)

    for key, value in data.items():
        setattr(db_landmark, key, value)

    db.commit()
    db.refresh(db_landmark)
    return db_landmark

@app.get("/get_by_id/{landmark_id}", response_model=Landmark)
def get_by_id(landmark_id: int, db: Session = Depends(get_db)):
    db_landmark = db.query(LandmarkModel).filter(LandmarkModel.id == landmark_id).first()
    if db_landmark is None:
        raise HTTPException(status_code=404, detail="Landmark not found")
    return db_landmark

@app.get("/health")
def health_check():
    return {"status": "OK"}



UPLOAD_DIR = Path("static/photos")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@app.post("/upload_photo/{landmark_id}")
def upload_photo(landmark_id: int, file: UploadFile = File(...), db: Session = Depends(get_db), request: Request = None):
    db_landmark = db.query(LandmarkModel).filter(LandmarkModel.id == landmark_id).first()
    if not db_landmark:
        raise HTTPException(status_code=404, detail="Landmark not found")
    
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    ext = os.path.splitext(file.filename)[1]
    filename = f"{landmark_id}{ext}"
    file_path = UPLOAD_DIR / filename

    for f in UPLOAD_DIR.glob(f"{landmark_id}.*"):
        f.unlink()

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    image = request.base_url._url.rstrip("/") + f"/static/photos/{filename}"
    db_landmark.image = image
    db.commit()
    db.refresh(db_landmark)

    return JSONResponse(content={"image": image})

@app.delete("/delete_photo/{landmark_id}")
def delete_photo(landmark_id: int, db: Session = Depends(get_db)):
    db_landmark = db.query(LandmarkModel).filter(LandmarkModel.id == landmark_id).first()
    if not db_landmark:
        raise HTTPException(status_code=404, detail="Landmark not found")
    
    delete_landmark_photo(landmark_id)
    db_landmark.image = None
    db.commit()
    return {"message": "Photo deleted"}


def delete_landmark_photo(landmark_id: int):
    for file in UPLOAD_DIR.glob(f"{landmark_id}.*"):
        try:
            file.unlink()
        except Exception as e:
            print(f"Error deleting file {file}: {e}")
            