import asyncio
import copy
import json
import pprint
import time
import traceback
import pytz
from datetime import datetime, timedelta
from threading import Thread

import requests
import aiohttp as aiohttp
import pandas as pd
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from sqlalchemy.testing import db

from config import HEADERS, COOKIES, month_order, month_days, ERRS_MAX
from models import Product, Proxy


fa = UserAgent()


class Parser(object):
    loop = None
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Parser, cls).__new__(cls)
            cls.instance.table_dict = None
            cls.instance.proxies = None
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
    def compare_delivery_duration_datetime(date, product):
        min_delivery_duration = product.commission.delivery_duration_from
        max_delivery_duration = product.commission.delivery_duration_to
        tz = pytz.timezone('Asia/Almaty')
        now = datetime.now(tz)

        if now.month == date.month:
            if min_delivery_duration <= int(date.day) - now.day <= max_delivery_duration:
                return True
            else:
                return False
        else:
            duration = month_days[now.month] - now.day + int(date.day)
            if min_delivery_duration <= duration <= max_delivery_duration:
                return True
            else:
                return False

    @staticmethod
    def compare_delivery_duration(delivery_date, product):
        min_delivery_duration = product.commission.delivery_duration_from
        max_delivery_duration = product.commission.delivery_duration_to
        if '??????????????' in delivery_date:
            return False
        elif '????????????' in delivery_date:
            if min_delivery_duration <= 1:
                return True
            else:
                return False
        day, month = delivery_date.split(' ')
        month = month_order[month]
        tz = pytz.timezone('Asia/Almaty')
        now = datetime.now(tz)

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
    async def request_kaspi(cls, url, proxy):
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
            offers = json.loads(data)['offers']
            print(data)
            return offers

    # @classmethod
    async def parse_kaspi(self, url, product, proxy: Proxy, db):
        try:
            try:
                offers = await self.request_kaspi(url, proxy)
            except Exception as e:
                print('proxy_err: ', e)
                proxy.status = 'WAIT'
                db.session.commit()

                Parser.loop.create_task(self.wait_proxy(proxy, db))
                self.products.append(product)
                return False
            # except ZeroDivisionError:
            #     proxy.status = 'EXPIRED'
            #     db.session.commit()
            #     return False

            offers_output = []
            for offer in offers:
                price = int(offer['price'])
                delivery = offer.get('delivery')
                if delivery:
                    delivery = delivery.split('.')[0]
                    date = datetime.strptime(delivery, '%Y-%m-%dT%H:%M:%S')
                    date = date + timedelta(hours=6)
                    if self.compare_delivery_duration_datetime(date, product):
                        offers_output.append(price)
                        break

            if offers_output:
                return min(offers_output)
            else:
                self.products.append(product)
                return False
        except:
            self.products.append(product)
            print(traceback.format_exc())
            return False

    @staticmethod
    def calculate_margin(product: Product, commission, db, i):

        b = getattr(product, f'supplier{i}_price') + commission.delivery_price
        setattr(product, f'supplier{i}_margin', round(
            product.kaspi_price - (product.kaspi_price * (commission.commission / 100)) - b, 2))

        setattr(product, f'supplier{i}_margin_percent', round(getattr(product, f'supplier{i}_margin') / product.kaspi_price, 4) * 100)
        db.session.commit()

    async def parse_prod(self, product: Product, commission, db, proxy: Proxy):
        self.proxies.remove(proxy)
        url = product.kaspi_url.replace('\t', '')
        price = await self.parse_kaspi(url, product, proxy, db)
        await asyncio.sleep(0.3)
        if not price:
            if self.errors.get(product):
                self.errors[product] += 1
            else:
                self.errors[product] = 1
            product.kaspi_price = 0
        else:
            product.kaspi_price = price
            for i in range(1, 11):
                code = getattr(product, f'supplier{i}_code')
                if not code:
                    continue
                row = self.table_dict[code]
                setattr(product, f'supplier{i}_name', row[3])
                setattr(product, f'supplier{i}_amount', row[1])
                setattr(product, f'supplier{i}_price', row[0])

                db.session.commit()
                self.calculate_margin(product, commission, db, i)

        db.session.commit()
        print(product)
        self.proxies.append(proxy)

    async def parse(self, loop, db):
        while True:
            try:
                self.parse_table()
                products = Product.query.all()
                proxies = Proxy.query.filter_by(status='OK').all()
                self.proxies = proxies
                self.products = products
                self.errors = {}

                i = 0

                while self.products and len([task for task in asyncio.all_tasks(loop) if not task.done()]) > i:
                    if i == 0:
                        i = 1
                    product = self.products[0]
                    print(product)
                    self.products.remove(product)
                    if self.errors.get(product):
                        if self.errors.get(product) > ERRS_MAX:
                            continue

                    commission = product.commission
                    while True:
                        try:
                            loop.create_task(self.parse_prod(product, commission, db, self.proxies[-1]))
                        except IndexError:
                            await asyncio.sleep(2)
                        else:
                            break
                    await asyncio.sleep(5)

                await asyncio.sleep(300)
            except Exception as e:
                print(traceback.format_exc())
                await asyncio.sleep(100)

    def start_parse(self, db):
        loop = asyncio.new_event_loop()
        Parser.loop = loop
        loop.create_task(self.parse(loop, db))
        Thread(target=loop.run_forever, args=()).start()

    async def wait_proxy(self, proxy: Proxy, db):
        await asyncio.sleep(30)
        proxy.status = 'OK'
        db.session.commit()
        self.proxies.append(proxy)
