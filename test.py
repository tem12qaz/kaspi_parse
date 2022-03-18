import requests

cookies = {
    'ks.ngs.s': '44ad37db1a147674ef1fae0a521f3160',
    'k_stat': '749f4aa0-f4a9-4d76-b84b-1c8328a0b147',
    'ks.tg': '15',
    'ssaid': 'c6c365b0-a6f7-11ec-a795-1fc8bccfaecc',
    '_hjSessionUser_283363': 'eyJpZCI6ImQ5YTgzNTUyLTUxMDItNTViMi1hZmQ0LWRkZmI1MmNmZWI1MCIsImNyZWF0ZWQiOjE2NDc2MzQzNjY2NjIsImV4aXN0aW5nIjp0cnVlfQ==',
    '_hjFirstSeen': '1',
    '_hjIncludedInSessionSample': '0',
    '_hjSession_283363': 'eyJpZCI6ImUwZGRmYWMyLTNmNzgtNDc3OS04NDZhLTljMWE4ZDE4YWRkMSIsImNyZWF0ZWQiOjE2NDc2MzQzNjcwNjUsImluU2FtcGxlIjpmYWxzZX0=',
    '_hjAbsoluteSessionInProgress': '0',
    '_fbp': 'fb.1.1647634367823.1301007092',
    '_ga': 'GA1.2.2146355550.1647634368',
    '_gid': 'GA1.2.930761080.1647634368',
    '_ym_uid': '1647634369219723563',
    '_ym_d': '1647634369',
    '_ym_isad': '2',
    '_ym_visorc': 'b',
    'kaspi.storefront.cookie.city': '750000000',
    'ks.cc': '-1',
    '.AspNetCore.Culture': 'c%3Dru%7Cuic%3Dru',
    'current-action-name': 'Index',
    '_dyjsession': 'yjv8hnckkwtvc1gao70sgmfs72dwiogq',
    'dy_fs_page': 'kaspi.kz%2Fshop%2F%3Fat%3D1',
    '_dy_csc_ses': 'yjv8hnckkwtvc1gao70sgmfs72dwiogq',
    '_dy_c_exps': '',
    '_dy_soct': '1048286.1115542.1647634400.yjv8hnckkwtvc1gao70sgmfs72dwiogq*1014383.1024804.1647634400*1019791.1035034.1647634400*1018356.1031862.1647634401',
    '_ALGOLIA': 'anonymous-c4664c81-8a38-411e-a2a5-bcfc86cd92ae',
    '_dycnst': 'dg',
    '_dyid': '-7651614901966411986',
    '_dyfs': '1647634401593',
    '_dycst': 'dk.w.f.ws.',
    '_dy_geo': 'RU.EU.RU_MOW.RU_MOW_Moscow',
    '_dy_df_geo': 'Russia..Moscow',
    '_dy_toffset': '-179',
    '_dy_user_has_affinity': '',
    '_dyid_server': '-7651614901966411986',
    '__tld__': 'null',
}

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

print(response.content)