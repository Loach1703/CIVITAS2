from django.db import models
from django.conf import settings

# Create your models here.
class Friend(models.Model):
    from_person = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,verbose_name='发起者',related_name='friend_from_person')
    to_person = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,verbose_name='接收者',related_name='friend_to_person')
    relationship_value = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.relationship_value)

class Social_behavior(models.Model):
    from_person = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,verbose_name='发起者',related_name='social_behavior_from_person')
    to_person = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,verbose_name='接收者',related_name='social_behavior_to_person')
    relationship_value_change = models.IntegerField()
    type_choice = (
        ("公开赞扬", "公开赞扬"),
        ("公开谴责", "公开谴责"),
        ("私下表扬", "私下表扬"),
        ("私下批评", "私下批评"),
        ("赠送礼物", "赠送礼物"),
    )
    type_of_behavior = models.CharField(
        max_length=20,
        choices=type_choice,
        default="公开赞扬",
    )
    date = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=100)
    def __str__(self):
        return str(self.relationship_value_change)