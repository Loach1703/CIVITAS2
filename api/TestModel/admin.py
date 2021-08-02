from django.contrib import admin
from .models import speech,weather,usersession,speech_attitude,personal_attributes
# Register your models here.
admin.site.register(speech)
admin.site.register(weather)
admin.site.register(usersession)
admin.site.register(speech_attitude)
admin.site.register(personal_attributes)
