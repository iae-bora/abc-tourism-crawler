from controllers.crawler import PlacesCrawler, RestaurantCrawler
import pandas as pd
from dotenv import load_dotenv
from config import SeleniumConfig, Config

load_dotenv()

selenium_config = SeleniumConfig()
driver = selenium_config.driver

places_crawler = PlacesCrawler()
restaurant_crawler = RestaurantCrawler()

places = []

for city in Config.CITIES_LIST:
    places.extend(places_crawler.web_scrape_pages(Config.CITIES_LIST[city], driver))

for city in Config.CITY_RESTAURANTS_LIST:
    places.extend(restaurant_crawler.web_scrape_pages(Config.CITY_RESTAURANTS_LIST[city], driver))

driver.close()

dataset = pd.DataFrame(places)
dataset.drop_duplicates(subset=['name'], inplace=True)
print(dataset)
dataset.to_csv('dataset.csv', sep=';', index=False, encoding='utf-8-sig')
