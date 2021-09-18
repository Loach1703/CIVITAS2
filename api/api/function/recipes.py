from django.db.models.expressions import F
from django.db.models.query_utils import Q
from django.shortcuts import redirect,render,HttpResponse
from assist import *
from django.contrib.sessions.models import Session
from django.contrib import auth
from MaterialModel.models import *
from UserModel.models import *
from RecipesModel.models import *
from WorkModel.models import *
import random
import json
import datetime

class Raw_material(models.Model):
    id = IntegerField(primary_key=True,)
    name = CharField(max_length=50,verbose_name='名字')
    health = FloatField(verbose_name='食物健康')
    Satiety = FloatField(verbose_name='饱食度')
    salty = FloatField(va)

    def __str__(self):
        return self.user.username



        
    