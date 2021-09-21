from .models import *
from django.contrib import admin

# Register your models here.
class ChoiceInline(admin.TabularInline):#物资表添加
    model = diet_materialDetail
    extra = 3
class materiallist(admin.ModelAdmin):
    list_display = ('material_id','name')
    inlines = [ChoiceInline]
admin.site.register(diet_material,materiallist)
admin.site.register(diet_recipes)
admin.site.register(Input_Recipe_Material)