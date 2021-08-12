
from django.db.models.query_utils import Q
from django.shortcuts import redirect,render,HttpResponse
from SkillModel.models import SkillName, UserBigSkill, UserSmallSkill
from assist import *
from django.contrib.sessions.models import Session
from django.contrib import auth

from api.models.UserModel.models import *
from api.models.WorkModel.models import *

import json
import datetime


#工作#未完成
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
        #调用该玩家副业统计表
        sideline_list=sideline_record.objects.filter(user_id=uid)
        if not sideline_record.exists():
            create_sideline(uid)
        #检查副业日期，重置
        if(sideline_list.sideline_day != datetime.datetime.now().strftime('%Y-%m-%d')):
            sideline_list.number_of_today_sideline = 0
        #调用副业id
        sideline_id=req.POST.get("sideline_id")
        sideline = sideline_work.objects.filter(sideline_id)
        
        if(sideline_xiaohao(uid,sideline_id,sideline_list.number_of_today_sideline) == 0 ):
            if sideline.exists():
                #调用，需要的技能大类，小类，产能，各技能增长效率，产能算法种类
                bigskills = str(sideline.sideline_bigskills).split()
                smallskills = str(sideline.sideline_smallskills).split()
                coefficient = str(sideline.sideline_coefficient).split()
                skills_increase_type = None
                skills_increase_type = str(sideline.sideline_skills_increase).split()
                c_type = None
                c_type = sideline.c_type
                #

                len_1 = len(bigskills)
                len_2 = len(smallskills)
                len_3 = len(coefficient)
                
                if(len_1 == len_2 == len_3  and (c_type!= None)):
                    capacity= 0 
                    for i in len_1:
                        #产能计算
                        capacity += sideline_capacity(uid,bigskills[i],smallskills[i],coefficient[i],c_type)

                        #技能增长计算
                        if len(skills_increase_type)>0:
                            sideline_skill_increase(uid,bigskills[i],smallskills[i],skills_increase_type[i])
                        else:
                            sideline_skill_increase(uid,bigskills[i],smallskills[i],1)

                    
                    #产出函数
                    #副业产出物品id
                    sideline_product = str(sideline.sideline_product).split()#*str
                    #副业产出物品的各比例
                    sideline_product_probability = str(sideline.sideline_product_probability).split()#*str
                    #.
                    #.
                    #.

                    #统计
                    sideline_list.sideline_day = datetime.datetime.now().strftime('%Y-%m-%d')
                    
                    today=(datetime.datetime.strptime(d,"%Y-%m-%d")-datetime.datetime.strptime('2021-6-3',"%Y-%m-%d")).days
                    sideline.sidline_day_c = today
                    
                    sideline.number_of_all_sideline +=1
                    # sideline.every_sideline_all 正式版上线之后做
                    




                    meg = "成功"
                    status = 1

                    data ={
                        'name':sideline.sideline_name,
                        'capacity':capacity
                        
                    }
                    
                else:
                    meg = '数据库数据设置错误'
                
            else:
                meg='副业代码错误'
        else:
            meg='四维属性不够进行副业'
    else:
        meg='您还没有登录'
    
    result={
            "status":status,
            "message":meg,
            "data":data,
        }
    return HttpResponse(json.dumps(result), content_type="application/json")


#副业产能计算
#coefficient 副业数据库的各技能产能系数
#c_type 0：采用数据库系数算法，1：采用通用产能算法
def sideline_capacity(uid,skill_id,skill_mini_id,coefficient,c_type = 0):
    #获得uid=uid的四维属性db的句柄
    getuserstatus = personal_attributes.objects.filter(uid=uid).first()
    #获得主技能 dbname
    bigskillsname = SkillName.objects.filter(big_id = skill_id).first().db_big_name
    #获得主技能具体数值
    bigskill = UserBigSkill.objects.filter(user_id=uid).values(bigskillsname)[0].values()#dict.values()
    if c_type == 0:
        if skill_mini_id != 0 :
            #获得小技能 dbname
            smallskillname = SkillName.objects.filter(big_id = skill_id,
                                                        small_id = skill_mini_id).first().db_small_name
            #获得小技能具体数值
            smallskill = UserSmallSkill.objects.filter(user_id=uid).values(smallskillname)[0].values()#dict.values()

            capacity = smallskill *coefficient
            
            
        else:
            capacity = bigskill * coefficient
    else:
         #获得小技能 dbname
        smallskillname = SkillName.objects.filter(big_id = skill_id,
                                                    small_id = skill_mini_id).first().db_small_name
        #获得小技能具体数值
        smallskill = UserSmallSkill.objects.filter(user_id=uid).values(smallskillname)[0].values()#dict.values()
        capacity = capacity_calculation(bigskill,smallskill,1,getuserstatus.happy)
    
    return capacity

