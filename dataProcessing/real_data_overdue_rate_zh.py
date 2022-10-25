import time
from collections import defaultdict

import pandas as pd


# 1012:
# 1855
# 41269
# 0.04494899319101505

# 1001:
# 1439
# 24589
# 0.058522103379559966


# 10131014：
# 3561
# 80059
# 0.044479696224034776

# 真实数据的每天超时率，和我模拟器模拟派单跑出来的超时率

# 超时时长分布---超时时长-次数CDF


#  超时单，当时骑手所拥有的订单数

def real_data_overdue_rate_comparison():
    df = pd.read_excel('../data/order20201012.xlsx')
    data = df.values
    overdue_order_num = 0
    order_sum = 0
    for line in data:
        promise_time = int(line[6])
        if promise_time <= 0:
            continue
        order_deliver_timestep = int((int(time.mktime(time.strptime(line[15], " %Y-%m-%d %H:%M:%S"))) - int(
            time.mktime(time.strptime("2020-10-12 00:00:00", "%Y-%m-%d %H:%M:%S")))))

        order_create_timestep = int((int(time.mktime(time.strptime(line[11], " %Y-%m-%d %H:%M:%S"))) - int(
            time.mktime(time.strptime("2020-10-12 00:00:00", "%Y-%m-%d %H:%M:%S")))))
        if order_deliver_timestep > 86400 or order_deliver_timestep < 0 or order_create_timestep > 86400 or order_create_timestep < 0:
            continue
        deliver_order_time = order_deliver_timestep - order_create_timestep
        if deliver_order_time > promise_time:
            overdue_order_num += 1

        order_sum += 1
    print(overdue_order_num)
    print(order_sum)
    overdue_rate = overdue_order_num / order_sum
    print(overdue_rate)


def real_data_overdue_duration_comparison():
    df = pd.read_excel('../data/order20201012.xlsx')
    data = df.values
    overdue_order_num = 0
    order_sum = 0
    overdue_duration = []
    for line in data:
        promise_time = int(line[6])
        if promise_time <= 0:
            continue
        order_deliver_timestep = int((int(time.mktime(time.strptime(line[15], " %Y-%m-%d %H:%M:%S"))) - int(
            time.mktime(time.strptime("2020-10-12 00:00:00", "%Y-%m-%d %H:%M:%S")))))

        order_create_timestep = int((int(time.mktime(time.strptime(line[11], " %Y-%m-%d %H:%M:%S"))) - int(
            time.mktime(time.strptime("2020-10-12 00:00:00", "%Y-%m-%d %H:%M:%S")))))
        if order_deliver_timestep > 86400 or order_deliver_timestep < 0 or order_create_timestep > 86400 or order_create_timestep < 0:
            continue
        deliver_order_time = order_deliver_timestep - order_create_timestep
        if deliver_order_time > promise_time:
            overdue_order_num += 1
            overdue_duration.append((deliver_order_time - promise_time) / 60)

        order_sum += 1
    print(overdue_order_num)
    print(order_sum)
    overdue_rate = overdue_order_num / order_sum
    print(overdue_rate)
    print(overdue_duration)

    sample_A = overdue_duration
    import numpy as np
    import matplotlib
    import os
    import matplotlib.pyplot as plt
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.grid(True)
    a = 0
    nhist = 100
    b = np.max(sample_A)
    c = b - a
    d = float(c) / float(nhist)  # size of each bin
    # tmp will contain a list of bins:  [a, a+d, a+2*d, a+3*d, ... b]
    tmp = [a]
    for i in range(nhist):
        if i == a:
            continue
        else:
            tmp.append(tmp[i - 1] + d)
    #  CDF of A
    ax.hist(sample_A, bins=tmp, cumulative=True, density=True, stacked=True,
            color='red', histtype='step', linewidth=2.0,
            label='samples A')
    plt.xlim([0, 40])
    plt.xlabel('Overdue Dutation')
    plt.ylabel('CDF')
    plt.show()


# # CDF of B
# plt.hist(samplesFromB, bins=tmp, cumulative=True, normed=True,
#         color='blue', alpha=0.5, histtype='step', linewidth=1.0,
#         label='samples B')

# real_data_overdue_rate_comparison()

def real_data_overdue_qishou_order_num_comparison1012():
    df = pd.read_excel('../data/order20201012.xlsx')
    data = df.values
    overdue_order_num = 0
    order_sum = 0
    overdue_order_id = defaultdict(list)  # courier_id : [order_id]
    courier_order_mapping = defaultdict(list)  # courier_id: [(order_id,create_time,deliver_time)]
    for line in data:
        # print(line)
        promise_time = int(line[6])
        order_id = int(line[0])
        courier_id = int(line[3])

        if promise_time <= 0:
            continue
        order_deliver_timestep = int((int(time.mktime(time.strptime(line[15], " %Y-%m-%d %H:%M:%S"))) - int(
            time.mktime(time.strptime("2020-10-12 00:00:00", "%Y-%m-%d %H:%M:%S")))))
        jiedan_timestep = int((int(time.mktime(time.strptime(line[12], " %Y-%m-%d %H:%M:%S"))) - int(
            time.mktime(time.strptime("2020-10-12 00:00:00", "%Y-%m-%d %H:%M:%S")))))
        order_create_timestep = int((int(time.mktime(time.strptime(line[11], " %Y-%m-%d %H:%M:%S"))) - int(
            time.mktime(time.strptime("2020-10-12 00:00:00", "%Y-%m-%d %H:%M:%S")))))

        if order_deliver_timestep > 86400 or order_deliver_timestep < 0 or order_create_timestep > 86400 or order_create_timestep < 0:
            continue
        deliver_order_time = order_deliver_timestep - order_create_timestep
        courier_order_mapping[courier_id].append((order_id, jiedan_timestep, order_deliver_timestep))
        if deliver_order_time > promise_time:
            overdue_order_num += 1
            overdue_order_id[courier_id].append((order_id, jiedan_timestep, order_deliver_timestep))

        order_sum += 1
    print(overdue_order_num)
    print(order_sum)
    overdue_rate = overdue_order_num / order_sum
    print(overdue_rate)

    overdue_courier_order_num = []

    for item_courier in overdue_order_id.keys():
        overdue_order_id_list = overdue_order_id[item_courier]
        for order_item in overdue_order_id_list:
            overdue_this_courier_order_num = 0
            cur_order_create = order_item[1]
            cur_order_deliver = order_item[2]
            for all_order_item in courier_order_mapping[item_courier]:
                all_order_item_create = all_order_item[1]
                all_order_item_deliver = all_order_item[2]
                # 配送超时单的时候也在配送这个单
                if not (all_order_item_create > cur_order_deliver or all_order_item_deliver < cur_order_create):
                    overdue_this_courier_order_num += 1
            overdue_courier_order_num.append(overdue_this_courier_order_num)
    return overdue_courier_order_num
    # sample_A = overdue_courier_order_num
    # import numpy as np
    # import matplotlib
    # import os
    # import matplotlib.pyplot as plt
    # fig = plt.figure()
    # ax = fig.add_subplot(1, 1, 1)
    # ax.grid(True)
    # a = 0
    # nhist = 100
    # b = np.max(sample_A)
    # c = b - a
    # d = float(c) / float(nhist)  # size of each bin
    # # tmp will contain a list of bins:  [a, a+d, a+2*d, a+3*d, ... b]
    # tmp = [a]
    # for i in range(nhist):
    #     if i == a:
    #         continue
    #     else:
    #         tmp.append(tmp[i - 1] + d)
    # #  CDF of A
    # ax.hist(sample_A, bins=tmp, cumulative=True, density=True, stacked=True,
    #         color='red', histtype='step', linewidth=2.0,
    #         label='samples A')
    # plt.xlim([0, 23])
    # plt.xlabel('Courier Order Num When The Overdue Event Happened')
    # plt.ylabel('CDF')
    # plt.show()


