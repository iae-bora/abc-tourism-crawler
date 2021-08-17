from sqlalchemy import Column, String, Integer, ForeignKey
from models import Base

class Place(Base):
    __tablename__ = 'place'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    image = Column(String)
    city_id = Column(Integer, ForeignKey("city.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False)
