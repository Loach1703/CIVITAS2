import numpy
import random
import pymysql
from secret import dbdict

#定义城市类
class city(object):
    #城市参数：名称，平均温度，温差（夏季与冬季平均温差），平均年降水量，平均降水日数，气候，平均年日照时数
    #后面是其他参数，包括日期，当前温度，当前降水量，当前天气
    #city("长安",82.6,"tem",1872.7)
    def __init__(self,name="城市",average_temperature=15,temperature_difference=20,average_rain=1000,average_rain_day=100,climate="tem",average_sunlight_hour=2000,\
        day=1,now_temperature=0,now_rain_num=0,now_weather="晴"):
        self.name = name
        self.average_temperature = average_temperature
        self.temperature_difference = temperature_difference
        self.average_rain = average_rain
        self.average_rain_day = average_rain_day
        self.climate = climate
        self.average_sunlight_hour = average_sunlight_hour
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
        #冲突，抛出错误
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
        #平均日降水量
        self.average_rain_num = self.average_rain / self.average_rain_day

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
    #天气种类：晴、多云、阴、小雨、大雨、小雪、大雪(sunny,cloudy,overcast,light_rain,heavy_rain,light_snow,heavy_snow)
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
            self.temperature += 1
        elif self.weather == "多云":
            self.temperature += 0
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
                    
    #主函数
    def weather_simulation(self):
        self.day_change()
        self.temperature_change()
        self.rain_change()
        if self.rain == True:
            self.weather_change_rain()
        elif self.rain == False:
            self.weather_change_no_rain()
        self.weather_effect_temperature()
        #self.typhoon()
        season_dict = {1:"春天",2:"夏天",3:"秋天",4:"冬天"}
        total_day=(int(self.year)-1)*80+(int(self.season)-1)*20+int(self.day)
        db=pymysql.connect(host=dbdict["ip"],user=dbdict["user"],password=dbdict["password"],database=dbdict["database"])
        cursor=db.cursor()
        sql = "INSERT INTO TestModel_weather (city, total_day, year, season, day, weather, temperature, rain_num) VALUES ('{0}', {1}, {2}, '{3}', {4}, '{5}', {6}, {7})".format(self.name,total_day,self.year,season_dict[self.season],self.day,self.weather,round(self.temperature,5),round(self.rain_num,5))
        try:
        # 执行sql语句
            cursor.execute(sql)
        # 提交到数据库执行
            db.commit()
        except:
           # 如果发生错误则回滚
           db.rollback()
           db.close

def weather():
    db=pymysql.connect(host=dbdict["ip"],user=dbdict["user"],password=dbdict["password"],database=dbdict["database"])
    cursor=db.cursor()
    sql='select * from TestModel_weather order by id desc limit 1 offset 0;'
    cursor.execute(sql)
    list1=cursor.fetchall()
    for var in list1:
        total_day=int(var[2])
        temperature=float(var[7])
        rain_num=float(var[8])
        weather=var[6]
    ca = city("长安",14.7,27.1,542.2,82.6,"tem",1872.7,total_day,temperature,rain_num,weather)
    ca.weather_simulation()