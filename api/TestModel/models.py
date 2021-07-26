from django.db import models

# Create your models here.
class speech(models.Model):
    uid = models.CharField(max_length=20)
    text = models.CharField(max_length=280)
    date = models.DateTimeField()


class weather(models.Model):
    city = models.CharField(max_length=20)
    total_day = models.CharField(max_length=20)
    year = models.CharField(max_length=20)
    season = models.CharField(max_length=20)
    day = models.CharField(max_length=20)
    weather = models.CharField(max_length=20)
    temperature = models.CharField(max_length=20)
    rain_num = models.CharField(max_length=20)

class usersession(models.Model):
    uid = models.CharField(max_length=20)
    sessionid = models.CharField(max_length=32)