import asyncio

import aiohttp
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0',
    'Accept': 'application/json, text/*',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://kaspi.kz/shop/p/samsung-galaxy-a52-8-256gb-chernyi-101198207/?c=750000000',
    'Content-Type': 'application/json; charset=utf-8',
    'Origin': 'https://kaspi.kz',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
}

data = '{"cityId":"750000000","id":"101198207","limit":64,"page":0,"sort":true}'

response = requests.post('https://kaspi.kz/yml/offer-view/offers/101198207', headers=headers, data=data)


async def ap(data):
    async with aiohttp.ClientSession() as session:
        resp = await session.post(
            url=f'https://kaspi.kz/yml/offer-view/offers/101198207',
            headers=headers,
            data=data
            # proxy=str(proxy)
        )
        data = (await resp.read()).decode('utf-8')
        print(data)


asyncio.run(ap(data))


# print(response.content)