import math
import datetime


def real_data_overdue_qishou_order_num_comparison1001():
    df = pd.read_excel('../data/2W_order20201001.xlsx')
    data = df.values
    overdue_order_num = 0
    order_sum = 0
    overdue_order_id = defaultdict(list)  # courier_id : [order_id]
    courier_order_mapping = defaultdict(list)  # courier_id: [(order_id,create_time,deliver_time)]

    max_courier_id = 99999999
    for line in data:
        print(line)
        promise_time = int(line[5])
        order_id = order_sum
        if math.isnan(line[2]):
            courier_id = max_courier_id
        else:
            courier_id = int(line[2])

        if promise_time <= 0:
            continue

        if line[14] == 'a' or line[11] == 'a' or line[10] == 'a':
            continue
        else:
            order_deliver_timestep = int((int(line[14].timestamp()) - int(
                time.mktime(time.strptime("2020-10-01 00:00:00", "%Y-%m-%d %H:%M:%S")))))
            jiedan_timestep = int((int(line[11].timestamp()) - int(
                time.mktime(time.strptime("2020-10-01 00:00:00", "%Y-%m-%d %H:%M:%S")))))
            # time_str = datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
            order_create_timestep = int((int(line[10].to_pydatetime().timestamp()) - int(
                time.mktime(time.strptime("2020-10-01 00:00:00", "%Y-%m-%d %H:%M:%S")))))
        # order_create_timestep = int((int(line[10].timestamp()) - int(
        #     time.mktime(time.strptime("2020-10-01 00:00:00", "%Y-%m-%d %H:%M:%S")))))

        if order_deliver_timestep > 86400 or order_deliver_timestep < 0 or order_create_timestep > 86400 or order_create_timestep < 0:
            continue
        deliver_order_time = order_deliver_timestep - order_create_timestep
        courier_order_mapping[courier_id].append((order_id, jiedan_timestep, order_deliver_timestep))
        print(deliver_order_time, promise_time)
        if deliver_order_time > promise_time:
            overdue_order_num += 1
            overdue_order_id[courier_id].append((order_id, jiedan_timestep, order_deliver_timestep))

        order_sum += 1
    print(overdue_order_num)
    print(order_sum)
    overdue_rate = overdue_order_num / order_sum
    print(overdue_rate)

    overdue_courier_order_num = []

    for item_courier in overdue_order_id.keys():
        overdue_order_id_list = overdue_order_id[item_courier]
        for order_item in overdue_order_id_list:
            overdue_this_courier_order_num = 0
            cur_order_create = order_item[1]
            cur_order_deliver = order_item[2]
            for all_order_item in courier_order_mapping[item_courier]:
                all_order_item_create = all_order_item[1]
                all_order_item_deliver = all_order_item[2]
                # 配送超时单的时候也在配送这个单
                if not (all_order_item_create > cur_order_deliver or all_order_item_deliver < cur_order_create):
                    overdue_this_courier_order_num += 1
            overdue_courier_order_num.append(overdue_this_courier_order_num)
    return overdue_courier_order_num
    # sample_A = overdue_courier_order_num
    # import numpy as np
    # import matplotlib
    # import os
    # import matplotlib.pyplot as plt
    # fig = plt.figure()
    # ax = fig.add_subplot(1, 1, 1)
    # ax.grid(True)
    # a = 0
    # nhist = 100
    # b = np.max(sample_A)
    # c = b - a
    # d = float(c) / float(nhist)  # size of each bin
    # # tmp will contain a list of bins:  [a, a+d, a+2*d, a+3*d, ... b]
    # tmp = [a]
    # for i in range(nhist):
    #
    #     if i == a:
    #         continue
    #     else:
    #         tmp.append(tmp[i - 1] + d)
    # #  CDF of A
    # ax.hist(sample_A, bins=tmp, cumulative=True, density=True, stacked=True,
    #         color='red', histtype='step', linewidth=2.0,
    #         label='samples A')
    # plt.xlim([0, 23])
    # plt.xlabel('Courier Order Num When The Overdue Event Happened')
    # plt.ylabel('CDF')
    # plt.show()


# shop_id	user_id	rider_id	food_t	deliver	promise	shop_longitu	shop _latitud	user longitu	user_latitude	order_create time	rider accept_order	rider arrive restaura	rider pickup_time	rider_delivery_time	ds

