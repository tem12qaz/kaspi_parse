
PG_HOST = 'localhost'
PG_PASSWORD = 'pass'
PG_USER = 'myuser'
PG_DATABASE = 'db'
delivery_duration = 7



class Configuration(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}/{PG_DATABASE}'
    SQLALCHEMY_POOL_SIZE = 1

    SECRET_KEY = 'someth3489rh6&r65r^R#2$%GkBHJKN98secret'

    SECURITY_PASSWORD_SALT = 'lkpoopfdJBGYlkp_r65j_98eJKkjui890Khbh_jhb45ff_Vhgv769V7'
    SECURITY_PASSWORD_HASH = 'sha512_crypt'



COOKIES = {
    'JSESSIONID': '5D4300FAD1B46A6686BB8F8E37DB5464',
    'ks.tck': 'bb6106d153e5041d9b7be9cb41b70ac1',
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
    '_dy_df_geo': 'Russia..Moscow',
    '_dy_geo': 'RU.EU.RU_MOW.RU_MOW_Moscow',
    'mabayaCookie': 'product',
    'ks.ngs.s': '2831746020959a463b5dc5c78e658456',
    '_hjSession_283363': 'eyJpZCI6ImI3ZTIzZDYzLTI1ZGYtNGQ3Ny04ZWE0LTQwOGJlYWRmMGI4YiIsImNyZWF0ZWQiOjE2NDc2MjI0MzUwMDcsImluU2FtcGxlIjpmYWxzZX0=',
    '_hjIncludedInSessionSample': '0',
    '_hjAbsoluteSessionInProgress': '0',
    '_gid': 'GA1.2.1559982132.1647622435',
    '_gat_ddl': '1',
    '_ym_isad': '2',
    '_ym_visorc': 'b',
    'ks.cc': '18',
    '_dyjsession': 'edsoa7u8ff7padw4fl5a1486hpj8gynq',
    'dy_fs_page': 'kaspi.kz%2Fshop%2F%3Fat%3D1',
    '_dy_csc_ses': 'edsoa7u8ff7padw4fl5a1486hpj8gynq',
    '_dy_toffset': '-179',
    '_dy_user_has_affinity': '',
    'current-action-name': 'Index',
    '.AspNetCore.Culture': 'c%3Dru%7Cuic%3Dru',
    '_dy_soct': '1048286.1115542.1647622442.edsoa7u8ff7padw4fl5a1486hpj8gynq*1014383.1024804.1647622458*1019791.1035034.1647622459*1018356.1031862.1647622459',
    '__tld__': 'null',
}

HEADERS = {
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

# month_days = {
#     'января': 31,
#     'февраля': 28,
#     'марта': 31,
#     'апреля': 30,
#     'мая': 31,
#     'июня': 30,
#     'июля': 31,
#     'августа': 31,
#     'сентября': 30,
#     'октября': 31,
#     'ноября': 30,
#     'декабря': 31,
# }

month_days = {
    1: 31,
    2: 28,
    3: 31,
    4: 30,
    5: 31,
    6: 30,
    7: 31,
    8: 31,
    9: 30,
    10: 31,
    11: 30,
    12: 31,
}

ERRS_MAX = 2