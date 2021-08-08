from django.contrib import admin

# Register your models here.
from .models import *
# Register your models here.
admin.site.register(work_record)
admin.site.register(personal_attributes)
admin.site.register(speech_attitude)
admin.site.register(speech)
admin.site.register(usersession)
admin.site.register(weather)