def real_data_overdue_qishou_order_num_comparison1013_14():
    df = pd.read_excel('../data/中环13-14整合.xlsx')
    data = df.values
    overdue_order_num = 0
    order_sum = 0
    overdue_order_id = defaultdict(list)  # courier_id : [order_id]
    courier_order_mapping = defaultdict(list)  # courier_id: [(order_id,create_time,deliver_time)]

    max_courier_id = 99999999
    for line in data:
        print(order_sum)
        print(line)
        if type(line[5]) != int or type(line[5]) == float:
            continue
        promise_time = int(line[5])
        order_id = order_sum
        if type(line[2]) == str:
            courier_id = max_courier_id
        else:
            if math.isnan(line[2]):
                courier_id = max_courier_id
            else:
                courier_id = int(line[2])

        if promise_time <= 0:
            continue

        if line[14] == 'a' or line[11] == 'a' or line[10] == 'a' or type(line[14]) == float or type(
                line[11]) == float or type(line[10]) == float or type(line[14]) == str or type(
            line[11]) == str or type(line[10]) == str:
            continue
        else:  # 区分1013，1014
            if line[14].strftime('%Y-%m-%d %H:%M:%S').split(' ')[0] == '2020-10-13':
                order_deliver_timestep = int((int(line[14].timestamp()) - int(
                    time.mktime(time.strptime("2020-10-13 00:00:00", "%Y-%m-%d %H:%M:%S")))))
                jiedan_timestep = int((int(line[11].timestamp()) - int(
                    time.mktime(time.strptime("2020-10-13 00:00:00", "%Y-%m-%d %H:%M:%S")))))
                order_create_timestep = int((int(line[10].timestamp()) - int(
                    time.mktime(time.strptime("2020-10-13 00:00:00", "%Y-%m-%d %H:%M:%S")))))
            elif line[14].strftime('%Y-%m-%d %H:%M:%S').split(' ')[0] == '2020-10-14':
                order_deliver_timestep = int((int(line[14].timestamp()) - int(
                    time.mktime(time.strptime("2020-10-14 00:00:00", "%Y-%m-%d %H:%M:%S")))))
                jiedan_timestep = int((int(line[11].timestamp()) - int(
                    time.mktime(time.strptime("2020-10-14 00:00:00", "%Y-%m-%d %H:%M:%S")))))
                order_create_timestep = int((int(line[10].timestamp()) - int(
                    time.mktime(time.strptime("2020-10-14 00:00:00", "%Y-%m-%d %H:%M:%S")))))
            else:
                print('什么情况')  # 14号点单，15号送完
                continue

        if order_deliver_timestep > 86400 or order_deliver_timestep < 0 or order_create_timestep > 86400 or order_create_timestep < 0:
            continue
        deliver_order_time = order_deliver_timestep - order_create_timestep
        courier_order_mapping[courier_id].append((order_id, jiedan_timestep, order_deliver_timestep))
        print(deliver_order_time, promise_time)
        if deliver_order_time < 0:
            continue

        if deliver_order_time > promise_time:
            overdue_order_num += 1
            overdue_order_id[courier_id].append((order_id, jiedan_timestep, order_deliver_timestep))

        order_sum += 1

    print(overdue_order_num)
    print(order_sum)
    overdue_rate = overdue_order_num / order_sum
    print(overdue_rate)

    overdue_courier_order_num = []

    for item_courier in overdue_order_id.keys():
        overdue_order_id_list = overdue_order_id[item_courier]
        for order_item in overdue_order_id_list:
            overdue_this_courier_order_num = 0
            cur_order_create = order_item[1]
            cur_order_deliver = order_item[2]
            for all_order_item in courier_order_mapping[item_courier]:
                all_order_item_create = all_order_item[1]
                all_order_item_deliver = all_order_item[2]
                # 配送超时单的时候也在配送这个单
                if not (all_order_item_create > cur_order_deliver or all_order_item_deliver < cur_order_create):
                    overdue_this_courier_order_num += 1
            overdue_courier_order_num.append(overdue_this_courier_order_num)
    return overdue_courier_order_num
    # sample_A = overdue_courier_order_num
    # import numpy as np
    # import matplotlib
    # import os
    # import matplotlib.pyplot as plt
    # fig = plt.figure()
    # ax = fig.add_subplot(1, 1, 1)
    # ax.grid(True)
    # a = 0
    # nhist = 100
    # b = np.max(sample_A)
    # c = b - a
    # d = float(c) / float(nhist)  # size of each bin
    # # tmp will contain a list of bins:  [a, a+d, a+2*d, a+3*d, ... b]
    # tmp = [a]
    # for i in range(nhist):
    #
    #     if i == a:
    #         continue
    #     else:
    #         tmp.append(tmp[i - 1] + d)
    # #  CDF of A
    # ax.hist(sample_A, bins=tmp, cumulative=True, density=True, stacked=True,
    #         color='red', histtype='step', linewidth=2.0,
    #         label='samples A')
    # plt.xlim([0, 23])
    # plt.xlabel('Courier Order Num When The Overdue Event Happened')
    # plt.ylabel('CDF')
    # plt.show()



# real_data_overdue_duration_comparison()
# overdue_courier_order_num1012 = real_data_overdue_qishou_order_num_comparison1012()
# # 骑手有多个单时的超时率
# overdue_courier_order_num1001 = real_data_overdue_qishou_order_num_comparison1001()
#
# overdue_courier_order_num1013_14 = real_data_overdue_qishou_order_num_comparison1013_14()
# merge_overdue_courier_order_num = overdue_courier_order_num1012 +overdue_courier_order_num1001 + overdue_courier_order_num1013_14
# sample_A = merge_overdue_courier_order_num
# import numpy as np
# import matplotlib
# import os
# import matplotlib.pyplot as plt
# fig = plt.figure()
# plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
# plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
# # plt.rc(size=20)
# plt.rcParams.update({'font.size':20})
# # plt.rc('font', family='Times New Roman', size=20)
# ax = fig.add_subplot(1, 1, 1)
# a = 0
# nhist = 100
# b = np.max(sample_A)
# c = b - a
# d = float(c) / float(nhist)  # size of each bin
# # tmp will contain a list of bins:  [a, a+d, a+2*d, a+3*d, ... b]
# tmp = [a]
# for i in range(nhist):
#
#     if i == a:
#         continue
#     else:
#         tmp.append(tmp[i - 1] + d)
# #  CDF of A
# ax.hist(sample_A, bins=tmp, cumulative=True, density=True, stacked=True,
#         color='black', histtype='step', linewidth=2.0,
#         label='samples A')
# plt.xlim([0, 23])
# plt.xlabel('骑手配送超时发生时的订单量')
# # plt.xlabel('Courier Order Num When The Overdue Event Happened')
# # plt.ylabel('CDF')
# plt.ylabel('累积概率分布')
# plt.show()
# # plt.show()
# plt.tight_layout()
# plt.savefig('骑手配送超时发生时的订单量zh.pdf',bbox_inches ='tight')



