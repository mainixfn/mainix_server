import requests
import pandas as pd
import datetime as dt
import sys
import os
import django
path = os.getcwd() #현재 파일 위치 문자열로 반환
path = os.path.split(path) #상위폴더위치 찾기 위한 스플릿
sys.path.append(path[0])#상위폴더위치 sys.path에 등록
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "svcode.settings")
django.setup()
from stock.models import Kospi_StockName,Kosdaq_StockName

origin_stock=['힘스']
target_stock=['덕산테코피아','에이아이비트','지스마트글로벌','케이피에스','아이씨디','루멘스','베셀','엘아이스','엘티씨','세미콘라이트','우리이앤엘',
              '제이스텍','씨티젠','영우디에스피','선익시스템','아나패스','서울반도체','로체시스템즈','실리콘웍스','AP시스템','야스']

time1 = dt.datetime.now()
nowtime = time1.strftime('%Y-%m-%d')

#top5_list=[['베셀', 3550877], ['아나패스', 3490131], ['아이씨디', 2981022], ['케이피에스', 2635580], ['엘티씨', 2625002]]

days = 500

def cumm_rtn(code):
    cumm_rtn = (1 + stock_price(code).pct_change())
    cumm_rtn= cumm_rtn.dropna()
    return cumm_rtn

def target_stcok_name(category_name):
    stock_names_list=[]
    i = category_business.index(category_name)
    tbody = all_table[i].find_all('dl', {'class': 'tbody'})
    for dl in tbody:
        stock_name = dl.find('dt').get_text()
        dd = dl.find('dd')
        code = dd.get('id').replace('dd_Item_', '')
        stock_names_list.append(stock_name)
    return stock_names_list

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

    dt_price=pd.concat(price_list)
    dt_price=dt_price.reset_index(drop=True,)
    dt_price=dt_price.sort_values(by=['날짜'],ascending=True)
    dt_price=dt_price.rename(columns={'날짜':'Date','시가':'openPrice'})
    dt_price=dt_price.set_index('Date')
    dt_price=dt_price[['openPrice']]

    return dt_price

def Kospi_Signals(name1):
    kospi_db = Kospi_StockName.objects.all()
    kospi_dic = {}
    for stock in kospi_db:
        s = stock.stock_name
        c = stock.stock_code
        kospi_dic[s] = c
    pair_signals = []

    for i in range(len(top5_list)):
        name2 = top5_list[i]
        Total_StockName_dic=kospi_dic
        window1=5
        window2=60
        code1 = Total_StockName_dic[name1]
        code2 = Total_StockName_dic[name2]
        S1 = stock_price(code1)
        S2 = stock_price(code2)
        ratios = S1.div(S2)
        S1 = S1.rename(columns={'openPrice':name1})
        S2 = S2.rename(columns={'openPrice':name2})
        ratios = ratios.rename(columns={'openPrice': 'ratios'})
        ratios = ratios.dropna()
        ma1 = ratios.rolling(window=window1,
                                 center=False).mean()
        ma2 = ratios.rolling(window=window2,
                             center=False).mean()
        std = ratios.rolling(window=window2,
                             center=False).std()
        zscore = (ma1 - ma2) / std
        # zscore = zscore[window2-1:]
        zscore = zscore.rename(columns={'ratios': 'zscore'})


        pair_signal = round(zscore['zscore'][-1], 3)
        if pair_signal>0.8:
            pair_signals.append({"Date":nowtime, "Stock1": name1,
                                 "Stock2": name2,"Signal":name1+"_매도"+'/'+ name2 +"_매수"})

        elif pair_signal<-0.8:
            pair_signals.append({"Date":nowtime, "Stock1": name1,
                                 "Stock2": name2,"Signal":name1 +'_매수'+'/'+ name2 +'_매도'})
        elif abs(pair_signal)<0.4:
            pair_signals.append({"Date": nowtime, "Stock1": name1, "Stock2": name2,
                                 'Signal':'청산'})
    return pair_signals


