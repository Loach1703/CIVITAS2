from django.shortcuts import redirect,render,HttpResponse
from TestModel.models import *

from SkillModel.models import UserSkill,social
from django.contrib.sessions.models import Session
from django.contrib import auth
from django.db.models import Avg,Max,Min,Count,Sum,F,Q
import datetime
import json
import random
import re
import math



def test(req):
    return render(req,"test.html")

#增加技能
#参数说明
#skill_now：当前技能
#type_buff：类型修正，范围0-1，如工作则为1，演讲为0.2，等等
#skill_level：门槛，学徒，匠人等
#happiness：当前快乐
#strategy_buff：工作策略加成，如果不是工作，则为1
def skill_increase(skill_now,type_buff,skill_level,happiness,strategy_buff=1):
    #技能增长e^(-技能等级/4)
    change = math.exp(-skill_now / 4)
    #进门槛降低技能增长速度
    if math.floor((skill_now / 4) + 1) > skill_level:
        diff = skill_now - skill_level * 4
        change *= (1 - math.sqrt(diff))
        #直接突破，临时的，以后要算概率
        skill_level += 1
    #快乐修正，20快乐-10%增长速度
    change *= (1 + ((happiness - 60) / 200))
    #类型修正
    change *= type_buff
    #工作策略修正
    change *= strategy_buff
    #返回值
    return skill_now + change,skill_level

#增加小类技能
#参数说明
#skill_mini_now：当前小类技能
#skill_now：当前技能
#type_buff：类型修正，范围0-1，如工作则为1，演讲为0.2，等等
#happiness：当前快乐
#strategy_buff：工作策略加成，如果不是工作，则为1
def skill_mini_increase(skill_mini_now,skill_now,type_buff,happiness,strategy_buff=1):
    #基础增长3%
    change = 0.03
    #当前技能每高12点，则增长速度翻一倍
    change *= 1 + (skill_now / 12)
    #当前小类技能越高，增长越慢，达到100%时增长速度减半
    change *= 1 - (skill_mini_now / 2)
    #快乐修正，20快乐-10%增长速度
    change *= (1 + ((happiness - 60) / 200))
    #类型修正
    change *= type_buff
    #工作策略修正
    change *= strategy_buff
    #返回值
    return skill_mini_now + change

