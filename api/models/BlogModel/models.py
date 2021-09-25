from django.db import models

# Create your models here.
class Blog(models.Model):
    text = models.TextField(max_length=10000)
    def __str__(self):
        return self.text