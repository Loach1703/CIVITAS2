from django.db import models

# Create your models here.
class Blog(models.Model):
    text = models.TextField(max_length=10000)
    title = models.CharField(max_length=40)
    author = models.CharField(max_length=40)
    time = models.CharField(max_length=40)
    def __str__(self):
        return self.text