from django.shortcuts import redirect,render,HttpResponse
from SpeechModel.models import speech,speech_attitude
from UserModel.models import personal_attributes
from SkillModel.models import UserBigSkill,UserSmallSkill,SkillName
from django.contrib.sessions.models import Session
from django.contrib import auth
from django.db.models import Count,F
from assist import *
import datetime
import json


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
        uid = req.GET.get("uid")
        if req.GET.get("page")!=None:
            page = is_int(req.GET.get("page"))
            if page == "error":
                meg = "存在需要传入数字的参数传入的不是数字"
                result={
                    "status":status,
                    "message":meg,
                    "data":{}
                }
                return HttpResponse(json.dumps(result), content_type="application/json")
            if uid == None:
                userspeech = speech.objects.all()
            else:
                uid = is_int(req.GET.get("uid"))
                if uid == "error":
                    meg = "存在需要传入数字的参数传入的不是数字"
                    result={
                        "status":status,
                        "message":meg,
                        "data":{}
                    }
                    return HttpResponse(json.dumps(result), content_type="application/json")
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
                    #UserBigSkill,UserSmallSkill,SkillName
                    getuserbigskill = UserBigSkill.objects.filter(user_id=uid).first()
                    skill_now = getuserbigskill.shejiao                                     #获取当前大类——社交技能点
                    skill_level = getuserbigskill.shejiao_level                             #获取当前大类技能等级
                    getusersmallskill = UserSmallSkill.objects.filter(user_id=uid).first()
                    happiness = eval(getuserstatus.happy)                                   #获取当前用户幸福值
                    skill_mini_now = getusersmallskill.xiongbian                            #获取当前小类——雄辩技能点
                    skill_num_now , skill_level_now = skill_increase(skill_now,0.2,skill_level,happiness,strategy_buff=1)    #大类技能增加
                    mini_increase = skill_mini_increase(skill_mini_now,skill_now,0.2,happiness,strategy_buff=1)    #小类技能增加
                    #修改大类——社交技能点、大类技能等级、小类——雄辩技能点
                    getuserbigskill.shejiao = skill_num_now
                    getuserbigskill.shejiao_level = skill_level_now
                    getusersmallskill.xiongbian = mini_increase
                    getuserstatus.energy = energy - 15
                    getuserbigskill.save()
                    getusersmallskill.save()
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
                now = datetime.datetime.now()
                if speech.objects.filter(pk=textid,date__gte=now-datetime.timedelta(days=1),date__lte=now).exists():
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
                    meg="您将要发表观点的演讲不存在或已经超过24小时"
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