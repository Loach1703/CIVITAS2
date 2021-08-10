from django.shortcuts import redirect,render,HttpResponse
from assist import *
from django.contrib.sessions.models import Session
from django.contrib import auth
from WorkModel.models import *
from UserModel.models import *
import json
import datetime


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