import numpy as np
import pandas as pd
from datetime import *
from route_planning.route_plan import *
from geopy import distance
import copy
# 验证距离
# location = [[] for i in range(5)]
# location[1].append(34)
# location[1].append(116)
# print(location)
df0 = pd.read_csv(r"/Users/guobaoshen/Desktop/ele数据/zeyu/data_for_zeyu_another_rider_2.csv")
df = df0[0:4]
"""
估计速度，即估计时长与距离的映射关系
"""
rider_delivery_time = pd.to_datetime(df['rider_delivery_time'])
# df['order_create_time'] = pd.to_datetime(df['order_create_time'])
rider_accept_order_time = pd.to_datetime(df['rider_accept_order_time'])
rider_pickup_time = pd.to_datetime(df['rider_pickup_time'])
rider_arrive_restaurant_time = pd.to_datetime(df['rider_arrive_restaurant_time'])
# order_create_time = df['order_create_time']

time_slot = [rider_arrive_restaurant_time[1] - rider_pickup_time[0],
             rider_arrive_restaurant_time[3] - rider_pickup_time[1],
             rider_arrive_restaurant_time[2] - rider_pickup_time[3]]
dis = [get_distance_hav(df['shop_latitude'][1], df['shop_longitude'][1],
                        df['shop_latitude'][0], df['shop_longitude'][0]),
       get_distance_hav(df['shop_latitude'][3], df['shop_longitude'][3],
                        df['shop_latitude'][1], df['shop_longitude'][1]),
       get_distance_hav(df['shop_latitude'][2], df['shop_longitude'][2],
                        df['shop_latitude'][3], df['shop_longitude'][3])]
dis2 = distance.distance((df['shop_latitude'][1], df['shop_longitude'][1]), (df['shop_latitude'][0], df['shop_longitude'][0]))
available_loc = []
a_l = []
users_loc = []

for i in range(len(df) - 1):
    shop_loc = Loc(df['shop_latitude'][i], df['shop_longitude'][i])
    user_loc = Loc(df['user_latitude'][i], df['user_longitude'][i])
    available_loc.append(shop_loc)
    a_l = copy.deepcopy(available_loc)
    users_loc.append(user_loc)
    u_l = copy.deepcopy(users_loc)
    # available_flag = [1 for _ in range(len(available_loc))]
    # print("第{}次接单".format(i))
    # # print(available_loc)
    # rp = Route(a_l, u_l, available_loc[0], 0, available_flag)
    # a, bb, t = rp.route_generation()
    # print("距离：{}，时间：{}".format(a, t))
    # for b in bb:
    #     print(b.latitude, b.longitude)

# print(available_loc)

# 测试 路径预测类
available_flag = [1 for _ in range(len(available_loc))]
available_flag[0] = 2
a_f = copy.deepcopy(available_flag)
rp = Route(a_l, u_l, available_loc[0], 0, a_f)
a, bb, t, ff = rp.route_generation()
print(available_loc)
print("距离：{}，时间：{}".format(a, t))
for b in bb:
    print(b.latitude, b.longitude)
print(ff)

shop_loc = Loc(df['shop_latitude'][3], df['shop_longitude'][3])
user_loc = Loc(df['user_latitude'][3], df['user_longitude'][3])
available_loc.append(shop_loc)
available_flag.append(1)
a_l = copy.deepcopy(available_loc)
users_loc.append(user_loc)
u_l = copy.deepcopy(users_loc)
# -------------------------------------
# available_flag.append(1)
a_f = copy.deepcopy(available_flag)
rp = Route(a_l, u_l, available_loc[0], 0, a_f)
a, bb, t, ff = rp.route_generation()
print(available_loc)
print("距离：{}，时间：{}".format(a, t))
for b in bb:
    print(b.latitude, b.longitude)
print(ff)
# -------------------------------------
available_flag[0] = 0
print(len(available_loc))
print(len(available_flag))
a_f = copy.deepcopy(available_flag)

for i in range(len(available_flag)):
    if available_flag[i] == 0:
        a_f.remove(available_flag[i])
        available_loc[i] = 0
for i in available_loc:
    if i == 0:
        available_loc.remove(i)
available_flag = a_f
print(available_flag)
print(len(available_loc))
print(len(available_flag))
# a_f = copy.deepcopy(available_flag)
# rp = Route(a_l, u_l, available_loc[0], 0, a_f)
# a, bb, t, ff = rp.route_generation()
# print(available_loc)
# print("距离：{}，时间：{}".format(a, t))
# for b in bb:
#     print(b.latitude, b.longitude)
# print(ff)


