from django.contrib import admin
from .models import Speech,SpeechAttitude,Topic
# Register your models here.
class topiclist(admin.ModelAdmin):
    list_display = ('topic_name',)

admin.site.register(Speech)
admin.site.register(SpeechAttitude)
admin.site.register(Topic,topiclist)