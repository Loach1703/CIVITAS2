from django.core.files import File
from TestModel.models import Avatar
from django.contrib.sessions.models import Session
from django.contrib import auth
from django.shortcuts import redirect,render,HttpResponse
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from io import BytesIO
from django.conf import settings
import os
import json


def is_login(req,sessionid):
    if not sessionid:
        return 0
    if not req.session.exists(sessionid):
        return 0
    return 1

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
                resize_avatar=Avatar.objects.filter(user__id=uid).first()
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
    uid=req.GET.get("uid")
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
        uid = req.GET.get("uid")
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
