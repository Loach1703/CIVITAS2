from django.db import models
from django.conf import settings

# Create your models here.
#工作
class work_record(models.Model):
    uid = models.CharField(max_length=20)
    work_id = models.CharField(max_length=20)
    work_station_id = models.CharField(max_length=20)
    work_date = models.CharField(max_length=20)

#副业
class sideline(models.Model):
    uid = models.OneToOneField(
        
        
        primary_key=True,
    )
    
    #统计玩家单日副业次数#正整数，从0到2147483647
    number_of_today_sideline = models.PositiveIntegerField()
    #彩蛋系列
    #统计该玩家的总副业次数，彩蛋用？#正的大整数，0到9223372036854775807，我觉得能用到服务器供应商倒闭
    number_of_all_sideline = models.PositiveBigIntegerField()
    #统计每种副业总次数
    every_sideline_all= models.JSONField()

def create_sideline(uid):
    sideline.objects.create(uidr=uid,number_of_today_sideline = 0,number_of_all_sideline = 0)

#副业产能
class sideline_work_capacity(models.Model):
    #后续添加
    #测试用，固定产能系数
    #采集
    gather = models.CharField(max_length=20)
