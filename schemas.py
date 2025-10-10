from pydantic import BaseModel
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

    class Config:
        orm_mode = True
