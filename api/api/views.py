from django.shortcuts import redirect,render,HttpResponse
from TestModel.models import speech,weather,usersession,speech_attitude,personal_attributes
from django.contrib.sessions.models import Session
from django.contrib import auth
from django.db.models import Avg,Max,Min,Count,Sum,F,Q
import datetime
import json
import random
import re

def is_login(req,sessionid):
    if not sessionid:
        return 0
    if not req.session.exists(sessionid):
        return 0
    return 1
        
    

def getspeech1(req):    #获取演讲，参数：page
    num_every_page=10
    status=0
    meg='失败'
    list2=[]
    total_page=0
    num=0
    sessionid=req.COOKIES.get("sessionid")
    if is_login(req,sessionid):
        session = Session.objects.filter(pk=sessionid).first()
        attuid=session.get_decoded()["_auth_user_id"]
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
                    my_att=None
                    cheer=0
                    onlooker=0
                    catcall=0
                    r = var.text
                    textid = var.id
                    uid=var.uid
                    user=auth.models.User.objects.filter(pk=uid)
                    if user.exists():
                        user.first()
                        username=user[0].username
                    else:
                        username="用户不存在"
                    d = str(var.date)[0:10]
                    a=(datetime.datetime.strptime(d,"%Y-%m-%d")-datetime.datetime.strptime('2021-6-3',"%Y-%m-%d")).days
                    b=str(var.date)[11:19]
                    dbatt=speech_attitude.objects.filter(uid=attuid).filter(textid=textid)
                    if dbatt.exists():
                        my_att=dbatt[0].att
                    cheer=speech_attitude.objects.filter(textid=textid).filter(att=1).count()
                    onlooker=speech_attitude.objects.filter(textid=textid).filter(att=2).count()
                    catcall=speech_attitude.objects.filter(textid=textid).filter(att=3).count()
                    list2.append({"textid":textid,"text":r,"day":a,"time":b,"username":username,"my_attitude":my_att,"cheer":cheer,"onlooker":onlooker,"catcall":catcall})
                    i+=1
                status=1
                meg='成功'
        else:
            status=0
            meg='失败，没有提供页码'
    else:
        meg='您还没有登录'
    result={
                "status":status,
                "message":meg,
                "data":{
                            "total_page":total_page,
                            "num":num,
                            "datalist":list2,
                        }
            }
    return HttpResponse(json.dumps(result), content_type="application/json")

def speech1(req):   #发送演讲，参数：text
    status=0
    meg="失败"
    sessionid=req.COOKIES.get("sessionid")
    if is_login(req,sessionid):
        session = Session.objects.filter(pk=sessionid).first()
        uid=session.get_decoded()["_auth_user_id"]
        text=req.POST.get("text")
        if text!=None:
            if 0<len(text)<=140:
                date=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                dbspeech = speech(text=text,date=date,uid=uid)
                dbspeech.save()
                status=1
                meg="演讲发布成功"
            else:
                status=0
                meg="失败，提交字数应该在1~140之间，当前字数：{}".format(len(text))
        else:
            status=0
            meg='失败，没有提供POST参数'
    else:
        status=0
        meg='您还没有登录'
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
    uid=None
    username=None
    sessionid=req.COOKIES.get("sessionid")
    if sessionid != None:
        if req.session.exists(sessionid)==False:
            meg="登录状态失效，请重新登录"
        else:
            status=1
            meg="成功"
            session = Session.objects.get(pk=sessionid)
            is_login=True
            uid=session.get_decoded()["_auth_user_id"]
            user=auth.models.User.objects.filter(pk=uid)
            user.first()
            username=user[0].username
    else:
        meg="未登录"
    result={
                "status":status,
                "message":meg,
                "data":{
                            "is_login":is_login,
                            "sessionid":sessionid,
                            "uid":uid,
                            "username":username
                        }
            }
    return HttpResponse(json.dumps(result), content_type="application/json")

