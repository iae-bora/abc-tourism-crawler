from config import Config
from db import Database
from models.city import City
from models.category import Category
from models.restaurant_category import RestaurantCategory

database = Database()

def load_cities_to_database():
    cities_list = list(Config.CITIES_LIST.keys())
    for city in cities_list:
        database.session.add(City(name=city))
        database.session.commit()

def load_categories_to_database():
    categories_list = list(Config.CATEGORIES_DICT.keys())
    for category in categories_list:
        database.session.add(Category(name=category))
        database.session.commit()

def load_restaurant_categories_to_database():
    restaurant_categories_list = list(Config.RESTAURANT_CATEGORIES_DICT.keys())
    restaurant_categories_list.remove('Bar')
    for restaurant_category in restaurant_categories_list:
        database.session.add(RestaurantCategory(name=restaurant_category))
        database.session.commit()
