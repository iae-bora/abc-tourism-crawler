from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from sqlalchemy import select
import time as timer
from datetime import time
import logging

from .places import get_place_details
from config import Config
from database.db import Database

from models.place import Place
from models.city import City
from models.category import Category
from models.restaurant_category import RestaurantCategory
from models.opening_hours import OpeningHours

logging.basicConfig(level=logging.INFO, filename='crawler.log', format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class Crawler:
    def __init__(self):
        self.db = Database()
        self.card_wrapper_list_xpath = ""
        self.next_page_xpath = ""
        self.categories_xpath = ""
        self.categories_dictionary = None
        self.place_name_xpath = ""
        self.place_image_xpath = ""
        self.image_property = ""
    
    def web_scrape_pages(self, city, url, driver):
        logger.info(f'Starting city {city}')
        driver.get(url)
        self.check_cookies_banner_exists(driver)

        try:
            for page in range(0, Config.MAX_PAGES_PER_CITY):
                timer.sleep(Config.SLEEP_INTERVAL)
                logger.info(f'Page {page} from city {city}')
                driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)

                card_wrapper_list = driver.find_elements_by_xpath(self.card_wrapper_list_xpath)
                self.iterate_cards(card_wrapper_list)
                
                timer.sleep(Config.SLEEP_INTERVAL)
                driver.find_element_by_xpath(self.next_page_xpath).click()
        except NoSuchElementException:
            logger.info(f'No more pages found from city {city}')
        except Exception as e:
            logger.error('Error in page iteration: ' + str(e))

    def check_cookies_banner_exists(self, driver):
        try:
            timer.sleep(Config.SLEEP_INTERVAL)
            driver.find_element_by_xpath("//button[@class='evidon-banner-acceptbutton']").click()
        except:
            logger.info('No cookies banner found')
        return

    def iterate_cards(self, cards):
        for card_index in range(len(cards)):
            self.get_information_of_place(cards[card_index])

    def get_information_of_place(self, card):
        try:
            place = Place()

            place.name = card.find_element_by_xpath(self.place_name_xpath).text.split('.', 1)[-1].strip()
            logger.info(f"----- {place.name} -----")
            
            place_already_exist = self.check_if_place_already_exist(place)
            if place_already_exist is not False:
                raise Exception(f'Place {place.name} already exists')

            categories_from_tripadvisor = card.find_element_by_xpath(self.categories_xpath).text.split(' ??? ') or []

            place = self.set_category_to_place(categories_from_tripadvisor, place)
            if place == None:
                raise Exception(f'Category of {place.name} does not match with list')

            place.image = self.get_image_from_card(card)

            place_details = get_place_details(place.name)
            if place_details == {}:
                raise Exception(f'Place {place.name} not found in Google Places')
            
            place = self.fill_place_with_details(place, place_details)

            if "opening_hours" in place_details:
                place_id = self.insert_place_in_database(place)
                if place_id is None:
                    raise Exception(f'Error adding {place.name} to database')
                
                self.save_opening_hours(place_details["opening_hours"]["weekday_text"], place_id)
                logger.info('Opening hours added successfully')
            else:
                raise Exception(f'Place {place.name} does not have opening_hours')

            self.db.session.commit()
            logger.info('Data inserted successfully')
        except Exception as e:
            logger.error(f'Error retrieving data: {e}')
            self.db.session.rollback()
    
    def insert_place_in_database(self, place):
        try:
            self.db.session.add(place)
            self.db.session.flush()
            self.db.session.refresh(place)

            logger.info(f'Place added successfully: {place.name}')
            return place.id
        except Exception as e:
            logger.error(f'Database error when inserting place: {str(e)}')
            return None
    
    def get_id_from_city(self, city_name):
        city = self.db.session.query(City).filter_by(name=city_name).first()
        return city.id

    def get_id_from_category(self, category_name):
        category = self.db.session.query(Category).filter_by(name=category_name).first()
        return category.id
    
    def set_category_to_place(self, categories_from_tripadvisor, place):
        category = ''
        for category_key, categories_variations in self.categories_dictionary.items():
            if any(category in ','.join(categories_from_tripadvisor).lower() for category in categories_variations):
                category = category_key
                break
        
        if category == '':
            return None

        place.category_id = self.get_id_from_category(category)
        place.restaurant_category_id = None
        
        return place
    
    def check_if_place_already_exist(self, new_place):
        statement = select(Place).where(Place.name == new_place.name)
        result = self.db.session.execute(statement).scalars().first()

        if result is None:
            return False
        else:
            return result

    def fill_place_with_details(self, place: Place, details: dict):
        city = self.get_city_from_address_components(details['address_components'])
        if city not in Config.CITIES_LIST.keys():
            raise Exception(f'City {city} is not located in ABC region')
        place.city_id = self.get_id_from_city(city)

        place.business_status = details["business_status"]
        place.address = details["formatted_address"]
        place.phone = details.get("formatted_phone_number", None)
        place.rating = details.get("rating", None)
        place.latitude = details["geometry"]["location"]["lat"]
        place.longitude = details["geometry"]["location"]["lng"]

        return place
    
    def get_city_from_address_components(self, address_components):
        for address_component in address_components:
            if 'administrative_area_level_2' in address_component['types']:
                city = address_component['long_name']
                return city
        return None
    
    def save_opening_hours(self, weekday_text_list, place_id):
        for weekday_text in weekday_text_list:
            day_of_week, opening_hour_list = weekday_text.split(':', 1)

            for opening_hour in opening_hour_list.split(','):
                opening_hours = OpeningHours()
                opening_hours.day_of_week = day_of_week
                
                if opening_hour.strip() == 'Fechado':
                    opening_hours.open = False
                else:
                    opening_hours.open = True

                    if opening_hour.strip() == 'Atendimento 24 horas':
                        opening_hours.start_hour = time(0, 0, 0)
                        opening_hours.end_hour = time(23, 59, 59)
                    else:
                        start_hour, end_hour = opening_hour.strip().split(' ??? ')
                        start_hour_hours, start_hour_minutes = start_hour.split(':')
                        end_hour_hours, end_hour_minutes = end_hour.split(':')

                        opening_hours.start_hour = time(int(start_hour_hours), int(start_hour_minutes), 0)
                        opening_hours.end_hour = time(int(end_hour_hours), int(end_hour_minutes), 0)
                
                opening_hours.place_id = place_id
                self.insert_opening_hours_in_database(opening_hours)
    
    def insert_opening_hours_in_database(self, opening_hours):
        try:
            self.db.session.add(opening_hours)
        except Exception as e:
            logger.error(f'Database error when inserting opening_hours: {str(e)}')
        

