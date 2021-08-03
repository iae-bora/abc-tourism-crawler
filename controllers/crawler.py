from selenium.common.exceptions import NoSuchElementException
import time
from .places import get_place_details
from config import Config

MAX_PAGES = 2

def web_scrape_city_pages(url, driver):
    places = []

    driver.get(url)
    check_cookies_banner_exists(driver)

    try:
        for page in range(0, MAX_PAGES):
            time.sleep(Config.SLEEP_INTERVAL)
            card_containers = driver.find_elements_by_xpath(".//div[@data-automation='cardWrapper']")
            places.extend(iterate_cards(card_containers))
            
            time.sleep(Config.SLEEP_INTERVAL)
            driver.find_element_by_xpath("//a[@aria-label='Próxima página']").click()
    except NoSuchElementException:
        print('No more pages found')
    except Exception as e:
        print('Error: ' + str(e))
    
    return places

def check_cookies_banner_exists(driver):
    try:
        time.sleep(Config.SLEEP_INTERVAL)
        driver.find_element_by_xpath("//button[@class='evidon-banner-acceptbutton']").click()
    except:
        print('No cookies banner found')
    return

def iterate_cards(cards):
    places_in_page = []
    for card_index in range(len(cards)):
        tourist_spot = get_information_of_place(cards[card_index])
        if tourist_spot != None:
            places_in_page.append(tourist_spot)
    
    return places_in_page

def get_information_of_place(card):
    place_information = {}

    categories_from_tripadvisor = card.find_element_by_xpath(".//span/div/div/div[2]/div[2]/div[1]/div/div/div[1]").text.split(' • ') or []

    place_information['category'] = ''
    for category_key, categories_variations in Config.CATEGORIES_DICT.items():
        if any(category in ','.join(categories_from_tripadvisor).lower() for category in categories_variations):
            place_information['category'] = category_key
            break
    
    if place_information['category'] == '':
        return None

    place_information['name'] = card.find_element_by_xpath(".//span[@name='title']").text.split('.', 1)[-1].strip()
    try:
        place_information['image'] = card.find_element_by_tag_name('img').get_attribute('src')
    except NoSuchElementException:
        place_information['image'] = ''

    return place_information


# def get_infos(card):
#     local = {}

#     # Obter nome
#     local['name'] = card.find(
#         'div', {'class': '_1gpq3zsA _1zP41Z7X'}).get_text().split('.')[-1].strip()
#     print(local['name'])
#     # Obter categorias
#     local['category'] = card.find(
#         'div', {'class': 'DrjyGw-P _26S7gyB4 _3SccQt-T'}).get_text().split(' • ') or []
#     local['category'] = ','.join(local['category'])

#     # Obter uma imagem
#     image = card.find('img')
#     local['image'] = image.get('src') if image != None else ''
    
#     place_details = get_place_details(local['name'])
#     print(place_details)
#     local.update(place_details)

#     return local
