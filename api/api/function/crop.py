import numpy
import random

#定义作物类
class crop(object):

    #作物有以下10个参数：作物名，作物所需产能，最低灌溉值，最适灌溉值，最高灌溉值，最适肥力值，最低温度，最适温度，最高温度，生产修正
    #灌溉值：0-300
    #肥力值：0-100
    #生产修正:正/负，增加/减少buff和debuff
    def __init__(self,name="杂草",capacity=1,min_irrigation=0,optimal_irrigation=100,max_irrigation=200,max_fertility=20,\
        min_temperature=0,optimal_temperature=10,max_temperature=20,production_correction=0):
        self.name = name
        self.capacity = capacity
        self.min_irrigation = min_irrigation
        self.optimal_irrigation = optimal_irrigation
        self.max_irrigation = max_irrigation
        self.max_fertility = max_fertility
        self.min_temperature = min_temperature
        self.optimal_temperature = optimal_temperature
        self.max_temperature = max_temperature
        self.production_correction = production_correction
        #生产修正不能超过0.5，否则出问题
        if self.production_correction >= 0.5:
            raise IOError("生产修正不能超过0.5！")
        #三个buff：灌溉，肥力，气温
        self.max_irrigation_buff = 0.5 + self.production_correction
        self.max_fertility_buff = 0.5 + self.production_correction
        self.max_temperature_buff = 0.5 + self.production_correction
        #一半最适肥力，1/4最适肥力
        self.max_fertility_half = max_fertility / 2
        self.max_fertility_quarter = max_fertility / 4
        #灌溉最适区间
        self.optimal_irrigation_section_min = self.optimal_irrigation - (self.optimal_irrigation - self.min_irrigation) / 4
        self.optimal_irrigation_section_max = self.optimal_irrigation + (self.max_irrigation - self.optimal_irrigation) / 4
        #灌溉中点
        self.midpoint_irrigation_min = (self.min_irrigation + self.optimal_irrigation_section_min) / 2
        self.midpoint_irrigation_max = (self.max_irrigation + self.optimal_irrigation_section_max) / 2
        #中点对应长度
        self.length_irrigation_min = self.optimal_irrigation_section_min - self.min_irrigation
        self.length_irrigation_max = self.max_irrigation - self.optimal_irrigation_section_max
        #灌溉适宜区间长
        self.length_irrigation_section = self.max_irrigation - min_irrigation
        #温度最适区间
        self.optimal_temperature_section_min = self.optimal_temperature - (self.optimal_temperature - self.min_temperature) / 4
        self.optimal_temperature_section_max = self.optimal_temperature + (self.max_temperature - self.optimal_temperature) / 4
        #温度中点
        self.midpoint_temperature_min = (self.min_temperature + self.optimal_temperature_section_min) / 2
        self.midpoint_temperature_max = (self.max_temperature + self.optimal_temperature_section_max) / 2
        #中点对应长度
        self.length_temperature_min = self.optimal_temperature_section_min - self.min_temperature
        self.length_temperature_max = self.max_temperature - self.optimal_temperature_section_max
        #温度适宜区间长
        self.length_temperature_section = self.max_temperature - min_temperature

    #计算产能buff/debuff的主函数
    def calculation(self,irrigation,fertility,temperature):
        #调用灌溉buff计算函数
        irrigation_buff = self.irrigation_calculation(irrigation)
        #调用肥力buff计算函数
        fertility_buff = self.fertility_calculation(fertility)
        #调用温度buff计算函数
        temperature_buff = self.temperature_calculation(temperature)
        #乘算
        buff = (1 + irrigation_buff) * (1 + fertility_buff) * (1 + temperature_buff)
        if self.name == "小麦":
            print(irrigation_buff,fertility_buff,temperature_buff)
        #返回加成
        return buff

    #返回分开buff/debuff的主函数
    def calculation2(self,irrigation,fertility,temperature):
        #调用灌溉buff计算函数
        irrigation_buff = self.irrigation_calculation(irrigation)
        #调用肥力buff计算函数
        fertility_buff = self.fertility_calculation(fertility)
        #调用温度buff计算函数
        temperature_buff = self.temperature_calculation(temperature)
        #返回加成
        return irrigation_buff,fertility_buff,temperature_buff

    #肥力buff计算函数
    def fertility_calculation(self,fertility):
        #大于最适肥力值，最大buff值
        if fertility >= self.max_fertility:
            return self.max_fertility_buff
        #小于最适肥力值，三种情况：
        #小于最适的1/4，debuff，公式：-根号(肥力/最适肥力1/4)*最大肥力buff
        elif fertility <= self.max_fertility_quarter:
            difference_value = self.max_fertility_quarter - fertility
            difference_percentage = difference_value / self.max_fertility_quarter
            return -difference_percentage ** 2 * self.max_fertility_buff
        #小于最适的一半，无任何加成
        elif fertility <= self.max_fertility_half:
            return 0
        #大于最适的一半，buff，公式：(与最适肥力一半的差值/最适肥力一半)平方*最大肥力buff
        elif fertility >= self.max_fertility_half:
            difference_value = fertility - self.max_fertility_half
            difference_percentage = difference_value / self.max_fertility_half
            return difference_percentage ** 2 * self.max_fertility_buff

    #灌溉值buff计算函数
    def irrigation_calculation(self,irrigation):
        #小于最小灌溉值或大于最大灌溉值，debuff最大
        if irrigation <= self.min_irrigation or irrigation >= self.max_irrigation:
            return -self.max_irrigation_buff
        #在最适区间内，buff最大
        elif irrigation <= self.optimal_irrigation_section_max and irrigation >= self.optimal_irrigation_section_min:
            return self.max_irrigation_buff
        #大于最小灌溉值，小于最适区间最小值
        elif irrigation > self.min_irrigation and irrigation < self.optimal_irrigation_section_min:
            #小于最小中点，debuff
            if irrigation < self.midpoint_irrigation_min:
                difference_value = self.midpoint_irrigation_min - irrigation
                difference_percentage = difference_value / self.length_irrigation_min * 2
                return -difference_percentage ** 2 * self.max_irrigation_buff
            #大于，buff
            else:
                difference_value = irrigation - self.midpoint_irrigation_min
                difference_percentage = difference_value / self.length_irrigation_min * 2
                return difference_percentage ** 2 * self.max_irrigation_buff
        #大于最适区间最大值，小于最大灌溉值
        elif irrigation < self.max_irrigation and irrigation > self.optimal_irrigation_section_max:
            #大于最大中点，debuff
            if irrigation > self.midpoint_irrigation_max:
                difference_value = irrigation - self.midpoint_irrigation_max
                difference_percentage = difference_value / self.length_irrigation_max * 2
                return -difference_percentage ** 2 * self.max_irrigation_buff
            #大于，buff
            else:
                difference_value = self.midpoint_irrigation_max - irrigation
                difference_percentage = difference_value / self.length_irrigation_max * 2
                return difference_percentage ** 2 * self.max_irrigation_buff

    #温度buff计算函数
    def temperature_calculation(self,temperature):
        #小于最小温度值或大于最大温度值，debuff最大
        if temperature <= self.min_temperature or temperature >= self.max_temperature:
            return -self.max_temperature_buff
        #在最适区间内，buff最大
        elif temperature <= self.optimal_temperature_section_max and temperature >= self.optimal_temperature_section_min:
            return self.max_temperature_buff
        #大于最小温度值，小于最适区间最小值
        elif temperature > self.min_temperature and temperature < self.optimal_temperature_section_min:
            #小于最小中点，debuff
            if temperature < self.midpoint_temperature_min:
                difference_value = self.midpoint_temperature_min - temperature
                difference_percentage = difference_value / self.length_temperature_min * 2
                return -difference_percentage ** 2 * self.max_temperature_buff
            #大于，buff
            else:
                difference_value = temperature - self.midpoint_temperature_min
                difference_percentage = difference_value / self.length_temperature_min * 2
                return difference_percentage ** 2 * self.max_temperature_buff
        #大于最适区间最大值，小于最大温度值
        elif temperature < self.max_temperature and temperature > self.optimal_temperature_section_max:
            #大于最大中点，debuff
            if temperature > self.midpoint_temperature_max:
                difference_value = temperature - self.midpoint_temperature_max
                difference_percentage = difference_value / self.length_temperature_max * 2
                return -difference_percentage ** 2 * self.max_temperature_buff
            #大于，buff
            else:
                difference_value = self.midpoint_temperature_max - temperature
                difference_percentage = difference_value / self.length_temperature_max * 2
                return difference_percentage ** 2 * self.max_temperature_buff

