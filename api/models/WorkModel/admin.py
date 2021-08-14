from django.contrib import admin
from .models import *
# Register your models here.
class workrecordlist(admin.ModelAdmin):
    list_display = ('uid','work_id','work_station_id','work_date')

class sidelinerecordlist(admin.ModelAdmin):
    list_display = ('uid','number_of_today_sideline','sideline_day_c','sideline_day','number_of_all_sideline')

class sidelineworklist(admin.ModelAdmin):
    list_display = ('sideline_id','sideline_name','sideline_bigskills','sideline_smallskills','sideline_coefficient','sideline_product'
    ,'sideline_product_probability','sideline_skills_increase','sideline_happy'
    ,'sideline_health','sideline_energy','c_type')

admin.site.register(work_record,workrecordlist)
admin.site.register(sideline_record,sidelinerecordlist)
admin.site.register(sideline_work,sidelineworklist)