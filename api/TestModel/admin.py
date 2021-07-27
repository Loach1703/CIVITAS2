from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.speech)
admin.site.register(models.weather)
admin.site.register(models.usersession)
admin.site.register(models.speech_attitude)
admin.site.register(models.personal_attributes)
