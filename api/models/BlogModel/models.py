from django.db import models
from django.conf import settings

# Create your models here.
class Blog(models.Model):
    text = models.TextField(max_length=10000)
    title = models.CharField(max_length=40)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,verbose_name='作者')
    time = models.DateField()
    def __str__(self):
        return self.title