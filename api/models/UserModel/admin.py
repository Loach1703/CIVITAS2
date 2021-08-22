from django.contrib import admin
from .models import usersession,Avatar,personal_attributes
# Register your models here.
class attributes(admin.ModelAdmin):
    list_display = ('uid','energy','healthy','happy','Hunger')
admin.site.register(usersession)
admin.site.register(Avatar)
admin.site.register(personal_attributes,attributes)