#小类技能衰减，换日时调用
#参数说明
#skill_mini_now：当前小类技能
#skill_now：当前技能
def skill_mini_decrease(skill_mini_now,skill_now):
    #基础衰减2%+原小类的8%
    change = 0.02 + 0.08 * skill_mini_now
    #当前技能每高12点，衰减减慢一半
    change *= (1 / 2) ** (skill_now / 12)
    #返回值
    return skill_mini_now - change

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
            uid = req.GET.get("uid")
            if uid == None:
                userspeech = speech.objects.all()
            else:
                user=auth.models.User.objects.filter(pk=uid)
                if user.exists():
                    userspeech = speech.objects.filter(uid=uid)
                    if not userspeech.exists():
                        status=1
                        meg='该用户没有发过演讲'
                        result={
                            "status":status,
                            "message":meg,
                            "data":{}
                            }
                        return HttpResponse(json.dumps(result), content_type="application/json")
                else:
                    meg='对应uid的用户不存在'
                    result={
                        "status":status,
                        "message":meg,
                        "data":{}
                    }
                    return HttpResponse(json.dumps(result), content_type="application/json")
                
            page = int(req.GET.get("page"))
            count=len(userspeech)
            if count%num_every_page==0:
                total_page=count/num_every_page
            else:
                total_page=(count+num_every_page)//num_every_page
            if count-num_every_page*page<-num_every_page or page<=0:
                status=0
                meg='失败，错误的页数'
            else:
                list1 = userspeech.order_by('-id')[0+num_every_page*(page-1):num_every_page*page]
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
                        uid=int(uid)
                    else:
                        username="用户不存在"
                        uid=0
                    d = str(var.date)[0:10]
                    a=(datetime.datetime.strptime(d,"%Y-%m-%d")-datetime.datetime.strptime('2021-6-3',"%Y-%m-%d")).days
                    b=str(var.date)[11:19]
                    dbatt=speech_attitude.objects.filter(uid=attuid).filter(textid=textid)
                    if dbatt.exists():
                        my_att=int(dbatt[0].att)
                    cheer=speech_attitude.objects.filter(textid=textid).filter(att=1).count()
                    onlooker=speech_attitude.objects.filter(textid=textid).filter(att=2).count()
                    catcall=speech_attitude.objects.filter(textid=textid).filter(att=3).count()
                    list2.append({"textid":textid,"text":r,"day":a,"time":b,"uid":uid,"username":username,"my_attitude":my_att,"cheer":cheer,"onlooker":onlooker,"catcall":catcall})
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
    data={}
    sessionid=req.COOKIES.get("sessionid")
    if is_login(req,sessionid):
        session = Session.objects.filter(pk=sessionid).first()
        uid=session.get_decoded()["_auth_user_id"]
        text=req.POST.get("text")
        getuserstatus = personal_attributes.objects.filter(uid=uid).first()
        energy = eval(getuserstatus.energy)
        if energy - 15 < 0 :
            meg="发表失败，您当前的精力不足"
        else:
            if text!=None:
                if 0<len(text)<=300:
                    date=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    dbspeech = speech(text=text,date=date,uid=uid)
                    dbspeech.save()
                    getuserskill = UserSkill.objects.filter(user_id=uid).first()
                    skill_now = getuserskill.social.skill_num   #获取当前大类——社交技能点
                    skill_level = getuserskill.social.level   #获取当前大类技能等级
                    happiness = eval(getuserstatus.happy)         #获取当前用户幸福值
                    skill_mini_now = getuserskill.social.eloquence  #获取当前小类——雄辩技能点
                    skill_num_now , skill_level_now = skill_increase(skill_now,0.2,skill_level,happiness,strategy_buff=1)    #大类技能增加
                    mini_increase = skill_mini_increase(skill_mini_now,skill_now,0.2,happiness,strategy_buff=1)    #小类技能增加
                    #修改大类——社交技能点、大类技能等级、小类——雄辩技能点
                    usersocialskill = social.objects.filter(user_id=uid).first()
                    usersocialskill.skill_num = skill_num_now
                    usersocialskill.level = skill_level_now
                    usersocialskill.eloquence = mini_increase
                    getuserstatus.energy = energy - 15
                    usersocialskill.save()
                    getuserstatus.save()
                    status=1
                    meg="演讲发布成功"
                    data={"skill_num_change":skill_num_now,"level_change":skill_level_now,"eloquence_skill_change":mini_increase}
                else:
                    status=0
                    meg="失败，提交字数应该在1~300之间，当前字数：{}".format(len(text))
            else:
                status=0
                meg='失败，没有提供POST参数'
    else:
        status=0
        meg='您还没有登录'
    result={
                "status":status,
                "message":meg,
                "data":data,
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

    #热门演讲
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
                    uid=int(uid)
                else:
                    username="用户不存在"
                    uid=0
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
                list2.append({"textid":textid,"text":r,"day":a,"time":b,"uid":uid,"username":username,"my_attitude":my_att,"cheer":cheer,"onlooker":onlooker,"catcall":catcall,"clout":clout})
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

#显示四维和换日回复值
def siwei(req):
    status = 0
    uid = None
    meg="失败"
    data={}
    sessionid=req.COOKIES.get("sessionid")
    if is_login(req,sessionid):
        session = Session.objects.filter(pk=sessionid).first()
        uid=int(session.get_decoded()["_auth_user_id"])

        siwei_db = None
        siwei = None

        siwei_db = personal_attributes.objects.order_by('id')
        siwei=personal_attributes.objects.filter(uid=uid).first()
        if siwei_db != None :
            if siwei.exists():
                meg ='成功'
                for var in siwei:
                    happy = eval(var.happy)
                    energy = eval(var.energy)
                    healthy = eval(var.healthy)
                    Hunger = eval(var.Hunger)
                    status = 1
                    data={
                        "stamina":energy,
                        "happiness":happy,
                        "health":healthy,
                        "starvation":Hunger,
                    }
                reply_data = status_recover(energy,happy,healthy,Hunger,0,1)
            else:
                if(uid != None ):
                    status = 1
                    meg = '新用户'
                    new_user_add = personal_attributes(uid = uid,energy = 100,healthy = 100,happy = 100 ,Hunger=100)
                    new_user_add.save()
                    data={
                        "happiness":100,
                        "stamina":100,
                        "health":100,
                        "starvation":100,
                    }
                    reply_data = status_recover(100,100,100,100,0,1)
                else:
                    meg = '找不到用户资料'


        else:
            meg='数据库连接失败'


    else:
        meg='您还没有登录'
    
    result={
                "status":status,
                "message":meg,
                "data":{"uid":uid,"today":data,"tomorrow":reply_data},
            }
    return HttpResponse(json.dumps(result), content_type="application/json")

def status_recover(stamina,happiness,health,starvation,house_type,house_level):
    #睡大街
    if house_type == 0:
        stamina_house_bonus = 0
        happiness_house_bonus = 0
        health_house_bonus = 0
    #楼房
    if house_type == 1:
        stamina_house_bonus = 10 * house_level
        happiness_house_bonus = 0.4 * (house_level - 1)
        health_house_bonus = 0.4 * (house_level - 1)
    #宅院
    if house_type == 2:
        stamina_house_bonus = 10 * house_level
        happiness_house_bonus = 0.2 + 0.6 * (house_level - 1)
        health_house_bonus = 0.2 + 0.6 * (house_level - 1)
    stamina_change = (30 + stamina_house_bonus) * (1 + ((health - 60) / 80))
    happiness_change = 3 + 0.2 * (min(60,starvation,health) - happiness) + 0.05 * (max(0,stamina + stamina_change - 100)) + happiness_house_bonus
    health_change = 3 + 0.2 * (min(60,starvation,stamina + 40) - health) + 0.05 * (max(0,stamina + stamina_change - 100)) + health_house_bonus
    starvation_change = -(0.08 * starvation + 2)
    really_stamina_change = stamina_change
    really_happiness_change = happiness_change
    really_health_change = health_change
    really_starvation_change = starvation_change
    #处理超界
    if stamina + stamina_change > 100:
        really_stamina_change = 100 - stamina
    elif stamina + stamina_change < 0:
        really_stamina_change = stamina
    if happiness + happiness_change > 100:
        really_happiness_change = 100 - happiness
    elif happiness + happiness_change < 0:
        really_happiness_change = happiness
    if health + health_change > 100:
        really_health_change = 100 - health
    elif health + health_change < 0:
        really_health_change = health
    if starvation + starvation_change > 100:
        really_starvation_change = 100 - starvation
    elif starvation + starvation_change < 0:
        really_starvation_change = starvation
    stamina += really_stamina_change
    happiness += really_happiness_change
    health += really_health_change
    starvation += really_starvation_change
    stamina = round(stamina,1)
    happiness = round(happiness,1)
    health = round(health,1)
    starvation = round(starvation,1)
    really_stamina_change = round(really_stamina_change,1)
    really_happiness_change = round(really_happiness_change,1)
    really_health_change = round(really_health_change,1)
    really_starvation_change = round(really_starvation_change,1)
    reply_data = {
        "stamina":stamina,
        "happiness":happiness,
        "health":health,
        "starvation":starvation,
        "stamina_change":really_stamina_change,
        "happiness_change":really_happiness_change,
        "health_change":really_health_change,
        "starvation_change":really_starvation_change,
    }
    return reply_data
#工作
def work(req):
    uid =None
    status = 0
    meg = "失败"
    data={}
    sessionid=req.COOKIES.get("sessionid")
    if is_login(req,sessionid):
        session = Session.objects.filter(pk=sessionid).first()
        uid=int(session.get_decoded()["_auth_user_id"])
        work_record_db = None
        work_record_list = None
        #work_record_db = personal_attributes.objects.order_by('id')
        work_record_list=work_record.objects.filter(uid=uid).first()
        if work_record_list.exists():
            work_id =work_record_list.work_id
            work_station_id = work_record_list.work_station_id
            work_date = work_record_list.work_date
            d=datetime.datetime.now().strftime('%Y-%m-%d')
            today=(datetime.datetime.strptime(d,"%Y-%m-%d")-datetime.datetime.strptime('2021-6-3',"%Y-%m-%d")).days
            if today != work_date:
                
                #获得工作策略
                #工作策略id=req.POST.get("工作策略")
                    #work-四维消耗
                        #修改四维值
                    #work-技能增长
                        #技能增长
                            #是否突破
                            #return 新技能值数据
                    #work-获得产物
                            #return 产出数据

                meg = "成功"
                work_record.work_date = today
                work_record.save()
                status = 1
                data ={
                    'work_id':work_id,
                    'work_station_id':work_station_id,
                    'work_date':work_date,
                    #'技能类':技能类
                    #'产出类':产出类


                }
            else:
                meg = "您今天已经工作了，无法继续工作"
        else:
            meg = "请先获得工作" 
    else:
        meg='您还没有登录'
    
    result={
            "status":status,
            "message":meg,
            "data":data,
        }
    return HttpResponse(json.dumps(result), content_type="application/json")

#副业
def get_sideline(req):
    uid =None
    status = 0
    meg = "失败"
    #data={}
    sessionid=req.COOKIES.get("sessionid")
    if is_login(req,sessionid):
        session = Session.objects.filter(pk=sessionid).first()
        uid=int(session.get_decoded()["_auth_user_id"])
        
        sideline_list=sideline.objects.filter(uid=uid).first()
        if not sideline.exists():
            create_sideline(uid)
            
        sideline_id=req.POST.get("sideline_id")
        if 1<int(sideline_id)<10:
            t1={
                1:{"name":{1:"采集",2:"gather"},"skills":{1:2},"miniskills":{1:1}} #野外采集，暂时，需要技能id-2的采伐技能，并且需要2-1小类，采集技能。
            }
            db_list_name = t1[sideline_id]["name"][2]
            sideline_list=sideline.objects.filter(db_list_name).first()
            skilldata_now = None
            for i in t1[sideline_id]["skills"]:
                if skilldata_now == None:
                    skilldata_now = change_skill(uid,t1[sideline_id]["skills"][i],t1[sideline_id]["miniskills"][i])
                else:
                    skilldata_now += change_skill(uid,t1[sideline_id]["skills"][i],t1[sideline_id]["miniskills"][i])

            meg = "成功"
            #产出函数
            #.
            #.
            #.
            
            status = 1
            sideline.objects
        
        else:
            meg='副业代码错误'
    else:
        meg='您还没有登录'
    
    result={
            "status":status,
            "message":meg,
            "data":skilldata_now,
        }
    return HttpResponse(json.dumps(result), content_type="application/json")
    
def change_skill(uid,skill_id,skill_mini_id):
    getuserstatus = personal_attributes.objects.filter(uid=uid).first()#获得uid=uid的四维属性db的句柄
    

    t1={
                1:{"name":"耕作","data":{1:"粮食种植",2:"蔬果种植",3:"经济作物种植",4:"开垦"}},
                2:{"name":"采伐","data":{1:"采集",2:"伐木",3:"开采",4:"勘探"}},
                3:{"name":"建设","data":{1:"建筑",2:"修缮"}},
                4:{"name":"加工","data":{1:"冶炼",2:"金属锻造",3:"纺织",4:"食品加工",5:"木石加工"}},
                5:{"name":"社交","data":{1:"雄辩",2:"交际",3:"文书",4:"管理"}},
                6:{"name":"舟车","data":{1:"陆上运输",2:"水上运输",3:"捕捞"}},
                7:{"name":"畜牧","data":{1:"狩猎",2:"家禽养殖",3:"家畜养殖"}},
            }
    t2={
            1:{'name':'farming','data':{1:'grain',2:'vegetables_fruit',3:'cash_crops',4:'reclaim'}},
            2:{'name':'cutting','data':{1:'collection',2:'lumbering',3:'exploitation',4:'prospecting'}},
            3:{'name':'construct','data':{1:'building',2:'mending'}},
            4:{'name':'processing','data':{1:'smelt',2:'forge',3:'spin',4:'food_processing',5:'wood_stone_processing'}},
            5:{'name':'social','data':{1:'eloquence',2:'communicate',3:'write',4:'manage'}},
            6:{'name':'vehicle','data':{1:'land_transport',2:'water_transport',3:'fishing'}},
            7:{'name':'husbandry','data':{1:'hunt',2:'fowl',3:'livestock'}},
        }
    getuserskill_1 = UserSkill.objects.filter(user_id=uid)
    getuserskill = getuserskill_1.vehicle_
    #.objects.filter(t2[skill_id]['name'])#获得user_id=uid的技能属性总表db的句柄
    

    skill_now = getuserskill.skill_num   #获取当前大类——社交技能点 #skill_now = getuserskill.object.filter(user_id=uid).skill_num 
    skill_level = getuserskill.level   #获取当前大类技能等级
    happiness = eval(getuserstatus.happy)         #获取当前用户幸福值
    skill_mini_now = getuserskill.filter(t2[skill_id]['data'][skill_mini_id]) #获取当前小类—技能
    energy= eval(getuserstatus.energy)

    skill_num_now , skill_level_now = skill_increase(skill_now,0.2,skill_level,happiness,strategy_buff=1)    #大类技能增加
    mini_increase = skill_mini_increase(skill_mini_now,skill_now,0.2,happiness,strategy_buff=1)    #小类技能增加

    #修改大类——技能点、大类技能等级、小类——技能点
    #usersocialskill = social.objects.filter(user_id=uid).first()
    getuserskill.skill_num = skill_num_now
    getuserskill.level = skill_level_now
    getuserskill.filter(t2[skill_id]['data'][skill_mini_id]) = mini_increase
    energy= getuserstatus.energy
    getuserstatus.energy = energy - 15
    getuserskill.save()
    getuserstatus.save()
    data={"skill_num_change":skill_num_now,"level_change":skill_level_now,"mini_skill_change":mini_increase}
    return data



# def siwei_test(req):
#     uid = 1
#     siwei = None
#     data = {}
#     siwei_db = personal_attributes.objects.order_by('id')
#     siwei=personal_attributes.objects.filter(uid=uid)
#     if siwei_db != None and siwei !=None:
#         for var in siwei:
#             happy = var.happy
#             energy = var.energy
#             healthy = var.happy
#             Hunger = var.Hunger
#             data={
#                 "uid":uid,
#                 "happy":happy,
#                 "energy":energy,
#                 "healthy":healthy,
#                 "hunger":Hunger,
#             }

#     result={
#                 "status":"1",
#                 "message":"成功",
#                 "data":data,
#             }
#     return HttpResponse(json.dumps(result), content_type="application/json")

def logout1(req):
    status=0
    mes="失败"
    sessionid=req.COOKIES.get("sessionid")
    if is_login(req,sessionid):
        filter_sessionid=Session.objects.filter(pk=sessionid)
        if filter_sessionid.exists():
            filter_usersessionid=usersession.objects.filter(sessionid=sessionid)
            if filter_sessionid.exists():
                filter_usersessionid.delete()
            req.session.flush()
            status=1
            meg="注销成功"
    else:
        meg="您还没有登录"
    result={
                "status":status,
                "message":meg,
            }
    return HttpResponse(json.dumps(result), content_type="application/json")

    