import asyncio

import aiohttp
# import httpx
import requests
from fake_useragent import UserAgent

fa = UserAgent()


cookies = {
    'JSESSIONID': 'FC8EED28B4520200C93B970739C0AECA',
    'ks.tck': '6e6761e26e9fa8cf83846764f0d27794',
    'k_stat': '0bd3355e-c17f-4431-885c-25769b5ce49f',
    'ks.tg': '25',
    '_ALGOLIA': 'anonymous-95f49eba-b37d-4386-a0f6-e3b0325f26b9',
    'ssaid': '0b826d00-9b62-11ec-9e8d-b90c9f2db05a',
    '_ga': 'GA1.2.1389746463.1646360595',
    '_gid': 'GA1.2.2055645266.1646360595',
    '_ym_uid': '1646360595443082129',
    '_ym_d': '1646360595',
    '_ym_isad': '2',
    '_fbp': 'fb.1.1646360594905.720965103',
    'kaspi.storefront.cookie.city': '750000000',
    'ks.cc': '-1',
    '_hjSessionUser_283363': 'eyJpZCI6Ijg5ODdhZDU3LTFjNGEtNTZmNS05MjNiLTU2YTk5ZDZkOTk3ZSIsImNyZWF0ZWQiOjE2NDYzNjA1OTQ1NjEsImV4aXN0aW5nIjp0cnVlfQ==',
    'ks.ngs.s': '09e61e0041fa3f3ef4a84dcc680f7abb',
    '_ym_visorc': 'b',
    '_hjSession_283363': 'eyJpZCI6IjNkMTdlNWI4LTQwNDctNGIxMS1hY2U3LTY5MDA5NDU1N2U0ZCIsImNyZWF0ZWQiOjE2NDY0MDc0OTA3NDEsImluU2FtcGxlIjpmYWxzZX0=',
    '_hjAbsoluteSessionInProgress': '0',
    '_dyjsession': 'i449ioaynegsta0uuz3quzx5zhosflnx',
    '_dy_csc_ses': 'i449ioaynegsta0uuz3quzx5zhosflnx',
    '_dy_c_exps': '',
    '_dycnst': 'dg',
    '_dyid': '896217199371497286',
    '_dy_df_geo': 'Russia..Moscow',
    '_dy_geo': 'RU.EU.RU_MOW.RU_MOW_Moscow',
    '_dy_toffset': '0',
    '_dyid_server': '896217199371497286',
    '_hjIncludedInSessionSample': '0',
    '_dy_c_att_exps': '',
    '_dycst': 'dk.w.c.ss.',
    '_dy_soct': '1048286.1115542.1646407494.i449ioaynegsta0uuz3quzx5zhosflnx*1014383.1024804.1646408318*1019791.1035034.1646408318*1018356.1031862.1646408318',
    '__tld__': 'null',
    '_gali': 'page',
}

headers = {
    'Connection': 'keep-alive',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
    'Accept': 'application/vnd.api+json',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
    'sec-ch-ua-platform': '"Windows"',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://kaspi.kz/shop/p/polaris-puh-7045-tfd-belyi-4300457/?ref=shared_link&c=750000000&at=1',
    'Accept-Language': 'ru-RU,ru;q=0.9,en;q=0.8,es;q=0.7',
}

params = (
    ('c', '750000000'),
    # ('id', '4300457'),
    ('limit', '100'),
    ('page', '0'),
    ('sort', 'asc'),
)

proxies = {
    "http": "http://50u3vE:M4QaXL@188.119.79.182:8000/",
    "https": "http://50u3vE:M4QaXL@188.119.79.182:8000/"
}

# proxies = {
#     "http": "http://rYtq9n:hjdPab@46.232.5.3:8000/",
#     "https": "http://rYtq9n:hjdPab@46.232.5.3:8000/",
# }


url = 'https://kaspi.kz/shop/p/polaris-puh-7045-tfd-belyi-4300457/?c=351010000'


def header_format(url_):
    headers = {
        'Connection': 'keep-alive',
        'X-KL-Ajax-Request': 'Ajax_Request',
        'Accept': 'application/vnd.api+json',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
        'sec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': f'{url_}/?c=750000000&ref=rec-goods&PageSpeed=noscript',
        'Accept-Language': 'ru-RU,ru;q=0.9,en;q=0.8,es;q=0.7',
    }
    return headers


def parse_new(url_):
    url_ = url_.split("/?")[0]
    print(url)
    response = requests.get(
        f'{url_}/offers/', headers=header_format(url_), params=params, cookies=cookies, proxies=proxies
    )
    data = response.content.decode('utf-8')
    return data


def test():
    response = requests.get(
        'https://ipaddress.my/', proxies=proxies
    )
    print(response.content.decode('utf-8'))


# print(parse_new(url))
# test()