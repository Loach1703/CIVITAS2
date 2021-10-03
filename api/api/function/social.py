from django.shortcuts import redirect,render,HttpResponse
from SocialContactModel.models import *
from UserModel.models import personal_attributes
from SkillModel.models import *
from django.contrib.sessions.models import Session
from django.contrib import auth
from django.db.models import Q
from assist import *
import datetime
import json
import math

#进行社交行为接口
def do_social_behavior(req):
    #类型：POST
    #参数：类型type，社交对象target_uid，附带消息message
    def make_return(meg):
        result = {
            "status":status,
            "message":meg,
            "data":data
        }
        return HttpResponse(json.dumps(result), content_type="application/json")
    status = 0
    meg = "失败"
    data = {}
    sessionid=req.COOKIES.get("sessionid")
    type_list = ["公开赞扬","公开谴责","私下表扬","私下批评","赠送礼物",]
    type_list_cost = [15,15,5,5,5]
    target_happiness_change = [1,-1,0.5,-0.5,1]
    relationship_value_change_list = [10,-10,5,-5,10]
    if is_login(req,sessionid):
        session = Session.objects.filter(pk=sessionid).first()
        uid = session.get_decoded()["_auth_user_id"]
        user = auth.models.User.objects.get(pk=uid)
        #社交类型
        type_social = is_int(req.POST.get("type"))
        if type_social == "error":
            return make_return("存在需要传入数字的参数传入的不是数字")
        #检查社交类型参数合法性
        if type_social not in list(range(5)):
            return make_return("社交类型不合法")
        #社交目标玩家uid
        target_uid = is_int(req.POST.get("target_uid"))
        if target_uid == "error":
            return make_return("存在需要传入数字的参数传入的不是数字")
        if target_uid == eval(uid):
            return make_return("你不能对自己进行社交")
        #社交目标玩家对象
        try:
            target_user = auth.models.User.objects.get(pk=target_uid)
        except:
            return make_return("对应uid的目标用户不存在")
        #留言检查
        message = req.POST.get("message")
        if not len(message) <= 100:
            return make_return("留言过长")
        #获得自身属性，判断是否满足条件
        getuserstatus = personal_attributes.objects.filter(uid=uid).first()
        energy = eval(getuserstatus.energy)
        if energy - type_list_cost[type_social] < 0 :
            return make_return("您当前的精力不足")
        #获得对方属性
        getuserstatus_target = personal_attributes.objects.filter(uid=target_uid).first()
        #检查是否有post参数
        if message == None and target_uid == None and type_social == None:
            return make_return("没有提供POST参数")
        #检查是否为好友
        is_friend1 = Friend.objects.filter(from_person=user,to_person=target_user).first()
        is_friend2 = Friend.objects.filter(from_person=target_user,to_person=user).first()
        #如果双向都无法找到，则不是好友，公开谴责除外
        if not is_friend1 and not is_friend2 and type_social != 1:
            return make_return("双方不是好友，只能公开谴责")
        elif is_friend1:
            is_friend = is_friend1
        elif is_friend2:
            is_friend = is_friend2
        else:
            is_friend = None
        #存储社交
        db_social_behavior = Social_behavior.objects.create(from_person=user,to_person=target_user,
            relationship_value_change=relationship_value_change_list[type_social],
            type_of_behavior=type_list[type_social],message=message)
        db_social_behavior.save()
        #获取当前大类——社交技能点
        getuserbigskill = UserBigSkill.objects.filter(user_id=uid).first()
        skill_now = getuserbigskill.shejiao
        skill_level = getuserbigskill.shejiao_level
        #获取小类技能值
        getusersmallskill = UserSmallSkill.objects.filter(user_id=uid).first()
        #获取当前用户快乐值
        happiness = eval(getuserstatus.happy)
        #获取当前小类——雄辩技能点
        skill_mini_now = getusersmallskill.jiaoji
        #大类技能增加
        skill_num_now = skill_increase(skill_now,0.2,skill_level,happiness,strategy_buff=1)
        #小类技能增加
        mini_increase = skill_mini_increase(skill_now,skill_mini_now,0.2,happiness,strategy_buff=1)
        #修改大类——社交技能点、大类技能等级、小类——雄辩技能点、当前用户精力值
        getuserbigskill.shejiao = skill_num_now
        getusersmallskill.jiaoji = mini_increase
        getuserstatus.energy = energy - type_list_cost[type_social]
        #获取目标用户快乐值
        target_happiness = eval(getuserstatus_target.happy)
        #修改目标用户快乐值
        getuserstatus_target.happy = max(min(target_happiness + target_happiness_change[type_social],100),-100)
        #修改关系值
        if is_friend:
            relationship_value = is_friend.relationship_value
            is_friend.relationship_value = max(min(relationship_value + relationship_value_change_list[type_social],100),-100)
        #保存修改值
        is_friend.save()
        getuserbigskill.save()
        getusersmallskill.save()
        getuserstatus.save()
        getuserstatus_target.save()
        #成功，返回
        status = 1
        data = {"skill_num_change":skill_num_now,"skill_mini_change":mini_increase,"relationship_value_change":relationship_value_change_list[type_social-1]}
        return make_return(type_list[type_social]+"成功")    
    else:
        return make_return("您还没有登录")

