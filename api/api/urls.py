"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
import os
import sys
#将django根目录下的api/function中的路径导入
sys.path.insert(0,os.path.join(settings.BASE_DIR,'api/function'))
#导入后请直接使用import导入对应的视图python文件（创建function文件夹的原因：便于整理和管理）
'''
user.py——用户相关接口函数（头像、用户表、四维）
skill.py——技能相关接口函数
civitas.py——civitas系统相关接口函数（天气）
material.py——物资相关接口函数
speech.py——演讲相关接口函数（演讲、演讲态度）
assist.py——创建的各项辅助用函数（is_login,is_int,skill_increase）等
views.py——测试界面、非接口页面视图函数
'''
import views,user,skill,civitas,speech,material,work,blog,city,diet
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

urlpatterns = [
    

    path('admin/', admin.site.urls),
    #演讲
    path('getspeech/', speech.getspeech1),#获得演讲内容
    path('speech/', speech.speech1),#发演讲
    path('assess/',speech.assess1),#点赞
    path('hotspeech/',speech.hotspeech1),#城墙

    path('getweather/',civitas.getweather1),#天气
    path('getdate/',civitas.getdate1),#游戏日历

    path('islogin/',user.islogin1),
    path('login/',user.login1),
    path('register/',user.register1),
    path('logout/',user.logout1),

    path('upload-avatar/',user.upload_avatar),#更新头像
    path('getavatar/',user.get_avatar),#获得头像
    path('getstatus/',user.siwei),#四维
    path('getuserdetail/',user.get_userdetail),#用户信息 

    path('test.html',views.test),

    path('getskill/',skill.getUserSkill),#获得技能

    path('getmaterial/',material.material_depository),#查看玩家物资

    path('dosideline/',work.get_sideline),#副业

    path('getblog/',blog.get_blog),
   
    # 城市
    path('city_info/', city.get_city_info),
    # 不动产
    path('building_list/', city.building_list),
    path('reclaim/', city.reclaim),

    #食谱
    path('getdiet/',diet.GetUserRecipes),#获得玩家食谱
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
