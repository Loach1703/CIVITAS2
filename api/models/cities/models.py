from django.db import models


class City(models.Model):
    name = models.CharField(max_length=20)  # 地区名
    avatar = models.CharField(max_length=200)  # 地区头像
    belong = models.IntegerField()  # 属于某城的 ID，0 为城
    land_h = models.IntegerField()  # 土地数量(百倍，hundredfold)
    flat_h = models.IntegerField()  # 平坦程度(百倍，hundredfold)
    weather = models.CharField(max_length=200)  # 今日天气（JSON 信息扩展）
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        json = '{'
        for key in self._meta.fields:
            value = getattr(self, key.attname)
            json += '"{0}": {1}'.format(key, value)
        json += '}'

        return json


class Building(models.Model):
    user_id = models.IntegerField()  # 用户 ID
    city_id = models.IntegerField()  # 城市 ID
    building_id = models.IntegerField()  # 建筑物 ID
    land_occupy_h = models.IntegerField()  # 土地占用(百倍，hundredfold)
    land_has_h = models.IntegerField(default=0)  # 已有土地数量(百倍，hundredfold)，等于 land_occupy 时，则建造成功
    status = models.IntegerField(default=0)  # 状态 0建造中 1建造完成
    created_at = models.DateTimeField(auto_now=True)

    STATUS_BUILD = 0
    STATUS_DONE = 1

    def __str__(self):
        land_occupy = self.land_occupy_h / 100
        print(land_occupy)
        land_has = self.land_has_h / 100
        json = '{'
        for key in self._meta.fields:
            value = getattr(self, key.attname)
            json += '"{0}": {1}'.format(key, value)
        json += '"{0}": {1}'.format('land_occupy', land_occupy)
        json += '"{0}": {1}'.format('land_has', land_has)
        json += '}'

        return json
