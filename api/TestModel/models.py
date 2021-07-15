from django.db import models

# Create your models here.
class speech(models.Model):
    #name = models.CharField(max_length=20)
    text = models.CharField(max_length=280)
    date = models.DateTimeField()