# real_data_overdue_qishou_order_num_comparison0606()
from simulator.envs_zh_1001_update_200_2min import *

def real_data_overdue_qishou_order_num_comparison1012_bushunlu():
    df = pd.read_excel('../data/order20201012.xlsx')
    data = df.values
    overdue_order_num = 0
    order_sum = 0
    overdue_order_id = defaultdict(list)  # courier_id : [order_id]
    courier_order_mapping = defaultdict(list)  # courier_id: [(order_id,create_time,deliver_time,user_lat,user_lon,mer_lat,mer_lon)]
    for line in data:
        # print(line)
        promise_time = int(line[6])
        order_id = int(line[0])
        courier_id = int(line[3])

        if promise_time <= 0:
            continue
        order_deliver_timestep = int((int(time.mktime(time.strptime(line[15], " %Y-%m-%d %H:%M:%S"))) - int(
            time.mktime(time.strptime("2020-10-12 00:00:00", "%Y-%m-%d %H:%M:%S")))))
        jiedan_timestep = int((int(time.mktime(time.strptime(line[12], " %Y-%m-%d %H:%M:%S"))) - int(
            time.mktime(time.strptime("2020-10-12 00:00:00", "%Y-%m-%d %H:%M:%S")))))
        order_create_timestep = int((int(time.mktime(time.strptime(line[11], " %Y-%m-%d %H:%M:%S"))) - int(
            time.mktime(time.strptime("2020-10-12 00:00:00", "%Y-%m-%d %H:%M:%S")))))
        shop_lat = float(line[8])
        shop_lon = float(line[7])
        user_lat = float(line[10])
        user_lon = float(line[9])

        if order_deliver_timestep > 86400 or order_deliver_timestep < 0 or order_create_timestep > 86400 or order_create_timestep < 0:
            continue
        deliver_order_time = order_deliver_timestep - order_create_timestep
        courier_order_mapping[courier_id].append((order_id, jiedan_timestep, order_deliver_timestep,user_lat,user_lon,shop_lat,shop_lon))
        if deliver_order_time > promise_time:
            overdue_order_num += 1
            overdue_order_id[courier_id].append((order_id, jiedan_timestep, order_deliver_timestep))

        order_sum += 1
    same_time_delivery_order_next_distance_distance = [] # 先拿用户位置_distance异同/商家位置异同的距离来看
    for item_courier in courier_order_mapping.keys():
        # 某一个骑手
        for all_order_item_id in range(len(courier_order_mapping[item_courier])):
            all_order_item_create = courier_order_mapping[item_courier][all_order_item_id][1]
            all_order_item_deliver = courier_order_mapping[item_courier][all_order_item_id][2]
            all_order_user_lat = courier_order_mapping[item_courier][all_order_item_id][3]
            all_order_user_lon = courier_order_mapping[item_courier][all_order_item_id][4]
            # 针对骑手某一个单，找同时配送的订单
            # same_time_deliver_order_distance = []
            for all_order_item_id_y in range(len(courier_order_mapping[item_courier])):
                if all_order_item_id_y <= all_order_item_id:
                    continue
                cur_order_create = courier_order_mapping[item_courier][all_order_item_id_y][1]
                cur_order_deliver = courier_order_mapping[item_courier][all_order_item_id_y][2]
                cur_order_user_lat = courier_order_mapping[item_courier][all_order_item_id_y][3]
                cur_order_user_lon = courier_order_mapping[item_courier][all_order_item_id_y][4]
                # 同时配送这个单
                if not (all_order_item_create > cur_order_deliver or all_order_item_deliver < cur_order_create):
                    tmp_distance = get_distance_hav(all_order_user_lat,all_order_user_lon,
                                                              cur_order_user_lat,
                                                              cur_order_user_lon)
                    same_time_delivery_order_next_distance_distance.append(tmp_distance)
        # same_time_delivery_order_distance.append(overdue_this_courier_order_num)

    return same_time_delivery_order_next_distance_distance
    # sample_A = overdue_courier_order_num
    # import numpy as np
    # import matplotlib
    # import os
    # import matplotlib.pyplot as plt
    # fig = plt.figure()
    # ax = fig.add_subplot(1, 1, 1)
    # ax.grid(True)
    # a = 0
    # nhist = 100
    # b = np.max(sample_A)
    # c = b - a
    # d = float(c) / float(nhist)  # size of each bin
    # # tmp will contain a list of bins:  [a, a+d, a+2*d, a+3*d, ... b]
    # tmp = [a]
    # for i in range(nhist):
    #     if i == a:
    #         continue
    #     else:
    #         tmp.append(tmp[i - 1] + d)
    # #  CDF of A
    # ax.hist(sample_A, bins=tmp, cumulative=True, density=True, stacked=True,
    #         color='red', histtype='step', linewidth=2.0,
    #         label='samples A')
    # plt.xlim([0, 23])
    # plt.xlabel('Courier Order Num When The Overdue Event Happened')
    # plt.ylabel('CDF')
    # plt.show()


import math
import datetime