#产能参考
def capacity_calculation(skill_now,skill_mini_now,type_buff,happiness,strategy_buff=1):
    #基础产能：8+(大类技能/2)^0.85次方*(1+小类技能/2)，即小类技能最高加成为50%
    capacity = 8 + (skill_now / 2) ** 0.85 * (1 + skill_mini_now / 2)
    #类型修正
    capacity *= type_buff
    #快乐修正，20快乐-10%增长速度
    capacity *= (1 + ((happiness - 60) / 200))
    #工作策略修正
    capacity *= strategy_buff
    #返回值
    return capacity

#副业技能增加
def sideline_skill_increase(uid,big_skill_id,mini_skill_id,type_buff):

    #获得uid=uid的四维属性db的句柄
    getuserstatus = personal_attributes.objects.filter(uid=uid).first()
    happiness = getuserstatus.happy
    #获得主技能dbname
    big_skill_name = SkillName.objects.filter(big_id = big_skill_id).first().db_big_name
    #获得主技能数值
    bigskill = UserBigSkill.objects.filter(user_id=uid).values(big_skill_name)[0].values()#dict.values()
    #获得主技能门槛dbname
    big_skill_level_name = big_skill_name + '_level'
    #获得主技能门槛数值
    big_skill_level = UserBigSkill.objects.filter(user_id=uid).values(big_skill_level_name)[0].values()#dict.values()

    if mini_skill_id != 0:
        #获得小技能 dbname
        smallskillname = SkillName.objects.filter(big_id = mini_skill_id,
                                                    small_id = mini_skill_id).first().db_small_name
        #获得小技能具体数值
        smallskill = UserSmallSkill.objects.filter(user_id=uid).values(smallskillname)[0].values()#dict.values()
        #获得新的小技能数值
        new_mini_skill = skill_mini_increase(smallskill,bigskill,type_buff,happiness)
        #更改小技能数值到表
        UserSmallSkill.objects.filter(user_id=uid).update(smallskillname = new_mini_skill)
    
    #获得新小技能数值
    new_big_skill = skill_increase(bigskill,type_buff,big_skill_level,happiness)
    #更改大技能到表
    UserBigSkill.objects.filter(user_id=uid).update(big_skill_name = new_big_skill)

    return 0 

def sideline_xiaohao(uid,sideline_id,item):
    getuserstatus = personal_attributes.objects.filter(uid=uid).first()
    #获得副业句柄
    sideline = sideline_record.objects.filter(sideline_id = sideline_id)
    #需要的四维属性 *副业次数（暂时是每次副业次数消耗翻倍）
    if(len(sideline.sideline_happy)):
        need_happy = sideline.sideline_happy *item
        need_healthy = sideline.sideline_health *item
        need_energy = sideline.sideline_energy*item
    else:
        need_happy = 15 *item
        need_healthy = 15 *item
        need_energy = 15 *item
    if((getuserstatus.energy> need_energy) and (getuserstatus.happy >need_happy) and (getuserstatus.healthy >need_healthy)):
        getuserstatus.energy -= need_energy
        getuserstatus.happy -= need_happy
        getuserstatus.healthy -= need_healthy
        getuserstatus.save()
        return 0
    else:
        return '四维属性不够'



    

    


    

    

        
    










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
    #快乐修正，20快乐---10%增长速度
    change *= (1 + ((happiness - 60) / 200))
    #类型修正
    change *= type_buff
    #工作策略修正
    change *= strategy_buff
    #返回值
    return skill_now + change,skill_level

