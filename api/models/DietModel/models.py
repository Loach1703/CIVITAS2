from django.db import models
from django.db.models.fields import CharField, FloatField, IntegerField, SmallIntegerField
from django.db.models import JSONField
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.conf import settings
from django.db.models.fields.related_descriptors import ManyToManyDescriptor

# Create your models here.
class diet_material(models.Model):

    
    raw_material_id = IntegerField(verbose_name='食材id',primary_key=True,default=0)
    material_id = IntegerField(verbose_name='物品id')
    name = CharField(max_length=20,verbose_name='食材名')

    def __str__(self):
        return self.name

class diet_materialDetail(models.Model):
    #食材表
    #id = IntegerField(primary_key=True)
    level_choices = ((1, 'Q1'), (2, 'Q2'),(3, 'Q3'))

    r_material = ForeignKey('diet_material',on_delete=models.CASCADE,verbose_name='食品')

    level = SmallIntegerField(verbose_name='食材等级',default=1,choices=level_choices)
    #name = CharField(max_length=50,verbose_name='名字')
    health = FloatField(verbose_name='健康度')
    Satiety = FloatField(verbose_name='饱食度')
    salty = FloatField(verbose_name='咸')
    sweet = FloatField(verbose_name='甜')
    bitterness= FloatField(verbose_name='苦')
    aroma = FloatField(verbose_name='味道度')
    

    # def __str__(self):
    #     return self.material.name+' Q.'+str(self.level)
    
    # class Meta:
    #     unique_together = [
    #         'material','level'
    #     ]
