from django.shortcuts import render

def test(req):
    return render(req,'test.html')