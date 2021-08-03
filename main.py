from controllers.crawler import web_scrape_city_pages
import pandas as pd
from dotenv import load_dotenv
from config import SeleniumConfig, Config

load_dotenv()

selenium_config = SeleniumConfig()
driver = selenium_config.driver

tourist_spots = []

for city in Config.CITIES_LIST:
    tourist_spots.extend(web_scrape_city_pages(Config.CITIES_LIST[city], driver))

driver.close()

dataset = pd.DataFrame(tourist_spots)
print(dataset)
dataset.to_csv('dataset.csv', sep=';', index=False, encoding='utf-8-sig')
