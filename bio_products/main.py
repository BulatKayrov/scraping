import requests
import json
from bs4 import BeautifulSoup
from fake_headers import Headers
import lxml
import time

# Парсер данных БАДов с сайта аптеки

headers = Headers(
        browser="firefox",
        headers=True
    ).generate()

domain_name = 'https://fitosila.ru'
page = 12
all_bio_products = []

for per_page in range(1, page + 1):
    url = f'{domain_name}/catalog/biologiceski-aktivnye-dobavki?page={per_page}'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    products = (
        soup.
        find('div', class_="row gutters catalog-view-grid").
        find_all('div', class_="item col col-4 col-lg-3 col-sm-6 attributes")
    )

    for item in products:
        article = item.find('span', class_="strong article").text.split()
        title = item.find('div', class_="head").find('a').text
        image = domain_name + item.find('div', class_="image").find('img').get('src')
        price = item.find('div', class_="col col-7 small strong").find_next('span').text
        count = item.find('div', class_="col col-12").find_next('span').text.split()[0]
        all_bio_products.append(
            {
                'article': {
                    article[1]: {
                        'title': title,
                        'image_link': image,
                        'price': price,
                        'count': count
                    }
                }
            }
        )
    time.sleep(2)
    left_page = page - per_page
    print(f'Обработана {per_page} страница, осталось {left_page}')

with open('all_bio_products.json', 'w', encoding='utf-8') as file:
    json.dump(all_bio_products, file, ensure_ascii=False, indent=4)







