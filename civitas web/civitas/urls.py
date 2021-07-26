"""civitas URL Configuration

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
from django.contrib import admin
from django.urls import path,re_path
from . import views
from . import rspeech
from . import map
from . import test
from django.conf.urls import include
from django.contrib.auth import views as loginViews
urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^$',views.views),
    path('map.html', map.map),
    path('index.html',views.views),
    path('test/',test.test),
    path('login.html',views.login),
    path('blog/1.html',views.blog1),
    path('register.html',views.register)
]
# urlpatterns += [
#     path('accounts/', include('django.contrib.auth.urls')),
    
# ]
#使用内置轮子进行登入和找回
#如果独立轮子，参考https://www.cnblogs.com/derek1184405959/p/8567522.html
urlpatterns += [
    path('', include('django.contrib.auth.urls')),
    # path('login/',loginViews.LoginView.as_view(), name='login'),
    # path('logout/',loginViews.LogoutView.as_view(), name='logout'),

    # path('password-reset/', loginViews.PasswordResetView.as_view(), name='password_reset'),
    # path('password-reset/done/', loginViews.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', loginViews.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', loginViews.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('login',loginViews.LoginView.as_view(), name='login'),
]
# 增加验证码的路径
# urlpatterns +=[
#     path('captcha', include('captcha.urls'))
# ]
urlpatterns +=[
    
    # path('regis/', views.regisview, name='regis'),
    path('logout/',loginViews.LogoutView.as_view(), name='logout'),


]