def real_data_overdue_qishou_order_num_comparison1001_bushunlu():
    df = pd.read_excel('../data/2W_order20201001.xlsx')
    data = df.values
    overdue_order_num = 0
    order_sum = 0
    overdue_order_id = defaultdict(list)  # courier_id : [order_id]
    courier_order_mapping = defaultdict(list)  # courier_id: [(order_id,create_time,deliver_time)]

    max_courier_id = 99999999
    for line in data:
        print(line)
        promise_time = int(line[5])
        order_id = order_sum
        if math.isnan(line[2]):
            courier_id = max_courier_id
        else:
            courier_id = int(line[2])

        if promise_time <= 0:
            continue

        if line[14] == 'a' or line[11] == 'a' or line[10] == 'a':
            continue
        else:
            order_deliver_timestep = int((int(line[14].timestamp()) - int(
                time.mktime(time.strptime("2020-10-01 00:00:00", "%Y-%m-%d %H:%M:%S")))))
            jiedan_timestep = int((int(line[11].timestamp()) - int(
                time.mktime(time.strptime("2020-10-01 00:00:00", "%Y-%m-%d %H:%M:%S")))))
            # time_str = datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
            order_create_timestep = int((int(line[10].to_pydatetime().timestamp()) - int(
                time.mktime(time.strptime("2020-10-01 00:00:00", "%Y-%m-%d %H:%M:%S")))))
        # order_create_timestep = int((int(line[10].timestamp()) - int(
        #     time.mktime(time.strptime("2020-10-01 00:00:00", "%Y-%m-%d %H:%M:%S")))))


            shop_lat = float(line[7])
            shop_lon = float(line[6])
            user_lat = float(line[9])
            user_lon = float(line[8])

            if order_deliver_timestep > 86400 or order_deliver_timestep < 0 or order_create_timestep > 86400 or order_create_timestep < 0:
                continue
            deliver_order_time = order_deliver_timestep - order_create_timestep
            courier_order_mapping[courier_id].append(
                (order_id, jiedan_timestep, order_deliver_timestep, user_lat, user_lon, shop_lat, shop_lon))
            if deliver_order_time > promise_time:
                overdue_order_num += 1
                overdue_order_id[courier_id].append((order_id, jiedan_timestep, order_deliver_timestep))

            order_sum += 1
    same_time_delivery_order_next_distance_distance = []  # 先拿用户位置_distance异同/商家位置异同的距离来看
    for item_courier in courier_order_mapping.keys():
        # 某一个骑手
        for all_order_item_id in range(len(courier_order_mapping[item_courier])):
            all_order_item_create = courier_order_mapping[item_courier][all_order_item_id][1]
            all_order_item_deliver = courier_order_mapping[item_courier][all_order_item_id][2]
            all_order_user_lat = courier_order_mapping[item_courier][all_order_item_id][3]
            all_order_user_lon = courier_order_mapping[item_courier][all_order_item_id][4]
            # 针对骑手某一个单，找同时配送的订单
            # same_time_deliver_order_distance = []
            for all_order_item_id_y in range(len(courier_order_mapping[item_courier])):
                if all_order_item_id_y <= all_order_item_id:
                    continue
                cur_order_create = courier_order_mapping[item_courier][all_order_item_id_y][1]
                cur_order_deliver = courier_order_mapping[item_courier][all_order_item_id_y][2]
                cur_order_user_lat = courier_order_mapping[item_courier][all_order_item_id_y][3]
                cur_order_user_lon = courier_order_mapping[item_courier][all_order_item_id_y][4]
                # 同时配送这个单
                if not (all_order_item_create > cur_order_deliver or all_order_item_deliver < cur_order_create):
                    tmp_distance = get_distance_hav(all_order_user_lat, all_order_user_lon,
                                                    cur_order_user_lat,
                                                    cur_order_user_lon)
                    same_time_delivery_order_next_distance_distance.append(tmp_distance)
        # same_time_delivery_order_distance.append(overdue_this_courier_order_num)

    return same_time_delivery_order_next_distance_distance


def real_data_overdue_qishou_order_num_comparison1001_bushunlu_max_distance():
    df = pd.read_excel('../data/2W_order20201001.xlsx')
    data = df.values
    overdue_order_num = 0
    order_sum = 0
    overdue_order_id = defaultdict(list)  # courier_id : [order_id]
    courier_order_mapping = defaultdict(list)  # courier_id: [(order_id,create_time,deliver_time)]

    max_courier_id = 99999999
    for line in data:
        print(line)
        promise_time = int(line[5])
        order_id = order_sum
        if math.isnan(line[2]):
            courier_id = max_courier_id
        else:
            courier_id = int(line[2])

        if promise_time <= 0:
            continue

        if line[14] == 'a' or line[11] == 'a' or line[10] == 'a':
            continue
        else:
            order_deliver_timestep = int((int(line[14].timestamp()) - int(
                time.mktime(time.strptime("2020-10-01 00:00:00", "%Y-%m-%d %H:%M:%S")))))
            jiedan_timestep = int((int(line[11].timestamp()) - int(
                time.mktime(time.strptime("2020-10-01 00:00:00", "%Y-%m-%d %H:%M:%S")))))
            # time_str = datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
            order_create_timestep = int((int(line[10].to_pydatetime().timestamp()) - int(
                time.mktime(time.strptime("2020-10-01 00:00:00", "%Y-%m-%d %H:%M:%S")))))
        # order_create_timestep = int((int(line[10].timestamp()) - int(
        #     time.mktime(time.strptime("2020-10-01 00:00:00", "%Y-%m-%d %H:%M:%S")))))

            shop_lat = float(line[7])
            shop_lon = float(line[6])
            user_lat = float(line[9])
            user_lon = float(line[8])

            if order_deliver_timestep > 86400 or order_deliver_timestep < 0 or order_create_timestep > 86400 or order_create_timestep < 0:
                continue
            deliver_order_time = order_deliver_timestep - order_create_timestep
            courier_order_mapping[courier_id].append(
                (order_id, jiedan_timestep, order_deliver_timestep, user_lat, user_lon, shop_lat, shop_lon))
            if deliver_order_time > promise_time:
                overdue_order_num += 1
                overdue_order_id[courier_id].append((order_id, jiedan_timestep, order_deliver_timestep))

            order_sum += 1
    same_time_delivery_order_next_distance_distance = []  # 先拿用户位置_distance异同/商家位置异同的距离来看
    group_num_list = []
    for item_courier in courier_order_mapping.keys():
        # 某一个骑手
        for all_order_item_id in range(len(courier_order_mapping[item_courier])):
            order_group_num =1
            all_order_item_create = courier_order_mapping[item_courier][all_order_item_id][1]
            all_order_item_deliver = courier_order_mapping[item_courier][all_order_item_id][2]
            all_order_user_lat = courier_order_mapping[item_courier][all_order_item_id][3]
            all_order_user_lon = courier_order_mapping[item_courier][all_order_item_id][4]
            # 针对骑手某一个单，找同时配送的订单
            # same_time_deliver_order_distance = []
            max_distance_exist = False
            max_distance = 0
            for all_order_item_id_y in range(len(courier_order_mapping[item_courier])):
                if all_order_item_id_y <= all_order_item_id:
                    continue
                cur_order_create = courier_order_mapping[item_courier][all_order_item_id_y][1]
                cur_order_deliver = courier_order_mapping[item_courier][all_order_item_id_y][2]
                cur_order_user_lat = courier_order_mapping[item_courier][all_order_item_id_y][3]
                cur_order_user_lon = courier_order_mapping[item_courier][all_order_item_id_y][4]
                # 同时配送这个单
                if not (all_order_item_create > cur_order_deliver or all_order_item_deliver < cur_order_create):
                    order_group_num+=1
                    tmp_distance = get_distance_hav(all_order_user_lat, all_order_user_lon,
                                                    cur_order_user_lat,
                                                    cur_order_user_lon)
                    max_distance_exist = True
                    if tmp_distance > max_distance:
                        max_distance = tmp_distance
            if max_distance_exist and order_group_num >2:
                same_time_delivery_order_next_distance_distance.append(max_distance)
            group_num_list.append(order_group_num)
        # same_time_delivery_order_distance.append(overdue_this_courier_order_num)

    return same_time_delivery_order_next_distance_distance,group_num_list

