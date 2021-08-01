import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class PlacesConfig():
    def __init__(self):
        self.categories_dict = {
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

class SeleniumConfig():
    def __init__(self):
        options = Options()
        options.headless = True

        if os.getenv('CRAWLER_ENVIRONMENT') == 'dev':
            self.driver = webdriver.Chrome(os.getenv("CHROME_DRIVER_PATH"), options=options)
        elif os.getenv('CRAWLER_ENVIRONMENT') == 'sandbox':
            self.driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub', options=options, desired_capabilities=DesiredCapabilities.CHROME)
