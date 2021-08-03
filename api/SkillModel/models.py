from django.db import models
from django.conf import settings

# Create your models here.


class farming(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        primary_key=True,
        unique=True
    )
    skill_num = models.FloatField(default=0)
    grain = models.FloatField(default=0)
    vegetables_fruit = models.FloatField(default=0)
    cash_crops = models.FloatField(default=0)
    reclaim = models.FloatField(default=0)
    level = models.SmallIntegerField(default=1)

class cutting(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        primary_key=True,
        unique=True
    )
    skill_num = models.FloatField(default=0)
    collection = models.FloatField(default=0)
    lumbering = models.FloatField(default=0)
    exploitation = models.FloatField(default=0)
    prospecting = models.FloatField(default=0)
    level = models.SmallIntegerField(default=1)

class processing(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        primary_key=True,
        unique=True
    )
    skill_num = models.FloatField(default=0)
    smelt = models.FloatField(default=0)
    forge = models.FloatField(default=0)
    spin = models.FloatField(default=0)
    food_processing = models.FloatField(default=0)
    wood_stone_processing = models.FloatField(default=0)
    level = models.SmallIntegerField(default=1)

class social(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        primary_key=True,
        unique=True
    )
    skill_num = models.FloatField(default=0)
    eloquence = models.FloatField(default=0)
    communicate = models.FloatField(default=0)
    write = models.FloatField(default=0)
    manage = models.FloatField(default=0)
    level = models.SmallIntegerField(default=1)

class vehicle(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        primary_key=True,
        unique=True
    )
    skill_num = models.FloatField(default=0)
    land_transport = models.FloatField(default=0)
    water_transport = models.FloatField(default=0)
    fishing = models.FloatField(default=0)
    level = models.SmallIntegerField(default=1)

class husbandry(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        primary_key=True,
        unique=True
    )
    skill_num = models.FloatField(default=0)
    hunt = models.FloatField(default=0)
    fowl = models.FloatField(default=0)
    livestock = models.FloatField(default=0)
    level = models.SmallIntegerField(default=1)

class construct(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        primary_key=True,
        unique=True
    )
    skill_num = models.FloatField(default=0)
    building = models.FloatField(default=0)
    mending = models.FloatField(default=0)
    level = models.SmallIntegerField(default=1)


class UserSkill(models.Model):
    user = models.OneToOneField(
         settings.AUTH_USER_MODEL,
         on_delete=models.DO_NOTHING,
         primary_key=True,
         unique=True
    )

    farming = models.OneToOneField(
        farming,
        on_delete=models.DO_NOTHING,
        to_field='user_id',
    )

    cutting = models.OneToOneField(
        cutting,
        on_delete=models.DO_NOTHING,
        to_field='user_id',
    )

    processing = models.OneToOneField(
        processing,
        on_delete=models.DO_NOTHING,
        to_field='user_id',
    )

    social = models.OneToOneField(
        social,
        on_delete=models.DO_NOTHING,
        to_field='user_id',
    )

    vehicle = models.OneToOneField(
        vehicle,
        on_delete=models.DO_NOTHING,
        to_field='user_id',
    )

    husbandry = models.OneToOneField(
        husbandry,
        on_delete=models.DO_NOTHING,
        to_field='user_id',
    )
    
    construct = models.OneToOneField(
        construct,
        on_delete=models.DO_NOTHING,
        to_field='user_id',
    )

    def __str__(self):
        return self.name

def create_skill(user):
    f=farming.objects.create(user=user)
    c=cutting.objects.create(user=user)
    p=processing.objects.create(user=user)
    s=social.objects.create(user=user)
    v=vehicle.objects.create(user=user)
    h=husbandry.objects.create(user=user)
    b=construct.objects.create(user=user)
    UserSkill.objects.create(user=user,farming=f,cutting=c,processing=p,social=s,vehicle=v,husbandry=h,construct=b)

def get_skill(user):
    f=farming.objects.filter(user=user).first()
    c=cutting.objects.filter(user=user).first()
    p=processing.objects.filter(user=user).first()
    s=social.objects.filter(user=user).first()
    v=vehicle.objects.filter(user=user).first()
    h=husbandry.objects.filter(user=user).first()
    b=construct.objects.filter(user=user).first()
    d={
        1:f,
        2:c,
        3:b,
        4:p,
        5:s,
        6:v,
        7:h
    }
    return d
