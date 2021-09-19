from django.db import models
from django.db import models
from django.db.models.fields import CharField, FloatField, IntegerField, SmallIntegerField
from django.db.models import JSONField
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.conf import settings
from django.db.models.fields.related_descriptors import ManyToManyDescriptor

# Create your models here.

class Raw_material(models.Model):
    material_id = IntegerField(verbose_name='食材id',unique=True)
    name = CharField(max_length=20,verbose_name='食材名',unique=True,null=True)



class Raw_materialDetail(models.Model):
    #食材表
    id = IntegerField(primary_key=True)
    level_choices = ((1, 'Q1'), (2, 'Q2'),(3, 'Q3'))

    r_material = ForeignKey('Raw_material',on_delete=models.CASCADE,verbose_name='食品')

    level = SmallIntegerField(verbose_name='食材等级',default=1,choices=level_choices)
    name = CharField(max_length=50,verbose_name='名字')
    health = FloatField(verbose_name='健康度')
    Satiety = FloatField(verbose_name='饱食度')
    salty = FloatField(verbose_name='咸')
    sweet = FloatField(verbose_name='甜')
    bitterness= FloatField(verbose_name='苦')
    aroma = FloatField(verbose_name='苦')

    # def __str__(self):
    #     return self.material.name+' Q.'+str(self.level)
    
    # class Meta:
    #     unique_together = [
    #         'material','level'
    #     ]
 



class Input_Recipe_Material(models.Model):
    recipe = ForeignKey('Recipes',on_delete=models.CASCADE,verbose_name='配方id')
    material = ForeignKey('Raw_materialDetail',on_delete=models.CASCADE,verbose_name='输入物资',default="")
    count = IntegerField(verbose_name='数量')

    class Meta:
        verbose_name_plural = '所需食材表'

class Recipes(models.Model):
    #食谱表、食品表
    name = CharField(max_length=50,verbose_name='名字')
    Owner = IntegerField(db_index=True,verbose_name='拥有者') #拥有者
    
    input = ManyToManyField('Raw_materialDetail',related_name='input',verbose_name='输入',through=Input_Recipe_Material)

    #食谱属性
    health = FloatField(verbose_name='健康度')
    Satiety = FloatField(verbose_name='饱食度')
    salty = FloatField(verbose_name='咸')
    sweet = FloatField(verbose_name='甜')
    bitterness= FloatField(verbose_name='苦')
    aroma = FloatField(verbose_name='苦')


