from django.db.models.expressions import F
from django.db.models.query_utils import Q
from django.forms.models import model_to_dict
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
            recipe = user_recipes.values('id','name','energy','happy','health','Satiety','acid','salty','sweet','bitterness','aroma','taste_description','treatment__name').order_by('name')  #
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
def Get_id_Recipes(req):
    status  = 0
    meg = "失败"
    datalist = []
    sessionid = req.COOKIES.get("sessionid")
    recipes_id = req.POST.get("recipes_id")
    if is_login(req,sessionid):
        
        session = Session.objects.filter(pk=sessionid)
        uid = session.get_decoded()["_auth_user_id"]
        user = auth.models.User.objects.get(pk=uid)
        user_recipes= diet_recipe.objects.filter(owner = user,id = recipes_id)
        if user_recipes.exists():
            # user_recipesdict = model_to_dict(user_recipes)
            recipe = user_recipes.values('id','name','energy','happy','health','Satiety','acid','salty','sweet','bitterness','aroma','taste_description','treatment__name')[0]
            #diet_material = user_recipes.values('input__r_material__raw_material_id','input__r_material__name','input__level')
            diet_material_list=Input_Recipe_Diet.objects.filter(recipe = recipes_id).order_by('material__r_material__raw_material_id')
            diet_material = diet_material_list.values('material__r_material__raw_material_id','material__r_material__name','material__level','count')


            count = len(diet_material)
            datalist = {
                
                'recipe':recipe,
                'count':count,
                'diet_material':diet_material,
            }
            status = 2
            meg = '成功'


        else:
            status = 1
            meg = '找不到该用户的查询id食谱'
    else:
        meg = "未登入"
    result = {
        "status":status,
        "message":meg,
        "data":datalist
    }
    return HttpResponse(json.dumps(result), content_type="application/json")
    


