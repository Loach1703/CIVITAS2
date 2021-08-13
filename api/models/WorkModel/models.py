from django.db import models
from django.conf import settings

# Create your models here.
#工作
class work_record(models.Model):
    uid = models.CharField(max_length=20)
    work_id = models.CharField(max_length=20)
    work_station_id = models.CharField(max_length=20)
    work_date = models.CharField(max_length=20)

#副业-玩家表
class sideline_record(models.Model):
    uid = models.OneToOneField(
        
        
        primary_key=True,
    )
    
    #统计玩家单日副业次数#正整数，从0到2147483647
    number_of_today_sideline = models.PositiveIntegerField(verbose_name='单日副业次数')
    #记录玩家最新的副业日期,civ时间制，避免增加换日运算工作量
    sideline_day_c= models.CharField(max_length=20,verbose_name='最新的副业日期,civ时间制')
    #记录玩家最新的副业日期,正常时间制，避免增加换日运算工作量
    sideline_day= models.CharField(max_length=30,verbose_name='最新的副业日期,正常时间制')

    #彩蛋系列
    #统计该玩家的总副业次数，彩蛋用
    number_of_all_sideline = models.CharField(max_length=30,verbose_name='总副业次数')
    #统计每种副业总次数
    every_sideline_all= models.JSONField(verbose_name='每种副业总次数')

def create_sideline(uid):
    sideline_record.objects.create(uidr=uid,number_of_today_sideline = 0,number_of_all_sideline = 0)

#副业
class sideline_work(models.Model):
    #后续添加
    #测试用，固定产能系数
    #副业id
    sideline_id = models.IntegerField(
        primary_key=True,
    )
    #副业名字
    sideline_name = models.CharField(max_length=50,verbose_name='副业名字')
    #使用的技能大类 dbname，以空格隔开
    sideline_bigskills = models.CharField(max_length=100,verbose_name='使用的技能大类 dbname，以空格隔开')
    #使用的技能小类 dbname，以空格隔开，如果没有适用的技能小类，设置为0，与大类对应。
    sideline_smallskills = models.CharField(max_length=100,verbose_name='使用的技能小类 dbname，以空格隔开，如果没有适用的技能小类，设置为0，与大类对应')
    #各自技能对应的产能加成，以空格隔开
    sideline_coefficient = models.CharField(max_length=100,verbose_name='各自技能对应的产能加成，以空格隔开')
    #副业产出物品id，以空格隔开
    sideline_product = models.CharField(max_length=100,verbose_name='副业产出物品id，以空格隔开')
    #副业产出物品的各比例。以空格隔开
    sideline_product_probability = models.CharField(max_length=100,verbose_name='副业产出物品的各比例。以空格隔开')
    #各技能增长修正，以空格隔开
    sideline_skills_increase = models.CharField(max_length=100,verbose_name='各技能增长修正，以空格隔开，不设置默认为1，设置需要全部都设置')
    #副业快乐消耗
    sideline_happy = models.CharField(max_length=20,verbose_name='快乐消耗,不设置默认15')
    #副业健康消耗
    sideline_health = models.CharField(max_length=20,verbose_name='健康消耗,不设置默认15')
    #副业精力消耗
    sideline_energy = models.CharField(max_length=20,verbose_name='精力消耗,不设置默认15')
    
    #产能算法种类
    c_type = models.IntegerField(verbose_name='产能算法种类,0:上设系数算法，1:通用产能算法')

    def __str__(self):
        return self.sideline_name
    

