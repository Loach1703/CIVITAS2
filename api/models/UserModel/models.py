from django.db import models
from django.conf import settings

# Create your models here.
class usersession(models.Model):
    uid = models.CharField(max_length=20)
    sessionid = models.CharField(max_length=32)

class personal_attributes(models.Model):
    uid = models.CharField(max_length=20)
    energy = models.CharField(max_length=20)
    healthy = models.CharField(max_length=20)
    happy = models.CharField(max_length=20)
    Hunger = models.CharField(max_length=20)

def avatar_path(instance, filename):
    filename = str(instance.user.id) + '.jpg'
    return 'avatar/{0}'.format(filename)

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