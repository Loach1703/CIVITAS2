from django.db import models
from django.db import models
from django.db.models.fields import CharField, FloatField, IntegerField, SmallIntegerField
from django.db.models import JSONField
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.conf import settings
from django.db.models.fields.related_descriptors import ManyToManyDescriptor

# Create your models here.

# class Raw_material(models.Model):

#     raw_material_id = IntegerField(verbose_name='食材id',default='')
#     material_id = IntegerField(verbose_name='物品id')
#     name = CharField(max_length=20,verbose_name='食材名')
    



# class Raw_materialDetail(models.Model):
#     #食材表
#     #id = IntegerField(primary_key=True)
#     level_choices = ((1, 'Q1'), (2, 'Q2'),(3, 'Q3'))

#     r_material = ForeignKey('Raw_material',on_delete=models.CASCADE,verbose_name='食品')

#     level = SmallIntegerField(verbose_name='食材等级',default=1,choices=level_choices)
#     #name = CharField(max_length=50,verbose_name='名字')
#     health = FloatField(verbose_name='健康度')
#     Satiety = FloatField(verbose_name='饱食度')
#     salty = FloatField(verbose_name='咸')
#     sweet = FloatField(verbose_name='甜')
#     bitterness= FloatField(verbose_name='苦')
#     aroma = FloatField(verbose_name='味道度')

#     # def __str__(self):
#     #     return self.material.name+' Q.'+str(self.level)
    
#     # class Meta:
#     #     unique_together = [
#     #         'material','level'

#     #     ]

# class diet_MaterialDetail(models.Model):
#     level_choices = ((1, 'Q1'), (2, 'Q2'),(3, 'Q3'))
#     #material = ForeignKey('Material',on_delete=models.CASCADE,verbose_name='物资')
#     productivity = FloatField(verbose_name='物资自身产能')
#     level = SmallIntegerField(verbose_name='物资等级',default=1,choices=level_choices)

#     # class Meta:
#     #     unique_together = [
#     #         'level'
#     #     ]

#     def __str__(self):
#         return self.material.name+' Q.'+str(self.level)

# class Input_Recipe_Material(models.Model):
#     recipe = ForeignKey('diet_recipe',on_delete=models.CASCADE,verbose_name='配方')
#     material = ForeignKey('diet_MaterialDetail',on_delete=models.CASCADE,verbose_name='输入物资')
#     count = IntegerField(verbose_name='数量')
#     class Meta:
#         verbose_name_plural = '所需食材表'

# class diet_recipe(models.Model):
#     name = CharField(max_length=50,verbose_name='名字',default=" ")
#     Owner = IntegerField(db_index=True,verbose_name='拥有者',default=" ") #拥有者
#     input = ManyToManyField('diet_MaterialDetail',related_name='input',verbose_name='输入',through=Input_Recipe_Material)
#     health = FloatField(verbose_name='健康度',default=0.00)
#     Satiety = FloatField(verbose_name='饱食度',default=0.00)
#     acid = FloatField(verbose_name='酸',default=0.00)
#     salty = FloatField(verbose_name='咸',default=0.00)
#     sweet = FloatField(verbose_name='甜',default=0.00)
#     bitterness= FloatField(verbose_name='苦',default=0.00)
#     aroma = FloatField(verbose_name='味道度',default=0.00)
    

# class diet_materialDetail(models.Model):
#     #食材表
#     #id = IntegerField(primary_key=True)
#     level_choices = ((1, 'Q1'), (2, 'Q2'),(3, 'Q3'))
#     level = SmallIntegerField(verbose_name='物资等级',default=1,choices=level_choices)
#     class Meta:
#         unique_together = [
#             'level'
#         ]

# class Input_Recipe_Material_1(models.Model):
#     recipe = ForeignKey('diet_recipes',on_delete=models.CASCADE,verbose_name='配方id')
#     material = ForeignKey('diet_materialDetail',on_delete=models.CASCADE,verbose_name='输入物资')
#     count = IntegerField(verbose_name='数量')
 
# class diet_recipes(models.Model):

#     input = ManyToManyField('Input_Recipe_Material',related_name='input',verbose_name='输入',through=Input_Recipe_Material)
    #input = ManyToManyField('diet_materialDetail',related_name='input',through=Input_Recipe_Material)


# from django.db import models
# # Create your models here.
 
# # 手动创建第三张表,查询还方便的查询
# class Book(models.Model):
#     # 默认会创建id
#     name = models.CharField(max_length=32)
#     # 中介模型,手动指定第三张中间表是Book2Author
#     authors = models.ManyToManyField(to='Author', through='Book2Author', through_fields=('book', 'author'))
 
 
# class Author(models.Model):
#     name = models.CharField(max_length=32)
 
#     def __str__(self):
#         return self.name
 
 
# class Book2Author(models.Model):
#     id = models.AutoField(primary_key=True)
#     book = models.ForeignKey(to='Book', to_field='id',on_delete=models.CASCADE,)
#     author = models.ForeignKey(to='Author', to_field='id',on_delete=models.CASCADE)





# class Input_Recipe_Material(models.Model):
#     recipe = ForeignKey('Recipes',on_delete=models.CASCADE,verbose_name='配方id')
#     material = ForeignKey('Raw_materialDetail',on_delete=models.CASCADE,verbose_name='输入物资',default="")
#     count = IntegerField(verbose_name='数量')

#     class Meta:
#         verbose_name_plural = '所需食材表'

# class Recipes(models.Model):
#     #食谱表、食品表
#     name = CharField(max_length=50,verbose_name='名字')
#     Owner = IntegerField(db_index=True,verbose_name='拥有者') #拥有者
    
#     input = ManyToManyField('Raw_materialDetail',related_name='input',verbose_name='输入',through=Input_Recipe_Material)

#     #食谱属性
#     health = FloatField(verbose_name='健康度')
#     Satiety = FloatField(verbose_name='饱食度')
#     salty = FloatField(verbose_name='咸')
#     sweet = FloatField(verbose_name='甜')
#     bitterness= FloatField(verbose_name='苦')
#     aroma = FloatField(verbose_name='苦')


