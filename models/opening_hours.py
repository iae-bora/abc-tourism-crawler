from sqlalchemy import Column, String, Integer, Boolean, Time, ForeignKey
from models import Base

class OpeningHours(Base):
    __tablename__ = 'opening_hours'

    id = Column(Integer, primary_key=True)
    day_of_week = Column(String)
    open = Column(Boolean)
    start_hour = Column(Time, nullable=True)
    end_hour = Column(Time, nullable=True)
    place_id = Column(Integer, ForeignKey("place.id"), nullable=False)