#增加小类技能
#参数说明
#skill_now：当前技能
#skill_mini_now：当前小类技能
#type_buff：类型修正，范围0-1，如工作则为1，演讲为0.2，等等
#happiness：当前快乐
#strategy_buff：工作策略加成，如果不是工作，则为1
def skill_mini_increase(skill_now,skill_mini_now,type_buff,happiness,strategy_buff=1):
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
    #不能超限
    if skill_mini_now + change > 1:
        change = 1 - skill_mini_now
    #返回值
    return skill_mini_now + change








    
# def change_skill(uid,skill_id,skill_mini_id):
#     getuserstatus = personal_attributes.objects.filter(uid=uid).first()#获得uid=uid的四维属性db的句柄
    

#     t1={
#                 1:{"name":"耕作","data":{1:"粮食种植",2:"蔬果种植",3:"经济作物种植",4:"开垦"}},
#                 2:{"name":"采伐","data":{1:"采集",2:"伐木",3:"开采",4:"勘探"}},
#                 3:{"name":"建设","data":{1:"建筑",2:"修缮"}},
#                 4:{"name":"加工","data":{1:"冶炼",2:"金属锻造",3:"纺织",4:"食品加工",5:"木石加工"}},
#                 5:{"name":"社交","data":{1:"雄辩",2:"交际",3:"文书",4:"管理"}},
#                 6:{"name":"舟车","data":{1:"陆上运输",2:"水上运输",3:"捕捞"}},
#                 7:{"name":"畜牧","data":{1:"狩猎",2:"家禽养殖",3:"家畜养殖"}},
#             }
#     t2={
#             1:{'name':'farming','data':{1:'grain',2:'vegetables_fruit',3:'cash_crops',4:'reclaim'}},
#             2:{'name':'cutting','data':{1:'collection',2:'lumbering',3:'exploitation',4:'prospecting'}},
#             3:{'name':'construct','data':{1:'building',2:'mending'}},
#             4:{'name':'processing','data':{1:'smelt',2:'forge',3:'spin',4:'food_processing',5:'wood_stone_processing'}},
#             5:{'name':'social','data':{1:'eloquence',2:'communicate',3:'write',4:'manage'}},
#             6:{'name':'vehicle','data':{1:'land_transport',2:'water_transport',3:'fishing'}},
#             7:{'name':'husbandry','data':{1:'hunt',2:'fowl',3:'livestock'}},
#         }
#     getuserskill_1 = UserSkill.objects.filter(user_id=uid)
#     getuserskill = getuserskill_1.vehicle_
#     #.objects.filter(t2[skill_id]['name'])#获得user_id=uid的技能属性总表db的句柄
    

#     skill_now = getuserskill.skill_num   #获取当前大类——社交技能点 #skill_now = getuserskill.object.filter(user_id=uid).skill_num 
#     skill_level = getuserskill.level   #获取当前大类技能等级
#     happiness = eval(getuserstatus.happy)         #获取当前用户幸福值
#     skill_mini_now = getuserskill.filter(t2[skill_id]['data'][skill_mini_id]) #获取当前小类—技能
#     energy= eval(getuserstatus.energy)

#     skill_num_now , skill_level_now = skill_increase(skill_now,0.2,skill_level,happiness,strategy_buff=1)    #大类技能增加
#     mini_increase = skill_mini_increase(skill_mini_now,skill_now,0.2,happiness,strategy_buff=1)    #小类技能增加

#     #修改大类——技能点、大类技能等级、小类——技能点
#     #usersocialskill = social.objects.filter(user_id=uid).first()
#     getuserskill.skill_num = skill_num_now
#     getuserskill.level = skill_level_now
#     getuserskill.filter(t2[skill_id]['data'][skill_mini_id]) = mini_increase
#     energy= getuserstatus.energy
#     getuserstatus.energy = energy - 15
#     getuserskill.save()
#     getuserstatus.save()
#     data={"skill_num_change":skill_num_now,"level_change":skill_level_now,"mini_skill_change":mini_increase}
#     return data