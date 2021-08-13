from selenium.common.exceptions import NoSuchElementException
import time
from models.place import Place
from .places import get_place_details
from config import Config
from database.db import Database

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
    
    def web_scrape_pages(self, url, driver):
        places = []

        driver.get(url)
        self.check_cookies_banner_exists(driver)

        try:
            for page in range(0, Config.MAX_PAGES_PER_CITY):
                time.sleep(Config.SLEEP_INTERVAL)
                card_wrapper_list = driver.find_elements_by_xpath(self.card_wrapper_list_xpath)
                places.extend(self.iterate_cards(card_wrapper_list))
                
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

    def iterate_cards(self, cards):
        places_in_page = []
        for card_index in range(len(cards)):
            place = self.get_information_of_place(cards[card_index])
            if place != None:
                places_in_page.append(place)
                self.insert_place_in_database(place)
        
        return places_in_page

    def get_information_of_place(self, card):
        place_information = {}

        categories_from_tripadvisor = card.find_element_by_xpath(self.categories_xpath).text.split(' • ') or []

        place_information['category'] = ''
        for category_key, categories_variations in self.categories_dictionary.items():
            if any(category in ','.join(categories_from_tripadvisor).lower() for category in categories_variations):
                place_information['category'] = category_key
                break
        
        if place_information['category'] == '':
            return None

        place_information['name'] = card.find_element_by_xpath(self.place_name_xpath).text.split('.', 1)[-1].strip()
        place_information['image'] = self.get_image_from_card(card)

        # place_details = get_place_details(place_information['name'])
        # place_information.update(place_details)

        place = Place()
        place.name = place_information['name']
        place.category = place_information['category']
        place.image = place_information['image']

        return place
    
    def insert_place_in_database(self, place):
        self.db.session.add(place)
        self.db.session.commit()

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