class PlacesCrawler(Crawler):
    def __init__(self):
        self.db = Database()
        self.card_wrapper_list_xpath = ".//div[@data-automation='cardWrapper']"
        self.next_page_xpath = "//a[@aria-label='Pr??xima p??gina']"
        self.categories_xpath = ".//span/div/div/div[2]/div[2]/div[1]/div/div/div[1]"
        self.categories_dictionary = Config.CATEGORIES_DICT
        self.place_name_xpath = ".//span[@name='title']"
        self.place_image_location = "img"
        self.image_property = "src"
    
    def get_image_from_card(self, card):
        image = ''
        try:
            image = card.find_element_by_tag_name(self.place_image_location).get_attribute(self.image_property)
        except NoSuchElementException:
            image = ''
        return image

class RestaurantCrawler(Crawler):
    def __init__(self):
        self.db = Database()
        self.card_wrapper_attribute_name = 'data-test'
        self.card_wrapper_list_xpath = f"//div[contains(@{self.card_wrapper_attribute_name}, '_list_item')]"
        self.next_page_xpath = "//a[contains(text(), 'Pr??ximas')]"
        self.categories_xpath = ".//span/div[1]/div[2]/div[2]/div/div[2]/span[1]/span"
        self.categories_dictionary = Config.RESTAURANT_CATEGORIES_DICT
        self.place_name_xpath = ".//span/div[1]/div[2]/div[1]/div/span/a"
        self.place_image_location = ".//span/div[1]/div[1]/span/a/div[2]/div/div[1]/ul/li[1]/div"
        self.image_property = "background-image"
        self.category_id = self.get_id_from_category('Restaurante')
    
    def get_image_from_card(self, card):
        image = ''
        try:
            image = card.find_element_by_xpath(self.place_image_location).value_of_css_property(self.image_property).lstrip('url("').rstrip('")')
        except NoSuchElementException:
            image = ''
        return image

    def get_id_from_restaurant_category(self, restaurant_category_name):
        restaurant_category = self.db.session.query(RestaurantCategory).filter_by(name=restaurant_category_name).first()
        return restaurant_category.id
    
    def set_category_to_place(self, categories_from_tripadvisor, place):
        category = ''
        for category_key, categories_variations in self.categories_dictionary.items():
            if any(category in ','.join(categories_from_tripadvisor).lower() for category in categories_variations):
                category = category_key
                break
        
        if category == '':
            return None
        
        if category == 'Bar':
            place.category_id = self.get_id_from_category(category)
            place.restaurant_category_id = None
        else:
            place.category_id = self.category_id
            place.restaurant_category_id = self.get_id_from_restaurant_category(category)
        
        return place
