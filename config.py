import os
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class Config:
    SLEEP_INTERVAL = os.getenv('SLEEP_INTERVAL', 5)

    MAX_PAGES_PER_CITY = os.getenv('MAX_PAGES_PER_CITY', 1)

    CATEGORIES_DICT = {
        'Parque': ['parque', 'parques de diversões', 'ar livre', 'bonde', 'natureza', 'trilha'],
        'Museu': ['museus', 'locais históricos', 'arte', 'religioso', 'igreja'],
        'Cinema': ['cinema'],
        'Shopping': ['shopping', 'lojas especializadas', 'outlet', 'calçadões'],
        'Bar': ['bar', 'bares', 'cervejarias', 'balada'],
        'Restaurante': ['restaurante', 'feira'],
        'Show': ['show'],
        'Biblioteca': ['biblioteca'],
        'Estádio': ['estádio', 'arenas', 'esportivo'],
        'Jogos': ['jogos', 'boliche', 'entretenimento', 'stand de tiro'],
        'Teatro': ['teatro']
    }

    RESTAURANT_CATEGORIES_DICT = {
        'Churrasco': ['churrasco', 'steakhouse', 'argentina', 'grelhado'],
        'Japonesa': ['japonesa', 'sushi'],
        'Italiana': ['italiana', 'pizza'],
        'FastFood': ['fast food', 'lanchonete', 'americana'],
        'Vegetariana': ['vegetariana', 'saudável'],
        'Bar': ['bar', 'pub', 'wine bar'],
        'Outros': ['mexicana', 'francesa', 'frutos do mar', 'árabe', 'libanesa'],
        'Caseira': ['caseira', 'brasileira']
    }

    CITIES_LIST = {
        'Santo André': 'https://www.tripadvisor.com.br/Attractions-g303624-Activities-Santo_Andre_State_of_Sao_Paulo.html',
        'São Bernardo do Campo': 'https://www.tripadvisor.com.br/Attractions-g303626-Activities-a_allAttractions.true-Sao_Bernardo_Do_Campo_State_of_Sao_Paulo.html',
        'São Caetano do Sul': 'https://www.tripadvisor.com.br/Attractions-g1162161-Activities-Sao_Caetano_do_Sul_State_of_Sao_Paulo.html',
        'Diadema': 'https://www.tripadvisor.com.br/Attractions-g780021-Activities-Diadema_State_of_Sao_Paulo.html',
        'Mauá': 'https://www.tripadvisor.com.br/Attractions-g2342768-Activities-Maua_State_of_Sao_Paulo.html',
        'Ribeirão Pires': 'https://www.tripadvisor.com.br/Attractions-g2343028-Activities-Ribeirao_Pires_State_of_Sao_Paulo.html',
        'Rio Grande da Serra': 'https://www.tripadvisor.com.br/Attractions-g2346575-Activities-Rio_Grande_Da_Serra_State_of_Sao_Paulo.html'
    }

    CITY_RESTAURANTS_LIST = {
        'Santo André': 'https://www.tripadvisor.com.br/Restaurants-g303624-Santo_Andre_State_of_Sao_Paulo.html',
        'São Bernardo do Campo': 'https://www.tripadvisor.com.br/Restaurants-g303626-Sao_Bernardo_Do_Campo_State_of_Sao_Paulo.html',
        'São Caetano do Sul': 'https://www.tripadvisor.com.br/Restaurants-g1162161-Sao_Caetano_do_Sul_State_of_Sao_Paulo.html',
        'Diadema': 'https://www.tripadvisor.com.br/Restaurants-g780021-Diadema_State_of_Sao_Paulo.html',
        'Mauá': 'https://www.tripadvisor.com.br/Restaurants-g2342768-Maua_State_of_Sao_Paulo.html',
        'Ribeirão Pires': 'https://www.tripadvisor.com.br/Restaurants-g2343028-Ribeirao_Pires_State_of_Sao_Paulo.html',
        'Rio Grande da Serra': 'https://www.tripadvisor.com.br/Restaurants-g2346575-Rio_Grande_Da_Serra_State_of_Sao_Paulo.html'
    }

class SeleniumConfig():
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')

        if os.getenv('CRAWLER_ENVIRONMENT') == 'dev':
            self.driver = webdriver.Chrome(os.getenv("CHROME_DRIVER_PATH"), chrome_options=chrome_options)
        elif os.getenv('CRAWLER_ENVIRONMENT') == 'sandbox':
            self.driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub', chrome_options=chrome_options, desired_capabilities=DesiredCapabilities.CHROME)
        elif os.getenv('CRAWLER_ENVIRONMENT') == 'production':
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.binary_location = os.getenv("GOOGLE_CHROME_BIN")

            self.driver = webdriver.Chrome(executable_path=os.getenv("CHROME_DRIVER_PATH"), chrome_options=chrome_options)
