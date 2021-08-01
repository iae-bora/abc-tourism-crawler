from controllers.crawler import web_scrape_city_pages
import pandas as pd
from dotenv import load_dotenv
from config.config import SeleniumConfig

load_dotenv()

selenium_config = SeleniumConfig()
driver = selenium_config.driver

tourist_spots = []
cities = {
    'Santo André': 'https://www.tripadvisor.com.br/Attractions-g303624-Activities-Santo_Andre_State_of_Sao_Paulo.html',
    'São Bernardo do Campo': 'https://www.tripadvisor.com.br/Attractions-g303626-Activities-a_allAttractions.true-Sao_Bernardo_Do_Campo_State_of_Sao_Paulo.html',
    'São Caetano do Sul': 'https://www.tripadvisor.com.br/Attractions-g1162161-Activities-Sao_Caetano_do_Sul_State_of_Sao_Paulo.html',
    'Diadema': 'https://www.tripadvisor.com.br/Attractions-g780021-Activities-Diadema_State_of_Sao_Paulo.html',
    'Mauá': 'https://www.tripadvisor.com.br/Attractions-g2342768-Activities-Maua_State_of_Sao_Paulo.html',
    'Ribeirão Pires': 'https://www.tripadvisor.com.br/Attractions-g2343028-Activities-Ribeirao_Pires_State_of_Sao_Paulo.html',
    'Rio Grande da Serra': 'https://www.tripadvisor.com.br/Attractions-g2346575-Activities-Rio_Grande_Da_Serra_State_of_Sao_Paulo.html'
}

for city in cities:
    tourist_spots.extend(web_scrape_city_pages(cities[city], driver))

driver.close()

dataset = pd.DataFrame(tourist_spots)
print(dataset)
dataset.to_csv('dataset.csv', sep=';', index=False, encoding='utf-8-sig')
