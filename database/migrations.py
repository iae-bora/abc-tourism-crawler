import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db import Database
from models import Base, place

database = Database()
Base.metadata.create_all(database.engine)