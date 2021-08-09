import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db import engine
from models import Base, place

Base.metadata.create_all(engine)