from django.shortcuts import redirect,render,HttpResponse
from CivitasModel.models import weather
from assist import *
import datetime
import json

def getweather1(req):   #获取天气，参数：day、city
    status=0
    meg='失败'
    data={}
    if req.GET.get("day")!=None and req.GET.get("city")!=None:
        last1=weather.objects.order_by('-id')[0]
        count=int(last1.total_day)
        day = is_int(req.GET.get("day"))
        if day == "error":
            meg = "存在需要传入数字的参数传入的不是数字"
            result={
                "status":status,
                "message":meg,
                "data":{}
            }
            return HttpResponse(json.dumps(result), content_type="application/json")
        if 1<=int(req.GET.get("day"))<=count:
            city=req.GET.get("city")
            list1=weather.objects.filter(city=city)
            if bool(list1)!=False:
                list1=list1.filter(total_day=day)
                status=1
                meg='成功'
                for var in list1:
                    city=var.city
                    total_day=int(var.total_day)
                    year=int(var.year)
                    season=var.season
                    day=int(var.day)
                    weather1=var.weather
                    temperature=eval(var.temperature)
                    rain_num=eval(var.rain_num)
                    data = {
                                "city":city,
                                "total_day":total_day,
                                "year":year,
                                "season":season,
                                "day":day,
                                "weather":weather1,
                                "temperature":temperature,
                                "rain_num":rain_num
                            }
            else:
                status=0
                meg='失败，城市查找错误'
                data={}
        else:
            status=0
            meg='失败，天数查找错误'
            data={}
    else:
        status=0
        meg='失败，缺少参数'
        data={}
    result={
                "status":status,
                "message":meg,
                "data":data
            }
    return HttpResponse(json.dumps(result), content_type="application/json")

def getdate1(req):  #获取日期
    year_length=80
    season_length=20
    status=1
    meg="成功"
    d=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    total_day=(datetime.datetime.strptime(d[0:10],"%Y-%m-%d")-datetime.datetime.strptime('2021-6-3',"%Y-%m-%d")).days
    time=d[11:19]
    days = total_day - 1
    days_left = days % year_length
    year = 1 + days // year_length
    days_left2 = days_left % season_length
    season = 1 + days_left // season_length
    day = days_left2 + 1
    season_dict = {1:"春天",2:"夏天",3:"秋天",4:"冬天"}
    result={
                "status":status,
                "message":meg,
                "data":{
                            "total_day":total_day,
                            "time":time,
                            "year":year,
                            "season":season_dict[season],
                            "day":day
                        }

            }
    return HttpResponse(json.dumps(result), content_type="application/json")