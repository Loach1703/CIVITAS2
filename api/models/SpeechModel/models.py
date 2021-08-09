from django.db import models

# Create your models here.
class speech(models.Model):
    uid = models.CharField(max_length=20)
    text = models.CharField(max_length=1000)
    date = models.DateTimeField()

class speech_attitude(models.Model):
    uid = models.CharField(max_length=20)
    textid = models.CharField(max_length=20)
    att = models.CharField(max_length=20)