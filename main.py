from controllers.crawler import PlacesCrawler, RestaurantCrawler
import pandas as pd
from dotenv import load_dotenv
from config import SeleniumConfig, Config

load_dotenv()

selenium_config = SeleniumConfig()
driver = selenium_config.driver

places_crawler = PlacesCrawler()
restaurant_crawler = RestaurantCrawler()

for city in Config.CITIES_LIST:
    places_crawler.web_scrape_pages(city, Config.CITIES_LIST[city], driver)

for city in Config.CITY_RESTAURANTS_LIST:
    restaurant_crawler.web_scrape_pages(city, Config.CITY_RESTAURANTS_LIST[city], driver)

driver.close()
