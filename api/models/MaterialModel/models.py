from typing import ChainMap
from django.db import models
from django.db.models.fields import CharField, FloatField, IntegerField, SmallIntegerField, AutoField
from django.db.models.fields.related import ForeignKey, ManyToManyField, OneToOneField
from django.conf import settings

# Create your models here.
class Material(models.Model):
    material_id = IntegerField(verbose_name='物资id',unique=True)
    name = CharField(max_length=20,verbose_name='物资名',unique=True)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    raw_material_detail = ForeignKey('MaterialDetail',related_name='raw_material_detail',on_delete=models.CASCADE,verbose_name='所需物资详情')
    needed_count = FloatField(verbose_name='所需数量')
    material_detail = ForeignKey('MaterialDetail',related_name='material_detail',on_delete=models.CASCADE,verbose_name='产出物资')
    produce_count = FloatField(verbose_name='产出物资数量',default=1)

    class Meta:
        unique_together = [
            'material_detail','raw_material_detail'
        ]

    def __str__(self):
        return str(self.material_detail.material)+' Q'+str(self.material_detail.level)

class UserMaterial(models.Model):
    user = ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,verbose_name='用户')
    material_detail = ForeignKey('MaterialDetail',on_delete=models.CASCADE,verbose_name='物资详情')
    count = FloatField(verbose_name='拥有数量')

    class Meta:
        unique_together = [
            'user','material_detail'
        ]

    def __str__(self):
        return self.user.username

class MaterialDetail(models.Model):
    level_choices = ((1, 'Q1'), (2, 'Q2'),(3, 'Q3'))
    material = ForeignKey('Material',on_delete=models.CASCADE,verbose_name='物资')
    productivity = FloatField(verbose_name='物资自身产能')
    level = SmallIntegerField(verbose_name='物资等级',default=1,choices=level_choices)

    class Meta:
        unique_together = [
            'material','level'
        ]

    def __str__(self):
        return self.material.name+' Q.'+str(self.level)