#定义城市类
class city(object):

    #城市基本参数：名称，平均温度，温差（夏季与冬季平均温差），平均年降水量，平均降水日数，气候，平均年日照时数
    #状态相关参数：当前日期，当前温度，当前降水量，当前天气
    #灌溉与肥力相关参数：默认灌溉值（最小，平均，最大），默认肥力值（泛滥肥力值，如果不会泛滥/泛滥不引起变化则不要填此字段，默认为None）
    def __init__(self,name="城市",average_temperature=15,temperature_difference=20,average_rain=1000,average_rain_day=100,climate="tem",average_sunlight_hour=1000,\
        day=1,now_temperature=0,now_rain_num=0,now_weather="晴",\
        min_irrigation_default=0,average_irrigation_default=50,max_irrigation_default=100,\
        fertility_default=20,flooding_fertility_default=None):
        self.name = name
        self.average_temperature = average_temperature
        self.temperature_difference = temperature_difference
        self.average_rain = average_rain
        self.average_rain_day = average_rain_day
        self.climate = climate
        self.average_sunlight_hour = average_sunlight_hour
        self.min_irrigation_default = min_irrigation_default
        self.average_irrigation_default = average_irrigation_default
        self.max_irrigation_default = max_irrigation_default
        self.raw_fertility_default = fertility_default
        self.flooding_fertility_default = flooding_fertility_default
        #年份长度，一般不要变
        self.year_length = 80
        self.season_length = int(self.year_length / 4)
        #定义气温最高/最低阈值
        self.max_threshold = self.average_temperature + self.temperature_difference
        self.min_threshold = self.average_temperature - self.temperature_difference
        #定义夏/冬均温
        self.average_summer = self.average_temperature + self.temperature_difference / 2
        self.average_winter = self.average_temperature - self.temperature_difference / 2
        self.average_summer_winter_difference = self.average_summer - self.average_winter
        #初始化开始日期，季节，年份，季节1，2，3，4为春夏秋冬
        self.day = day
        self.really_day = day
        self.season = 1
        self.year = 1
        self.year_season_calc()
        #初始化天气参数
        self.weather_list = ["晴","多云","阴","小雨","小雪","大雨","大雪"]
        self.rain_day = 0
        self.weather = now_weather
        self.rain_num = now_rain_num
        self.temperature = now_temperature
        self.average_rain_num = self.average_rain / self.average_rain_day
        #冲突的天气参数，抛出错误
        if self.weather not in self.weather_list:
            raise IOError("不存在的天气类型！")
        if (self.weather == "小雨" or self.weather == "小雪" or self.weather == "大雨" or self.weather == "大雪") and self.rain_num == 0:
            raise IOError("雨天降水量不能为0！")
        if (self.weather == "晴" or self.weather == "多云" or self.weather == "阴") and self.rain_num != 0:
            raise IOError("不是雨天不能有降水量！")
        #是否下雨
        if self.weather == "小雨" or self.weather == "小雪" or self.weather == "大雨" or self.weather == "大雪":
            self.rain = True
        else:
            self.rain = False
        #初始化灌溉/肥力参数
        self.irrigation_default = self.average_irrigation_default
        self.fertility_default = self.raw_fertility_default
        self.flooding = False
        if self.flooding_fertility_default != None:
            self.whether_flooding = True
        else:
            self.whether_flooding = False

        #气候对应降水概率 
        #rain_chance_list 季节降水概率 公式：(某季节降水日数)/90
        #rain_season_buff_list 季节降水量修正 公式：(某季节降水量)/(某季节降水日数)/平均日降水量
        #气候类型说明：tem：温带季风 strm：亚热带季风 trm：热带季风 ms：地中海 tc：温带大陆 tes：温带海洋
        #温带季风（北京）
        if self.climate == "tem":
            self.rain_chance_list = [0.16,0.37,0.17,0.07]
            self.rain_season_buff_list = [0.65,1.38,0.81,0.21]
            self.raw_rain_days = 69
        #亚热带季风（上海）
        elif self.climate == "strm":
            self.rain_chance_list = [0.37,0.42,0.27,0.3]
            self.rain_season_buff_list = [0.78,1.51,0.89,0.67]
            self.raw_rain_days = 122
        #热带季风（高雄）
        elif self.climate == "trm":
            self.rain_chance_list = [0.2,0.47,0.19,0.1]
            self.rain_season_buff_list = [0.74,1.36,0.79,0.27]
            self.raw_rain_days = 87
        #地中海（罗马）
        elif self.climate == "ms":
            self.rain_chance_list = [0.21,0.08,0.24,0.29]
            self.rain_season_buff_list = [0.79,0.95,1.28,0.94]
            self.raw_rain_days = 74
        #温带大陆（莫斯科）
        elif self.climate == "tc":
            self.rain_chance_list = [0.39,0.49,0.5,0.59]
            self.rain_season_buff_list = [0.87,1.41,1.08,0.68]
            self.raw_rain_days = 178
        #温带海洋（伦敦）
        elif self.climate == "tes":
            self.rain_chance_list = [0.3,0.26,0.32,0.34]
            self.rain_season_buff_list = [0.90,1.08,1.10,0.91]
            self.raw_rain_days = 110
        #默认参数
        else:
            self.rain_chance_list = [0.2,0.2,0.2,0.2]
            self.rain_season_buff_list = [1,1,1,1]
            self.raw_rain_days = 100
        #真实降水概率，根据降水日数进行修正
        for i,x in enumerate(self.rain_chance_list):
            self.rain_chance_list[i] = x * self.average_rain_day / self.raw_rain_days

        #根据日照时数，进行晴/多云/阴概率修正
        #天文日照时数，取4500
        self.max_sunlight_hour = 4500
        #去掉下雨日数
        self.no_rain_sunlight_hour = self.max_sunlight_hour * (1 - self.average_rain_day / 365)
        #减去日照数，即为多云，阴天小时数
        self.cloudy_overcast_hour = self.no_rain_sunlight_hour - self.average_sunlight_hour
        #晴天概率
        self.sunny_chance = self.average_sunlight_hour / self.no_rain_sunlight_hour
        #多云概率
        self.cloudy_chance = (1 - self.sunny_chance) * 1 / 3
        #阴天概率
        self.overcast_chance = (1 - self.sunny_chance) * 2 / 3

    #计算年份，季节，日期
    def year_season_calc(self):
        days = self.day - 1
        days_left = days % self.year_length
        self.year = 1 + days // self.year_length
        days_left2 = days_left % self.season_length
        self.season = 1 + days_left // self.season_length
        self.day = days_left2 + 1

    #日期变化
    def day_change(self):
        self.really_day += 1
        self.day += 1
        if self.day > self.season_length:
            self.day = 1
            self.season += 1
        if self.season > 4:
            self.season = 1
            self.year += 1
        #如果需要固定季节，使用下面的代码
        #self.season = 4

    #气温变化
    def temperature_change(self):
        #气温变化为正负3
        temperature_change_value = random.uniform(-3,3)
        #设置目标温度，冬夏季比均温稍高/低，春秋季则线性变化
        if self.season == 1 :
            target_temperature = self.average_winter + self.average_summer_winter_difference * self.day / self.season_length
        elif self.season == 2:
            if self.day <= self.season_length / 2:
                target_temperature = self.average_summer * (self.day/(self.season_length/20) + 100) / 100
            else:
                target_temperature = self.average_summer * (120 - self.day/(self.season_length/20)) / 100
        elif self.season == 3:
            target_temperature = self.average_summer - self.average_summer_winter_difference * self.day / self.season_length
        elif self.season == 4:
            if self.temperature < 0:
                if self.day <= self.season_length / 2:
                    target_temperature = self.average_winter * (self.day/(self.season_length/20) + 100) / 100
                else:
                    target_temperature = self.average_winter * (120 - self.day/(self.season_length/20)) / 100
            else:
                if self.day <= self.season_length / 2:
                    target_temperature = self.average_winter * (100 - self.day/(self.season_length/20)) / 100
                else:
                    target_temperature = self.average_winter * (self.day/(self.season_length/20) + 80) / 100
        #低于目标温度，修正气温变化量，最高为低于15度——增加变化量3
        if self.temperature < target_temperature:
            dif = target_temperature - self.temperature
            if dif < 15:
                temperature_change_value += dif / 5
            else:
                temperature_change_value += 3
        #高于目标温度，修正气温变化量，最高为高于15度——减少变化量3
        if self.temperature > target_temperature:
            dif = self.temperature - target_temperature
            if dif < 15:
                temperature_change_value -= dif / 5
            else:
                temperature_change_value -= 3
        #第二天气温如超过气温阈值，修改气温变化量，第二天气温不超过阈值
        if self.temperature + temperature_change_value > self.max_threshold:
            temperature_change_value = self.max_threshold - self.temperature
        if self.temperature + temperature_change_value < self.min_threshold:
            temperature_change_value = self.min_threshold - self.temperature
        #修改温度
        self.temperature += temperature_change_value
    
    #降水变化
    def rain_change(self):
        #读取基础下雨概率，季节修正
        rain_chance = self.rain_chance_list[self.season-1]
        rain_season_buff = self.rain_season_buff_list[self.season-1]
        #根据前一天天气调整下雨概率
        #晴天
        if self.weather == "晴":
            rain_yesterday = False
            rain_num_yesterday = 0
            rain_chance *= 0.4
        #多云
        elif self.weather == "多云":
            rain_yesterday = False
            rain_num_yesterday = 0
            rain_chance *= 0.8
        #阴
        elif self.weather == "阴":
            rain_yesterday = False
            rain_num_yesterday = 0
            rain_chance *= 1
        #小雨，小雪
        elif self.weather == "小雨" or self.weather == "小雪":
            rain_yesterday = True
            rain_num_yesterday = self.rain_num
            rain_chance *= 1.4
        #大雨，大雪
        elif self.weather == "大雨" or self.weather == "大雪":
            rain_yesterday = True
            rain_num_yesterday = self.rain_num
            rain_chance *= 1.8
        #超过0.9则改为0.9
        if rain_chance > 0.9:
            rain_chance = 0.9
        #判定是否下雨
        if random.random() < rain_chance:
            self.rain = True
            self.rain_day += 1
        else:
            self.rain = False
        #判定降水量
        if self.rain == True:
            #刚开始下雨，随机生成雨量(平均降水量的1/3-2倍)
            if rain_yesterday == False:
                rain_highorlow = random.randint(0,1)
                rain_new_buff = random.uniform(1,3)
                #小于平均
                if rain_highorlow == 0:
                    self.rain_num = self.average_rain_num * rain_season_buff / rain_new_buff
                #大于平均
                elif rain_highorlow == 1:
                    self.rain_num = self.average_rain_num * rain_season_buff * (rain_new_buff / 3 * 2)
            #前一天有下雨，根据前一天雨量增加/减少
            elif rain_yesterday == True:
                self.rain_num = rain_num_yesterday * random.uniform(0.5,1.5)
        #没下雨
        else:
            self.rain_num = 0

    #天气变化
    #天气种类：晴、多云、阴、小雨、大雨、小雪、大雪
    #如果没有降水，则为晴、多云、阴互相转换
    def weather_change_no_rain(self):
        #晴天
        if self.weather == "晴":
            sunny_chance = self.sunny_chance * 2
            cloundy_chance = self.cloudy_chance
            overcast_chance = self.overcast_chance
            weather_random = random.uniform(0,sunny_chance+cloundy_chance+overcast_chance)
            if weather_random <= sunny_chance:
                self.weather = "晴"
            elif weather_random <= sunny_chance + cloundy_chance:
                self.weather = "多云"
            elif weather_random <= sunny_chance+cloundy_chance+overcast_chance:
                self.weather = "阴"
        #多云
        elif self.weather == "多云":
            sunny_chance = self.sunny_chance
            cloundy_chance = self.cloudy_chance * 6
            overcast_chance = self.overcast_chance * 3
            weather_random = random.uniform(0,sunny_chance+cloundy_chance+overcast_chance)
            if weather_random <= sunny_chance:
                self.weather = "晴"
            elif weather_random <= sunny_chance + cloundy_chance:
                self.weather = "多云"
            elif weather_random <= sunny_chance+cloundy_chance+overcast_chance:
                self.weather = "阴"
        #阴
        elif self.weather == "阴":
            sunny_chance = self.sunny_chance
            cloundy_chance = self.cloudy_chance * 3
            overcast_chance = self.overcast_chance * 6
            weather_random = random.uniform(0,sunny_chance+cloundy_chance+overcast_chance)
            if weather_random <= sunny_chance:
                self.weather = "晴"
            elif weather_random <= sunny_chance + cloundy_chance:
                self.weather = "多云"
            elif weather_random <= sunny_chance+cloundy_chance+overcast_chance:
                self.weather = "阴"
        #从雨天转没雨
        else:
            sunny_chance = self.sunny_chance
            cloundy_chance = self.cloudy_chance * 6
            overcast_chance = self.overcast_chance * 6
            weather_random = random.uniform(0,sunny_chance+cloundy_chance+overcast_chance)
            if weather_random <= sunny_chance:
                self.weather = "晴"
            elif weather_random <= sunny_chance + cloundy_chance:
                self.weather = "多云"
            elif weather_random <= sunny_chance+cloundy_chance+overcast_chance:
                self.weather = "阴"
    #如果有降水
    def weather_change_rain(self):
        #小雨，小雪
        if self.rain_num <= 10:
            self.weather = "小雨"
            self.rain_snow_check()
        #大雨，大雪
        elif self.rain_num > 10:
            self.weather = "大雨"
            self.rain_snow_check()
    #检查气温，转换雨雪
    def rain_snow_check(self):
        if self.temperature <= 0:
            self.weather = self.weather.replace('雨','雪')
        elif self.temperature > 0:
            self.weather = self.weather.replace('雪','雨')

    #天气影响温度
    def weather_effect_temperature(self):
        if self.weather == "晴":
            self.temperature += 1.5
        elif self.weather == "多云":
            self.temperature += 0.5
        elif self.weather == "阴":
            self.temperature -= 0.5
        elif self.weather == "小雨":
            self.temperature -= 1
        elif self.weather == "小雪":
            self.temperature -= 2
        elif self.weather == "大雨":
            self.temperature -= 1.5
        elif self.weather == "大雪":
            self.temperature -= 3
    
    #刮台风
    def typhoon(self):
        typhoon_random = random.uniform(0,1)
        if self.season != 4:
            if self.season == 2:
                typhoon_chance = 0.01
            else:
                typhoon_chance = 0.005
            if typhoon_random <= typhoon_chance:
                self.rain_num = random.uniform(20,150)
                print("刮台风了！现在季节是%s，第%s年，第%s天，台风的降水量是%.2f" % (self.season,self.year,self.day,self.rain_num))
                self.weather = "大雨"
                self.rain_snow_check()
                    
    #主函数1
    def weather_simulation1(self,days):
        day_list = []
        temperature_list = []
        rain_list = []
        rain_num_list = []
        weather_list = []
        rain_num_total = 0
        temperature_total = 0
        #天气数
        sunny_total = 0
        cloudy_total = 0
        overcast_total = 0
        light_rain_total = 0
        heavy_rain_total = 0
        light_snow_total = 0
        heavy_snow_total = 0
        days1 = days
        while days > 0:
            day_list.append(self.really_day)
            temperature_list.append(self.temperature)
            rain_list.append(self.rain)
            rain_num_list.append(self.rain_num)
            #天气
            if self.weather == "晴":
                weather_list.append(0)
                sunny_total += 1
            elif self.weather == "多云":
                weather_list.append(10)
                cloudy_total += 1
            elif self.weather == "阴":
                weather_list.append(20)
                overcast_total += 1
            elif self.weather == "小雨":
                weather_list.append(30)
                light_rain_total += 1
            elif self.weather == "小雪":
                weather_list.append(30)
                light_snow_total += 1
            elif self.weather == "大雨":
                weather_list.append(40)
                heavy_rain_total += 1
            elif self.weather == "大雪":
                weather_list.append(40)
                heavy_snow_total += 1
            else:
                weather_list.append(50)
            self.day_change()
            self.temperature_change()
            self.rain_change()
            if self.rain == True:
                self.weather_change_rain()
            elif self.rain == False:
                self.weather_change_no_rain()
            self.weather_effect_temperature()
            #self.typhoon()
            days -= 1
        for x in rain_num_list:
            rain_num_total += x
        for x in temperature_list:
            temperature_total += x
        dl = numpy.asarray(day_list)
        tl = numpy.asarray(temperature_list)
        rl = numpy.asarray(rain_num_list)
        wl = numpy.asarray(weather_list)
        print("%s的平均降水量为%.2f，平均降水日数为%.2f，平均温度为%.2f" % (self.name,rain_num_total*365/days1,self.rain_day*365/days1,temperature_total/days1))
        print("%s的晴天日数为%s，多云日数为%s，阴天日数为%s，小雨日数为%s，大雨日数为%s，小雪日数为%s，大雪日数为%s" % (self.name,\
            sunny_total,cloudy_total,overcast_total,light_rain_total,heavy_rain_total,light_snow_total,heavy_snow_total))
        print("%s的最高温为%.2f，最低温为%.2f，最大降水量为%.2f" % (self.name,numpy.max(tl),numpy.min(tl),numpy.max(rl)))
        return dl,tl,rl,wl
    
    #主函数2
    def weather_simulation2(self):
        self.day_change()
        self.temperature_change()
        self.rain_change()
        if self.rain == True:
            self.weather_change_rain()
        elif self.rain == False:
            self.weather_change_no_rain()
        self.weather_effect_temperature()
        self.irrigation_default_change()
        self.fertility_default_change()
        #self.typhoon()
    
    #默认灌溉值变化
    def irrigation_default_change(self):
        if self.season == 1 and self.day == 1:
            self.irrigation_default = random.uniform(self.average_irrigation_default*0.9,self.average_irrigation_default*1.1)
            print("春天来了！默认灌溉值变为%.2f" % self.irrigation_default)
        elif self.season == 2 and self.day == 1:
            self.irrigation_default = random.uniform(self.max_irrigation_default*0.9,self.max_irrigation_default*1.1)
            print("夏天来了！默认灌溉值变为%.2f" % self.irrigation_default)
        elif self.season == 3 and self.day == 1:
            self.irrigation_default = random.uniform(self.average_irrigation_default*0.9,self.average_irrigation_default*1.1)
            print("秋天来了！默认灌溉值变为%.2f" % self.irrigation_default)
        elif self.season == 4 and self.day == 1:
            self.irrigation_default = random.uniform(self.min_irrigation_default*0.9,self.min_irrigation_default*1.1)
            print("冬天来了！默认灌溉值变为%.2f" % self.irrigation_default)

    #默认肥力值变化
    def fertility_default_change(self):
        #不会泛滥的河流跳过
        if self.whether_flooding == False:
            return None
        #会泛滥
        else:
            #在夏天泛滥
            if self.season == 2 and self.day == 1:
                self.fertility_default = random.uniform(self.flooding_fertility_default*0.9,self.flooding_fertility_default*1.1)
                #不能超过100
                if self.fertility_default > 100:
                    self.fertility_default = 100
                self.flooding = True
                print("河流泛滥了！默认肥力值变为%.2f" % self.fertility_default)
            elif self.season == 3 and self.day == 1:
                self.fertility_default = self.raw_fertility_default
                self.flooding = False
                print("河流恢复正常了！")

