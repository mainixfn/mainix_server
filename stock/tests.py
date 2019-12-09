from django.test import TestCase

import requests
import pandas as pd



def read_stock_price(code,page_num):
    url=('https://finance.naver.com/item/sise_day.nhn?code='+code+'&page='+str(page_num)+'')
    data=pd.read_html(url)
    data=data[0]
    data.columns=['날짜','당일종가','전일비','시가','고가','저가','거래량']
    price_data=data.dropna(axis=0,how='any')
    price_data=price_data.drop(price_data.index[0])
    price_data=price_data.reset_index(drop=True)
    price_data['날짜']=pd.to_datetime(price_data['날짜'],format='%Y/%m/%d')
    return price_data

def stock_price(code):
    price_list =[]
    page=1
    while True:
        try:
            data=read_stock_price(code,page)
            time_limit=dt.datetime.now()-data['날짜'][0]
            if time_limit.days > days: break
            price_list.append(data)
            page=page+1

        except:break
    '''
    dt_price=pd.concat(price_list)
    dt_price=dt_price.reset_index(drop=True,)
    dt_price=dt_price.sort_values(by=['날짜'],ascending=True)
    dt_price=dt_price.rename(columns={'날짜':'Date','시가':'openPrice'})
    dt_price=dt_price.set_index('Date')
    dt_price=dt_price[['openPrice']]
    '''
    return price_list
# Create your tests here.


#print(read_stock_price('238490','10'))