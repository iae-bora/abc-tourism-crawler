from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from models import Base

class RestaurantCategory(Base):
    __tablename__ = 'restaurant_category'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    places = relationship("Place", backref="restaurant_category")