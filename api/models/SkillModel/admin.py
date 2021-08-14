from django.contrib import admin
from SkillModel.models import UserBigSkill,UserSmallSkill,SkillName
from .models import SkillName

# Register your models here.
class biglist(admin.ModelAdmin):
    list_display = ('user','gengzuo','gengzuo_level','caifa','caifa_level','jianshe','jianshe_level','jiagong','jiagong_level','shejiao','shejiao_level','zhouche','zhouche_level','xumu','xumu_level')

class smalllist(admin.ModelAdmin):
    list_display = ('user','liangshi','suguo','jingji','kaiken','caiji','famu','kaicai','kantan','jianzhu','xiushan','yelian','jinsu','fangzhi'
    ,'shiping','mushi','xiongbian','jiaoji','wenshu','guanli','lushang','shuishang','bulao','shoulie','jiaqin','jiachu')

class skilllist(admin.ModelAdmin):
    list_display = ('big_id','big_name','small_id','small_name')

admin.site.register(UserBigSkill,biglist)
admin.site.register(UserSmallSkill,smalllist)
admin.site.register(SkillName,skilllist)