import json
import requests
import pandas as pd
import urllib3

headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


url = 'http://127.0.0.1:8000/api/b2b/crypto/blockchail/trend';
#url ='http://www.mainix.net/signals/hours/data'
#url ='https://crix-api-endpoint.upbit.com/v1/crix/candles/minutes/60?code=CRIX.UPBIT.KRW-BTC&count=100'
res = requests.get(url, headers=headers)
#data=pd.read_html(url)
data = res.json()

print(data)
