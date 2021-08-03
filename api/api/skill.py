from SkillModel.models import UserSkill,create_skill,get_skill
from django.contrib.sessions.models import Session
from django.contrib import auth
from django.shortcuts import redirect,render,HttpResponse
import json

def is_login(req,sessionid):
    if not sessionid:
        return 0
    if not req.session.exists(sessionid):
        return 0
    return 1

def getUserSkill(req):
    status  = 0
    meg = "失败"
    data = []
    sessionid = req.COOKIES.get("sessionid")
    if is_login(req,sessionid):
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
                1:{1:"grain",2:"vegetables_fruit",3:"cash_crops",4:"reclaim"},
                2:{1:"collection",2:"lumbering",3:"exploitation",4:"prospecting"},
                3:{1:"building",2:"mending"},
                4:{1:"smelt",2:"forge",3:"spin",4:"food_processing",5:"wood_stone_processing"},
                5:{1:"eloquence",2:"communicate",3:"write",4:"manage"},
                6:{1:"land_transport",2:"water_transport",3:"fishing"},
                7:{1:"hunt",2:"fowl",3:"livestock"},
            }
        session = Session.objects.filter(pk=sessionid).first()
        uid = session.get_decoded()["_auth_user_id"]
        user_detail = auth.models.User.objects.filter(pk=uid).first()
        userskill = UserSkill.objects.filter(user__id=uid)
        if not userskill.exists():
            create_skill(user_detail)
        for i in t1:
            d=get_skill(user_detail)
            l=[]
            for j in t1[i]["data"]:
                l.append({
                    "name":t1[i]["data"][j],
                    "id":j,
                    "skill":d[i].__dict__[t2[i][j]]
                })
            data.append({
                "name":t1[i]["name"],
                "id":i,
                "skill":d[i].__dict__["skill_num"],
                "level":d[i].__dict__["level"],
                "list":l
            })
        status = 1
        meg = "获取成功"
    else:
        meg='您还没有登录'
    result={
        "status":status,
        "message":meg,
        "data":data
    }
    return HttpResponse(json.dumps(result), content_type="application/json")