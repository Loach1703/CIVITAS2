from django.shortcuts import redirect,render,HttpResponse
from TestModel.models import speech,weather
from django.contrib.sessions.models import Session
import datetime
import json

def getspeech1(req):    #获取演讲，参数：page
    num_every_page=10
    status=0
    meg='失败'
    list2=[]
    total_page=0
    num=0
    if req.GET.get("page")!=None:
        page = int(req.GET.get("page"))
        count=len(speech.objects.all())
        if count%num_every_page==0:
            total_page=count/num_every_page
        else:
            total_page=(count+num_every_page)//num_every_page
        if count-num_every_page*page<-num_every_page or page<=0:
            status=0
            meg='失败，错误的页数'    
        else:
            list1 = speech.objects.order_by('-id')[0+num_every_page*(page-1):num_every_page*page]
            i=0
            num=len(list1)
            for var in list1:
                r = var.text
                textid = var.id
                d = str(var.date)[0:10]
                a=(datetime.datetime.strptime(d,"%Y-%m-%d")-datetime.datetime.strptime('2021-6-3',"%Y-%m-%d")).days
                b=str(var.date)[11:19]
                list2.append({"textid":textid,"text":r,"day":a,"time":b})
                i+=1
            status=1
            meg='成功'
    else:
        status=0
        meg='失败，没有提供页码'
    result={
                "status":status,
                "message":meg,
                "data":{
                            "total_page":total_page,
                            "num":num,
                            "datalist":list2
                        }
            }
    return HttpResponse(json.dumps(result), content_type="application/json")

def speech1(req):   #发送演讲，参数：text
    status=0
    meg="失败"
    text=req.POST.get("text")
    if text!=None:
        if 0<len(text)<=140:
            date=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            dbspeech = speech(text=text,date=date)
            dbspeech.save()
            status=1
            meg="演讲发布成功"
        else:
            status=0
            meg="失败，提交字数应该在1~140之间，当前字数：{}".format(len(text))
    else:
        status=0
        meg='失败，没有提供POST参数'
    result={
                "status":status,
                "message":meg,
            }
    return HttpResponse(json.dumps(result), content_type="application/json")

def getweather1(req):   #获取天气，无参数
    status=0
    meg='失败'
    data={}
    if req.GET.get("day")!=None and req.GET.get("city")!=None:
        last1=weather.objects.order_by('-id')[0]
        count=int(last1.total_day)
        if 1<=int(req.GET.get("day"))<=count:
            day=req.GET.get("day")
            city=req.GET.get("city")
            list1=weather.objects.filter(city=city)
            if bool(list1)!=False:
                list1=list1.filter(total_day=day)
                status=1
                meg='成功'
                for var in list1:
                    city=var.city
                    total_day=var.total_day
                    year=var.year
                    season=var.season
                    day=var.day
                    weather1=var.weather
                    temperature=var.temperature
                    rain_num=var.rain_num
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

def year_season_calc(self): #天气计算，非接口
    days = self.day - 1
    days_left = days % self.year_length
    self.year = 1 + days // self.year_length
    days_left2 = days_left % self.season_length
    self.season = 1 + days_left // self.season_length
    self.day = days_left2 + 1

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

def islogin1(req):
    status=0
    meg="失败"
    is_login=False
    sessionid=req.COOKIES.get("sessionid")
    if sessionid != None:
        if req.session.exists(sessionid)==False:
            meg="登录状态失效"
        else:
            status=1
            meg="成功"
            is_login=True
    else:
        meg="没有提供sessionid"
    result={
                "status":status,
                "message":meg,
                "data":{
                            "is_login":is_login,
                            "sessionid":sessionid
                        }
            }
    return HttpResponse(json.dumps(result), content_type="application/json")
    
