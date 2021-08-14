from django.shortcuts import redirect,render,HttpResponse
from SpeechModel.models import Speech,SpeechAttitude,Topic
from UserModel.models import personal_attributes
from SkillModel.models import UserBigSkill,UserSmallSkill,SkillName
from django.contrib.sessions.models import Session
from django.contrib import auth
from django.db.models import Count,F,Q,Sum,Max
from assist import *
import datetime
import json
import re

def getspeech1(req):    #获取演讲，参数：page
    num_every_page=10
    status=0
    meg='失败'
    list2=[]
    total_page=0
    num=0
    sessionid=req.COOKIES.get("sessionid")
    topic_name = None
    topicid = None
    if is_login(req,sessionid):
        uid = req.GET.get("uid")
        topicid = req.GET.get("tagid")
        if req.GET.get("page")!=None:
            page = is_int(req.GET.get("page"))                                              #判断page是不是数字
            if page == "error":
                meg = "存在需要传入数字的参数传入的不是数字"
                result={
                    "status":status,
                    "message":meg,
                    "data":{}
                }
                return HttpResponse(json.dumps(result), content_type="application/json")
            userspeech = Speech.objects.all()
            if topicid != None:                                                             #判断有没有提供topicid
                topicid = is_int(req.GET.get("tagid"))
                if topicid == "error":                                                      #判断topicid是不是数字
                    meg = "存在需要传入数字的参数传入的不是数字"
                    result={
                        "status":status,
                        "message":meg,
                        "data":{}
                    }
                    return HttpResponse(json.dumps(result), content_type="application/json")
                else:                                                                       
                    speech_topic = Topic.objects.filter(pk=topicid)
                    if not speech_topic.exists():
                        status=0
                        meg='对应topicid的话题不存在'
                        result={
                            "status":status,
                            "message":meg,
                            "data":{}
                            }
                        return HttpResponse(json.dumps(result), content_type="application/json")
                    else:                                                                     #以topicid筛选演讲
                        speech_topic = speech_topic.first()
                        userspeech = speech_topic.speech.all()
                        topic_name = speech_topic.topic_name
            if uid != None:                                                                     #以uid筛选演讲
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
                    userspeech = userspeech.filter(user_id=uid)
                    if not userspeech.exists():
                        status=1
                        if topicid != None:
                            meg='该用户没有对该话题发过演讲'
                        else:
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
            session = Session.objects.filter(pk=sessionid).first()
            uid = session.get_decoded()["_auth_user_id"]
            user=auth.models.User.objects.get(pk=uid)
            count=len(userspeech)                                                                       #演讲展示部分
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
                    textid = var.id
                    uid = var.user_id
                    username = var.user.username
                    cheer = var.cheer
                    onlooker = var.onlooker
                    catcall = var.catcall
                    clout = cheer + onlooker + catcall
                    get_att = var.speechattitude_set.filter(user=user)
                    if get_att.exists():
                        my_att = get_att[0].att
                    r = var.text
                    speech_topic = var.topic_set.all()
                    for st in speech_topic:
                        r = r.replace('#'+st.topic_name+'#','<a href="speechtag.html?tagid={0}">{1}</a>'.format(st.id,'#'+st.topic_name+'#'))
                    d = str(var.date)[0:10]
                    a=(datetime.datetime.strptime(d,"%Y-%m-%d")-datetime.datetime.strptime('2021-6-3',"%Y-%m-%d")).days
                    b=str(var.date)[11:19]
                    list2.append({"textid":textid,"text":r,"day":a,"time":b,"uid":uid,"username":username,"my_attitude":my_att,"cheer":cheer,"onlooker":onlooker,"catcall":catcall,"clout":clout})
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
                            "tagid":topicid,
                            "tagname":topic_name,
                            "datalist":list2,
                        }
            }
    return HttpResponse(json.dumps(result), content_type="application/json")

