from django.contrib import admin
from .models import Material,Recipe,UserMaterial,MaterialDetail,Input_Recipe_Material,Output_Recipe_Material
# Register your models here.
class ChoiceInline(admin.TabularInline):#物资表添加
    model = MaterialDetail
    extra = 3

class ChoiceForRecipe_input(admin.TabularInline):
    model = Input_Recipe_Material
    extra = 1

class ChoiceForRecipe_output(admin.TabularInline):
    model = Output_Recipe_Material
    extra = 1

class usermateriallist(admin.ModelAdmin):
    list_display = ('user','material_detail','count')

class recipelist(admin.ModelAdmin):
    list_display = ('id','所需物资','产出物资')
    inlines = [ChoiceForRecipe_input,ChoiceForRecipe_output]
    def 所需物资(self,obj):
        input_all = Input_Recipe_Material.objects.filter(recipe_id=obj.pk)
        list_input = []
        for i in input_all:
            list_input.append(str(i.count) +'个' + i.material.material.name + 'Q' + str(i.material.level))
        return '，'.join(list_input)
    def 产出物资(self,obj):
        input_all = Output_Recipe_Material.objects.filter(recipe_id=obj.pk)
        list_input = []
        for i in input_all:
            list_input.append(str(i.count) +'个' + i.material.material.name + 'Q' + str(i.material.level))
        return '，'.join(list_input)

class materiallist(admin.ModelAdmin):
    list_display = ('material_id','name')
    inlines = [ChoiceInline]

admin.site.register(Material,materiallist)
admin.site.register(Recipe,recipelist)
admin.site.register(UserMaterial,usermateriallist)