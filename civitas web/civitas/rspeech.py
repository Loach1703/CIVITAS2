from TestModel.models import speech
from django.shortcuts import redirect,render
from django.views.decorators import csrf
import datetime

def rspeech(request):
    t = request.POST['text']
    if len(request.POST['text'])<=140:
        date=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        dbspeech = speech(text=t,date=date)
        dbspeech.save()
        return redirect("/")
    else:
        return redirect("/",{"status":"演讲字数超过140字，当前字数：{}".format(len(request.POST['text']))})