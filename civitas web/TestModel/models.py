from django.db import models

# Create your models here.
class speech(models.Model):
    #name = models.CharField(max_length=20)
    text = models.CharField(max_length=280)
    date = models.DateTimeField()

#计划，用户表单的扩展，包括电话，随机长id等等。