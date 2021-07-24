from django.shortcuts import render
from TestModel.models import speech
import datetime

from .forms import RegisterForm

def views(request):
    list1 = speech.objects.order_by('-id')[0:5]
    i=0
    dict1={}
    for var in list1:
        r = var.text
        d = str(var.date)[0:10]
        a=(datetime.datetime.strptime(d,"%Y-%m-%d")-datetime.datetime.strptime('2021-6-3',"%Y-%m-%d")).days
        b=str(var.date)[11:19]
        dict1[str(i)]={"text":r,"day":a,"time":b}
        i+=1
    list2=list(dict1.values())
    return render(request, "index.html", {"list":list2})

def regisview(request):
  return render(request,"regis/regis.html")

def register(request):
    # if request.session.get('is_login', None):
    #     # 登录状态不允许注册。你可以修改这条原则！
    #     return redirect("/index/")
    # if request.method == "POST":
    #     register_form = RegisterForm(request.POST)
    #     message = "请检查填写的内容！"
    #     if register_form.is_valid():  # 获取数据
    #         username = register_form.cleaned_data['username']
    #         password1 = register_form.cleaned_data['password1']
    #         password2 = register_form.cleaned_data['password2']
    #         email = register_form.cleaned_data['email']
    #         sex = register_form.cleaned_data['sex']
    #         if password1 != password2:  # 判断两次密码是否相同
    #             message = "两次输入的密码不同！"
    #             return render(request, 'user19/register.html', locals())
    #         else:
    #             same_name_user = models.User.objects.filter(name=username)
    #             if same_name_user:  # 用户名唯一
    #                 message = '用户已经存在，请重新选择用户名！'
    #                 return render(request, 'user19/register.html', locals())
    #             same_email_user = models.User.objects.filter(email=email)
    #             if same_email_user:  # 邮箱地址唯一
    #                 message = '该邮箱地址已被注册，请使用别的邮箱！'
    #                 return render(request, 'user19/register.html', locals())
  
    #             # 当一切都OK的情况下，创建新用户
  
    #             new_user = models.User.objects.create()
    #             new_user.name = username
    #             new_user.password = password1
    #             new_user.email = email
    #             new_user.sex = sex
    #             new_user.save()
    #             return redirect('/login/')  # 自动跳转到登录页面
    # register_form = RegisterForm()
    form = NameForm(request)
    your_name = forms.CharField(label='Your name', max_length=100)

    #return render(request,"regis/regis.html", locals())
    return render(request, 'regis/regis.html', {'form': form})
