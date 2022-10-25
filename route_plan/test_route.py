import numpy as np
import pandas as pd
from datetime import *
from route_planning.route_plan import *
from geopy import distance
import copy
from simulator.order import *

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
order_list = []
order_dic = {}
for i in range(len(df)):
    iorder = Order(i, df['shop_latitude'][i], df['shop_longitude'][i],
                   df['user_latitude'][i], df['user_longitude'][i],
                   rider_accept_order_time[i], 0, 0, 0,)
    order_list.append(iorder)
    order_dic[iorder.order_id] = iorder

available_loc = []
a_l = []
users_loc = []
available_flag = []
for i in range(len(order_list)):
    available_loc.append(order_list[i].shop_loc)
    users_loc.append(order_list[i].user_loc)
    available_flag.append(order_list[i].flag)


# 测试 路径预测类
a_l = copy.deepcopy(available_loc)
a_f = copy.deepcopy(available_flag)
u_l = copy.deepcopy(users_loc)
rp = Route(a_l, u_l, available_loc[0], 2, a_f)
a, bb, t, ff = rp.route_generation()
# print(available_loc)
print("距离：{}，时间：{}".format(a, t))
for b in bb:
    print(b.latitude, b.longitude)
print("--------------------------")
print(ff)
print(available_flag)
print(rp.time_list)
# ---------------------------------

time = 4  # 三分钟一个时间步
i = 0
# while sum(available_flag) != 0:
#     while i < len(ff):
#         t = rp.time_list[i]
#         lat = rp.route_plan[i].latitude
#         long = rp.route_plan[i].longitude
#         if rp.time_list[i] > time*0.05:
#             print("时间步：{}, 时间：{}, 位置：{} ".format(time, t, ff[i]), available_flag, i)
#             break
#         if available_flag[ff[i]] == 1:
#             available_flag[ff[i]] = 2
#         elif available_flag[ff[i]] == 2:
#             order_list[ff[i]] = 0
#             available_flag[ff[i]] = 0
#         i += 1
#
#     time += 1
m = 0
for i in range(len(ff)):
    t = rp.time_list[i]
    lat = rp.route_plan[i].latitude
    long = rp.route_plan[i].longitude
    if rp.time_list[i] > 2+time*0.5:
        print("时间步：{}, 时间：{}, 位置：{} ".format(time, t, ff[i]), available_flag, i)
        break
    if available_flag[ff[i]] == 1:
        available_flag[ff[i]] = 2
    elif available_flag[ff[i]] == 2:
        order_list[ff[i]] = 0
        available_flag[ff[i]] = 0
    m = i
del(ff[0:i])
for k in available_flag:
    if k == 0:
        available_flag.remove(k)
for j in order_list:
    if j == 0:
        order_list.remove(j)
print("order_list", order_list)
print("ff", ff)
# for i in range(len(ff)):
#     # 模拟位置变化
#     t = rp.time_list[i]
#     lat = rp.route_plan[i].latitude
#     long = rp.route_plan[i].longitude
#     if available_flag[ff[i]] == 1:
#         available_flag[ff[i]] = 2
#     elif available_flag[ff[i]] == 2:
#         order_list[ff[i]] = 0
#         available_flag[ff[i]] = 0
#     print("时间：{}, 位置：{} ".format(t, ff[i]), available_flag)
# print(order_list)
print(available_flag)
