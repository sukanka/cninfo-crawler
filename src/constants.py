import json
from fake_useragent import UserAgent
import requests as r
import json
UA = UserAgent()
FILE = r.get("http://www.cninfo.com.cn/new/data/szse_stock.json",
             allow_redirects=True)
if FILE.status_code != 200:
    raise Exception('failed to get szse_stock list')
MAP = json.loads(FILE.content.decode('utf8'))
MAPS = MAP['stockList']
DICT = {}
for map in MAPS:
    DICT[map['code']] = map
