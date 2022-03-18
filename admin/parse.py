import asyncio
import copy
import json
import pprint
import time
import traceback
from datetime import datetime
from threading import Thread

import requests
import aiohttp as aiohttp
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from config import HEADERS, COOKIES, month_order, month_days
from models import Product, Commission, Proxy


class Parser(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Parser, cls).__new__(cls)
        return cls.instance

    @staticmethod
    def get_cookies(proxy: Proxy):
        cookies_output = {}

        options = Options()
        # options.headless = True
        driver = webdriver.Firefox(
            options=options
        )

        driver.get('https://kaspi.kz/shop/p/samsung-galaxy-a52-8-256gb-chernyi-101198207/?at=1&c=750000000')
        time.sleep(2)

        driver.find_element('xpath', '//a[@data-city-id="750000000"]').click()
        time.sleep(5)

        cookies = driver.get_cookies()
        for cookie in cookies:
            cookies_output[cookie['name']] = cookie['value']

        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(cookies_output)

    @staticmethod
    def compare_delivery_duration(delivery_date, product):
        min_delivery_duration = product.commission.delivery_duration_from
        max_delivery_duration = product.commission.delivery_duration_to
        if 'сегодня' in delivery_date:
            return False
        elif 'завтра' in delivery_date:
            if min_delivery_duration <= 1:
                return True
            else:
                return False
        day, month = delivery_date.split(' ')
        month = month_order[month]
        now = datetime.today()

        if now.month == month:
            if min_delivery_duration <= int(day) - now.day <= max_delivery_duration:
                return True
            else:
                return False
        else:
            duration = month_days[now.month] - now.day + int(day)
            if min_delivery_duration <= duration <= max_delivery_duration:
                return True
            else:
                return False

    @staticmethod
    def format_headers(url):
        headers = copy.deepcopy(HEADERS)
        headers['Referer'] = url + '&ref=rec-goods'
        return headers

    @staticmethod
    def format_url(url):
        url1, url2 = url.split('&')[0].split('?')
        url = url1 + 'offers/?' + url2 + '&limit=100&page=0'
        return url

    @classmethod
    async def request_kaspi(cls, url, proxy: Proxy):
        async with aiohttp.ClientSession(cookies=COOKIES) as session:
            resp = await session.get(
                url=f'https://kaspi.kz/shop/p/samsung-galaxy-a52-8-256gb-chernyi-101198207/offers/',
                headers=cls.format_headers(url),
                proxy=str(proxy)
            )
            data = (await resp.read()).decode('utf-8')
            return data

    @classmethod
    async def parse_kaspi(cls, url, product, proxy: Proxy):
        try:
            try:
                data = cls.request_kaspi(url)
            except:
                pass
            offers = json.loads(data)['data']
            offers_output = []
            for offer in offers:
                price = int(offer['priceFormatted'].replace('₸', '').replace(' ', ''))
                for delivery in offer['deliveryOptions']:
                    if delivery['type'] == 'DELIVERY':
                        delivery_price = delivery['price'].replace('₸', '').replace(' ', '')
                        # if delivery_price == 'бе��платно' or delivery_price == 'бесплатно':
                        #     delivery_price = 0
                        # else:
                        #     delivery_price = int(delivery_price)
                        if compare_delivery_duration(delivery['date'], product):
                            offers_output.append(price)
                            break

            if offers_output:
                return min(offers_output)
            else:
                return False
        except:
            print(traceback.format_exc())
            return False

    def parse(self):
        pass







def parse_table():
    file_source = requests.get(
        'https://ru.pricedata.com/datafeed/1X/inc_trendo.xlsx',
        headers={'User-Agent': fa.random}
    ).content

    with open('inc_trendo.xlsx', 'wb') as f:
        f.write(file_source)

    df = pd.read_excel('inc_trendo.xlsx')
    df.to_csv("table.csv", index=None, header=False, sep=';', na_rep='-')
    table_dict = {}
    with open('table.csv', 'r', encoding='utf-8') as f:
        for row in f:
            row = row.split(';')
            table_dict[row[0]] = (row[1], row[2], row[3], row[4])
    return table_dict


def calculate_margin(product: Product, commission):
    b = product.supplier1_price + commission.delivery_price
    product.supplier1_margin = round(product.kaspi_price - (product.kaspi_price * (commission.commission / 100)) - b, 2)

    product.supplier1_margin_percent = round(product.supplier1_margin / product.kaspi_price, 4) * 100


async def parse(product: Product, commission, table_dict, db):
    price = await parse_kaspi(product.kaspi_url, product)
    if not price:
        product.kaspi_price = 0
    else:
        product.kaspi_price = price
        for i in range (1, 11):
            # setattr(product, 'supplier1_name', table_dict[product.supplier1_code][0])
            # setattr(product, 'supplier1_name') = table_dict[product.supplier1_code][0]
            product.supplier1_name = table_dict[product.supplier1_code][3]

        db.session.commit()
        calculate_margin(product, commission)
    db.session.commit()
    print(product)


async def parse_cycle(loop, db):
    while True:
        table_dict = parse_table()
        products = Product.query.all()
        for product in products:
            commission = product.commission
            loop.create_task(parse(product, commission, table_dict, db))

        while len([task for task in asyncio.all_tasks(loop) if not task.done()]) > 1:
            await asyncio.sleep(5)

        await asyncio.sleep(300)


def parse_cycle_start(db):
    loop = asyncio.new_event_loop()
    loop.create_task(parse_cycle(loop, db))
    Thread(target=loop.run_forever, args=()).start()


p = Parser()
print(p)
p.get_cookies(Proxy)