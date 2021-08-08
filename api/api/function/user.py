from django.shortcuts import redirect,render,HttpResponse
from UserModel.models import usersession,personal_attributes,Avatar
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.sessions.models import Session
from django.contrib import auth
from django.conf import settings
from PIL import Image
from assist import *
from io import BytesIO
import os
import json

def upload_avatar(req):
    status = 0
    meg = "失败"
    sessionid = req.COOKIES.get("sessionid")
    if req.FILES.get('img') != None:
        if is_login(req,sessionid):
            if req.method == "POST":
                getavatar = req.FILES.get('img')
                session = Session.objects.filter(pk=sessionid).first()
                uid = session.get_decoded()["_auth_user_id"]
                user_detail = auth.models.User.objects.filter(pk=uid).first()
                Avatar_exists = Avatar.objects.filter(user__id=uid)
                if Avatar_exists.exists():
                    Avatar_exists.first().avatar.delete()
                new_avatar = Avatar(
                    avatar = getavatar,
                    user = user_detail,
                )
                new_avatar.save()
                path_jpg = os.path.join(settings.BASE_DIR,'media/avatar/'+str(uid)+'.jpg')
                img1 = Image.open(path_jpg)
                w, h = img1.size
                img2 = img1.convert('RGB')
                if w != h:
                    background = Image.new('RGB', size=(max(w, h), max(w, h)), color=(255, 255, 255))
                    length = int(abs(w - h) // 2)  # 一侧需要填充的长度
                    box = (length, 0) if w < h else (0, length)  # 粘贴的位置
                    background.paste(img2, box)
                    img2 = background
                img2.save(path_jpg)
                img1.close()
                rate = 1.0
                size = os.path.getsize(path_jpg)/1024
                while size >= 50:
                    img1 = Image.open(path_jpg)
                    imgsize = int(512*rate)
                    img2 = img1.convert('RGB').resize((imgsize,imgsize),Image.ANTIALIAS)
                    img_io=BytesIO()
                    img2.save(img_io,img1.format)
                    img_file = InMemoryUploadedFile(img_io,None,str(uid)+'.jpg',None,None,None)
                    img1.close()
                    if Avatar_exists.exists():
                        Avatar_exists.first().avatar.delete()
                    new_avatar = Avatar(
                        avatar = img_file,
                        user = user_detail,
                    )
                    new_avatar.save()
                    rate -= 0.1
                    size = os.path.getsize(path_jpg)/1024
                status = 1
                meg = "头像上传成功"
        else:
            meg = "您还没有登录"
    else:
        meg = "您还没有选择文件"
    result = {
        "status":status,
        "message":meg
    }
    return HttpResponse(json.dumps(result), content_type="application/json")

def get_avatar(req):
    status = 0
    meg = "失败"
    uid = is_int(req.GET.get("uid"))
    if uid == "error":
        meg = "存在需要传入数字的参数传入的不是数字"
        result={
            "status":status,
            "message":meg,
            "data":{}
        }
        return HttpResponse(json.dumps(result), content_type="application/json")
    Avatar_exists = Avatar.objects.filter(user__id=uid)
    if Avatar_exists.exists():
        image_data=Avatar_exists.first().avatar
        return HttpResponse(image_data,content_type="image/jpg")
    else:
        default_path=os.path.join(settings.BASE_DIR, "media/avatar/default.jpg")
        with open(default_path, 'rb') as f:
            image_data = f.read()
        return HttpResponse(image_data,content_type="image/jpg")

def get_userdetail(req):
    status = 0
    meg = "失败"
    data = {}
    sessionid = req.COOKIES.get("sessionid")
    if is_login(req,sessionid):
        session = Session.objects.filter(pk=sessionid).first()
        uid = is_int(req.GET.get("uid"))
        if uid == "error":
            meg = "存在需要传入数字的参数传入的不是数字"
            result={
                "status":status,
                "message":meg,
                "data":{}
            }
            return HttpResponse(json.dumps(result), content_type="application/json")
        if uid == None:
            uid = session.get_decoded()["_auth_user_id"]
        user = auth.models.User.objects.filter(pk=uid)
        if user.exists():
            username = user.first().username
            data = {"username":username}
            meg = "成功"
            status = 1
        else:
            meg = "对应uid的用户不存在"
    else:
        meg = "您还没有登录"
    result={
            "status":status,
            "message":meg,
            "data":data
        }
    return HttpResponse(json.dumps(result), content_type="application/json")


def islogin1(req):
    status=0
    meg="失败"
    is_login=False
    uid=None
    username=None
    sessionid=req.COOKIES.get("sessionid")
    if sessionid != None:
        if req.session.exists(sessionid)==False:
            meg="登录状态失效，请重新登录"
        else:
            status=1
            meg="成功"
            session = Session.objects.get(pk=sessionid)
            is_login=True
            uid=session.get_decoded()["_auth_user_id"]
            user=auth.models.User.objects.filter(pk=uid)
            user.first()
            username=user[0].username
    else:
        meg="未登录"
    result={
                "status":status,
                "message":meg,
                "data":{
                            "is_login":is_login,
                            "sessionid":sessionid,
                            "uid":uid,
                            "username":username
                        }
            }
    return HttpResponse(json.dumps(result), content_type="application/json")

def login1(req):
    status=0
    meg="失败"
    sessionid=None
    uid=None
    if req.POST.get("username")==None or req.POST.get("password")==None:
        meg="POST参数缺少"
        user=0
    else:
        username=req.POST.get("username")
        pwd=req.POST.get("password")
        user=auth.authenticate(username=username,password=pwd)
        if user:
            finduid = auth.models.User.objects.get(username=username)           
            uid = finduid.id                                                    #根据用户名从User表中获取uid
            usersession1=usersession.objects.filter(uid=uid)                    #usersession为自建表，记录用户登录所使用的sessionid
            if usersession1.exists():                                           #查找对应uid用户是否登录并留下sessionid
                for var in usersession1:                                        #留下sessionid，对Session表进行清理
                    session1=Session.objects.filter(session_key=var.sessionid)
                    session1.delete()
                usersession1.delete()
            auth.login(req,user)                                                #登录
            sessionid=req.session.session_key
            if not req.session.session_key:                                     #sessionid重复时req.session.session_key为None，此处防止用户处于登录情况下重复登录账户返回sessionid为None
                req.session.create()
                sessionid=req.session.session_key
            dbuser = usersession(uid=uid,sessionid=sessionid)                   #更新usersession表为最新sessionid
            dbuser.save()
            status=1
            meg="登录成功"
        else:
            meg="账号或密码有误"
    result={
                "status":status,
                "message":meg,
                "data":{"sessionid":sessionid,"uid":uid}
            }
    return HttpResponse(json.dumps(result), content_type="application/json")

def register1(req):
    status=0
    meg="失败"
    username=req.POST.get("username")
    pwd=req.POST.get("password")
    repwd=req.POST.get("repeat_password")
    email=req.POST.get("email")
    if not (username and pwd and email):
        meg="缺少参数"
    else:
        s=1
        u=auth.models.User.objects.filter(username=username).first()
        if u:
            meg=meg+",该用户名已被注册"
            s=0
        if len(username)> 20:
            meg=meg+",用户名不能超过20个字符"
            s=0
        if len(pwd)<6 or len(pwd)>20:
            meg=meg+",密码需要在6~20字符之间"
            s=0
        if pwd!=repwd:
            meg=meg+",两次输入的密码不一致"
            s=0
        if not validateEmail(email):
            meg=meg+",邮箱不符合规范"
            s=0
        if s:
            auth.models.User.objects.create_user(username=username,password=pwd,email=email)
            status=1
            meg="注册成功"
    result={
                "status":status,
                "message":meg,
                "data":{}
            }
    return HttpResponse(json.dumps(result), content_type="application/json")

def siwei(req):
    status = 0
    uid = None
    meg="失败"
    data={}
    sessionid=req.COOKIES.get("sessionid")
    if is_login(req,sessionid):
        session = Session.objects.filter(pk=sessionid).first()
        uid=int(session.get_decoded()["_auth_user_id"])
        siwei_db = None
        siwei = None
        siwei_db = personal_attributes.objects.order_by('id')
        siwei=personal_attributes.objects.filter(uid=uid)
        if siwei_db != None :
            if siwei.exists():
                meg ='成功'
                for var in siwei:
                    happy = eval(var.happy)
                    energy = eval(var.energy)
                    healthy = eval(var.healthy)
                    Hunger = eval(var.Hunger)
                    status = 1
                    data={
                        "stamina":energy,
                        "happiness":happy,
                        "health":healthy,
                        "starvation":Hunger,
                    }
                reply_data = status_recover(energy,happy,healthy,Hunger,0,1)
            else:
                if(uid != None ):
                    status = 1
                    meg = '新用户'
                    new_user_add = personal_attributes(uid = uid,energy = 100,healthy = 100,happy = 100 ,Hunger=100)
                    new_user_add.save()
                    data={
                        "happiness":100,
                        "stamina":100,
                        "health":100,
                        "starvation":100,
                    }
                    reply_data = status_recover(100,100,100,100,0,1)
                else:
                    meg = '找不到用户资料'


        else:
            meg='数据库连接失败'


    else:
        meg='您还没有登录'
    
    result={
                "status":status,
                "message":meg,
                "data":{"uid":uid,"today":data,"tomorrow":reply_data},
            }
    return HttpResponse(json.dumps(result), content_type="application/json")

def logout1(req):
    status=0
    mes="失败"
    sessionid=req.COOKIES.get("sessionid")
    if is_login(req,sessionid):
        filter_sessionid=Session.objects.filter(pk=sessionid)
        if filter_sessionid.exists():
            filter_usersessionid=usersession.objects.filter(sessionid=sessionid)
            if filter_sessionid.exists():
                filter_usersessionid.delete()
            req.session.flush()
            status=1
            meg="注销成功"
    else:
        meg="您还没有登录"
    result={
                "status":status,
                "message":meg,
            }
    return HttpResponse(json.dumps(result), content_type="application/json")