import requests
import re
from bs4 import BeautifulSoup
import json
from fake_headers import Headers
from areas import get_areas_id

def get_headers():
    return Headers(browser='chrome', os='win').generate()

params = {
    'page': 1,
    'text': 'python',
    'area': get_areas_id()
}
response = requests.get('https://api.hh.ru/vacancies', headers=get_headers(), params=params)
data = response.json()

vacancies_list = []
for vacancy in data['items']:
    vacancy_dict = {}
    vacancy_dict['name'] = vacancy['name']
    vacancy_dict['url'] = vacancy['alternate_url']
    salary_info = vacancy['salary']
    if salary_info is not None:
        if salary_info['from'] is not None and salary_info['to'] is not None:
            vacancy_dict['salary'] = f'{salary_info['from']} - {salary_info['to']} {salary_info['currency']}'
        elif salary_info['from'] is None:
            vacancy_dict['salary'] = f'{salary_info['to']} {salary_info['currency']}'
        elif salary_info['to'] is None:
            vacancy_dict['from'] = f'{salary_info['from']} {salary_info['currency']}'
    else:
        vacancy_dict['salary'] = 'Зарплата не указана'
    vacancy_dict['employer'] = vacancy['employer']['name']
    vacancy_dict['city'] = vacancy['area']['name']
    vacancies_list.append(vacancy_dict)

result_list = []
for item in vacancies_list:
    r = requests.get(item['url'], headers=get_headers())
    soup = BeautifulSoup(r.text, features='lxml')
    attrs = {
        'data-qa': 'vacancy-description'
    }
    discrp = soup.find('div', class_='g-user-content', attrs=attrs)
    if discrp is None:
        attrs = {
            'itemprop': 'description', 
            'data-qa': 'vacancy-description'
        }
        discrp = soup.find('div', class_='vacancy-branded-user-content', attrs=attrs)
    reg_exp = r'Djungo|Flask'
    check = re.search(reg_exp, discrp.text, flags=re.I)
    if check != None:
        result_list.append(item)

with open('vacancies.json', 'w', encoding='utf-8') as f:
    json.dump(result_list, f)