def real_data_overdue_qishou_order_num_comparison1012_bushunlu_max_distance():
    df = pd.read_excel('../data/order20201012.xlsx')
    data = df.values
    overdue_order_num = 0
    order_sum = 0
    overdue_order_id = defaultdict(list)  # courier_id : [order_id]
    courier_order_mapping = defaultdict(list)  # courier_id: [(order_id,create_time,deliver_time,user_lat,user_lon,mer_lat,mer_lon)]
    for line in data:
        # print(line)
        promise_time = int(line[6])
        order_id = int(line[0])
        courier_id = int(line[3])

        if promise_time <= 0:
            continue
        order_deliver_timestep = int((int(time.mktime(time.strptime(line[15], " %Y-%m-%d %H:%M:%S"))) - int(
            time.mktime(time.strptime("2020-10-12 00:00:00", "%Y-%m-%d %H:%M:%S")))))
        jiedan_timestep = int((int(time.mktime(time.strptime(line[12], " %Y-%m-%d %H:%M:%S"))) - int(
            time.mktime(time.strptime("2020-10-12 00:00:00", "%Y-%m-%d %H:%M:%S")))))
        order_create_timestep = int((int(time.mktime(time.strptime(line[11], " %Y-%m-%d %H:%M:%S"))) - int(
            time.mktime(time.strptime("2020-10-12 00:00:00", "%Y-%m-%d %H:%M:%S")))))
        shop_lat = float(line[8])
        shop_lon = float(line[7])
        user_lat = float(line[10])
        user_lon = float(line[9])

        if order_deliver_timestep > 86400 or order_deliver_timestep < 0 or order_create_timestep > 86400 or order_create_timestep < 0:
            continue
        deliver_order_time = order_deliver_timestep - order_create_timestep
        courier_order_mapping[courier_id].append((order_id, jiedan_timestep, order_deliver_timestep,user_lat,user_lon,shop_lat,shop_lon))
        if deliver_order_time > promise_time:
            overdue_order_num += 1
            overdue_order_id[courier_id].append((order_id, jiedan_timestep, order_deliver_timestep))

        order_sum += 1
    same_time_delivery_order_next_distance_distance = [] # 先拿用户位置_distance异同/商家位置异同的距离来看
    group_order_num = []
    for item_courier in courier_order_mapping.keys():
        # 某一个骑手
        for all_order_item_id in range(len(courier_order_mapping[item_courier])):
            order_group_num = 1
            all_order_item_create = courier_order_mapping[item_courier][all_order_item_id][1]
            all_order_item_deliver = courier_order_mapping[item_courier][all_order_item_id][2]
            all_order_user_lat = courier_order_mapping[item_courier][all_order_item_id][3]
            all_order_user_lon = courier_order_mapping[item_courier][all_order_item_id][4]
            # 针对骑手某一个单，找同时配送的订单
            # same_time_deliver_order_distance = []
            max_distance_exist = False
            max_distance = 0
            for all_order_item_id_y in range(len(courier_order_mapping[item_courier])):
                if all_order_item_id_y <= all_order_item_id:
                    continue
                cur_order_create = courier_order_mapping[item_courier][all_order_item_id_y][1]
                cur_order_deliver = courier_order_mapping[item_courier][all_order_item_id_y][2]
                cur_order_user_lat = courier_order_mapping[item_courier][all_order_item_id_y][3]
                cur_order_user_lon = courier_order_mapping[item_courier][all_order_item_id_y][4]
                # 同时配送这个单
                if not (all_order_item_create > cur_order_deliver or all_order_item_deliver < cur_order_create):
                    tmp_distance = get_distance_hav(all_order_user_lat,all_order_user_lon,
                                                              cur_order_user_lat,
                                                              cur_order_user_lon)
                    max_distance_exist = True
                    order_group_num +=1
                    if tmp_distance > max_distance:
                        max_distance = tmp_distance
            if max_distance_exist and order_group_num >2:
                same_time_delivery_order_next_distance_distance.append(max_distance)
            group_order_num.append(order_group_num)
        # same_time_delivery_order_distance.append(overdue_this_courier_order_num)

    return same_time_delivery_order_next_distance_distance,group_order_num
    # sample_A = overdue_courier_order_num
    # import numpy as np
    # import matplotlib
    # import os
    # import matplotlib.pyplot as plt
    # fig = plt.figure()
    # ax = fig.add_subplot(1, 1, 1)
    # ax.grid(True)
    # a = 0
    # nhist = 100
    # b = np.max(sample_A)
    # c = b - a
    # d = float(c) / float(nhist)  # size of each bin
    # # tmp will contain a list of bins:  [a, a+d, a+2*d, a+3*d, ... b]
    # tmp = [a]
    # for i in range(nhist):
    #     if i == a:
    #         continue
    #     else:
    #         tmp.append(tmp[i - 1] + d)
    # #  CDF of A
    # ax.hist(sample_A, bins=tmp, cumulative=True, density=True, stacked=True,
    #         color='red', histtype='step', linewidth=2.0,
    #         label='samples A')
    # plt.xlim([0, 23])
    # plt.xlabel('Courier Order Num When The Overdue Event Happened')
    # plt.ylabel('CDF')
    # plt.show()