#加好友接口
def add_friend(req):
    #类型：POST
    #参数：加好友对象target_uid
    def make_return(meg):
        result={
            "status":status,
            "message":meg,
            "data":data
        }
        return HttpResponse(json.dumps(result), content_type="application/json")
    status = 0
    meg = "失败"
    data = {}
    sessionid=req.COOKIES.get("sessionid")
    if is_login(req,sessionid):
        session = Session.objects.filter(pk=sessionid).first()
        uid = session.get_decoded()["_auth_user_id"]
        user = auth.models.User.objects.get(pk=uid)
        #加好友目标玩家uid
        target_uid = is_int(req.POST.get("target_uid"))
        if target_uid == "error":
            return make_return("存在需要传入数字的参数传入的不是数字")
        if target_uid == eval(uid):
            return make_return("你不能加自己为好友")
        #社交目标玩家对象
        try:
            target_user = auth.models.User.objects.get(pk=target_uid)
        except:
            return make_return("对应uid的目标用户不存在")
        #检查是否有post参数
        if target_uid == None:
            return make_return("没有提供POST参数")
        #检查是否为好友
        is_friend1 = Friend.objects.filter(from_person=user,to_person=target_user).first()
        is_friend2 = Friend.objects.filter(from_person=target_user,to_person=user).first()
        #如果其中一个找到，则是好友，不能再添加了
        if is_friend1 or is_friend2:
            return make_return("你们已经是好友了")
        #存储社交
        db_friend = Friend.objects.create(from_person=user,to_person=target_user,relationship_value=0)
        db_friend.save()
        #成功，返回
        status = 1
        return make_return("添加好友成功")    
    else:
        return make_return("您还没有登录")

#删好友接口
def remove_friend(req):
    #类型：POST
    #参数：删好友对象target_uid
    def make_return(meg):
        result = {
            "status":status,
            "message":meg,
            "data":data
        }
        return HttpResponse(json.dumps(result), content_type="application/json")
    status = 0
    meg = "失败"
    data = {}
    sessionid=req.COOKIES.get("sessionid")
    if is_login(req,sessionid):
        session = Session.objects.filter(pk=sessionid).first()
        uid = session.get_decoded()["_auth_user_id"]
        user = auth.models.User.objects.get(pk=uid)
        #删好友目标玩家uid
        target_uid = is_int(req.POST.get("target_uid"))
        if target_uid == "error":
            return make_return("存在需要传入数字的参数传入的不是数字")
        if target_uid == eval(uid):
            return make_return("你不能删除自己的好友")
        #社交目标玩家对象
        try:
            target_user = auth.models.User.objects.get(pk=target_uid)
        except:
            return make_return("对应uid的目标用户不存在")
        #检查是否有post参数
        if target_uid == None:
            return make_return("没有提供POST参数")
        #检查是否为好友
        is_friend1 = Friend.objects.filter(from_person=user,to_person=target_user).first()
        is_friend2 = Friend.objects.filter(from_person=target_user,to_person=user).first()
        #如果双向都无法找到，则不是好友
        if not is_friend1 and not is_friend2:
            return make_return("你们还不是好友")
        elif is_friend1:
            is_friend = is_friend1
        elif is_friend2:
            is_friend = is_friend2
        #删除好友
        is_friend.delete()
        #成功，返回
        status = 1
        return make_return("删除好友成功")    
    else:
        return make_return("您还没有登录")

