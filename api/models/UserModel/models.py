from django.db import models
from django.conf import settings

# Create your models here.
class usersession(models.Model):
    uid = models.CharField(max_length=20)
    sessionid = models.CharField(max_length=32)

class personal_attributes(models.Model):
    uid = models.CharField(max_length=20)
    energy = models.CharField(max_length=20,verbose_name='精力')
    healthy = models.CharField(max_length=20,verbose_name='健康')
    happy = models.CharField(max_length=20,verbose_name='快乐')
    Hunger = models.CharField(max_length=20,verbose_name='饥饿')
    def __str__(self):
        return 'uid'+self.uid+'精力'+self.energy+'健康'+self.healthy+'快乐'+self.happy+'饥饿'+self.Hunger


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