#定义农田类
class farm(object):

    #农田参数，名字，所在城市，所种粮食
    def __init__(self,name,city,crop):
        self.name = name
        self.city = city
        self.crop = crop
        #灌溉值，肥力值由城市决定
        self.irrigation = self.city.irrigation_default
        self.fertility = self.city.fertility_default
        #最大恢复量，泛滥时恢复多
        self.max_recover = 10

    #灌溉值变化
    def irrigation_change(self):
        #判断有没有泛滥
        if self.city.flooding == True:
            self.max_recover = 40
        #天气影响
        #基础蒸发量
        base_evaporation = self.city.temperature / 10 + 1
        #偏移默认灌溉值带来的蒸发/恢复量
        shifting_evaporation = (self.city.irrigation_default - self.irrigation) / 4
        if self.name == "1号田":
            pass
        #不超过10/-10
        if shifting_evaporation >= self.max_recover:
            shifting_evaporation = self.max_recover
        elif shifting_evaporation <= -self.max_recover:
            shifting_evaporation = -self.max_recover
        #如果没有下雨，只会蒸发，蒸发量和温度挂钩
        if self.city.rain == False:
            self.irrigation += shifting_evaporation
            if self.city.weather == "晴":
                self.irrigation -= base_evaporation
            elif self.city.weather == "多云":
                self.irrigation -= base_evaporation / 2
            elif self.city.weather == "阴":
                self.irrigation -= base_evaporation / 4
        #如果下雨，则蒸发很小，灌溉值增加
        elif self.city.rain == True:
            self.irrigation += shifting_evaporation
            self.irrigation -= base_evaporation / 8
            if self.city.weather == "小雨" or self.city.weather == "大雨":
                self.irrigation += self.city.rain_num
            elif self.city.weather == "小雪" or self.city.weather == "大雪":
                self.irrigation += self.city.rain_num
        #每天耕作需要消耗灌溉值
        self.irrigation -= 4
        if self.city.season == 4:
            #self.irrigation += 4
            pass
        #不能超限
        if self.irrigation < 0:
            self.irrigation = 0
        elif self.irrigation > 300:
            self.irrigation = 300

    #肥力值变化
    def fertility_change(self):
        #少于默认肥力值，恢复
        if self.fertility < self.city.fertility_default:
            self.fertility += (self.city.fertility_default - self.fertility) / 8
        #大于也不会减少
        #每天耕作需要消耗肥力值
        self.fertility -= 2
        if self.city.season == 4:
            #self.fertility += 4
            pass
        #不能超限
        if self.fertility < 0:
            self.fertility = 0
        elif self.fertility > 100:
            self.fertility = 100

    #主函数
    def farm_simulation(self):
        self.irrigation_change()
        self.fertility_change()
        buff = self.crop.calculation(self.irrigation,self.fertility,self.city.temperature)
        if self.city.season == 4:
            #buff = 0
            pass
        return buff