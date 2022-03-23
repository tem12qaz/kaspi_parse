import asyncio

import aiohttp
import requests

from parse import Parser

cookies = {
    'ks.ngs.s': '9ad2ab19b88142d90362073b150e9cc2',
    'k_stat': '200338b6-5e12-4e37-8881-417e4815fbd0',
    'ks.tg': '72',
    'ssaid': 'eb5306c0-a944-11ec-b937-6fbde8700606',
    '_hjSessionUser_283363': 'eyJpZCI6ImY4ZmIxZmViLWU3MmQtNWYzMy04YTQ2LTg1NzViZGEzYTdiNyIsImNyZWF0ZWQiOjE2NDc4ODc0MDIwNDUsImV4aXN0aW5nIjp0cnVlfQ==',
    '_hjFirstSeen': '1',
    '_hjIncludedInSessionSample': '0',
    '_hjSession_283363': 'eyJpZCI6IjgyM2E1ZjZlLWNlYjgtNDU4Yi04YWVkLTA5MDhkYTQwZTFlZSIsImNyZWF0ZWQiOjE2NDc4ODc0MDIwNDgsImluU2FtcGxlIjpmYWxzZX0=',
    '_hjAbsoluteSessionInProgress': '0',
    '_ga': 'GA1.2.420676541.1647887402',
    '_gid': 'GA1.2.1614969253.1647887402',
    '_ym_uid': '16478874021015833236',
    '_ym_d': '1647887402',
    '_fbp': 'fb.1.1647887402484.1816566389',
    '_ym_visorc': 'b',
    '_ym_isad': '2',
    'kaspi.storefront.cookie.city': '750000000',
    'ks.cc': '-1',
    '_ALGOLIA': 'anonymous-05d309c6-ebd9-483c-82c0-43ef03401012',
    '__tld__': 'null',
    '_gat_ddl': '1',
}
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0',
    'Accept': 'application/json, text/*',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://kaspi.kz/shop/p/xiaomi-dreame-d9-belyi-100987780/?at=2&c=750000000&ref=rec-goods',
    'Content-Type': 'application/json; charset=utf-8',
    'Origin': 'https://kaspi.kz',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0',
    'Accept': 'application/json, text/*',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/json; charset=utf-8',
    'Origin': 'https://kaspi.kz',
    'Connection': 'keep-alive',
    'Referer': 'https://kaspi.kz/shop/p/xiaomi-dreame-d9-belyi-100987780/?at=2&c=750000000',
    # Requests sorts cookies= alphabetically
    # 'Cookie': 'ks.ngs.s=9ad2ab19b88142d90362073b150e9cc2; k_stat=200338b6-5e12-4e37-8881-417e4815fbd0; ks.tg=72; ssaid=eb5306c0-a944-11ec-b937-6fbde8700606; _hjSessionUser_283363=eyJpZCI6ImY4ZmIxZmViLWU3MmQtNWYzMy04YTQ2LTg1NzViZGEzYTdiNyIsImNyZWF0ZWQiOjE2NDc4ODc0MDIwNDUsImV4aXN0aW5nIjp0cnVlfQ==; _hjFirstSeen=1; _hjIncludedInSessionSample=0; _hjSession_283363=eyJpZCI6IjgyM2E1ZjZlLWNlYjgtNDU4Yi04YWVkLTA5MDhkYTQwZTFlZSIsImNyZWF0ZWQiOjE2NDc4ODc0MDIwNDgsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=0; _ga=GA1.2.420676541.1647887402; _gid=GA1.2.1614969253.1647887402; _ym_uid=16478874021015833236; _ym_d=1647887402; _fbp=fb.1.1647887402484.1816566389; _ym_visorc=b; _ym_isad=2; kaspi.storefront.cookie.city=750000000; ks.cc=-1; _ALGOLIA=anonymous-05d309c6-ebd9-483c-82c0-43ef03401012; __tld__=null; _gat_ddl=1',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
}

data = '{"cityId":"750000000","id":"100987780","limit":64,"page":0,"sort":true}'
url = 'https://kaspi.kz/shop/p/xiaomi-dreame-d9-belyi-100987780/?c=750000000'
# response = requests.post('https://kaspi.kz/yml/offer-view/offers/100987780', headers=HEADERS, data=data)
# print(response.content)

proxies = [
    "http://aLDL3a:1fdrsP@31.134.10.116:8000/",
    "http://HfWCLD:W4CEm8@194.67.215.225:9054/",
    "http://HfWCLD:W4CEm8@194.67.215.30:9416/",
    "http://50u3vE:M4QaXL@188.119.79.182:8000/",
    "http://rYtq9n:hjdPab@46.232.5.3:8000/"

]

'''https://kaspi.kz/shop/p/poco-x3-pro-8-256gb-chernyi-101372406/?c=750000000'''


async def ee():
    async with aiohttp.ClientSession() as session:
        data = '{"cityId":"750000000","id":"100987780","limit":64,"page":0,"sort":true}'
        resp = await session.post(
            url=url,
            headers=HEADERS,
            data=data,
            proxy=str(proxies[0])
        )
        data = (await resp.read()).decode('utf-8')
        print(data)


parser = Parser()
asyncio.run(parser.request_kaspi(url, proxies[0]))
# asyncio.run(ee())
