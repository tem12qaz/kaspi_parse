
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