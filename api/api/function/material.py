from django.contrib.sessions.models import Session
from django.contrib import auth
from MaterialModel.models import Material, UserMaterial, MaterialDetail
from django.shortcuts import redirect,render,HttpResponse
import json
from assist import *
from django.db.models import Sum, F

def del_material(uid,material_id,level,count):
    material_detail = MaterialDetail.object.filter(Material__material_id=material_id).filter(level=level).first()
    usermaterial = UserMaterial.objects.filter(user__id=uid).filter(material_detail=material_detail)
    if usermaterial.exists():
        usermaterial = usermaterial.first()
        if usermaterial.count < count:
            return 0
        if usermaterial.count >= count:
            usermaterial.count = F('count') - count
            return 1
    

def material_depository(req):
    status = 0
    meg = "失败"
    datalist = []
    sessionid = req.COOKIES.get('sessionid')
    if is_login(req,sessionid):                 #判断登录
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
        usermaterial = UserMaterial.objects.filter(user__id=uid)
        if usermaterial.exists():               #判断用户有没有物品
            # 物品结构
                # 大类：物品id、物品名称、物品单位质量、物品损耗率，所有同大类物品总和
                    #小类（依据物品等级划分）：大类中不同等级，同等级物品数量
            distinct_set = usermaterial.values('material_detail__material').distinct().order_by('material_detail__material')   #去除物品id重复的物品，并根据id排序
            for material_id_dict in distinct_set:                                                       #获取用户所拥有的物品id
                material_id = material_id_dict['material_detail__material']
                large_class_material = Material.objects.filter(id=material_id).first()
                name = large_class_material.name
                unitmass = 0                  #预留，单位质量
                wastage = 0                   #预留，损耗率
                real_material_id = large_class_material.material_id
                filter_by_id = usermaterial.filter(material_detail__material_id=material_id)
                total = filter_by_id.aggregate(Sum('count'))['count__sum']
                find_material = filter_by_id.order_by('material_detail__level')
                levellist = []
                for var in find_material:                                                              #小类相关获取
                    count = var.count
                    level = var.material_detail.level
                    levellist.append({"level":level,"count":count})
                datalist.append({"id":real_material_id,"name":name,"unitmass":unitmass,"wastage":wastage,"total":total,"detail":levellist})
            status = 1
            meg = "查询成功"
            result = {
                "status":status,
                "message":meg,
                "data":datalist
            }
            return HttpResponse(json.dumps(result), content_type="application/json")
        else:
            status = 1
            meg = "用户没有物品"
            result = {
                "status":status,
                "message":meg,
                "data":datalist
            }
            return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        meg = "您还没有登录"