import re
import math

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
def skill_increase(skill_now,type_buff,skill_level,happiness,strategy_buff=1):
    #技能增长e^(-技能等级/4)
    change = math.exp(-skill_now / 4)
    #进门槛降低技能增长速度
    if math.floor((skill_now / 4) + 1) > skill_level:
        diff = skill_now - skill_level * 4
        change *= (1 - math.sqrt(diff))
        #直接突破，临时的，以后要算概率
        skill_level += 1
    #快乐修正，20快乐-10%增长速度
    change *= (1 + ((happiness - 60) / 200))
    #类型修正
    change *= type_buff
    #工作策略修正
    change *= strategy_buff
    #返回值
    return skill_now + change,skill_level

#增加小类技能
#参数说明
#skill_mini_now：当前小类技能
#skill_now：当前技能
#type_buff：类型修正，范围0-1，如工作则为1，演讲为0.2，等等
#happiness：当前快乐
#strategy_buff：工作策略加成，如果不是工作，则为1
def skill_mini_increase(skill_mini_now,skill_now,type_buff,happiness,strategy_buff=1):
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
    #返回值
    return skill_mini_now + change

#小类技能衰减，换日时调用
#参数说明
#skill_mini_now：当前小类技能
#skill_now：当前技能
def skill_mini_decrease(skill_mini_now,skill_now):
    #基础衰减2%+原小类的8%
    change = 0.02 + 0.08 * skill_mini_now
    #当前技能每高12点，衰减减慢一半
    change *= (1 / 2) ** (skill_now / 12)
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