from django.shortcuts import render

import datetime

from .forms import RegisterForm

def views(request):
    # list1 = speech.objects.order_by('-id')[0:5]
    # i=0
    # dict1={}
    # for var in list1:
    #     r = var.text
    #     d = str(var.date)[0:10]
    #     a=(datetime.datetime.strptime(d,"%Y-%m-%d")-datetime.datetime.strptime('2021-6-3',"%Y-%m-%d")).days
    #     b=str(var.date)[11:19]
    #     dict1[str(i)]={"text":r,"day":a,"time":b}
    #     i+=1
    # list2=list(dict1.values())
    # return render(request, "index.html", {"list":list2})
    return render(request, "index.html")

def login(req):
    return render(req, "login/login.html")

def blog1(req):
    return render(req, "blog/1.html")

def register(req):
    return render(req, "login/register.html")

def logout(req):
    return render(req, "registration/logout.html")

def test(req):
    return render(req,"test.html")