def Kosdaq_Signals(name1,top5_list):
    kosdaq_db = Kosdaq_StockName.objects.all()
    kosdaq_dic = {}
    for stock in kosdaq_db:
        s = stock.stock_name
        c = stock.stock_code
        kosdaq_dic[s] = c
    pair_signals = []
    for i in range(len(top5_list)):
        name2 = top5_list[i]
        Total_StockName_dic=kosdaq_dic
        window1=5
        window2=60
        code1 = Total_StockName_dic[name1]
        code2 = Total_StockName_dic[name2]
        S1 = stock_price(code1)
        S2 = stock_price(code2)
        ratios = S1.div(S2)
        S1 = S1.rename(columns={'openPrice':name1})
        S2 = S2.rename(columns={'openPrice':name2})
        ratios = ratios.rename(columns={'openPrice': 'ratios'})
        ratios = ratios.dropna()
        ma1 = ratios.rolling(window=window1,
                                 center=False).mean()
        ma2 = ratios.rolling(window=window2,
                             center=False).mean()
        std = ratios.rolling(window=window2,
                             center=False).std()
        zscore = (ma1 - ma2) / std
        # zscore = zscore[window2-1:]
        zscore = zscore.rename(columns={'ratios': 'zscore'})


        pair_signal = round(zscore['zscore'][-1], 3)
        if pair_signal>0.8:
            pair_signals.append({"Date":nowtime, "Stock1": name1,
                                 "Stock2": name2,"Signal":name2 +"_매수"})

        elif pair_signal<-0.8:
            pair_signals.append({"Date":nowtime, "Stock1": name1,
                                 "Stock2": name2,"Signal":name1 +'_매수'})
        elif abs(pair_signal)<0.4:
            pair_signals.append({"Date": nowtime, "Stock1": name1, "Stock2": name2,
                                 'Signal':'청산'})
        else:
            pair_signals.append({"Date": nowtime, "Stock1": name1, "Stock2": name2,
                                 'Signal': '대기'})

    return pair_signals



def Pairtrade_dt(name1,name2,zscore,S1,S2,ratios):
    Price_ratios = pd.concat([S1, S2, ratios, zscore], axis=1, sort=True)
    Price_ratios = Price_ratios.dropna()
    money = 0
    countS1 = 0
    countS2 = 0
    position = []
    trade_num= 20
    S1_price = []
    S2_price = []

    for i in range(len(Price_ratios)):
        # Sell short if the z-score is > 1
        Date = Price_ratios.index[i]
        if i > 1:
            if Price_ratios['zscore'].values[i-1] >1 :
                money += 0
                countS1 -= trade_num
                countS2 += Price_ratios['ratios'][i]*trade_num
                S2_price.append(Price_ratios[name2][i])
                #assessment =
                #total = money + Price_ratios[name1][i] * countS1 + Price_ratios[name2][i] * countS2
                position.append({'Date': Date,'signal':round(Price_ratios['zscore'].values[i],3),  'postion':'매도','수익': money, name1: countS1,'1_편입가':Price_ratios[name1][i],
                                 name2: countS2,'2_편입가':Price_ratios[name2][i]})
            elif Price_ratios['zscore'].values[i-1] < -1:
                money -= 0
                countS1 += trade_num
                countS2 -= Price_ratios['ratios'][i]*trade_num
                S1_price.append(Price_ratios[name1][i])
                #total = money + Price_ratios[name1][i] * countS1 + Price_ratios[name2][i] * countS2
                position.append({'Date': Date,'signal':round(Price_ratios['zscore'].values[i],3),  'postion':'매수','수익': money,name1: countS1,'1_편입가':Price_ratios[name1][i],
                                 name2: countS2,'2_편입가':Price_ratios[name2][i]})

            # Clear positions if the z-score between -.5 and .5
            # -0.5~0.5 사이인 경우 수익일 경우 이익 실현
            elif abs(Price_ratios['zscore'].values[i-1]) < 0.4 and (Price_ratios[name1][i] * countS1 + Price_ratios[name2][i] * countS2) > 0:
                if countS1 > 0 :
                    money += int(countS1*(sum(S1_price)/len(S1_price))*(Price_ratios[name1][i]/(sum(S1_price)/len(S1_price))-1))
                elif countS2 > 0 :
                    money += int(countS2 * (sum(S2_price) / len(S2_price)) * (Price_ratios[name2][i]/(sum(S2_price) / len(S2_price)) - 1))
                else:
                    pass
                countS1 = 0
                countS2 = 0
                #total = money + Price_ratios[name1][i] * countS1 + Price_ratios[name2][i] * countS2
                S1_price.clear()
                S2_price.clear()
                position.append({'Date': Date,'signal':round(Price_ratios['zscore'].values[i],3), 'postion': '청산','수익': money, name1: countS1,'1_편입가':Price_ratios[name1][i],
                                 name2: countS2,'2_편입가':Price_ratios[name2][i]})
            position_dt = pd.DataFrame(position)
        else:
            pass
    return position_dt
