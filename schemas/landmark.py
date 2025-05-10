from pydantic import BaseModel, Field, model_validator
from typing import Optional

class LandmarkBase(BaseModel):
    lat: float = Field(..., ge=-90, le=90)
    lng: float = Field(..., ge=-180, le=180)
    name: str = Field(..., min_length=1, max_length=100)
    type: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    image: Optional[str] = None

class LandmarkCreate(LandmarkBase):
    id: Optional[int] = None 

    @model_validator(mode='before')
    def ignore_id_on_create(cls, values):
        if 'id' in values and values['id'] is not None:
            values.pop('id')
        return values

class Landmark(LandmarkBase):
    id: int = Field(..., ge=1)

    class Config:
        from_attributes = True
        