from django.contrib import admin

# Register your models here.
from .models import speech,weather,usersession,speech_attitude,personal_attributes,work_record
# Register your models here.
admin.site.register(speech)
admin.site.register(weather)
admin.site.register(usersession)
admin.site.register(speech_attitude)
admin.site.register(personal_attributes)

admin.site.register(work_record)