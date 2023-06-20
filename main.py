import requests
from bs4 import BeautifulSoup
import json

url = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

vacancy_items = soup.find_all(class_='vacancy-serp-item')

results = []

for item in vacancy_items:
    link = item.find(class_='bloko-link HH-LinkModifier').get('href')

    company = item.find(class_='vacancy-serp-item__meta-info-company').text.strip()

    city = item.find(class_='vacancy-serp-item__meta-info').find_all('span')[-1].text.strip()

    salary = item.find(class_='vacancy-serp-item__compensation')

    if salary is not None:
        salary = salary.text.strip()
    else:
        salary = 'Зарплата не указана'

    description = item.find(class_='vacancy-serp-item__snippet').text.lower()
    if 'django' in description and 'flask' in description:
        vacancy_info = {
            'link': link,
            'salary': salary,
            'company': company,
            'city': city
        }
        results.append(vacancy_info)

with open('vac.json', 'w') as file:
    json.dump(results, file, ensure_ascii=False, indent=4)

print('Парсинг завершен. Результаты сохранены в файле vac.json.')