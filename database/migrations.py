import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db import Database
from models import Base, place, city, category, restaurant_category
from seed import load_cities_to_database, load_categories_to_database, load_restaurant_categories_to_database

database = Database()
Base.metadata.create_all(database.engine)

load_cities_to_database()
load_categories_to_database()
load_restaurant_categories_to_database()
