import asyncio
import json
import time
import traceback
from threading import Thread
from fake_useragent import UserAgent
import aiohttp as aiohttp
import requests

fa = UserAgent()





urls = [
    'https://kaspi.kz/shop/p/xiaomi-mi-band-6-global-version-chernyi-101380052/',
    'https://kaspi.kz/shop/p/skmei-m5-chernyi-103113565',
    'https://kaspi.kz/shop/p/honor-band-6-chernyi-101461897',
    'https://kaspi.kz/shop/p/xiaomi-fettian-cotrack1-belyi-102477371',
    'https://kaspi.kz/shop/p/apple-airtag-belyi-4-pack--101701962',
    'https://kaspi.kz/shop/p/samsung-galaxy-smarttag-ei-t5300bbegru-chernyi-101090463',
    'https://kaspi.kz/shop/p/samsung-galaxy-a52-8-256gb-chernyi-101198207',
    'https://kaspi.kz/shop/p/apple-iphone-13-pro-256gb-goluboi-102298652',
    'https://kaspi.kz/shop/p/xiaomi-redmi-note-10s-6-64gb-sinii-101501013',
    'https://kaspi.kz/shop/p/samsung-ue43t5300auxce-109-sm-chernyi-100182013',
    'https://kaspi.kz/shop/p/birjusa-155kx-belyi-2800647',
    'https://kaspi.kz/shop/p/birjusa-305kx-belyi-2800631',
    'https://kaspi.kz/shop/p/jandeks-novaja-stantsija-mini-chernyi-102813865',
    'https://kaspi.kz/shop/p/jandeks-stantsija-mini-yndx-00021-krasnyi-103346930',
    'https://kaspi.kz/shop/p/jandeks-stantsija-maks-s-alisoi-krasnyi-101284433',
    'https://kaspi.kz/shop/p/jandeks-stantsija-lait-birjuzovyi-101808994',
    'https://kaspi.kz/shop/p/smart-balance-transformer-8-space-11900229',
    'https://kaspi.kz/shop/p/smart-balance-wheel-6-5-pirates-chernyi-belyi-11900069',
    'https://kaspi.kz/shop/p/smart-balance-10-fire-krasnyi-sinii-11900380'
]

# proxies = {
#     "http": "http://jQN3TQ:4szonK@186.65.114.22:9173/",
#     "https": "http://jQN3TQ:4szonK@186.65.114.22:9173/",
# }
# proxies = {
#     "http": "http://rYtq9n:hjdPab@46.232.5.3:8000/",
# }

proxies = {
    "http": "http://7AQuMf:oP6uwq@193.124.178.42:8000/",
}

rating = 0


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


async def parse(url_):
    global rating
    params = (
        ('c', '750000000'),
        ('limit', '100'),
        ('page', '0'),
        ('sort', 'asc'),
    )
    try:
        async with aiohttp.ClientSession() as session:
            resp = await session.get(
                url=f'{url_}/offers/',
                headers=header_format(url_),
                params=params,
                proxy=proxies['http']
            )
            data = (await resp.read()).decode('utf-8')
            # print(data)

        offers = json.loads(data)['data']
        print(offers[0])
        e = len(offers)
    except:
        print(traceback.format_exc())
        return False
    else:
        rating += 1


# for i in range(10):
#     thread = Thread(target=parse, args=(,))
loop = asyncio.new_event_loop()


async def async_parse():
    while True:
        for url_ in urls:
            loop.create_task(parse(url_))

        await asyncio.sleep(10)
        print(rating)


for url in urls:
    loop.run_until_complete(async_parse())

# loop.run_until_complete()