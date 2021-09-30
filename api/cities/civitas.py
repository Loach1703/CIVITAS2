from django.shortcuts import redirect, render, HttpResponse
from django.contrib.sessions.models import Session
from django.core import serializers
from api.function.assist import *
from UserModel.models import personal_attributes
from cities.models import City, Building
import datetime
import json


# 获取城市信息
def get_city_info(request):
    if request.GET.get('id') is None:
        return HttpResponse(json.dumps({
            "status": 0,
            "message": 'ID 不能为空',
            "data": {},
        }), content_type="application/json")

    city_id = request.GET.get('id')
    city = City.objects.filter(pk=city_id)

    return HttpResponse(json.dumps({
        "status": 0,
        "message": '',
        "data": city.__str__(),
    }), content_type="application/json")


# 建筑列表
def building_list(request=None):
    list = [
        {},  # 考虑 ID 从 1 开始，此处留空
        {'name': '仓库', 'land_occupy': 1},
        {'name': '住宅', 'land_occupy': 0.5},
    ]
    if request is None:
        return list

    return HttpResponse(json.dumps({
        "status": 0,
        "message": '',
        "data": list,
    }), content_type="application/json")


# 垦荒
def reclaim(request):
    session_id = request.COOKIES.get("sessionid")
    if is_login(request, session_id) == 0:
        return HttpResponse(json.dumps({
            "status": 0,
            "message": '您还没有登录',
            "data": {},
        }), content_type="application/json")

    session = Session.objects.filter(pk=session_id).first()
    uid = session.get_decoded()["_auth_user_id"]
    buildings = building_list()
    building_id = int(request.POST.get('building_id'))

    city_id = request.POST.get('city_id')
    if city_id is None or building_id is None:
        return HttpResponse(json.dumps({
            "status": 0,
            "message": 'ID 不能为空',
            "data": {},
        }), content_type="application/json")

    # TODO 四维数值检测与更新
    attr = personal_attributes.objects.filter(uid=uid).first()
    happy = int(attr.happy)
    energy = int(attr.energy)
    healthy = int(attr.healthy)
    hunger = int(attr.Hunger)

    city = City.objects.filter(pk=city_id).first()

    need_hunger = 10
    if hunger < need_hunger:
        return HttpResponse(json.dumps({
            "status": 0,
            "message": '你快饿死啦，不能做这个工作',
            "data": {},
        }), content_type="application/json")
    product = int(4 / city.flat_h)
    attr.Hunger = int(attr.Hunger) - need_hunger

    if city is None:
        return HttpResponse(json.dumps({
            "status": 0,
            "message": '城市已不存在',
            "data": {},
        }), content_type="application/json")

    # 建筑处理
    try:
        building = Building.objects.get(
            user_id=uid,
            city_id=city_id,
            building_id=building_id,
            status=Building.STATUS_BUILD
        )
    except Building.DoesNotExist:
        from django.utils import timezone
        building = Building(
            user_id=uid,
            status=Building.STATUS_BUILD,
            city_id=city_id,
            building_id=building_id,
            land_occupy_h=buildings[building_id]['land_occupy'] * 100,
            land_has_h=0,
            created_at=timezone.now()
        )

        from django_redis import get_redis_connection
        cache = get_redis_connection("default")
        # eval 是 Redis 的标准同步执行办法，运行 Lua 脚本，一般情况还是直接使用 cache.get/set
        lua = """
            local key = string.format("city:land:%s", KEYS[1])
            local has = redis.call('EXISTS', key)
            if(has == 1)
            then
                local value = redis.call('GET', key) - ARGV[1]
                if(value > 0)
                then
                    redis.call('SET', key, value)
                    return value
                end
            return -1
            end
            """
        # 以支持原子化 Cache 的值为准，避免 DB 异步 Select 与 Update 导致数值异常
        city.land_h = cache.eval(lua, 1, str(city_id), buildings[building_id]['land_occupy'] * 100)
        if city.land_h == -1:
            return HttpResponse(json.dumps({
                "status": 0,
                "message": '本地没有闲置的土地',
                "data": {},
            }), content_type="application/json")

    building.land_has_h += product
    if building.land_has_h >= building.land_occupy_h:
        building.land_has_h = building.land_occupy_h
        building.status = Building.STATUS_DONE

    attr.save()
    building.save()
    city.save()

    return HttpResponse(json.dumps({
        "status": 0,
        "message": '',
        "data": {
            'city': city.__str__(),
            'building': building.__str__(),
        },
    }), content_type="application/json")
