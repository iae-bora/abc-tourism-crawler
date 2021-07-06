import pandas as pd

from controllers.crawler import get_html_from_url, scrape_page

base_url = 'https://www.tripadvisor.com.br'
tourist_spots = []

cities = {
    # 'Santo André': 'https://www.tripadvisor.com.br/Attractions-g303624-Activities-Santo_Andre_State_of_Sao_Paulo.html',
    'São Bernardo do Campo': 'https://www.tripadvisor.com.br/Attractions-g303626-Activities-a_allAttractions.true-Sao_Bernardo_Do_Campo_State_of_Sao_Paulo.html',
    # 'São Caetano do Sul': 'https://www.tripadvisor.com.br/Attractions-g1162161-Activities-Sao_Caetano_do_Sul_State_of_Sao_Paulo.html',
    # 'Diadema': 'https://www.tripadvisor.com.br/Attractions-g780021-Activities-Diadema_State_of_Sao_Paulo.html',
    # 'Mauá': 'https://www.tripadvisor.com.br/Attractions-g2342768-Activities-Maua_State_of_Sao_Paulo.html',
    # 'Ribeirão Pires': 'https://www.tripadvisor.com.br/Attractions-g2343028-Activities-Ribeirao_Pires_State_of_Sao_Paulo.html',
    # 'Rio Grande da Serra': 'https://www.tripadvisor.com.br/Attractions-g2346575-Activities-Rio_Grande_Da_Serra_State_of_Sao_Paulo.html'
}

for city in cities:
    urls = [cities[city]]

    # Obter HTML da página da cidade no Tripadvisor
    soup = get_html_from_url(cities.get(city))

    # Obter as páginas para pegar mais resultados (limite de 30 locais por página)
    # pages = soup.find(
    #     'div', {'class': '_2SeCgktb'}).find_all('a')

    # for page in pages:
    #     urls.append(base_url + page.get('href'))

    # Iterar nas URLs das páginas e guardar em uma lista
    for url in urls:
        tourist_spots.extend(scrape_page(url, base_url))

    print(city + ' done')

# Criando um DataFrame com os resultados
dataset = pd.DataFrame(tourist_spots)
dataset
dataset.to_csv('dataset.csv', sep=';', index=False, encoding='utf-8-sig')
