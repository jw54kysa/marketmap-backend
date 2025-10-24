from sqlalchemy import Table, Column, Integer, String, Float, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from database import Base

stand_offer_association = Table(
    "stand_offer_association",
    Base.metadata,
    Column("stand_id", Integer, ForeignKey("stands.id")),
    Column("offer_id", Integer, ForeignKey("offers.id"))
)

class Stand(Base):
    __tablename__ = "stands"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, nullable=False, default="lpz")
    event = Column(String, nullable=False, default="25_lpz_wm")
    section = Column(String, nullable=True, default="markt")
    name = Column(String, nullable=False)
    icon = Column(String, nullable=True)
    type_id = Column(Integer, ForeignKey("types.id"), nullable=True)
    type = relationship("Type", backref="stands")
    
    offers = relationship(
        "Offer",
        secondary=stand_offer_association,
        back_populates="stands"
    )

    info = Column(String, nullable=True, default="Hier gibts lecker lecker essen")
    lat = Column(Float, nullable=True)
    lng = Column(Float, nullable=True)
    open_time = Column(String, nullable=True, default="12:00")
    close_time = Column(String, nullable=True, default="22:00")
    is_active = Column(Boolean, nullable=True, default=True)
    image = Column(String, nullable=True)

    device_ratings = relationship("DeviceStandRating", back_populates="stand", cascade="all, delete-orphan")

class Offer(Base):
    __tablename__ = "offers"
    id = Column(Integer, primary_key=True)
    stand_id = Column(Integer, ForeignKey("stands.id"))
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    
    stands = relationship(
        "Stand",
        secondary=stand_offer_association,
        back_populates="offers"
    )
    
    def __str__(self):
        return f"{self.name} (${self.price})"
    
class Type(Base):
    __tablename__ = "types"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    icon = Column(String, nullable=True)
    color = Column(String, nullable=True)

    def __str__(self):
        return f"{self.name}"


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String, unique=True, index=True)
    activations = relationship("DeviceActivation", back_populates="device", cascade="all, delete-orphan")
    
    stand_ratings = relationship("DeviceStandRating", back_populates="device", cascade="all, delete-orphan")


class DeviceActivation(Base):
    __tablename__ = "device_activations"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    device = relationship("Device", back_populates="activations")


class DeviceStandRating(Base):
    __tablename__ = "device_stand_ratings"

    device_id = Column(Integer, ForeignKey("devices.id"), primary_key=True)
    stand_id = Column(Integer, ForeignKey("stands.id"), primary_key=True)
    rating = Column(Integer, nullable=False)

    device = relationship("Device", back_populates="stand_ratings")
    stand = relationship("Stand", back_populates="device_ratings")