def real_data_overdue_qishou_order_num_comparison1001_bushunlu_leiji_distance():
    df = pd.read_excel('../data/2W_order20201001.xlsx')
    data = df.values
    overdue_order_num = 0
    order_sum = 0
    overdue_order_id = defaultdict(list)  # courier_id : [order_id]
    courier_order_mapping = defaultdict(list)  # courier_id: [(order_id,create_time,deliver_time)]

    max_courier_id = 99999999
    for line in data:
        print(line)
        promise_time = int(line[5])
        order_id = order_sum
        if math.isnan(line[2]):
            courier_id = max_courier_id
        else:
            courier_id = int(line[2])

        if promise_time <= 0:
            continue

        if line[14] == 'a' or line[11] == 'a' or line[10] == 'a':
            continue
        else:
            order_deliver_timestep = int((int(line[14].timestamp()) - int(
                time.mktime(time.strptime("2020-10-01 00:00:00", "%Y-%m-%d %H:%M:%S")))))
            jiedan_timestep = int((int(line[11].timestamp()) - int(
                time.mktime(time.strptime("2020-10-01 00:00:00", "%Y-%m-%d %H:%M:%S")))))
            # time_str = datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
            order_create_timestep = int((int(line[10].to_pydatetime().timestamp()) - int(
                time.mktime(time.strptime("2020-10-01 00:00:00", "%Y-%m-%d %H:%M:%S")))))
        # order_create_timestep = int((int(line[10].timestamp()) - int(
        #     time.mktime(time.strptime("2020-10-01 00:00:00", "%Y-%m-%d %H:%M:%S")))))
            daodian_timestep = int((int(line[12].to_pydatetime().timestamp()) - int(
                time.mktime(time.strptime("2020-10-01 00:00:00", "%Y-%m-%d %H:%M:%S")))))

            shop_lat = float(line[7])
            shop_lon = float(line[6])
            user_lat = float(line[9])
            user_lon = float(line[8])

            if order_deliver_timestep > 86400 or order_deliver_timestep < 0 or order_create_timestep > 86400 or order_create_timestep < 0:
                continue
            deliver_order_time = order_deliver_timestep - order_create_timestep
            courier_order_mapping[courier_id].append(
                (order_id, jiedan_timestep, order_deliver_timestep, user_lat, user_lon, shop_lat, shop_lon,daodian_timestep))
            if deliver_order_time > promise_time:
                overdue_order_num += 1
                overdue_order_id[courier_id].append((order_id, jiedan_timestep, order_deliver_timestep))

            order_sum += 1
    same_time_delivery_order_next_distance_distance = []  # 先拿用户位置_distance异同/商家位置异同的距离来看
    for item_courier in courier_order_mapping.keys():
        # 某一个骑手
        if len(courier_order_mapping[item_courier])<=1:
            continue
        same_time_delivery_order_list =[]
        for all_order_item_id in range(len(courier_order_mapping[item_courier])):
            temp_same_time_delivery_order_group = []
            temp_same_time_delivery_order_group.append(courier_order_mapping[item_courier][all_order_item_id])
            same_time_delivery_order_list.append(courier_order_mapping[item_courier][all_order_item_id][0])
            # all_order_item_create = courier_order_mapping[item_courier][all_order_item_id][1]
            # all_order_item_deliver = courier_order_mapping[item_courier][all_order_item_id][2]
            for all_order_item_id_y in range(len(courier_order_mapping[item_courier])):
                if all_order_item_id_y <= all_order_item_id:
                    continue
                # cur_order_create = courier_order_mapping[item_courier][all_order_item_id_y][1]
                # cur_order_deliver = courier_order_mapping[item_courier][all_order_item_id_y][2]
                # 同时配送这个单
                if not (all_order_item_create > cur_order_deliver or all_order_item_deliver < cur_order_create):
                    temp_same_time_delivery_order_group.append(courier_order_mapping[item_courier][all_order_item_id_y])
                    same_time_delivery_order_list.append(courier_order_mapping[item_courier][all_order_item_id_y][0])
                    # tmp_distance = get_distance_hav(all_order_user_lat, all_order_user_lon,
                    #                                 cur_order_user_lat,
                    #                                 cur_order_user_lon)
                    # max_distance_exist = True
                    # if tmp_distance > max_distance:
                    #     max_distance = tmp_distance
            # if max_distance_exist:
            # 找出骑手的路径出来


            same_time_delivery_order_next_distance_distance.append(max_distance)
        # same_time_delivery_order_distance.append(overdue_this_courier_order_num)

    return same_time_delivery_order_next_distance_distance


