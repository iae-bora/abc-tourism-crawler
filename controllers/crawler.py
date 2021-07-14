from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

from .places import get_place_details

# def get_base_url(url):
#     parsed_uri = urlparse(cities.get(city))
#     base_url = '{uri.scheme}://{uri.netloc}/'[:-1].format(uri=parsed_uri)
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0'}

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
