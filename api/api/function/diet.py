from django.db.models.expressions import F
from django.db.models.query_utils import Q
from django.shortcuts import redirect,render,HttpResponse

from django.contrib.sessions.models import Session
from django.contrib import auth
from MaterialModel.models import *
from UserModel.models import *
from WorkModel.models import *
import random
import json
import datetime
from DietModel.models import *

def is_login(req,sessionid):
    if not sessionid:
        return 0
    if not req.session.exists(sessionid):
        return 0
    return 1

def GetUserRecipes(req):
    status  = 0
    meg = "失败"
    datalist = []
    sessionid = req.COOKIES.get("sessionid")
    if is_login(req,sessionid):
        
        session = Session.objects.filter(pk=sessionid).first()
        uid = session.get_decoded()["_auth_user_id"]
        user = auth.models.User.objects.get(pk=uid)
        user_recipes= diet_recipe.objects.filter(owner = user)
        if user_recipes.exists():
            recipe = user_recipes.values('name','energy','happy','health','Satiety','acid','salty','sweet','bitterness','aroma','taste_description','treatment__name')  #
            count = len(recipe)
            datalist = {
                'count':count,
                'recipe':recipe
            }
            status = 2
            meg = '成功'


        else:
            status = 1
            meg = '还没有创建食谱'
    else:
        meg = "未登入"
    result = {
        "status":status,
        "message":meg,
        "data":datalist
    }
    return HttpResponse(json.dumps(result), content_type="application/json")
    


