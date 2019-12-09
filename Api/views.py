from django.shortcuts import render
from django.http import HttpResponse
import sys
import os
import django
path = os.getcwd() #현재 파일 위치 문자열로 반환
path = os.path.split(path) #상위폴더위치 찾기 위한 스플릿
sys.path.append(path[0])#상위폴더위치 sys.path에 등록
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "svcode.settings")
django.setup()
from django.core import serializers
from stock.models import Stock_Table ,Kosdaq_StockName
# Create your views here.

def trend_api(request):
    dt =Kosdaq_StockName.objects.all()
    name=[]
    for  i in dt :
        name.append({'name':i.stock_name , 'code':i.stock_code})

    return HttpResponse(name ,content_type=u"application/json; charset=utf-8")

#print(trend_api())