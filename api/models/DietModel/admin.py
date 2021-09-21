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

class ChoiceForRecipe_input(admin.TabularInline):
    model = Input_Recipe_Material
    extra = 1
class recipelist(admin.ModelAdmin):
    list_display = ('id','所需物资')
    inlines = [ChoiceForRecipe_input]
    def 所需物资(self,obj):
        input_all = Input_Recipe_Material.objects.filter(recipe_id=obj.pk)
        list_input = []
        for i in input_all:
            list_input.append(str(i.count) +'个' + i.material.diet_material.name + 'Q' + str(i.material.level))
        return '，'.join(list_input)

admin.site.register(diet_recipe,recipelist)

