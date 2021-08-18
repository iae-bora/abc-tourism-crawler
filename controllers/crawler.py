from selenium.common.exceptions import NoSuchElementException
from sqlalchemy import select
import time
from .places import get_place_details
from config import Config
from database.db import Database

from models.place import Place
from models.city import City
from models.category import Category

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
        places = []

        driver.get(url)
        self.check_cookies_banner_exists(driver)

        city_id = self.get_id_from_city(city)

        try:
            for page in range(0, Config.MAX_PAGES_PER_CITY):
                time.sleep(Config.SLEEP_INTERVAL)
                card_wrapper_list = driver.find_elements_by_xpath(self.card_wrapper_list_xpath)
                places.extend(self.iterate_cards(card_wrapper_list, city_id))
                
                time.sleep(Config.SLEEP_INTERVAL)
                driver.find_element_by_xpath(self.next_page_xpath).click()
        except NoSuchElementException:
            print('No more pages found')
        except Exception as e:
            print('Error: ' + str(e))
        
        return places

    def check_cookies_banner_exists(self, driver):
        try:
            time.sleep(Config.SLEEP_INTERVAL)
            driver.find_element_by_xpath("//button[@class='evidon-banner-acceptbutton']").click()
        except:
            print('No cookies banner found')
        return

    def iterate_cards(self, cards, city_id):
        places_in_page = []
        for card_index in range(len(cards)):
            place = self.get_information_of_place(cards[card_index], city_id)
            if place != None:
                places_in_page.append(place)
                self.insert_place_in_database(place)
            break
        
        return places_in_page

    def get_information_of_place(self, card, city_id):
        place = Place()

        categories_from_tripadvisor = card.find_element_by_xpath(self.categories_xpath).text.split(' • ') or []

        category = ''
        for category_key, categories_variations in self.categories_dictionary.items():
            if any(category in ','.join(categories_from_tripadvisor).lower() for category in categories_variations):
                category = category_key
                break
        
        if category == '':
            return None

        place.category_id = self.get_id_from_category(category)
        place.name = card.find_element_by_xpath(self.place_name_xpath).text.split('.', 1)[-1].strip()
        
        place_already_exist = self.check_if_place_already_exist(place)
        if place_already_exist == True:
            return None

        place.image = self.get_image_from_card(card)
        place.city_id = city_id

        place_details = get_place_details(place.name)
        if place_details == {}:
            return None
        
        place.business_status = place_details["business_status"]
        place.address = place_details["formatted_address"]
        place.phone = place_details["formatted_phone_number"]
        place.rating = place_details["rating"]
        place.latitude = place_details["geometry"]["location"]["lat"]
        place.longitude = place_details["geometry"]["location"]["lng"]

        opening_hours = {}
        for weekday_text in place_details["opening_hours"]["weekday_text"]:
            weekday, opening_hour = weekday_text.split(':', 1)
            opening_hours.update({weekday: opening_hour.strip()})
        place.opening_hours = opening_hours

        return place
    
    def insert_place_in_database(self, place):
        try:
            self.db.session.add(place)
            self.db.session.commit()
        except Exception as e:
            print(f'[ERROR] Database error: {str(e)}')
    
    def get_id_from_city(self, city_name):
        city = self.db.session.query(City).filter_by(name=city_name).first()
        return city.id
    
    def get_id_from_category(self, category_name):
        category = self.db.session.query(Category).filter_by(name=category_name).first()
        return category.id
    
    def check_if_place_already_exist(self, new_place):
        statement = select(Place).where(Place.name == new_place.name)
        result = self.db.session.execute(statement).first()

        if result is None:
            return False
        else:
            return True

class PlacesCrawler(Crawler):
    def __init__(self):
        self.db = Database()
        self.card_wrapper_list_xpath = ".//div[@data-automation='cardWrapper']"
        self.next_page_xpath = "//a[@aria-label='Próxima página']"
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
        self.next_page_xpath = "//a[contains(text(), 'Próximas')]"
        self.categories_xpath = ".//span/div[1]/div[2]/div[2]/div/div[2]/span[1]/span"
        self.categories_dictionary = Config.RESTAURANT_CATEGORIES_DICT
        self.place_name_xpath = ".//span/div[1]/div[2]/div[1]/div/span/a"
        self.place_image_location = ".//span/div[1]/div[1]/span/a/div[2]/div/div[1]/ul/li[1]/div"
        self.image_property = "background-image"
    
    def get_image_from_card(self, card):
        image = ''
        try:
            image = card.find_element_by_xpath(self.place_image_location).value_of_css_property(self.image_property).lstrip('url("').rstrip('")')
        except NoSuchElementException:
            image = ''
        return image
