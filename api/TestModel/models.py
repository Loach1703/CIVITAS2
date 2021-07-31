from django.db import models
from django.conf import settings

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

class speech_attitude(models.Model):
    uid = models.CharField(max_length=20)
    textid = models.CharField(max_length=20)
    att = models.CharField(max_length=20)

class personal_attributes(models.Model):
    uid = models.CharField(max_length=20)
    energy = models.CharField(max_length=20)
    healthy = models.CharField(max_length=20)
    happy = models.CharField(max_length=20)
    Hunger = models.CharField(max_length=20) 

class Avatar(models.Model):
    user = models.OneToOneField(
         settings.AUTH_USER_MODEL,
         on_delete=models.DO_NOTHING,
         primary_key=True,
    )
    avatar = models.ImageField(
        verbose_name="头像",
        upload_to=avatar_path,
    )

    def __str__(self):
        return self.name
