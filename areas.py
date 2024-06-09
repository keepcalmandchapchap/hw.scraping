import requests
from fake_headers import Headers

def get_headers():
    return Headers(browser='chrome', os='win').generate()

def get_areas_id():
    params = {
        'locale': 'RU',
        'host': 'hh.ru'
    }

    response = requests.get('https://api.hh.ru/areas', params=params, headers=get_headers())

    areas = response.json()

    areas_id = []

    for item in areas[0]['areas']:
        if item['name'] == 'Москва':
            areas_id.append(item['id'])
        elif item['name'] == 'Санкт-Петербург':
            areas_id.append(item['id'])

    return areas_id


