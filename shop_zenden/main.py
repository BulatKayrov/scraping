import json
from time import sleep

import requests
from bs4 import BeautifulSoup
from fake_headers import Headers


def get_detail_product(product_link, headers) -> dict:
    """
    Детальная информация о товаре
    """
    res = requests.get(url=product_link, headers=headers)

    obj_soup = BeautifulSoup(res.text, 'lxml')

    detail_info = (
        obj_soup.
        find('div', class_='product-info__main').
        find(class_='product-info__summary')
    )

    clean_data = {}
    for _ in detail_info:
        if _.text.split():
            clean_data.update({_.find('th').text: str(_.find('td').text.split()[0])})

    return clean_data


def get_data() -> None:
    """
    Функция сбора информации о мужской обуви с сайта zenden.ru.
    Полученные данные записывает в json
    :return: None
    """
    PAGE: int = 22
    ALL_PRODUCTS = []
    DOMAIN_NAME: str = 'https://zenden.ru'

    headers = Headers(browser="firefox", headers=True).generate()
    count = 0
    obj_count = 0

    for per_page in enumerate(range(1, PAGE + 1)):

        url = f'{DOMAIN_NAME}/catalog/men/?nav=page-{per_page[1]}'

        response = requests.get(url=url, headers=headers).text

        soup = BeautifulSoup(response, 'lxml')

        products = (
            soup.
            find('div', class_='products-list__main js-list-view').
            find_all('div', class_='products-list__item product-card product-card-new js-product-card js-reveal')
        )

        for product in products:
            obj_count += 1
            article = product.find('div', class_='product-card__article js-productArticle').text
            title = product.find('div', class_='product-card__title js-productTitle').find('a').text
            image_link = product.find('img').get('data-src')
            old_price = (' '.join(product.
                         find('div', class_='product-card__price product-price product-price_size_m').
                         find('del').text.split()[:2]))
            new_price = (' '.join(product.find('span').text.split()[:2]))
            size = (
                product.
                find('div', class_='product-card__sizes js-productSizes').text.split()
            )
            link = f"{DOMAIN_NAME}{product.find('a', class_='product-card__image link').get('href')}"
            details = get_detail_product(product_link=link, headers=headers)
            print(f'Данные о #{obj_count}-ом товаре собраны')
            ALL_PRODUCTS.append(
                {
                    'Article': article,
                    'Title': title,
                    'Image link': image_link,
                    'Old price': old_price,
                    'New price': new_price,
                    'size': size,
                    'detail_info': details
                }
            )
        # sleep(2)
        # count += 1
        # print('-' * 100)
        # print(f'Все данные собраны с #{per_page[0]}-ой странице')
        # print('-' * 100)
        print(f'Обработана {per_page[0]}-ая страница')

    # with open('zenden_v2.json', 'w', encoding='utf-8') as file:
    with open('zenden_v3.json', 'w', encoding='utf-8') as file:
        json.dump(ALL_PRODUCTS, file, ensure_ascii=False, indent=4)


def main():
    get_data()


if __name__ == '__main__':
    main()
