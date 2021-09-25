from django.db import models

# Create your models here.
class Blog(models.Model):
    text = models.CharField(max_length=100000)
    def __str__(self):
        return self.text