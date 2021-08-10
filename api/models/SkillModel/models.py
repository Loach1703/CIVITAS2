from django.conf import settings
from django.db import models
from django.db.models.base import Model
from django.db.models.enums import Choices
# Create your models here.
class UserBigSkill(models.Model):
    level_choices = (
        (1,'学徒'),
        (2,'匠人'),
        (3,'匠师'),
        (4,'专家'),
        (5,'大师'),
        (6,'宗师'),
        (7,'大宗师'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    gengzuo = models.FloatField(verbose_name='耕作技能点',default=0)
    gengzuo_level = models.SmallIntegerField(choices=level_choices,verbose_name='耕作等级',default=1)
    caifa = models.FloatField(verbose_name='采伐技能点',default=0)
    caifa_level = models.SmallIntegerField(choices=level_choices,verbose_name='采伐等级',default=1)
    jianshe = models.FloatField(verbose_name='建设技能点',default=0)
    jianshe_level = models.SmallIntegerField(choices=level_choices,verbose_name='建设等级',default=1)
    jiagong = models.FloatField(verbose_name='加工技能点',default=0)
    jiagong_level = models.SmallIntegerField(choices=level_choices,verbose_name='加工等级',default=1)
    shejiao = models.FloatField(verbose_name='社交技能点',default=0)
    shejiao_level = models.SmallIntegerField(choices=level_choices,verbose_name='社交等级',default=1)
    zhouche = models.FloatField(verbose_name='舟车技能点',default=0)
    zhouche_level = models.SmallIntegerField(choices=level_choices,verbose_name='舟车等级',default=1)
    xumu = models.FloatField(verbose_name='畜牧技能点',default=0)
    xumu_level = models.SmallIntegerField(choices=level_choices,verbose_name='畜牧等级',default=1)

    def __str__(self):
        return self.user.username

class UserSmallSkill(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    liangshi = models.FloatField(verbose_name='耕作——粮食种植技能点',default=0)
    suguo = models.FloatField(verbose_name='耕作——蔬果种植技能点',default=0)
    jingji = models.FloatField(verbose_name='耕作——经济作物种植技能点',default=0)
    kaiken = models.FloatField(verbose_name='耕作——开垦技能点',default=0)
    caiji = models.FloatField(verbose_name='采伐——采集技能点',default=0)
    famu = models.FloatField(verbose_name='采伐——伐木技能点',default=0)
    kaicai = models.FloatField(verbose_name='采伐——开采技能点',default=0)
    kantan = models.FloatField(verbose_name='采伐——勘探技能点',default=0)
    jianzhu = models.FloatField(verbose_name='建设——建筑技能点',default=0)
    xiushan = models.FloatField(verbose_name='建设——修缮技能点',default=0)
    yelian = models.FloatField(verbose_name='加工——冶炼技能点',default=0)
    jinsu = models.FloatField(verbose_name='加工——金属锻造技能点',default=0)
    fangzhi = models.FloatField(verbose_name='加工——纺织技能点',default=0)
    shiping = models.FloatField(verbose_name='加工——食品加工技能点',default=0)
    mushi = models.FloatField(verbose_name='加工——木石加工技能点',default=0)
    xiongbian = models.FloatField(verbose_name='社交——雄辩技能点',default=0)
    jiaoji = models.FloatField(verbose_name='社交——交际技能点',default=0)
    wenshu = models.FloatField(verbose_name='社交——文书技能点',default=0)
    guanli = models.FloatField(verbose_name='社交——管理技能点',default=0)
    lushang = models.FloatField(verbose_name='舟车——陆上运输技能点',default=0)
    shuishang = models.FloatField(verbose_name='舟车——水上运输技能点',default=0)
    bulao = models.FloatField(verbose_name='舟车——捕捞技能点',default=0)
    shoulie = models.FloatField(verbose_name='畜牧——狩猎技能点',default=0)
    jiaqin = models.FloatField(verbose_name='畜牧——家禽养殖技能点',default=0)
    jiachu = models.FloatField(verbose_name='畜牧——家畜养殖技能点',default=0)

    def __str__(self):
        return self.user.username

class SkillName(models.Model):
    big_id = models.SmallIntegerField(verbose_name='大类id')
    big_name = models.CharField(max_length=20,verbose_name='大类名称')
    small_id = models.SmallIntegerField(verbose_name='大类下的小类id')
    small_name = models.CharField(max_length=20,verbose_name='小类名称')

    def __str__(self):
        return self.big_name + "——" + self.small_name

# from django.core.exceptions import ValidationError
# from django.utils.translation import gettext_lazy as _

# class UserSkill(models.Model):
#     level_choices = (
#         (1,'学徒'),
#         (2,'匠人'),
#         (3,'匠师'),
#         (4,'专家'),
#         (5,'大师'),
#         (6,'宗师'),
#         (7,'大宗师'),
#     )
#     user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
#     big_skill = models.ForeignKey('BigSkill',on_delete=models.CASCADE,verbose_name='大类技能',blank=True,null=True)
#     big_level = models.SmallIntegerField(choices=level_choices,verbose_name='大类技能等级',blank=True,null=True)
#     big_skillnum = models.FloatField(verbose_name='大类技能点',blank=True,null=True)
#     small_skill = models.ForeignKey('SmallSkill',on_delete=models.CASCADE,verbose_name='小类技能',blank=True,null=True)
#     small_skillnum = models.FloatField(verbose_name='小类技能点',blank=True,null=True)

#     class Meta:
#         unique_together = (
#             ('user','big_skill'),
#             ('user','small_skill')
#         )

#     def clean(self):
#         if self.big_skill == None and self.small_skill == None:
#             raise ValidationError(_('大类技能和小类技能不能同时为空'))
#         elif self.big_skill != None and self.small_skill != None:
#             raise ValidationError(_('大类技能和小类技能不能同时存在'))
#         elif self.big_skill != None and (self.big_skillnum == None or self.big_level == None):
#             raise ValidationError(_('大类技能已选择，必须提供大项技能点和技能等级'))
#         elif self.small_skill != None and self.small_skillnum == None:
#             raise ValidationError(_('小类技能已选择，必须提供小项技能点'))
#         elif self.big_skill != None and self.small_skillnum != None:
#             raise ValidationError(_('大项技能已经选择，不能提供小项技能点'))
#         elif self.small_skill != None and (self.big_skillnum != None or self.big_level != None):
#             raise ValidationError(_('小项技能已经选择，不能提供大项技能点或技能等级'))
#         else:
#             pass
    
#     def save(self, *args, **kwargs):
#         from django.core.exceptions import NON_FIELD_ERRORS
#         try:
#             self.full_clean()
#             super().save(*args, **kwargs)
#         except ValidationError as e:
#             print('验证没通过： %s' % e.message_dict[NON_FIELD_ERRORS])


#     def __str__(self):
#         return self.user.username

# class BigSkill(models.Model):
#     id = models.SmallIntegerField(primary_key=True,verbose_name='大类技能id')
#     name = models.CharField(max_length=20,verbose_name='大类技能名称')

#     def __str__(self):
#         return self.name

# class SmallSkill(models.Model):
#     sub = models.ForeignKey('BigSkill',on_delete=models.CASCADE,verbose_name='所属大类')
#     subid = models.SmallIntegerField(verbose_name='大类下的小类id')
#     name = models.CharField(max_length=20,verbose_name='小类名称')
#     class Meta:
#         unique_together = [
#             'sub','subid'
#         ]

#     def __str__(self):
#         return self.name

# class farming(models.Model):
#     user = models.OneToOneField(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.DO_NOTHING,
#         primary_key=True,
#         unique=True
#     )
#     skill_num = models.FloatField(default=0)
#     grain = models.FloatField(default=0)
#     vegetables_fruit = models.FloatField(default=0)
#     cash_crops = models.FloatField(default=0)
#     reclaim = models.FloatField(default=0)
#     level = models.SmallIntegerField(default=1)

#     def __str__(self):
#         return "技能点："+str(self.skill_num)+" 等级："+str(self.level)

# class cutting(models.Model):
#     user = models.OneToOneField(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.DO_NOTHING,
#         primary_key=True,
#         unique=True
#     )
#     skill_num = models.FloatField(default=0)
#     collection = models.FloatField(default=0)
#     lumbering = models.FloatField(default=0)
#     exploitation = models.FloatField(default=0)
#     prospecting = models.FloatField(default=0)
#     level = models.SmallIntegerField(default=1)

#     def __str__(self):
#         return "技能点："+str(self.skill_num)+" 等级："+str(self.level)

# class processing(models.Model):
#     user = models.OneToOneField(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.DO_NOTHING,
#         primary_key=True,
#         unique=True
#     )
#     skill_num = models.FloatField(default=0)
#     smelt = models.FloatField(default=0)
#     forge = models.FloatField(default=0)
#     spin = models.FloatField(default=0)
#     food_processing = models.FloatField(default=0)
#     wood_stone_processing = models.FloatField(default=0)
#     level = models.SmallIntegerField(default=1)

#     def __str__(self):
#         return "技能点："+str(self.skill_num)+" 等级："+str(self.level)

# class social(models.Model):
#     user = models.OneToOneField(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.DO_NOTHING,
#         primary_key=True,
#         unique=True
#     )
#     skill_num = models.FloatField(default=0)
#     eloquence = models.FloatField(default=0)
#     communicate = models.FloatField(default=0)
#     write = models.FloatField(default=0)
#     manage = models.FloatField(default=0)
#     level = models.SmallIntegerField(default=1)

#     def __str__(self):
#         return "技能点："+str(self.skill_num)+" 等级："+str(self.level)

# class vehicle(models.Model):
#     user = models.OneToOneField(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.DO_NOTHING,
#         primary_key=True,
#         unique=True
#     )
#     skill_num = models.FloatField(default=0)
#     land_transport = models.FloatField(default=0)
#     water_transport = models.FloatField(default=0)
#     fishing = models.FloatField(default=0)
#     level = models.SmallIntegerField(default=1)

#     def __str__(self):
#         return "技能点："+str(self.skill_num)+" 等级："+str(self.level)
        
# class husbandry(models.Model):
#     user = models.OneToOneField(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.DO_NOTHING,
#         primary_key=True,
#         unique=True
#     )
#     skill_num = models.FloatField(default=0)
#     hunt = models.FloatField(default=0)
#     fowl = models.FloatField(default=0)
#     livestock = models.FloatField(default=0)
#     level = models.SmallIntegerField(default=1)

#     def __str__(self):
#         return "技能点："+str(self.skill_num)+" 等级："+str(self.level)

# class construct(models.Model):
#     user = models.OneToOneField(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.DO_NOTHING,
#         primary_key=True,
#         unique=True
#     )
#     skill_num = models.FloatField(default=0)
#     building = models.FloatField(default=0)
#     mending = models.FloatField(default=0)
#     level = models.SmallIntegerField(default=1)

#     def __str__(self):
#         return "技能点："+str(self.skill_num)+" 等级："+str(self.level)

# class UserSkill(models.Model):
#     user = models.OneToOneField(
#          settings.AUTH_USER_MODEL,
#          on_delete=models.DO_NOTHING,
#          primary_key=True,
#          unique=True
#     )

#     farming = models.OneToOneField(
#         farming,
#         on_delete=models.DO_NOTHING,
#         to_field='user_id',
#     )

#     cutting = models.OneToOneField(
#         cutting,
#         on_delete=models.DO_NOTHING,
#         to_field='user_id',
#     )

#     processing = models.OneToOneField(
#         processing,
#         on_delete=models.DO_NOTHING,
#         to_field='user_id',
#     )

#     social = models.OneToOneField(
#         social,
#         on_delete=models.DO_NOTHING,
#         to_field='user_id',
#     )

#     vehicle = models.OneToOneField(
#         vehicle,
#         on_delete=models.DO_NOTHING,
#         to_field='user_id',
#     )

#     husbandry = models.OneToOneField(
#         husbandry,
#         on_delete=models.DO_NOTHING,
#         to_field='user_id',
#     )
    
#     construct = models.OneToOneField(
#         construct,
#         on_delete=models.DO_NOTHING,
#         to_field='user_id',
#     )

#     def __str__(self):
#         return self.user.username

# def create_skill(user):
#     f=farming.objects.create(user=user)
#     c=cutting.objects.create(user=user)
#     p=processing.objects.create(user=user)
#     s=social.objects.create(user=user)
#     v=vehicle.objects.create(user=user)
#     h=husbandry.objects.create(user=user)
#     b=construct.objects.create(user=user)
#     UserSkill.objects.create(user=user,farming=f,cutting=c,processing=p,social=s,vehicle=v,husbandry=h,construct=b)

# def get_skill(user):
#     f=farming.objects.filter(user=user).first()
#     c=cutting.objects.filter(user=user).first()
#     p=processing.objects.filter(user=user).first()
#     s=social.objects.filter(user=user).first()
#     v=vehicle.objects.filter(user=user).first()
#     h=husbandry.objects.filter(user=user).first()
#     b=construct.objects.filter(user=user).first()
#     d={
#         1:f,
#         2:c,
#         3:b,
#         4:p,
#         5:s,
#         6:v,
#         7:h
#     }
#     return d


