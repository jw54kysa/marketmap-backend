from sqlalchemy import Table, Column, Integer, String, Float, Boolean, ForeignKey
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
    city = Column(String, nullable=False, default="LPZ")
    event = Column(String, nullable=False, default="WNM25")
    section = Column(String, nullable=True)
    name = Column(String, nullable=False)
    icon = Column(String, nullable=True)
    type = Column(String, nullable=True)

    offers = relationship(
        "Offer",
        secondary=stand_offer_association,
        back_populates="stands"
    )

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
    
    stands = relationship(
        "Stand",
        secondary=stand_offer_association,
        back_populates="offers"
    )
    
    def __str__(self):
        return f"{self.name} (${self.price})"
