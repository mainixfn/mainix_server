from django.shortcuts import render
import sys
import os
import django
path = os.getcwd() #현재 파일 위치 문자열로 반환
path = os.path.split(path) #상위폴더위치 찾기 위한 스플릿
sys.path.append(path[0])#상위폴더위치 sys.path에 등록
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "svcode.settings")
django.setup()
#from  stock.models import Stock_Table, Stock_Pair_Trade, Kosdaq_StockName

'''
Stock_name_db = Kosdaq_StockName.objects.all()
stock_name ={}
for st in Stock_name_db:
    s=st.stock_name
    c=st.stock_code
    stock_name[s]=c



stock_list = ['베셀','케이피에스','아나패스','아이씨디', '엘티씨']

def mainpage(request):
    stock_code = []
    trade_data = {}
    Trade_data = Stock_Pair_Trade.objects.all()
    target= Target_StockName.objects.all()
    for i in range(len(stock_list)):
        name = stock_list[i]
        code = str(stock_name[name])
        stock_code.append(code)
        name = Trade_data.filter(Pair_stock=name)
        trade_data[name] = name
    trade_data['targets']=target
    return render(request,'pair_stock_index.html',trade_data)
'''
def stock_main(request):

    return render(request,'stock_main.html')


# Create your views here.
