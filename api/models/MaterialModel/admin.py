from django.contrib import admin
from django.db import models
from .models import Material,Recipe,UserMaterial,MaterialDetail
# Register your models here.
class usermateriallist(admin.ModelAdmin):
    list_display = ('user','material_detail','count')

class recipelist(admin.ModelAdmin):
    list_display = ('material_detail','produce_count','raw_material_detail','needed_count')

class materiallist(admin.ModelAdmin):
    list_display = ('id','name')

class materialdetaillist(admin.ModelAdmin):
    list_display = ('material','productivity','level')

admin.site.register(Material,materiallist)
admin.site.register(Recipe,recipelist)
admin.site.register(UserMaterial,usermateriallist)
admin.site.register(MaterialDetail,materialdetaillist)