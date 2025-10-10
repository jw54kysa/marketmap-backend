from sqlalchemy import Column, Integer, String, Float, Boolean, JSON
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import relationship
from database import Base

class Stand(Base):
    __tablename__ = "stands"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, nullable=False, default="LPZ")
    event = Column(String, nullable=False, default="WNM25")
    section = Column(String, nullable=True)
    name = Column(String, nullable=False)
    icon = Column(String, nullable=True)
    type = Column(String, nullable=True)
    offers = relationship("Offer", back_populates="stand", cascade="all, delete-orphan")
    info = Column(String, nullable=True)
    lat = Column(Float, nullable=True)
    lng = Column(Float, nullable=True)
    open_time = Column(String, nullable=True)
    close_time = Column(String, nullable=True)
    is_active = Column(Boolean, nullable=True)
    image = Column(String, nullable=True)


class Offer(Base):
    __tablename__ = "offers"
    id = Column(Integer, primary_key=True)
    stand_id = Column(Integer, ForeignKey("stands.id"))
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    stand = relationship("Stand", back_populates="offers")