def real_data_overdue_qishou_order_num_comparison1001_bushunlu_next_stop_distance():
    df = pd.read_excel('../data/2W_order20201001.xlsx')
    data = df.values
    overdue_order_num = 0
    order_sum = 0
    overdue_order_id = defaultdict(list)  # courier_id : [order_id]
    courier_order_mapping = defaultdict(list)  # courier_id: [(order_id,create_time,deliver_time)]

    max_courier_id = 99999999
    for line in data:
        print(line)
        promise_time = int(line[5])
        order_id = order_sum
        if math.isnan(line[2]):
            courier_id = max_courier_id
        else:
            courier_id = int(line[2])

        if promise_time <= 0:
            continue

        if line[14] == 'a' or line[11] == 'a' or line[10] == 'a':
            continue
        else:
            order_deliver_timestep = int((int(line[14].timestamp()) - int(
                time.mktime(time.strptime("2020-10-01 00:00:00", "%Y-%m-%d %H:%M:%S")))))
            jiedan_timestep = int((int(line[11].timestamp()) - int(
                time.mktime(time.strptime("2020-10-01 00:00:00", "%Y-%m-%d %H:%M:%S")))))
            # time_str = datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
            order_create_timestep = int((int(line[10].to_pydatetime().timestamp()) - int(
                time.mktime(time.strptime("2020-10-01 00:00:00", "%Y-%m-%d %H:%M:%S")))))
        # order_create_timestep = int((int(line[10].timestamp()) - int(
        #     time.mktime(time.strptime("2020-10-01 00:00:00", "%Y-%m-%d %H:%M:%S")))))
            daodian_timestep = int((int(line[12].to_pydatetime().timestamp()) - int(
                time.mktime(time.strptime("2020-10-01 00:00:00", "%Y-%m-%d %H:%M:%S")))))

            shop_lat = float(line[7])
            shop_lon = float(line[6])
            user_lat = float(line[9])
            user_lon = float(line[8])

            if order_deliver_timestep > 86400 or order_deliver_timestep < 0 or order_create_timestep > 86400 or order_create_timestep < 0:
                continue
            deliver_order_time = order_deliver_timestep - order_create_timestep
            courier_order_mapping[courier_id].append(
                (order_id, jiedan_timestep, order_deliver_timestep, user_lat, user_lon, shop_lat, shop_lon))
            if deliver_order_time > promise_time:
                overdue_order_num += 1
                overdue_order_id[courier_id].append((order_id, jiedan_timestep, order_deliver_timestep))

            order_sum += 1
    same_time_delivery_order_next_distance_distance = []  # 先拿用户位置_distance异同/商家位置异同的距离来看
    for item_courier in courier_order_mapping.keys():
        # 某一个骑手
        if len(courier_order_mapping[item_courier])<=1:
            continue
        for all_order_item_id in range(len(courier_order_mapping[item_courier])):
            all_order_item_create = courier_order_mapping[item_courier][all_order_item_id][1]
            all_order_item_deliver = courier_order_mapping[item_courier][all_order_item_id][2]
            all_order_user_lat = courier_order_mapping[item_courier][all_order_item_id][3]
            all_order_user_lon = courier_order_mapping[item_courier][all_order_item_id][4]
            # # 针对骑手某一个单，找同时配送的订单
            # # same_time_deliver_order_distance = []
            # # max_distance_exist = False
            # # max_distance = 0
            # leiji_distance = 0
            for all_order_item_id_y in range(len(courier_order_mapping[item_courier])):
                if all_order_item_id_y <= all_order_item_id:
                    continue
                cur_order_create = courier_order_mapping[item_courier][all_order_item_id_y][1]
                cur_order_deliver = courier_order_mapping[item_courier][all_order_item_id_y][2]
                cur_order_user_lat = courier_order_mapping[item_courier][all_order_item_id_y][3]
                cur_order_user_lon = courier_order_mapping[item_courier][all_order_item_id_y][4]
                # 同时配送这个单
                if not (all_order_item_create > cur_order_deliver or all_order_item_deliver < cur_order_create):
                    tmp_distance = get_distance_hav(all_order_user_lat, all_order_user_lon,
                                                    cur_order_user_lat,
                                                    cur_order_user_lon)
                    max_distance_exist = True
                    if tmp_distance > max_distance:
                        max_distance = tmp_distance
            if max_distance_exist:
                same_time_delivery_order_next_distance_distance.append(max_distance)
        # same_time_delivery_order_distance.append(overdue_this_courier_order_num)

    return same_time_delivery_order_next_distance_distance
# order_distance1001 = real_data_overdue_qishou_order_num_comparison1001_bushunlu()
order_distance1001_max_distance,group_order_num1001 = real_data_overdue_qishou_order_num_comparison1001_bushunlu_max_distance()
# order_distance1012 = real_data_overdue_qishou_order_num_comparison1012_bushunlu()
order_distance1012_max_distance,group_order_num1012 = real_data_overdue_qishou_order_num_comparison1012_bushunlu_max_distance()
# order_distance1001_leiji_distance = real_data_overdue_qishou_order_num_comparison1001_bushunlu_leiji_distance()
# order_distance1001_next_stop_distance = real_data_overdue_qishou_order_num_comparison1001_bushunlu_next_stop_distance()

# sample_A = order_distance1001
# sample_A =order_distance1001_max_distance
# sample_A =order_distance1012

# sample_A = order_distance1001_leiji_distance


# 1.
# group_order_num =group_order_num1001+group_order_num1012
# sample_A =group_order_num




sample_A =order_distance1012_max_distance+order_distance1001_max_distance


import numpy as np
import matplotlib
import os
import matplotlib.pyplot as plt
fig = plt.figure()
plt.rc('font', family='Times New Roman', size=25)
# plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
plt.rcParams.update({'font.size':20})
ax = fig.add_subplot(1, 1, 1)
# ax.grid(True)
a = 0
nhist = 100
b = np.max(sample_A)
c = b - a
d = float(c) / float(nhist)  # size of each bin
# tmp will contain a list of bins:  [a, a+d, a+2*d, a+3*d, ... b]
tmp = [a]
for i in range(nhist):
    if i == a:
        continue
    else:
        tmp.append(tmp[i - 1] + d)

#  CDF of A
ax.hist(sample_A, bins=tmp, cumulative=True, density=True, stacked=True,
        color='black', histtype='step', linewidth=2.0,
        label='samples A')

# plt.xlim([0,10])
plt.xlim([0, 4.5])
plt.yticks(size=28)
plt.xticks(size=28)
# plt.xlabel('Order Similarity During Concurrent Delivery')
plt.xlabel('Offset Distance Between Orders(km)', size=28)
# plt.xlabel('Number of Orders When Overdue')
# plt.ylabel('CDF')
plt.ylabel('CDF', size=28)
# plt.show()
# plt.show()
plt.tight_layout()
plt.savefig('Order Similarity During Concurrent Delivery0521.pdf',bbox_inches ='tight')
# plt.savefig('Number of Orders When Overdue.pdf',bbox_inches ='tight')
# plt.savefig('骑手配送超时发生时的订单量zh.pdf',bbox_inches ='tight')