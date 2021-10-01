from django.db.models.expressions import F
from django.db.models.query_utils import Q
from django.shortcuts import redirect,render,HttpResponse
from assist import *
from django.contrib.sessions.models import Session
from django.contrib import auth
from MaterialModel.models import *
from UserModel.models import *
from WorkModel.models import *
import random
import json
import datetime
from DietModel.models import *


def GetUserRecipes(req):
    status  = 0
    meg = "失败"
    datalist = []
    sessionid = req.COOKIES.get("sessionid")
    if is_login(req,sessionid):
        
        session = Session.objects.filter(pk=sessionid).first()
        uid = session.get_decoded()["_auth_user_id"]
        user = auth.models.User.objects.get(pk=uid)

        

                               




    





        
    