def login1(req):
    status=0
    meg="失败"
    sessionid=None
    uid=None
    if req.POST.get("username")==None or req.POST.get("password")==None:
        meg="POST参数缺少"
        user=0
    else:
        username=req.POST.get("username")
        pwd=req.POST.get("password")
        user=auth.authenticate(username=username,password=pwd)
        if user:
            finduid = auth.models.User.objects.get(username=username)           
            uid = finduid.id                                                    #根据用户名从User表中获取uid
            usersession1=usersession.objects.filter(uid=uid)                    #usersession为自建表，记录用户登录所使用的sessionid
            if usersession1.exists():                                           #查找对应uid用户是否登录并留下sessionid
                for var in usersession1:                                        #留下sessionid，对Session表进行清理
                    session1=Session.objects.filter(session_key=var.sessionid)
                    session1.delete()
                usersession1.delete()
            auth.login(req,user)                                                #登录
            sessionid=req.session.session_key
            if not req.session.session_key:                                     #sessionid重复时req.session.session_key为None，此处防止用户处于登录情况下重复登录账户返回sessionid为None
                req.session.create()
                sessionid=req.session.session_key
            dbuser = usersession(uid=uid,sessionid=sessionid)                   #更新usersession表为最新sessionid
            dbuser.save()
            status=1
            meg="登录成功"
        else:
            meg="账号或密码有误"
    result={
                "status":status,
                "message":meg,
                "data":{"sessionid":sessionid,"uid":uid}
            }
    return HttpResponse(json.dumps(result), content_type="application/json")

def validateEmail(email):
    if len(email) > 7:
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
            return 1
    return 0

def register1(req):
    status=0
    meg="失败"
    username=req.POST.get("username")
    pwd=req.POST.get("password")
    repwd=req.POST.get("repeat_password")
    email=req.POST.get("email")
    if not (username and pwd and email):
        meg="缺少参数"
    else:
        s=1
        u=auth.models.User.objects.filter(username=username).first()
        if u:
            meg=meg+",该用户名已被注册"
            s=0
        if len(username)> 20:
            meg=meg+",用户名不能超过20个字符"
            s=0
        if len(pwd)<6 or len(pwd)>20:
            meg=meg+",密码需要在6~20字符之间"
            s=0
        if pwd!=repwd:
            meg=meg+",两次输入的密码不一致"
            s=0
        if not validateEmail(email):
            meg=meg+",邮箱不符合规范"
            s=0
        if s:
            auth.models.User.objects.create_user(username=username,password=pwd,email=email)
            status=1
            meg="注册成功"
    result={
                "status":status,
                "message":meg,
                "data":{}
            }
    return HttpResponse(json.dumps(result), content_type="application/json")

def assess1(req):
    status=0
    meg="失败"
    att=req.POST.get("attitude")
    textid=req.POST.get("textid")
    sessionid=req.COOKIES.get("sessionid")
    attdict={"1":"欢呼","2":"关注","3":"倒彩"}
    if is_login(req,sessionid):
        if att==None or textid==None:
            meg="缺少必要参数"
        else:
            if att=="1" or att=="2" or att=="3":
                if speech.objects.filter(pk=textid).exists():
                    session=Session.objects.filter(pk=sessionid).first()
                    uid=session.get_decoded()["_auth_user_id"]
                    if speech_attitude.objects.filter(textid=textid).filter(uid=uid).exists():
                        if speech_attitude.objects.filter(textid=textid).filter(uid=uid)[0].att==att:
                            speech_attitude.objects.filter(textid=textid).filter(uid=uid).delete()
                            meg="您已经撤销对这个演讲的态度"
                        else:
                            meg="您已经对这个演讲发表过态度了,请先取消之前的态度再点击"
                    else:
                        sendatt=speech_attitude(uid=uid,textid=textid,att=att)
                        sendatt.save()
                        status=1
                        meg="{}成功".format(attdict[att])
                else:
                    meg="您将要发表观点的演讲不存在"
            else:
                meg="您的态度无效"
    else:
        meg='您还没有登录'
    result={
                "status":status,
                "message":meg,
                "data":{}
            }
    return HttpResponse(json.dumps(result), content_type="application/json")

