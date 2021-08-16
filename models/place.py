from sqlalchemy import Column, String, Integer
from models import Base

class Place(Base):
    __tablename__ = 'place'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    category = Column(String)
    image = Column(String)
