import asyncio

from parse import Parser


url = 'https://kaspi.kz/shop/p/xiaomi-dreame-d9-belyi-100987780/?c=750000000	'
print(repr(url))

proxies = [
    "http://aLDL3a:1fdrsP@31.134.10.116:8000/",
    "http://HfWCLD:W4CEm8@194.67.215.225:9054/",
    "http://HfWCLD:W4CEm8@194.67.215.30:9416/",
    "http://50u3vE:M4QaXL@188.119.79.182:8000/",
    "http://rYtq9n:hjdPab@46.232.5.3:8000/"

]

parser = Parser()
asyncio.run(parser.request_kaspi(url, proxies[0]))
# asyncio.run(ee())
