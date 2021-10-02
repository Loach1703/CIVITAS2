from django.contrib import admin
from .models import *
# Register your models here.
class friend_display(admin.ModelAdmin):
    list_display = ('from_person','to_person','relationship_value','date',)

admin.site.register(Friend,friend_display)
admin.site.register(Social_behavior)