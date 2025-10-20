from pydantic import BaseModel, conint
from datetime import datetime
from typing import List, Optional


class OfferSchema(BaseModel):
    id: int
    name: str
    price: float

    class Config:
        orm_mode = True


class StandSchema(BaseModel):
    id: int
    city: str
    event: str
    section: Optional[str]
    name: str
    icon: Optional[str]
    type: Optional[str]
    info: Optional[str]
    lat: Optional[float]
    lng: Optional[float]
    open_time: Optional[str]
    close_time: Optional[str]
    image: Optional[str]
    offers: List[OfferSchema]
    rating: Optional[float]

    class Config:
        orm_mode = True


# Tracker Device Activation

class DeviceInitSchema(BaseModel):
    uuid: str

class DeviceInitResponseSchema(BaseModel):
    uuid: str
    markets: List[str]

class DeviceResponsesSchema(BaseModel):
    uuid: str
    activations: List[datetime]

    class Config:
        orm_mode = True

# Rating

class RatingSchema(BaseModel):
    device_uuid: str
    stand_id: int
    rating: conint(ge=1, le=5)

class DeviceStandRatingResponse(BaseModel):
    device_uuid: str
    stand_id: int
    rating: Optional[int]