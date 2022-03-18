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
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from sqlalchemy.testing import db

from config import HEADERS, COOKIES, month_order, month_days
from models import Product, Commission, Proxy


fa = UserAgent()


class Parser(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Parser, cls).__new__(cls)
            cls.instance.table_dict = None
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

    def parse_table(self):
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

        self.table_dict = table_dict

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

    @staticmethod
    def get_city_and_prod(url):
        city = url.split('c=')[1].split('&')[0]
        prod = url.split('/?')[0].split('-')[-1]
        return city, prod

    @classmethod
    async def _request_kaspi(cls, url, proxy: Proxy):
        url = cls.format_url(url)
        async with aiohttp.ClientSession(cookies=COOKIES) as session:
            resp = await session.get(
                url=url,
                headers=cls.format_headers(url),
                proxy=str(proxy)
            )
            data = (await resp.read()).decode('utf-8')
            return data

    @classmethod
    async def request_kaspi(cls, url, proxy: Proxy):
        city, prod = cls.get_city_and_prod(url)
        data = f'"cityId":"{city}","id":"{prod}","limit":64,"page":0,"sort":true'
        data = '{' + data + '}'
        async with aiohttp.ClientSession() as session:
            resp = await session.post(
                url=f'https://kaspi.kz/yml/offer-view/offers/{prod}',
                headers=cls.format_headers(url),
                data=data,
                proxy=str(proxy)
            )
            data = (await resp.read()).decode('utf-8')
            print(data)
            return data

    @classmethod
    async def parse_kaspi(cls, url, product, proxy: Proxy):
        try:
            try:
                data = cls.request_kaspi(url, proxy)
            except ImportError:
                proxy.status = 'WAIT'
                db.session.commit()
                await cls.wait_proxy(proxy)
            except:
                proxy.status = 'EXPIRED'
                db.session.commit()

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
                        if cls.compare_delivery_duration(delivery['date'], product):
                            offers_output.append(price)
                            break

            if offers_output:
                return min(offers_output)
            else:
                return False
        except:
            print(traceback.format_exc())
            return False

    @staticmethod
    def calculate_margin(product: Product, commission):
        b = product.supplier1_price + commission.delivery_price
        product.supplier1_margin = round(
            product.kaspi_price - (product.kaspi_price * (commission.commission / 100)) - b, 2)
        product.supplier1_margin_percent = round(product.supplier1_margin / product.kaspi_price, 4) * 100
        db.session.commit()

    async def parse_prod(self, product: Product, commission, db, proxy: Proxy):
        price = await self.parse_kaspi(product.kaspi_url, product, proxy)
        if not price:
            product.kaspi_price = 0
        else:
            product.kaspi_price = price
            for i in range(1, 11):
                setattr(product, f'supplier{i}_name', self.table_dict[product.supplier1_code][3])
                setattr(product, f'supplier{i}_amount', self.table_dict[product.supplier1_code][1])
                setattr(product, f'supplier{i}_price', self.table_dict[product.supplier1_code][0])

            db.session.commit()
            self.calculate_margin(product, commission)
        db.session.commit()
        print(product)

    async def parse(self, loop, db):
        while True:
            self.parse_table()
            products = Product.query.all()
            proxies = Proxy.query.filter_by(status='OK')
            i = 0
            for product in products:
                commission = product.commission
                loop.create_task(self.parse_prod(product, commission, db, proxies[i]))
                i += 1
                if i == len(proxies):
                    i = 0

            while len([task for task in asyncio.all_tasks(loop) if not task.done()]) > 1:
                await asyncio.sleep(5)

            await asyncio.sleep(300)

    def start_parse(self):
        loop = asyncio.new_event_loop()
        loop.create_task(self.parse(loop, db))
        Thread(target=loop.run_forever, args=()).start()

    @staticmethod
    async def wait_proxy(proxy: Proxy):
        await asyncio.sleep(20)
        proxy.status = 'OK'
        db.session.commit()