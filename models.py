from sqlalchemy import Column, Integer, String, Float, Boolean
from database import Base

class Stand(Base):
    __tablename__ = "stands"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    icon = Column(String, nullable=True)
    type = Column(String, nullable=True)
    info = Column(String, nullable=True)
    lat = Column(Float, nullable=True)
    lng = Column(Float, nullable=True)
    open_time = Column(String, nullable=True)
    close_time = Column(String, nullable=True)
    is_active = Column(Boolean, nullable=True)

