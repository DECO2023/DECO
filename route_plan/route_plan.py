import numpy as np
from datetime import *
from math import sin, asin, cos, radians, fabs, sqrt

EARTH_RADIUS = 6371  # 地球平均半径，6371km


def hav(theta):
    s = sin(theta / 2)
    return s * s


def get_distance_hav(lat0, lng0, lat1, lng1):
    """
     用haversine公式计算球面两点间的距离
    """
    # 经纬度转换成弧度
    lat0 = radians(lat0)
    lat1 = radians(lat1)
    lng0 = radians(lng0)
    lng1 = radians(lng1)

    dlng = fabs(lng0 - lng1)
    dlat = fabs(lat0 - lat1)
    h = hav(dlat) + cos(lat0) * cos(lat1) * hav(dlng)
    distance = 2 * EARTH_RADIUS * asin(sqrt(h))

    return distance


class Loc:

    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude


class Route:

    def __init__(self, shop_loc, user_loc, courier_loc, timestamp, available_flag):
        self.shop_loc = shop_loc
        self.user_loc = user_loc
        self.courier_loc = courier_loc
        self.time_duration = timestamp
        self.route_plan = []
        self.route_distance = 0
        self.available_loc = shop_loc
        self.available_flag = available_flag  # 用来标记路径规划
        self.route_flag = []
        self.time_list = []  # 每一个位置结束时的时间
        self.cost_time = 0
        # self.available_flag = [1 for _ in range(len(self.available_loc))]

    def next_stop_generation(self, avail_loc, avail_flag):
        # print("计算每个点与当前点的距离")
        # min_dis = 100
        # min_loc_id = 0
        _distance = []
        for i in range(len(avail_loc)):
            if avail_flag[i] != 0:
                _distance.append((i, get_distance_hav(self.courier_loc.latitude, self.courier_loc.longitude,
                                                      avail_loc[i].latitude, avail_loc[i].longitude)))

        _distance.sort(key=lambda x: x[1])
        min_loc_id = _distance[0][0] # distance 改成 features， 决策树
        min_dis = _distance[0][1]
        # print("贪心的选择下一站, 或者改成决策树决定下一站")
        self.time_duration = self.time_duration + min_dis / 12.11 * 12
        # self.time_duration = self.time_duration + min_dis / 12.11
        self.time_list.append(self.time_duration)
        # 时速，12.11 km/h, 简单的估计
        self.courier_loc = avail_loc[min_loc_id]
        return min_loc_id, min_dis

    def route_generation(self):
        while sum(self.available_flag) != 0:
            loc_id, loc_dis = self.next_stop_generation(self.available_loc, self.available_flag)
            self.route_plan.append(self.available_loc[loc_id])
            self.route_flag.append(loc_id)
            self.route_distance += loc_dis
            if self.available_flag[loc_id] == 1:
                self.available_loc[loc_id] = self.user_loc[loc_id]
                self.available_flag[loc_id] = 2
            elif self.available_flag[loc_id] == 2:
                self.available_flag[loc_id] = 0
                self.available_loc[loc_id] = 0
            elif self.available_flag[loc_id] == 0:
                pass
        self.cost_time = self.time_list[-1]
        # print("time_list: {}".format(self.time_list))
        return self.route_distance, self.route_plan, self.time_list, self.route_flag

    '''
    def next_stop_generation(self, avail_loc, avail_flag):
        # print("计算每个点与当前点的距离")
        min_dis = 100
        min_loc_id = 0
        for i in range(len(avail_loc)):
            if avail_flag[i] != 0:
                print(self.courier_loc)
                if min_dis > get_distance_hav(self.courier_loc.latitude, self.courier_loc.longitude,
                                              avail_loc[i].latitude, avail_loc[i].longitude):
                    min_dis = get_distance_hav(self.courier_loc.latitude, self.courier_loc.longitude,
                                               avail_loc[i].latitude, avail_loc[i].longitude)
                    min_loc_id = i
        # print("贪心的选择下一站")
        self.time_duration = self.time_duration + min_dis/12.11*12
        # self.time_duration = self.time_duration + min_dis / 12.11
        self.time_list.append(self.time_duration)
        # 时速，12.11 km/h, 简单的估计
        self.courier_loc = avail_loc[min_loc_id]
        return min_loc_id, min_dis
    '''