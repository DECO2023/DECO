'''
1、处理一下输入：之前7-10有些promise=0 的订单需要过滤；
2、至少先保证没换单前【两个结果一致】
'''

import pickle
import tensorflow as tf
from simulator.encounter import Encounter
from simulator.envs import *
import numpy as np
from algorithm.A2C import *
from algorithm.alg_utility import *
import itertools
import copy

# 输入
# 一天的所有订单10.12,未转网格，未转时间步
order_real = pickle.load(open("D:/exchange/dataProcessing/all_orders_target_20201012.pkl", 'rb'))
# 10.12骑手第一次出现的时间及地点, 未转网格，未转时间步
couriers_init = pickle.load(open("D:/exchange/dataProcessing/courier_init_20201012.pkl", 'rb'))

# 时间步:10s，平台派单(根据距离最近)
# 时间步: 遍历检查是否存在相遇可换单事件：判断可换单的逻辑

# 全局参数的初始化
repeat_time = 10000
gamma = 0.9  # RL中计算未来reward的 折扣因子

max_iter = 86400  # 10s一个时间步=8640，可能有很多空白时间点-----10min

max_train_step = 1000

tf.compat.v1.set_random_seed(1)

env = Region(couriers_init, order_real)
env_state = env.env_initialize()

order_to_wait_to_next_timestep = []  # 当前时间步未得到分派的订单

