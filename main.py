from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from database import engine, get_db
from models import Base, Landmark as LandmarkModel
from schemas import Landmark, LandmarkCreate
from seed import seed_landmarks

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


# API Endpoints
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