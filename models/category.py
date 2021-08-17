from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from models import Base

class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    places = relationship("Place", backref="category")