# train:10.12
T = 0
while T < max_iter:

    # *********************1********************平台派单（按10min 按批派单）(根据距离最近),来一个新订单就派单
    time_step_courier_state_file_name_exchange = "D:/exchange/train/update-2021-8-24/no-exchange" \
                                                 "/time_step_" + str(T) + "_courier_state.txt"
    time_step_courier_state_file_name_encounter = "D:/exchange/train/update-2021-8-24/no-exchange-encounter" \
                                                  "/time_step_" + str(T) + "_encounter.txt"
    # 每一个时间步，用txt文档记录，骑手状态及分派状态的记录。
    # print(T)
    if T > 0:
        # 每个时间步---更新骑手新一个时间步的状态、订单状态(对于初始时刻T=0的状态，不做更新)
        for x_courier_id in env.couriers_dict:
            env.couriers_dict[x_courier_id].update_courier_state()

    order_to_deal_with = env.day_orders[T]
    # 更新订单和骑手信息(订单如果当前时间步没有人接，就保留到下一时刻继续找骑手，【记录订单的等待时间？】)
    if len(order_to_wait_to_next_timestep) != 0:
        for added_order in order_to_wait_to_next_timestep:
            order_to_deal_with.append(added_order)
        order_to_wait_to_next_timestep = []

    # 针对该时间步的每一个订单+之前时间步找到骑手的订单，找距离最近的骑手派给他.
    for i_order in order_to_deal_with:
        # 找到最近的骑手，给他派单;写一个将每个订单派给最近骑手的一个简单调度策略。
        available_courier_list, courier_distance = env.couriers_info_collect(i_order, T)
        # 有骑手之后，还是有很多单没人接，available_courier_list为空*****************

        if len(available_courier_list) == 0:
            order_to_wait_to_next_timestep.append(i_order)
        else:
            c_id = np.argmin(courier_distance)
            chosen_courier = available_courier_list[c_id]
            chosen_courier.take_order(i_order, T)

    # *****************2*******************判断相遇换单事件(需要换单的相遇事件)
    # 每个时间步，监测到两个骑手相遇了(遍历骑手找他们的位置持续10s距离小于5m),问题：骑手的每个轨迹点可以获得吗
    online_couriers = []  # 存储骑手对象的在线骑手列表
    for courier_id in env.couriers_dict:
        if env.couriers_dict[courier_id].online:
            online_couriers.append(env.couriers_dict[courier_id])
    cur_time_step_encounter_events = []  # 当前时间步要处理的相遇换单事件
    # 将遍历得到相遇的骑手(id1,id2)[相遇对象]存入day_encounter[time_step],依次对每个时间步的encounter对象做换单决策
    for online_courier_count_x in range(len(online_couriers)):
        for online_courier_count_y in range(online_courier_count_x + 1, len(online_couriers)):
            courier_encounter_distance = get_distance_hav(online_couriers[online_courier_count_x].lat,
                                                          online_couriers[online_courier_count_x].lon,
                                                          online_couriers[online_courier_count_y].lat,
                                                          online_couriers[online_courier_count_y].lon)
            # 距离单位为km，10m=0.01km
            if courier_encounter_distance < 0.01 and \
                    not (online_couriers[online_courier_count_x].cur_order_num == 0 and
                         online_couriers[online_courier_count_y].cur_order_num == 0) and \
                    not (online_couriers[online_courier_count_x].cur_order_num == 1 and
                         online_couriers[online_courier_count_y].cur_order_num == 1) and \
                    not (online_couriers[online_courier_count_x].cur_order_num == 1 and
                         online_couriers[online_courier_count_y].cur_order_num == 0) and \
                    not (online_couriers[online_courier_count_x].cur_order_num == 0 and
                         online_couriers[online_courier_count_y].cur_order_num == 1):  # 这里体现 换单骑手意愿度！！！！！！！！！！！！！！！
                isNewEncounterEvent = True
                for last_time_encounter_event in env.encounter_exchange_event:
                    if (T - last_time_encounter_event.encounter_end_time_slot < 10) and \
                            (last_time_encounter_event.encounter_id1 ==
                             online_couriers[online_courier_count_x].courier_id and
                             last_time_encounter_event.encounter_id2 ==
                             online_couriers[online_courier_count_y].courier_id) or \
                            (last_time_encounter_event.encounter_id2 ==
                             online_couriers[online_courier_count_x].courier_id and
                             last_time_encounter_event.encounter_id1 ==
                             online_couriers[online_courier_count_y].courier_id):
                        last_time_encounter_event.encounter_end_time_slot = T
                        isNewEncounterEvent = False
                        break
                if isNewEncounterEvent:
                    courier_encounter_event = Encounter(online_couriers[online_courier_count_x].courier_id,
                                                        online_couriers[online_courier_count_y].courier_id,
                                                        T)
                    print('encounterEvent:', T, 'courier_id1:', online_couriers[online_courier_count_x].courier_id,
                          'courier_id2:', online_couriers[online_courier_count_y].courier_id)
                    with open(time_step_courier_state_file_name_encounter, "a") as file:
                        file.writelines('time:' + str(T) +
                                        ', courier_id1:' + str(online_couriers[online_courier_count_x].courier_id) +
                                        ', courier1_loc: (' + str(online_couriers[online_courier_count_x].lat) + ',' +
                                        str(online_couriers[online_courier_count_x].lon) +
                                        '), courier_id2:' + str(online_couriers[online_courier_count_y].courier_id) +
                                        ', courier2_loc: (' + str(online_couriers[online_courier_count_y].lat) + ',' +
                                        str(online_couriers[online_courier_count_y].lon) + ')' + '\n'
                                        )
                        courier1_id = online_couriers[online_courier_count_x].courier_id
                        courier2_id = online_couriers[online_courier_count_y].courier_id
                        file.writelines('courier1, id:' + str(courier1_id) + ',order_list:' + '\n')
                        for order in env.couriers_dict[courier1_id].order_list:
                            file.writelines(',order_id:' + str(order.order_id) +
                                            ',shop_loc:' + str(order.shop_latitude) + ',' + str(order.shop_longitude) +
                                            ',user_loc:' + str(order.user_latitude) + ',' + str(order.user_longitude) +
                                            ',order_create_time:' + str(order.order_create_time) +
                                            ',arrive_merchant_time:' + str(order.arrive_merchant_time) +
                                            ',order_deliver_time:' + str(order.order_deliver_time) +
                                            ',promise_deliver_time:' + str(order.promise_deliver_time) +
                                            ', dispatch_stage:' + str(order.dispatch_stage) +
                                            '\n')
                        file.writelines('courier2, id:' + str(courier2_id) + ',order_list:' + '\n')
                        for order in env.couriers_dict[courier2_id].order_list:
                            file.writelines(',order_id:' + str(order.order_id) +
                                            ',shop_loc:' + str(order.shop_latitude) + ',' + str(order.shop_longitude) +
                                            ',user_loc:' + str(order.user_latitude) + ',' + str(order.user_longitude) +
                                            ',order_create_time:' + str(order.order_create_time) +
                                            ',arrive_merchant_time:' + str(order.arrive_merchant_time) +
                                            ',order_deliver_time:' + str(order.order_deliver_time) +
                                            ',promise_deliver_time:' + str(order.promise_deliver_time) +
                                            ', dispatch_stage:' + str(order.dispatch_stage) +
                                            '\n')
                    env.encounter_exchange_event.append(courier_encounter_event)
                    cur_time_step_encounter_events.append(courier_encounter_event)
    if T % 10 == 9:
        with open(time_step_courier_state_file_name_exchange, "w") as file:
            for courier_id in env.couriers_dict:
                if env.couriers_dict[courier_id].online:
                    file.writelines('time:' + str(env.couriers_dict[courier_id].cur_time) +
                                    ',courier_id:' + str(courier_id) + ',courier_lon:' +
                                    str(env.couriers_dict[courier_id].lon) + ', courier_lat:' +
                                    str(env.couriers_dict[courier_id].lon) + ', orders_num:' +
                                    str(env.couriers_dict[courier_id].cur_order_num) +
                                    ', used_time:' + str(env.couriers_dict[courier_id].cost_time) +
                                    ',day_all_order_num:' + str(len(env.couriers_dict[courier_id].order_list) +
                                                                len(env.couriers_dict[courier_id].
                                                                    encounter_before_finished_orders)) +
                                    ',overdue_order_num' + str(env.couriers_dict[courier_id].overdue_order_num) + '\n')
                    # print('time:', env.couriers_dict[courier_id].cur_time, ',courier_id:', courier_id, ',courier_lon:',
                    #       env.couriers_dict[courier_id].lon, ', courier_lat:', env.couriers_dict[courier_id].lon,
                    #       ', orders_num:', env.couriers_dict[courier_id].cur_order_num,
                    #       ', used_time:', env.couriers_dict[courier_id].cost_time,
                    #       ',day_all_order_num:' + str(len(env.couriers_dict[courier_id].order_list) +
                    #                                   len(env.couriers_dict[
                    #                                           courier_id].encounter_before_finished_orders)),
                    #       ',overdue_order_num', env.couriers_dict[courier_id].overdue_order_num)
                    for order in env.couriers_dict[courier_id].order_list:
                        # print('order_id:', order.order_id,
                        #       ',shop_loc:' + str(order.shop_latitude) + ',' + str(order.shop_longitude) +
                        #       ',user_loc:' + str(order.user_latitude) + ',' + str(order.user_longitude) +
                        #       ',order_create_time:' + str(order.order_create_time) +
                        #       ',arrive_merchant_time:' + str(order.arrive_merchant_time) +
                        #       ',order_deliver_time:' + str(order.order_deliver_time) +
                        #       ',promise_deliver_time:' + str(order.promise_deliver_time) +
                        #       ', dispatch_stage:' + str(order.dispatch_stage)
                        #       )
                        file.writelines(',order_id:' + str(order.order_id) +
                                        ',shop_loc:' + str(order.shop_latitude) + ',' + str(order.shop_longitude) +
                                        ',user_loc:' + str(order.user_latitude) + ',' + str(order.user_longitude) +
                                        ',order_create_time:' + str(order.order_create_time) +
                                        ',arrive_merchant_time:' + str(order.arrive_merchant_time) +
                                        ',order_deliver_time:' + str(order.order_deliver_time) +
                                        ',promise_deliver_time:' + str(order.promise_deliver_time) +
                                        ', dispatch_stage:' + str(order.dispatch_stage) +
                                        '\n')
    T = T + 1
