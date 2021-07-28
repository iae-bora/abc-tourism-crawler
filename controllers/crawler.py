from urllib.request import urlopen, Request
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import time

from .places import get_place_details

MAX_PAGES = 2

def web_scrape_city(url, driver):
    spots = []
    driver.get(url)
    check_cookies_banner_exists(driver)

    try:
        for page in range(0, MAX_PAGES):
            time.sleep(2)
            print('Page')
            card_containers = driver.find_elements_by_xpath(".//div[@data-automation='cardWrapper']")

            # card_container = driver.find_elements_by_xpath("//div[@data-automation='cardWrapper']")
            # for i in range(len(card_container)):
            #     print(i)

            for card_index in range(len(card_containers)):
                tourist_spot = get_place_information(card_containers[card_index])
                spots.append(tourist_spot)
            
            time.sleep(2)
            driver.find_element_by_xpath("//a[@aria-label='Próxima página']").click()
    except NoSuchElementException:
        print('No more pages found')
    except Exception as e:
        print('Error ' + e)
    return spots

def check_cookies_banner_exists(driver):
    time.sleep(3)
    try:
        driver.find_element_by_xpath("//button[@class='evidon-banner-acceptbutton']").click()
    except:
        print('No cookies banner found')
    return

def get_place_information(card):
    local = {}

    # Obter nome
    local['name'] = card.find_element_by_xpath(".//span[@name='title']").text.split('.')[-1].strip()
    print(local['name'])
    # Obter categorias
    # local['category'] = card.find(
    #     'div', {'class': 'DrjyGw-P _26S7gyB4 _3SccQt-T'}).get_text().split(' • ') or []
    # local['category'] = ','.join(local['category'])

    # # Obter uma imagem
    # image = card.find('img')
    # local['image'] = image.get('src') if image != None else ''

    return local

def get_html_from_url(url):
    # Acessando a URL da página
    req = Request(url, headers=headers)
    print(req)
    response = urlopen(req)
    print(response)
    # Obtendo o HTML da página
    html = response.read().decode('utf-8')
    # Fazendo o parse do HTML para permitir a busca das tags
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def get_infos(card):
    local = {}

    # Obter nome
    local['name'] = card.find(
        'div', {'class': '_1gpq3zsA _1zP41Z7X'}).get_text().split('.')[-1].strip()
    print(local['name'])
    # Obter categorias
    local['category'] = card.find(
        'div', {'class': 'DrjyGw-P _26S7gyB4 _3SccQt-T'}).get_text().split(' • ') or []
    local['category'] = ','.join(local['category'])

    # Obter uma imagem
    image = card.find('img')
    local['image'] = image.get('src') if image != None else ''
    
    place_details = get_place_details(local['name'])
    print(place_details)
    local.update(place_details)

    return local


def scrape_page(url, base_url):
    spots = []
    soup = get_html_from_url(url)

    cards = soup.find_all('div', {'class': 'oQFSuk9j'})

    for card in cards:
        tourist_spot = get_infos(card)
        spots.append(tourist_spot)

    return spots
