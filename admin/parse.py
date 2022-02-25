import asyncio
import json
import traceback
from datetime import datetime
from threading import Thread

import requests
from fake_useragent import UserAgent
import aiohttp as aiohttp
import pandas as pd

from config import delivery_duration
from models import Product, Commission

fa = UserAgent()

proxies = {
    "http": "http://7AQuMf:oP6uwq@193.124.178.42:8000/",
}

month_order = {
    'января': 1,
    'февраля': 2,
    'марта': 3,
    'апреля': 4,
    'мая': 5,
    'июня': 6,
    'июля': 7,
    'августа': 8,
    'сентября': 9,
    'октября': 10,
    'ноября': 11,
    'декабря': 12,
}

month_days = {
    'января': 31,
    'февраля': 28,
    'марта': 31,
    'апреля': 30,
    'мая': 31,
    'июня': 30,
    'июля': 31,
    'августа': 31,
    'сентября': 30,
    'октября': 31,
    'ноября': 30,
    'декабря': 31,
}


def compare_delivery_duration(delivery_date):
    if 'сегодня' in delivery_date or 'завтра' in delivery_date:
        return False
    day, month = delivery_date.split(' ')
    month = month_order[month]
    now = datetime.today()
    if now.month == month:
        if now.day - int(day) == delivery_duration:
            return True
        else:
            return False
    else:
        duration = month_days[now.month] - now.day + day
        if duration == delivery_duration:
            return True
        else:
            return False


def header_format(url_):
    headers = {
        'Connection': 'keep-alive',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
        'Accept': 'application/vnd.api+json',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': fa.random,
        'sec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': f'{url_}/?c=750000000&ref=rec-goods&PageSpeed=noscript',
        'Accept-Language': 'ru-RU,ru;q=0.9,en;q=0.8,es;q=0.7',
    }
    return headers


async def parse_kaspi(url):
    params = (
        ('c', '750000000'),
        ('limit', '100'),
        ('page', '0'),
        ('sort', 'asc'),
    )
    try:
        async with aiohttp.ClientSession() as session:
            url = url.split("/?")[0]
            print(url)
            resp = await session.get(
                url=f'{url}/offers/',
                headers=header_format(url),
                params=params,
                proxy=proxies['http']
            )
            data = (await resp.read()).decode('utf-8')
            # print(data)

        offers = json.loads(data)['data']
        offers_output = []
        for offer in offers:
            price = int(offer['priceFormatted'].replace('₸', '').replace(' ', ''))
            for delivery in offer['deliveryOptions']:
                if delivery['type'] == 'DELIVERY':
                    delivery_price = delivery['price'].replace('₸', '').replace(' ', '')
                    if delivery_price == 'бе��платно' or delivery_price == 'бесплатно':
                        delivery_price = 0
                    else:
                        delivery_price = int(delivery_price)
                    if compare_delivery_duration(delivery['date']):
                        offers_output.append(price + delivery_price)
                        break

        if offers_output:
            return min(offers_output)
        else:
            return False
    except:
        print(traceback.format_exc())
        return False


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
    b = product.supplier1_price - commission.delivery_price
    product.supplier1_margin = int(product.kaspi_price - (product.kaspi_price * (commission.commission / 100)) - b)

    product.supplier1_margin_percent = round(product.supplier1_margin / product.supplier1_price, 2)


async def parse(product: Product, commission, table_dict, db):
    price = await parse_kaspi(product.kaspi_url)
    if not price:
        product.kaspi_price = 0
    else:
        product.supplier1_price = table_dict[product.supplier1_code][0]
        product.supplier1_name = table_dict[product.supplier1_code][3]

        db.session.commit()
        calculate_margin(product, commission)
        db.session.commit()
        print(product)


async def parse_cycle(loop, db):
    while True:
        table_dict = parse_table()
        commission = Commission.query.all()[0]
        products = Product.query.all()
        for product in products:
            loop.create_task(parse(product, commission, table_dict, db))

        while [task for task in asyncio.all_tasks(loop) if not task.done()]:
            await asyncio.sleep(5)

        await asyncio.sleep(300)


def parse_cycle_start(db):
    loop = asyncio.new_event_loop()
    loop.create_task(parse_cycle(loop, db))
    Thread(target=loop.run_forever, args=()).start()
