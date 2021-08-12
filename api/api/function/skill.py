from django.contrib.sessions.models import Session
from SkillModel.models import UserBigSkill,UserSmallSkill,SkillName
from django.contrib import auth
from django.shortcuts import redirect,render,HttpResponse
from django.forms.models import model_to_dict
import json
from assist import *

def getUserSkill(req):
    status  = 0
    meg = "失败"
    datalist = []
    sessionid = req.COOKIES.get("sessionid")
    if is_login(req,sessionid):
        # t1={
        #         1:{"name":"耕作","data":{1:"粮食种植",2:"蔬果种植",3:"经济作物种植",4:"开垦"}},
        #         2:{"name":"采伐","data":{1:"采集",2:"伐木",3:"开采",4:"勘探"}},
        #         3:{"name":"建设","data":{1:"建筑",2:"修缮"}},
        #         4:{"name":"加工","data":{1:"冶炼",2:"金属锻造",3:"纺织",4:"食品加工",5:"木石加工"}},
        #         5:{"name":"社交","data":{1:"雄辩",2:"交际",3:"文书",4:"管理"}},
        #         6:{"name":"舟车","data":{1:"陆上运输",2:"水上运输",3:"捕捞"}},
        #         7:{"name":"畜牧","data":{1:"狩猎",2:"家禽养殖",3:"家畜养殖"}},
        #     }
        uid = req.GET.get("uid")
        if uid == None:                         #判断是否提供uid，没有则读取登录用户的uid
            session = Session.objects.filter(pk=sessionid).first()
            uid = session.get_decoded()["_auth_user_id"]
        uid = is_int(uid)                       #判断uid是否为非数字
        if uid == "error":                      #如果uid非数字，返回错误信息
            meg = "存在需要传入数字的参数传入的不是数字"
            result = {
                "status":status,
                "message":meg,
                "data":datalist
            }
            return HttpResponse(json.dumps(result), content_type="application/json")
        user = auth.models.User.objects.get(pk=uid)
        getbigskill = UserBigSkill.objects.get_or_create(user=user)[0]
        getsmallskill = UserSmallSkill.objects.get_or_create(user=user)[0]
        bigskilldict = model_to_dict(getbigskill)
        smallskilldict = model_to_dict(getsmallskill)
        bigskill = list(bigskilldict.values())[2::]
        smallskill = list(smallskilldict.values())[2::]
        datalist = []
        t = 0
        for i in range(1,(int(len(bigskill)/2)+1)):
            big_skillnum = bigskill[2*i-2]
            getname = SkillName.objects.filter(big_id=i)
            if big_skillnum:
                small_skill_count = len(getname) + 1
                name_object = getname.first()
                bigname = name_object.big_name
                big_level = bigskill[2*i-1]
                small_skill_list = []
                for j in range(1,small_skill_count):
                    small_skillnum = smallskill[t+j-1]
                    if small_skillnum:
                        getsmallname = getname.filter(small_id=j)
                        name_object = getsmallname.first()
                        smallname = name_object.small_name
                        small_skill_list.append({'id':j,'name':smallname,'skill':small_skillnum})
                datalist.append({'id':i,'name':bigname,'skill':big_skillnum,'level':big_level,'list':small_skill_list})
            t += len(getname)
        status = 1
        meg = '查询技能成功'
        result = {
                "status":status,
                "message":meg,
                "data":datalist
            }
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        meg = "您还没有登录"