def hotspeech1(req):
    status=0
    meg="失败"
    now=datetime.datetime.now()
    speech_in_24h=speech.objects.filter(date__gte=now-datetime.timedelta(days=1),date__lte=now)
    order=speech_in_24h.order_by('id')
    num=0
    sessionid=req.COOKIES.get("sessionid")
    if is_login(req,sessionid):
        session = Session.objects.filter(pk=sessionid).first()
        attuid=session.get_decoded()["_auth_user_id"]
        if order.exists():
            min1=order.first().id
            max1=order.last().id
            satisfied_attitude=speech_attitude.objects.filter(textid__range=[min1,max1])
            table1=satisfied_attitude.values("textid","att").annotate(count_divide=Count("att"))
            table2=table1.values("textid").annotate(clout=F("count_divide")).order_by("-clout","-textid").first()
            textid=table2["textid"]
            hot_speech=speech_in_24h.filter(id=textid)
            for var in hot_speech:
                my_att=None
                cheer=0
                onlooker=0
                catcall=0
                list2=[]
                r = var.text
                textid = var.id
                uid=var.uid
                user=auth.models.User.objects.filter(pk=uid)
                if user.exists():
                    user.first()
                    username=user[0].username
                else:
                    username="用户不存在"
                d = str(var.date)[0:10]
                a=(datetime.datetime.strptime(d,"%Y-%m-%d")-datetime.datetime.strptime('2021-6-3',"%Y-%m-%d")).days
                b=str(var.date)[11:19]
                dbatt=speech_attitude.objects.filter(uid=attuid).filter(textid=textid)
                if dbatt.exists():
                    my_att=dbatt[0].att
                cheer=speech_attitude.objects.filter(textid=textid).filter(att=1).count()
                onlooker=speech_attitude.objects.filter(textid=textid).filter(att=2).count()
                catcall=speech_attitude.objects.filter(textid=textid).filter(att=3).count()
                clout=cheer+catcall
                list3=[]
                list2.append({"textid":textid,"text":r,"day":a,"time":b,"username":username,"my_attitude":my_att,"cheer":cheer,"onlooker":onlooker,"catcall":catcall,"clout":clout})
                num+=1
            status=1
            meg="热门演讲获取成功"
        else:
            meg="24小时内无人发言"
    else:
        meg='您还没有登录'
    result={
                "status":status,
                "message":meg,
                "data":{
                            "num":num,
                            "datalist":list2,
                        }
            }
    return HttpResponse(json.dumps(result), content_type="application/json")

def siwei(req):
    status = 0
    uid = None
    meg="失败"
    data={}
    sessionid=req.COOKIES.get("sessionid")
    if is_login(req,sessionid):
        session = Session.objects.filter(pk=sessionid).first()
        uid=session.get_decoded()["_auth_user_id"]

        siwei_db = None
        siwei = None

        siwei_db = personal_attributes.objects.order_by('id')
        siwei=personal_attributes.objects.filter(uid=uid)
        if siwei_db != None :
            if siwei !=None:
                meg ='成功'
                for var in siwei:
                    happy = var.happy
                    energy = var.energy
                    healthy = var.happy
                    Hunger = var.Hunger
                    status = 1
                    data={
                        "uid":uid,
                        "happy":happy,
                        "energy":energy,
                        "healthy":healthy,
                        "hunger":Hunger,
                    }
            else:
                if(uid != None ):
                    status = 1
                    meg = '新用户'
                    new_user_add = personal_attributes(uid =uid,energy = 100,healthy = 100,happy = 100 ,Hunger=100)
                    new_user_add.save()
                    data={
                        "uid":uid,
                        "happy":100,
                        "energy":100,
                        "healthy":100,
                        "hunger":100,
                    }
                else:
                    meg = '找不到用户资料'


        else:
            meg='数据库连接失败'


    else:
        meg='您还没有登录'
    
    result={
                "status":status,
                "message":meg,
                "data":data,
            }
    return HttpResponse(json.dumps(result), content_type="application/json")


def siwei_test(req):
    uid = 1
    siwei = None
    data = {}
    siwei_db = personal_attributes.objects.order_by('id')
    siwei=personal_attributes.objects.filter(uid=uid)
    if siwei_db != None and siwei !=None:
        for var in siwei:
            happy = var.happy
            energy = var.energy
            healthy = var.happy
            Hunger = var.Hunger
            data={
                "uid":uid,
                "happy":happy,
                "energy":energy,
                "healthy":healthy,
                "hunger":Hunger,
            }

    result={
                "status":"1",
                "message":"成功",
                "data":data,
            }
    return HttpResponse(json.dumps(result), content_type="application/json")

        
        


    






def logout(req):
    status = 0
    sessionid=req.COOKIES.get("sessionid")

    