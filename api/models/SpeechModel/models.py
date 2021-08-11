from django.db import models
from django.conf import settings
from django.db.models.fields.related import ManyToManyField
from django.db.models.query_utils import check_rel_lookup_compatibility

# Create your models here.
class Speech(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)
    cheer = models.IntegerField(default=0)
    onlooker = models.IntegerField(default=0)
    catcall = models.IntegerField(default=0)

    def __str__(self):
        return self.text
    
class SpeechAttitude(models.Model):
    att_choice = (
        (1,'欢呼'),
        (2,'关注'),
        (3,'倒彩')
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    speech = models.ForeignKey('Speech',on_delete=models.CASCADE)
    att = models.SmallIntegerField(choices=att_choice)

class Topic(models.Model):
    speech = models.ManyToManyField('Speech')
    topic_name = models.CharField(max_length=1000)
