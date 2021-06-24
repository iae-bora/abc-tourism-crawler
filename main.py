# -*- coding: utf-8 -*-

def get_html_from_url(url):
  #Acessando a URL da página
  response = urlopen(url)

  #Obtendo o HTML da página
  html = response.read().decode('utf-8')
  
  #Fazendo o parse do HTML para permitir a busca das tags
  soup = BeautifulSoup(html, 'html.parser')
  return soup

def get_infos(card, base_url):
    local = {}

    #Obter nome
    local['Nome'] = card.find('div', {'class': '_1gpq3zsA _1zP41Z7X'}).get_text().split('.')[-1].strip()
    #Obter categorias
    local['Categoria'] = card.find('div', {'class': 'DrjyGw-P _26S7gyB4 _3SccQt-T'}).get_text().split(' • ') or []

    #Obter uma imagem
    image = card.find('img')
    local['Imagem'] = image.get('src') if image != None else ''
    # Salvar imagem
    # urlretrieve(image.get('src'), './output/img/' + image.get('alt'))

    #Obter a URL do ponto turístico
    touristic_spot_url = card.find('div', {'class': '_3W_31Rvp _1nUIPWja _1l7Rsl_O _3ksqqIVm _2b3s5IMB'}).find('a').get('href')

    #Obter o HTML dessa página
    soup = get_html_from_url(base_url + touristic_spot_url)    

    #Obter o endereço
    address = soup.find('div', {'class': 'LjCWTZdN'})
    local['Endereço'] = address.get_text() if address != None else ''

    #Obter as categorias da página do local
    category2 = soup.find('div', {'class': '_3RTCF0T0'})
    #Juntar as categorias (nem sempre as categorias são as mesmas na página geral e na página do ponto turístico)
    local['Categoria'] = ', '.join(set(category2.get_text().split(',') + local['Categoria'])) if category2 != None else ', '.join(local['Categoria'])

    return local

def scrape_page(url, base_url):
  spots = []

  #Obtendo o HTML
  soup = get_html_from_url(url)
  
  #Obtendo os cards dos locais
  cards = soup.find_all('div', {'class': 'oQFSuk9j'})

  #Coletando as informações
  for card in cards:
      tourist_spot = get_infos(card, base_url)
      spots.append(tourist_spot)
  
  return spots

# Importando bibliotecas
from urllib.request import urlopen, urlretrieve
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import pandas as pd

tourist_spots = []

cities = {
    'Santo André': 'https://www.tripadvisor.com.br/Attractions-g303624-Activities-Santo_Andre_State_of_Sao_Paulo.html',
    # 'São Bernardo do Campo': 'https://www.tripadvisor.com.br/Attractions-g303626-Activities-a_allAttractions.true-Sao_Bernardo_Do_Campo_State_of_Sao_Paulo.html',
    # 'São Caetano do Sul': 'https://www.tripadvisor.com.br/Attractions-g1162161-Activities-Sao_Caetano_do_Sul_State_of_Sao_Paulo.html',
    # 'Diadema': 'https://www.tripadvisor.com.br/Attractions-g780021-Activities-Diadema_State_of_Sao_Paulo.html',
    # 'Mauá': 'https://www.tripadvisor.com.br/Attractions-g2342768-Activities-Maua_State_of_Sao_Paulo.html',
    # 'Ribeirão Pires': 'https://www.tripadvisor.com.br/Attractions-g2343028-Activities-Ribeirao_Pires_State_of_Sao_Paulo.html',
    # 'Rio Grande da Serra': 'https://www.tripadvisor.com.br/Attractions-g2346575-Activities-Rio_Grande_Da_Serra_State_of_Sao_Paulo.html'
}

#Iterando pelas cidades
for city in cities:
  urls = [cities[city]]

  #Obter URL de base (no caso https://tripadvisor.com.br)
  parsed_uri = urlparse(cities.get(city))
  base_url = '{uri.scheme}://{uri.netloc}/'[:-1].format(uri=parsed_uri)

  #Obter HTML da página da cidade no Tripadvisor
  soup = get_html_from_url(cities.get(city))

  #Obter as páginas para pegar mais resultados (limite de 30 locais por página)
  pages = soup.find_all('a', {'class': '_23XJjgWS _1hF7hP_9 _1XffX-CB'})
  for page in pages:
    urls.append(base_url + page.get('href'))

  #Iterar nas URLs das páginas e guardar em uma lista
  for url in urls:
    tourist_spots.extend(scrape_page(url, base_url))
  
  print(city + ' done')

#Criando um DataFrame com os resultados
dataset = pd.DataFrame(tourist_spots)
dataset
dataset.to_csv('dataset.csv', sep=';', index=False, encoding='utf-8-sig')

