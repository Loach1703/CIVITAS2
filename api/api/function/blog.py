from BlogModel.models import Blog
from django.shortcuts import redirect,render,HttpResponse
import json
from assist import *    

def get_blog(req):
    status = 0
    meg = "失败"
    datalist = {}
    sessionid = req.COOKIES.get('sessionid')
    if is_login(req,sessionid):
        id = req.GET.get("id")                
        if id == None:
            id = 1
        id = is_int(id)
        if id == "error":
            meg = "存在需要传入数字的参数传入的不是数字"
            result = {
                "status":status,
                "message":meg,
                "data":datalist
            }
            return HttpResponse(json.dumps(result), content_type="application/json")
        try:
            blog_text = Blog.objects.get(pk=id)
            all_blog = Blog.objects.all()
            datalist["total_blog"] = len(all_blog)
            datalist["text"] = blog_text.text
            datalist["title"] = blog_text.title
            datalist["author"] = blog_text.author
            datalist["time"] = blog_text.time
            status = 1
            meg = "查询开发日志成功"
        except:
            status = 0
            meg = "没有指定id的开发日志"
    else:
        meg = "您还没有登录"
    result = {
        "status":status,
        "message":meg,
        "data":datalist
    }
    return HttpResponse(json.dumps(result), content_type="application/json")