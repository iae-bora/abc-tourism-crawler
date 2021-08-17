from sqlalchemy import Column, String, Integer
from models import Base

class City(Base):
    __tablename__ = 'city'

    id = Column(Integer, primary_key=True)
    name = Column(String)