#是否为好友接口
def is_friend(req):
    #类型：GET
    #参数：对象target_uid
    def make_return(meg):
        result = {
            "status":status,
            "message":meg,
            "data":data
        }
        return HttpResponse(json.dumps(result), content_type="application/json")
    status = 0
    meg = "失败"
    data = {}
    sessionid=req.COOKIES.get("sessionid")
    if is_login(req,sessionid):
        session = Session.objects.filter(pk=sessionid).first()
        uid = session.get_decoded()["_auth_user_id"]
        user = auth.models.User.objects.get(pk=uid)
        #目标玩家uid
        target_uid = is_int(req.GET.get("target_uid"))
        if target_uid == "error":
            return make_return("存在需要传入数字的参数传入的不是数字")
        if target_uid == eval(uid):
            return make_return("你不是自己的好友")
        #社交目标玩家对象
        try:
            target_user = auth.models.User.objects.get(pk=target_uid)
        except:
            return make_return("对应uid的目标用户不存在")
        #检查是否有参数
        if target_uid == None:
            return make_return("没有提供GET参数")
        #检查是否为好友
        is_friend1 = Friend.objects.filter(from_person=user,to_person=target_user).first()
        is_friend2 = Friend.objects.filter(from_person=target_user,to_person=user).first()
        #如果双向都无法找到，则不是好友
        if not is_friend1 and not is_friend2:
            status = 1
            return make_return("你们还不是好友")
        else:
            status = 1
            return make_return("你们是好友")    
    else:
        return make_return("您还没有登录")

#查询社交行为记录接口
def get_social(req):
    #类型：GET
    #参数：页码page（可选，默认为1），查询对象uid（可选，默认为自己）
    def make_return(meg):
        result = {
            "status":status,
            "message":meg,
            "data":data
        }
        return HttpResponse(json.dumps(result), content_type="application/json")
    status = 0
    meg = "失败"
    data = {}
    sessionid=req.COOKIES.get("sessionid")
    num_every_page=10
    if is_login(req,sessionid):
        session = Session.objects.filter(pk=sessionid).first()
        #自己的uid
        uid = session.get_decoded()["_auth_user_id"]
        user = auth.models.User.objects.get(pk=uid)
        #目标玩家uid
        target_uid = req.GET.get("uid")
        if target_uid == None:
            target_uid = eval(uid)
        elif is_int(target_uid) == "error":
            return make_return("不合法的uid参数")
        #社交目标玩家对象
        try:
            target_user = auth.models.User.objects.get(pk=target_uid)
        except:
            return make_return("对应uid的目标用户不存在")
        #页码page
        page = req.GET.get("page")
        if page == None:
            page = 1
        page = is_int(page)
        if page == "error":
            return make_return("不合法的页码参数")
        usersocial = Social_behavior.objects.filter(from_person=target_user)
        usersocial2 = Social_behavior.objects.filter(to_person=target_user)
        usersocial.union(usersocial2)
        usersocial = Social_behavior.objects.filter(Q(from_person=target_user) | Q(to_person=target_user))
        #检查是否为好友
        is_friend1 = Friend.objects.filter(from_person=user,to_person=target_user).first()
        is_friend2 = Friend.objects.filter(from_person=target_user,to_person=user).first()
        #如果双向都无法找到，则不是好友，只能显示公开谴责和公开赞扬
        if not is_friend1 and not is_friend2:
            usersocial = usersocial.filter(Q(type_of_behavior = "公开赞扬") | Q(type_of_behavior = "公开谴责"))
        #分页
        count = len(usersocial)
        total_page = math.ceil(count / num_every_page)
        #没有记录，直接返回
        if total_page == 0:
            status = 1
            return make_return("查询成功，但该居民没有社交记录")
        #验证page参数合法性
        if page > total_page or page <= 0:
            return make_return("不合法的页码参数")
        #切片出对应页码的Queryset
        list1 = usersocial.order_by('-id')[0 + num_every_page * (page - 1) : num_every_page * page]
        rtl = []
        for var in list1:
            from_person_username = var.from_person.username
            to_person_username = var.to_person.username
            from_person_uid = var.from_person.id
            to_person_uid = var.to_person.id
            social_type = var.type_of_behavior
            message = var.message
            d = str(var.date)[0:10]
            day = (datetime.datetime.strptime(d,"%Y-%m-%d") - datetime.datetime.strptime('2021-6-3',"%Y-%m-%d")).days
            time = str(var.date)[11:19]
            rtl.append({
                "from_person_username":from_person_username,"to_person_username":to_person_username,
                "from_person_uid":from_person_uid,"to_person_uid":to_person_uid,"social_type":social_type,"message":message,
                "day":day,"time":time})
        #成功，返回
        status = 1
        data = {
            "total_page":total_page,
            "num":len(usersocial),
            "datalist":rtl,
        }
        return make_return("查询成功")    
    else:
        return make_return("您还没有登录")