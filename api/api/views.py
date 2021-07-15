from django.shortcuts import redirect,render,HttpResponse
from TestModel.models import speech
import datetime
import json


def views(req):
    status=0
    meg='失败'
    list2=[]
    if req.GET.get("page")!=None:
        page = int(req.GET.get("page"))
        count=len(speech.objects.all())
        if count-5*page<0 or page<=0:
            status=0
            meg='失败，错误的页数'    
        else:
            list1 = speech.objects.order_by('-id')[0+5*(page-1):5*page]
            i=0
            for var in list1:
                r = var.text
                textid = var.id
                d = str(var.date)[0:10]
                a=(datetime.datetime.strptime(d,"%Y-%m-%d")-datetime.datetime.strptime('2021-6-3',"%Y-%m-%d")).days
                b=str(var.date)[11:19]
                list2.append({"textid":textid,"text":r,"day":a,"time":b})
                i+=1
            status=1
            meg='成功'
    else:
        status=0
        meg='失败，没有提供页码'


    result={
                "status":"{}".format(status),
                "message":"{}".format(meg),
                "data":{
                            "datalist":list2
                        }
            }

    return HttpResponse(json.dumps(result), content_type="application/json")
