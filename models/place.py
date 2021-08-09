import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import Column, String, Integer
from models import Base

class Place(Base):
    __tablename__ = 'places'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    category = Column(String)
    image = Column(String)
