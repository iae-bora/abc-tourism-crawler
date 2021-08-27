from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from models import Base

class Place(Base):
    __tablename__ = 'place'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    image = Column(String)
    business_status = Column(String)
    address = Column(String)
    phone = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    rating = Column(Float)
    city_id = Column(Integer, ForeignKey("city.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False)
    restaurant_category_id = Column(Integer, ForeignKey("restaurant_category.id"), nullable=True)
    opening_hours = relationship("OpeningHours", backref="place")
