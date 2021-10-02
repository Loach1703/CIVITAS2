from django.contrib import admin
from .models import *
# Register your models here.
class friend_display(admin.ModelAdmin):
    list_display = ('from_person','to_person','relationship_value','date',)

class social_behavior_display(admin.ModelAdmin):
    list_display = ('from_person','to_person','relationship_value_change','type_of_behavior','date','message',)

admin.site.register(Friend,friend_display)
admin.site.register(Social_behavior,social_behavior_display)