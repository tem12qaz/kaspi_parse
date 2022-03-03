import asyncio

import aiohttp
# import httpx
import requests
from fake_useragent import UserAgent

fa = UserAgent()


cookies = {
    'JSESSIONID': 'C8DA2AB733DCCE8CF07A326BFEDBD546',
    'ks.tck': 'd7d5b7dbeab40fd8d2342b024c1f9b66',
    'user-device-type': 'Desktop',
    'kaspi-region-confirm-shown': 'true',
    'ssaid': 'a2cb61c0-7bce-11ec-8607-73738c46fbe4',
    'test.user.group': '57',
    '_gcl_au': '1.1.1951022373.1642888797',
    '_fbp': 'fb.1.1642888797063.1758907459',
    'kaspi-payment-region': '18',
    'kaspi-trusted-region-id': '18',
    '_hjSessionUser_283363': 'eyJpZCI6IjE0ODE2ZDQyLTUyNzYtNTlhYS05NTliLTE0ZWFkZjA5ZTQzZiIsImNyZWF0ZWQiOjE2NDI4ODg3OTc5NDgsImV4aXN0aW5nIjp0cnVlfQ==',
    'k_stat': 'b2308aaac0894b248e23439736caddf5',
    'ks.tg': '62',
    '_ALGOLIA': 'anonymous-7ad0a56c-e001-4c59-aa1d-fc6b36def883',
    '_dy_c_exps': '',
    '_dycnst': 'dg',
    '_dyid': '-1067352229575621104',
    '_dycst': 'dk.w.c.ws.',
    '_ga': 'GA1.2.1545286132.1642890802',
    '_ym_uid': '1642890802554897734',
    '_ym_d': '1642890802',
    'kaspi.storefront.cookie.city': '750000000',
    '_dyid_server': '-1067352229575621104',
    '_dy_c_att_exps': '',
    '_dy_geo': 'RU.EU.RU_MOW.RU_MOW_Moscow',
    '_dy_df_geo': 'Russia..Moscow',
    '_dy_toffset': '-118',
    '_dy_soct': '1048286.1115542.1645662857.tqpp3lcnwi1tdi6ftpzqnp145e02exqd*1014383.1024804.1645662857*1019791.1035034.1645662857*1018356.1031862.1645662857',
    'ks.ngs.oc': 'd1ab8e5a46259e3fdec85eab4a902f70',
    'mabayaCookie': 'product',
    '_gid': 'GA1.2.1644835090.1646331752',
    '_ym_isad': '2',
    '_hjIncludedInSessionSample': '0',
    '_hjSession_283363': 'eyJpZCI6ImY5MjczMDkyLWJhMGYtNGMxNi04ODdhLWVmZTRlNTNiMDVkMCIsImNyZWF0ZWQiOjE2NDYzMzE3NTI0MzEsImluU2FtcGxlIjpmYWxzZX0=',
    '_hjAbsoluteSessionInProgress': '0',
    '_ym_visorc': 'b',
    'ks.ngs.s': 'd854eef12485816e90bc107806389b98',
    '__tld__': 'null',
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
    "http": "http://50u3vE:M4QaXL@188.119.79.182:8000/"
}

url = 'https://kaspi.kz/shop/p/polaris-puh-7045-tfd-belyi-4300457/?c=351010000'


def header_format(url_):
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
        'Referer': f'{url_}/?c=750000000&ref=rec-goods&PageSpeed=noscript',
        'Accept-Language': 'ru-RU,ru;q=0.9,en;q=0.8,es;q=0.7',
    }
    return headers


# async def ss():
#     proxy = {'https://': f'{proxies["http"]}'}
#     async with httpx.AsyncClient(proxies=proxy, timeout=60.0) as client:
#         resp = await client.request(
#             'GET',
#             url,
#             headers=headers,
#             cookies=cookies,
#             params=params
#         )
#         print(resp.text)
# async with aiohttp.ClientSession(cookies=cookies) as session:
#
#         resp = await session.get(
#             url=url,
#             headers=headers,
#             params=params,
#             proxy=proxies['http']
#         )
#         data = (await resp.read()).decode('utf-8')
#         print(data)


# response = requests.get(f'{url}/offers/', headers=headers, params=params, cookies=cookies, proxies=proxies)
# # print(response.content)
#
# asyncio.run(ss())
def parse_new(url_):
    url_ = url_.split("/?")[0]
    print(url)
    response = requests.get(
        f'{url_}/offers/', headers=header_format(url_), params=params, cookies=cookies, proxies=proxies
    )
    data = response.content.decode('utf-8')
    return data


print(parse_new(url))