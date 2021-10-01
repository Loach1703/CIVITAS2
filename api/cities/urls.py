from django.urls import path

from . import civitas

urlpatterns = [
    # 城市
    path('city_info/', civitas.get_city_info),

    # 不动产
    path('building_list/', civitas.building_list),
    path('reclaim/', civitas.reclaim),
]
