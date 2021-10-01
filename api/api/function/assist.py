import re
import math
import random
from MaterialModel.models import Material, UserMaterial, MaterialDetail
from django.db.models import Sum, F

def is_int(para):
    try:
        return int(para)
    except:
        return "error"

def is_login(req,sessionid):
    if not sessionid:
        return 0
    if not req.session.exists(sessionid):
        return 0
    return 1


#增加技能
#参数说明
#skill_now：当前技能
#type_buff：类型修正，范围0-1，如工作则为1，演讲为0.2，等等
#skill_level：门槛，学徒，匠人等
#happiness：当前快乐
#strategy_buff：工作策略加成，如果不是工作，则为1
#comprehension：当前悟性，只有教育需要使用
def skill_increase(skill_now,type_buff,skill_level,happiness,strategy_buff=1,comprehension=0):
    #技能增长e^(-技能等级/4)
    change = math.exp(-skill_now / 4)
    #进门槛降低技能增长速度
    if math.floor((skill_now / 4) + 1) > skill_level and skill_now < 28:
        diff = skill_now - skill_level * 4
        change *= (1 - math.sqrt(diff))
        # 直接突破，临时的，以后要算概率
        # skill_level += 1
    #快乐修正，20快乐---10%增长速度
    change *= (1 + ((happiness - 60) / 200))
    #类型修正
    change *= type_buff
    #工作策略修正
    change *= strategy_buff
    #悟性修正
    change *= 1 + comprehension / 4
    #返回值
    return skill_now + change

#增加小类技能
#参数说明
#skill_now：当前技能
#skill_mini_now：当前小类技能
#type_buff：类型修正，范围0-1，如工作则为1，演讲为0.2，等等
#happiness：当前快乐
#strategy_buff：工作策略加成，如果不是工作，则为1
def skill_mini_increase(skill_now,skill_mini_now,type_buff,happiness,strategy_buff=1):
    #基础增长3%
    change = 0.03
    #当前技能每高12点，则增长速度翻一倍
    change *= 1 + (skill_now / 12)
    #当前小类技能越高，增长越慢，达到100%时增长速度减半
    change *= 1 - (skill_mini_now / 2)
    #快乐修正，20快乐-10%增长速度
    change *= (1 + ((happiness - 60) / 200))
    #类型修正
    change *= type_buff
    #工作策略修正
    change *= strategy_buff
    #不能超限
    if skill_mini_now + change > 1:
        change = 1 - skill_mini_now
    #返回值
    return skill_mini_now + change


#小类技能衰减，换日时调用
#参数说明
#skill_now：当前技能
#skill_mini_now：当前小类技能
def skill_mini_decrease(skill_now,skill_mini_now):
    #基础衰减2%+原小类的8%
    change = 0.02 + 0.08 * skill_mini_now
    #当前技能每高12点，衰减减慢一半
    change *= (1 / 2) ** (skill_now / 12)
    #不能超限
    if skill_mini_now - change < 0:
        change = skill_mini_now
    #返回值
    return skill_mini_now - change

def year_season_calc(self): #天气计算，非接口
    days = self.day - 1
    days_left = days % self.year_length
    self.year = 1 + days // self.year_length
    days_left2 = days_left % self.season_length
    self.season = 1 + days_left // self.season_length
    self.day = days_left2 + 1

def validateEmail(email):
    if len(email) > 7:
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
            return 1
    return 0