def speech1(req):   #发送演讲，参数：text
    status=0
    meg="失败"
    data = {}
    sessionid=req.COOKIES.get("sessionid")
    if is_login(req,sessionid):
        session = Session.objects.filter(pk=sessionid).first()
        uid = session.get_decoded()["_auth_user_id"]
        user = auth.models.User.objects.get(pk=uid)
        text = req.POST.get("text")
        getuserstatus = personal_attributes.objects.filter(uid=uid).first()
        energy = eval(getuserstatus.energy)
        if energy - 15 < 0 :
            meg="发表失败，您当前的精力不足"
        else:
            if text!=None:
                if 0<len(text)<=300:
                    #存储演讲数据
                    text=re.sub(r'</?\w+[^>]*>','',text)
                    templist = re.findall('#[^#].*?#',text)
                    if templist:
                        topiclist = list(set(templist))
                        topiclist.sort(key=templist.index)
                        for i in range(len(topiclist)):
                            templist[i] = topiclist[i].strip('#').strip()
                            text = text.replace(topiclist[i],'#'+templist[i]+'#')
                        dbspeech = Speech.objects.create(user=user,text=text)
                        try:
                            templist.remove('')
                        except:
                            pass
                        topiclist = list(set(templist))
                        topiclist.sort(key=templist.index)
                        #提取演讲话题
                        t=0
                        for i in topiclist:
                            dbtopic_get = Topic.objects.get_or_create(topic_name=i)
                            dbtopic_get[0].speech.add(dbspeech)
                            dbtopic_get[0].save()
                            t+=1
                            if t==5:
                                break
                    else:
                        dbspeech = Speech.objects.create(user=user,text=text)
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
    attdict={1:"欢呼",2:"关注",3:"倒彩"}
    if is_login(req,sessionid):
        if att==None or textid==None:
            meg="缺少必要参数"
        else:
            att = is_int(att)
            if att == "error":
                meg = "存在需要传入数字的参数传入的不是数字"
                result={
                    "status":status,
                    "message":meg,
                    "data":{}
                }
                return HttpResponse(json.dumps(result), content_type="application/json")
            if att==1 or att==2 or att==3:
                now = datetime.datetime.now()
                getspeech = Speech.objects.filter(pk=textid,date__gte=now-datetime.timedelta(days=1),date__lte=now)
                if getspeech.exists():
                    session=Session.objects.filter(pk=sessionid).first()
                    uid=session.get_decoded()["_auth_user_id"]
                    getatt = SpeechAttitude.objects.filter(speech_id=textid).filter(user_id=uid)
                    if getatt.exists():
                        if getatt.first().att==att:
                            getatt.delete()
                            getspeech = getspeech.filter(pk=textid).first()
                            if att == 1:
                                getspeech.cheer = F('cheer') - 1
                            elif att == 2:
                                getspeech.onlooker = F('onlooker') - 1
                            elif att == 3:
                                getspeech.catcall = F('catcall') - 1
                            getspeech.save()
                            meg="您已经撤销对这个演讲的态度"
                        else:
                            meg="您已经对这个演讲发表过态度了,请先取消之前的态度再点击"
                    else:
                        user = auth.models.User.objects.get(pk=uid)
                        speech_instance = Speech.objects.get(pk=textid)
                        sendatt=SpeechAttitude(user=user,speech=speech_instance,att=att)
                        sendatt.save()
                        getspeech = getspeech.filter(pk=textid).first()
                        if att == 1:
                            getspeech.cheer = F('cheer') + 1
                        elif att == 2:
                            getspeech.onlooker = F('onlooker') + 1
                        elif att == 3:
                            getspeech.catcall = F('catcall') + 1
                        getspeech.save()
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
    speech_in_24h=Speech.objects.filter(date__gte=now-datetime.timedelta(days=1),date__lte=now)
    num=0
    sessionid=req.COOKIES.get("sessionid")
    if is_login(req,sessionid):
        session = Session.objects.filter(pk=sessionid).first()
        attuid=session.get_decoded()["_auth_user_id"]
        user = auth.models.User.objects.get(pk=attuid)
        if speech_in_24h.exists():
            satisfied_attitude=speech_in_24h.annotate(clout=F("cheer")+F("onlooker")+F("catcall"))
            maxclout=satisfied_attitude.aggregate(max=Max("clout"))["max"]
            hot_speech=satisfied_attitude.filter(clout=maxclout)
            for var in hot_speech:
                list2=[]
                my_att=None
                cheer=0
                onlooker=0
                catcall=0
                textid = var.id
                uid = var.user_id
                username = var.user.username
                cheer = var.cheer
                onlooker = var.onlooker
                catcall = var.catcall
                clout = cheer + onlooker + catcall
                get_att = var.speechattitude_set.filter(user=user)
                if get_att.exists():
                    my_att = get_att[0].att
                r = var.text
                speech_topic = var.topic_set.all()
                for st in speech_topic:
                    r = r.replace('#'+st.topic_name+'#','<a href="speechtag.html?tagid={0}">{1}</a>'.format(st.id,'#'+st.topic_name+'#'))
                d = str(var.date)[0:10]
                a=(datetime.datetime.strptime(d,"%Y-%m-%d")-datetime.datetime.strptime('2021-6-3',"%Y-%m-%d")).days
                b=str(var.date)[11:19]
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