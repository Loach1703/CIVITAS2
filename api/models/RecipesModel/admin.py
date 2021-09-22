from django.contrib import admin
from RecipesModel.models import *
# Register your models here.



# class ChoiceInline(admin.TabularInline):#物资表添加
#     model = Raw_materialDetail
#     extra = 3

# class materiallist(admin.ModelAdmin):
#     list_display = ('raw_material_id','name')
#     inlines = [ChoiceInline]


# admin.site.register(Raw_material)
# # admin.site.register(Input_Recipe_Material)
# # admin.site.register(Recipes)