def status_recover(stamina,happiness,health,starvation,house_type,house_level):
    #睡大街
    if house_type == 0:
        stamina_house_bonus = 0
        happiness_house_bonus = 0
        health_house_bonus = 0
    #楼房
    if house_type == 1:
        stamina_house_bonus = 10 * house_level
        happiness_house_bonus = 0.4 * (house_level - 1)
        health_house_bonus = 0.4 * (house_level - 1)
    #宅院
    if house_type == 2:
        stamina_house_bonus = 10 * house_level
        happiness_house_bonus = 0.2 + 0.6 * (house_level - 1)
        health_house_bonus = 0.2 + 0.6 * (house_level - 1)
    stamina_change = (30 + stamina_house_bonus) * (1 + ((health - 60) / 80))
    happiness_change = 3 + 0.2 * (min(60,starvation,health) - happiness) + 0.05 * (max(0,stamina + stamina_change - 100)) + happiness_house_bonus
    health_change = 3 + 0.2 * (min(60,starvation,stamina + 40) - health) + 0.05 * (max(0,stamina + stamina_change - 100)) + health_house_bonus
    starvation_change = -(0.08 * starvation + 2)
    really_stamina_change = stamina_change
    really_happiness_change = happiness_change
    really_health_change = health_change
    really_starvation_change = starvation_change
    #处理超界
    if stamina + stamina_change > 100:
        really_stamina_change = 100 - stamina
    elif stamina + stamina_change < 0:
        really_stamina_change = stamina
    if happiness + happiness_change > 100:
        really_happiness_change = 100 - happiness
    elif happiness + happiness_change < 0:
        really_happiness_change = happiness
    if health + health_change > 100:
        really_health_change = 100 - health
    elif health + health_change < 0:
        really_health_change = health
    if starvation + starvation_change > 100:
        really_starvation_change = 100 - starvation
    elif starvation + starvation_change < 0:
        really_starvation_change = starvation
    stamina += really_stamina_change
    happiness += really_happiness_change
    health += really_health_change
    starvation += really_starvation_change
    stamina = round(stamina,1)
    happiness = round(happiness,1)
    health = round(health,1)
    starvation = round(starvation,1)
    really_stamina_change = round(really_stamina_change,1)
    really_happiness_change = round(really_happiness_change,1)
    really_health_change = round(really_health_change,1)
    really_starvation_change = round(really_starvation_change,1)
    reply_data = {
        "stamina":stamina,
        "happiness":happiness,
        "health":health,
        "starvation":starvation,
        "stamina_change":really_stamina_change,
        "happiness_change":really_happiness_change,
        "health_change":really_health_change,
        "starvation_change":really_starvation_change,
    }
    return reply_data

def random_choice(sequence, probability):
    x = random.uniform(0, 1)
    cumulative_probability = 0.0
    for item, item_probability in zip(sequence, probability):
        cumulative_probability += item_probability
        if x < cumulative_probability:
            break
    return item

#计算是否突破
#参数说明
#skill_now：当前技能
#level：等级（学徒：1，匠人：2......）
#comprehension：悟性，数值为0-1
def eureka(skill_now,level,comprehension):
    if not (math.floor((skill_now / 4) + 1) > level and level < 7):
        return False
    #基础突破概率
    eureka_0 = 0.5
    #与门槛基础差值提高基础概率，最高为3倍
    diff = skill_now - level * 4
    eureka_really = eureka_0 * (1 + diff * 2)
    num = random.random()
    #悟性提高突破概率，最高为2倍
    eureka_really *= comprehension + 1
    #实际突破概率，每高一级等级就降低一半
    eureka_really *= 1 / (2 ** level)
    #判断是否突破，需要返回突破概率，因为前端要显示，如果有其他办法显示也可以不返回
    if num < eureka_really:
        return True
    else:
        return False

def eureka_chance(skill_now,level,comprehension):
    if not (math.floor((skill_now / 4) + 1) > level and level < 7):
        return 0.0
    eureka_0 = 0.5
    diff = skill_now - level * 4
    eureka_really = eureka_0 * (1 + diff * 2)
    #悟性提高突破概率，最高为2倍
    eureka_really *= comprehension + 1
    #实际突破概率，每高一级等级就降低一半
    eureka_really *= 1 / (2 ** level)
    return eureka_really

#悟性增加
#参数说明
#skill_now：当前技能
def comprehension_increase(skill_now,comprehension_now):
    #增加0.1+当前技能/100
    change = 0.1 + skill_now / 100
    if comprehension_now + change <= 1:
        return comprehension_now + change
    else:
        return 1.0

#悟性换日减少
#参数说明
#comprehension：当前悟性
def comprehension_decrease(comprehension):
    #减少0.05+当前悟性*0.2
    change = 0.05 + comprehension * 0.2
    return change

#删除数据库中某项物品
def del_material(uid,material_id,level,count):
    material_detail = MaterialDetail.object.filter(Material__material_id=material_id).filter(level=level).first()
    usermaterial = UserMaterial.objects.filter(user__id=uid).filter(material_detail=material_detail)
    if usermaterial.exists():
        u = usermaterial
        usermaterial = usermaterial.first()
        if usermaterial.count < count:
            return 0
        elif usermaterial.count > count:
            usermaterial.count = F('count') - count
        elif usermaterial.count == count:
            u.delete()
            return 1
    else:
        return 0