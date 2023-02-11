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
    time_step_courier_state_file_name_exchange = "D:/exchange/train/baseline/SD-OSquare-record" \
                                                 "/time_step_" + str(T) + "_courier_state.txt"
    time_step_courier_state_file_name_encounter = "D:/exchange/train/baseline/SD-Osquare-encounter" \
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

                    encounter_two_couriers = [
                        env.couriers_dict[online_couriers[online_courier_count_x].courier_id],
                        env.couriers_dict[online_couriers[online_courier_count_y].courier_id]]

                    # deal with 一次相遇换单事件
                    encounter_to_exchange_order_list = []  # 要筛选掉已送完的订单
                    encounter_order_next_stop_location = []
                    to_exchange_order_raw_courier_id_list = []
                    # 订单由当前骑手送达的预计还需时间
                    # to_exchange_order_raw_courier_cost_left_time = []
                    if encounter_two_couriers[0].cur_order_num > encounter_two_couriers[1].cur_order_num:
                        for encounter_order1_id in range(len(encounter_two_couriers[0].order_list)):
                            if encounter_two_couriers[0].order_list[encounter_order1_id].dispatch_stage != 0:
                                encounter_to_exchange_order_list.append(
                                    encounter_two_couriers[0].order_list[encounter_order1_id])
                                encounter_order_next_stop_location.append(
                                    encounter_two_couriers[0].available_loc_real_time[encounter_order1_id])
                                to_exchange_order_raw_courier_id_list.append(0)
                                # to_exchange_order_raw_courier_cost_left_time.append(list(encounter_two_couriers[0].route_flag_to_be_updated.keys())[
                                #                                                         list(encounter_two_couriers[0].route_flag_to_be_updated.values()).index((encounter_order1_id,0))] - T)
                        for encounter_order2_id in range(len(encounter_two_couriers[1].order_list)):
                            if encounter_two_couriers[1].order_list[encounter_order2_id].dispatch_stage != 0:
                                encounter_to_exchange_order_list.append(
                                    encounter_two_couriers[1].order_list[encounter_order2_id])
                                encounter_order_next_stop_location.append(
                                    encounter_two_couriers[1].available_loc_real_time[encounter_order2_id])
                                to_exchange_order_raw_courier_id_list.append(1)
                                # to_exchange_order_raw_courier_cost_left_time.append(list(encounter_two_couriers[1].route_flag_to_be_updated.keys())[
                                #                                                         list(encounter_two_couriers[1].route_flag_to_be_updated.values()).index((encounter_order2_id,0))] -T)
                    else:
                        for encounter_order2_id in range(len(encounter_two_couriers[1].order_list)):
                            if encounter_two_couriers[1].order_list[encounter_order2_id].dispatch_stage != 0:
                                encounter_to_exchange_order_list.append(
                                    encounter_two_couriers[1].order_list[encounter_order2_id])
                                encounter_order_next_stop_location.append(
                                    encounter_two_couriers[1].available_loc_real_time[encounter_order2_id])
                                to_exchange_order_raw_courier_id_list.append(1)
                        for encounter_order1_id in range(len(encounter_two_couriers[0].order_list)):
                            if encounter_two_couriers[0].order_list[encounter_order1_id].dispatch_stage != 0:
                                encounter_to_exchange_order_list.append(
                                    encounter_two_couriers[0].order_list[encounter_order1_id])
                                encounter_order_next_stop_location.append(
                                    encounter_two_couriers[0].available_loc_real_time[encounter_order1_id])
                                to_exchange_order_raw_courier_id_list.append(0)

                    if len(encounter_to_exchange_order_list) > 12:
                        print('debug')
                    if len(encounter_to_exchange_order_list) == 0:
                        continue

                    for encounter_order_id in range(len(encounter_to_exchange_order_list)):
                        if encounter_to_exchange_order_list[encounter_order_id].dispatch_stage == 1:
                            cur_order_next_stop_lon = encounter_to_exchange_order_list[
                                encounter_order_id].shop_longitude
                            cur_order_next_stop_lat = encounter_to_exchange_order_list[encounter_order_id].shop_latitude
                        elif encounter_to_exchange_order_list[encounter_order_id].dispatch_stage == 2:
                            cur_order_next_stop_lon = encounter_to_exchange_order_list[
                                encounter_order_id].user_longitude
                            cur_order_next_stop_lat = encounter_to_exchange_order_list[encounter_order_id].user_latitude
                        else:
                            continue

                        to_exchange_order_raw_courier_cost_left_time = -9999
                        if to_exchange_order_raw_courier_id_list[encounter_order_id] == 0:
                            cur_this_order_loc_id = -1
                            for loc_id in range(len(encounter_two_couriers[0].order_list)):
                                if encounter_to_exchange_order_list[encounter_order_id].order_id == \
                                        encounter_two_couriers[0].order_list[loc_id].order_id:
                                    cur_this_order_loc_id = loc_id
                                    break
                            if cur_this_order_loc_id == -1:
                                print('problem')
                            if encounter_two_couriers[0].route_flag_to_be_updated == {}:
                                to_exchange_order_raw_courier_cost_left_time = 0
                            elif max(encounter_two_couriers[0].route_flag_to_be_updated.keys()) <= T:
                                to_exchange_order_raw_courier_cost_left_time = 0
                            else:
                                for time_step_id in range(T, max(
                                        encounter_two_couriers[0].route_flag_to_be_updated.keys()) + 1):
                                    for state_change_id in range(
                                            len(encounter_two_couriers[0].route_flag_to_be_updated[time_step_id])):
                                        if encounter_two_couriers[0].route_flag_to_be_updated[time_step_id][
                                            state_change_id] == (
                                                cur_this_order_loc_id, 0):
                                            to_exchange_order_raw_courier_cost_left_time = time_step_id - T
                                            break
                        else:
                            cur_this_order_loc_id = -1
                            for loc_id in range(len(encounter_two_couriers[1].order_list)):
                                if encounter_to_exchange_order_list[encounter_order_id].order_id == \
                                        encounter_two_couriers[1].order_list[loc_id].order_id:
                                    cur_this_order_loc_id = loc_id
                                    break
                            if cur_this_order_loc_id == -1:
                                print('problem')
                            # 应该存T时刻之后的那个时间
                            # to_exchange_order_raw_courier_cost_left_time = list(encounter_two_couriers[1].route_flag_to_be_updated.keys())[list(encounter_two_couriers[1].route_flag_to_be_updated.values()).index((cur_this_order_loc_id, 0))] - T
                            if encounter_two_couriers[1].route_flag_to_be_updated == {}:
                                to_exchange_order_raw_courier_cost_left_time = 0
                            elif max(encounter_two_couriers[1].route_flag_to_be_updated.keys()) <= T:
                                to_exchange_order_raw_courier_cost_left_time = 0
                            else:
                                for time_step_id in range(T, max(
                                        encounter_two_couriers[1].route_flag_to_be_updated.keys()) + 1):
                                    # if len(encounter_two_couriers[1].route_flag_to_be_updated[time_step_id]) >1:
                                    #     print('debug')
                                    for change_state_id1 in range(
                                            len(encounter_two_couriers[1].route_flag_to_be_updated[time_step_id])):
                                        if encounter_two_couriers[1].route_flag_to_be_updated[time_step_id][
                                            change_state_id1] == (
                                                cur_this_order_loc_id, 0):
                                            to_exchange_order_raw_courier_cost_left_time = time_step_id - T
                                            break
                        if to_exchange_order_raw_courier_cost_left_time == -9999:
                            print('debug')

                        if encounter_two_couriers[0].route_flag_to_be_updated == {}:
                            encounter_courier1_all_order_deliver_cost_time = 0
                        elif max(encounter_two_couriers[0].route_flag_to_be_updated.keys()) <= T:
                            encounter_courier1_all_order_deliver_cost_time = 0
                        else:
                            encounter_courier1_all_order_deliver_cost_time = max(
                                encounter_two_couriers[0].route_flag_to_be_updated.keys()) - T

                        if encounter_two_couriers[1].route_flag_to_be_updated == {}:
                            encounter_courier2_all_order_deliver_cost_time = 0
                        elif max(encounter_two_couriers[1].route_flag_to_be_updated.keys()) <= T:
                            encounter_courier2_all_order_deliver_cost_time = 0
                        else:
                            encounter_courier2_all_order_deliver_cost_time = max(
                                encounter_two_couriers[1].route_flag_to_be_updated.keys()) - T

                        courier1_avail_loc_list = []
                        courier1_avail_loc_and_order_distance = []
                        for avail_loc_id in range(len(encounter_two_couriers[0].available_loc_real_time)):
                            if encounter_two_couriers[0].available_loc_real_time[avail_loc_id] != 0 and \
                                    encounter_two_couriers[0].order_list[avail_loc_id].order_id != \
                                    encounter_to_exchange_order_list[encounter_order_id].order_id:
                                courier1_avail_loc_list.append(
                                    encounter_two_couriers[0].available_loc_real_time[avail_loc_id])
                                courier1_avail_loc_and_order_distance.append(
                                    get_distance_hav(
                                        encounter_two_couriers[0].available_loc_real_time[avail_loc_id].lat,
                                        encounter_two_couriers[0].available_loc_real_time[avail_loc_id].lon,
                                        cur_order_next_stop_lat, cur_order_next_stop_lon)
                                )
                        if len(courier1_avail_loc_list) == 0:
                            courier1_next_stop_location_lat = encounter_two_couriers[0].lat
                            courier1_next_stop_location_lon = encounter_two_couriers[0].lon
                        else:
                            chosen_courier1_next_stop_id = np.argmin(courier1_avail_loc_and_order_distance)
                            courier1_next_stop_location_lat = courier1_avail_loc_list[chosen_courier1_next_stop_id].lat
                            courier1_next_stop_location_lon = courier1_avail_loc_list[chosen_courier1_next_stop_id].lon

                        courier2_avail_loc_list = []
                        courier2_avail_loc_and_order_distance = []
                        for avail_loc_id in range(len(encounter_two_couriers[1].available_loc_real_time)):
                            if encounter_two_couriers[1].available_loc_real_time[avail_loc_id] != 0 and \
                                    encounter_two_couriers[1].order_list[avail_loc_id].order_id != \
                                    encounter_to_exchange_order_list[encounter_order_id].order_id:
                                courier2_avail_loc_list.append(
                                    encounter_two_couriers[1].available_loc_real_time[avail_loc_id])
                                courier2_avail_loc_and_order_distance.append(
                                    get_distance_hav(
                                        encounter_two_couriers[1].available_loc_real_time[avail_loc_id].lat,
                                        encounter_two_couriers[1].available_loc_real_time[avail_loc_id].lon,
                                        cur_order_next_stop_lat, cur_order_next_stop_lon)
                                )
                        if len(courier2_avail_loc_list) == 0:
                            courier2_next_stop_location_lat = encounter_two_couriers[1].lat
                            courier2_next_stop_location_lon = encounter_two_couriers[1].lon
                        else:
                            chosen_courier2_next_stop_id = np.argmin(courier2_avail_loc_and_order_distance)
                            courier2_next_stop_location_lat = courier2_avail_loc_list[chosen_courier2_next_stop_id].lat
                            courier2_next_stop_location_lon = courier2_avail_loc_list[chosen_courier2_next_stop_id].lon

                        encounter_distances = [
                            get_distance_hav(courier1_next_stop_location_lat, courier1_next_stop_location_lon,
                                             cur_order_next_stop_lat, cur_order_next_stop_lon),
                            get_distance_hav(courier2_next_stop_location_lat,
                                             courier2_next_stop_location_lon,
                                             cur_order_next_stop_lat, cur_order_next_stop_lon),
                        ]
                        chosen_courier_id = np.argmin(encounter_distances)
                        if encounter_two_couriers[chosen_courier_id].cur_order_num >= 6:
                            # 该谁的还是谁的，没变化，也不用来更新换单模型
                            continue

                        courier1_huandan_time_lat = 0
                        courier1_huandan_time_lon = 0
                        courier2_huandan_time_lat = 0
                        courier2_huandan_time_lon = 0
                        if T + 5 in encounter_two_couriers[0].route_time_step.keys():
                            courier1_huandan_time_lat = encounter_two_couriers[0].route_time_step[
                                T + 5].lat
                            courier1_huandan_time_lon = encounter_two_couriers[0].route_time_step[
                                T + 5].lon
                        else:
                            courier1_huandan_time_lat = encounter_two_couriers[1].lat
                            courier1_huandan_time_lon = encounter_two_couriers[1].lon

                        if T + 5 in encounter_two_couriers[1].route_time_step.keys():
                            courier2_huandan_time_lat = encounter_two_couriers[1].route_time_step[
                                T + 5].lat
                            courier2_huandan_time_lon = encounter_two_couriers[1].route_time_step[
                                T + 5].lon
                        else:
                            courier2_huandan_time_lat = encounter_two_couriers[1].lat
                            courier2_huandan_time_lon = encounter_two_couriers[1].lon

                        if chosen_courier_id != to_exchange_order_raw_courier_id_list[encounter_order_id]:
                            # 出现换单
                            if chosen_courier_id == 0:
                                # if encounter_two_couriers[0].courier_id == 103401162:
                                #     print('debug')
                                # elif encounter_two_couriers[1].courier_id == 103401162:
                                #     print('debug')
                                encounter_two_couriers[0].exchange_take_order(
                                    encounter_to_exchange_order_list[encounter_order_id], T,courier1_huandan_time_lat,
                                            courier1_huandan_time_lon,
                                            courier2_huandan_time_lat,
                                            courier2_huandan_time_lon)
                                encounter_two_couriers[1].exchange_drop_order(
                                    encounter_to_exchange_order_list[encounter_order_id], T,courier1_huandan_time_lat,
                                            courier1_huandan_time_lon,
                                            courier2_huandan_time_lat,
                                            courier2_huandan_time_lon)

                                this_order_loc_id = -1
                                for loc_id in range(len(encounter_two_couriers[0].order_list)):
                                    if encounter_to_exchange_order_list[encounter_order_id].order_id == \
                                            encounter_two_couriers[0].order_list[loc_id].order_id:
                                        this_order_loc_id = loc_id
                                        break
                                if this_order_loc_id == -1:
                                    print('problem')

                                this_order_new_courier_cost_left_time = -9999
                                if encounter_two_couriers[0].route_flag_to_be_updated == {}:
                                    this_order_new_courier_cost_left_time = 0
                                elif max(encounter_two_couriers[0].route_flag_to_be_updated.keys()) <= T:
                                    this_order_new_courier_cost_left_time = 0
                                else:
                                    for time_step_id in range(T, max(
                                            encounter_two_couriers[0].route_flag_to_be_updated.keys()) + 1):
                                        for change_state_id_exchange in range(
                                                len(encounter_two_couriers[0].route_flag_to_be_updated[time_step_id])):
                                            if encounter_two_couriers[0].route_flag_to_be_updated[time_step_id][
                                                change_state_id_exchange] == (
                                                    this_order_loc_id, 0):
                                                this_order_new_courier_cost_left_time = time_step_id - T
                                                break
                                if this_order_new_courier_cost_left_time == -9999:
                                    print('problem')

                                if encounter_two_couriers[0].route_flag_to_be_updated == {}:
                                    encounter_courier1_all_order_deliver_cost_time_exchange = 0
                                elif max(encounter_two_couriers[0].route_flag_to_be_updated) <= T:
                                    encounter_courier1_all_order_deliver_cost_time_exchange = 0
                                else:
                                    encounter_courier1_all_order_deliver_cost_time_exchange = max(
                                        encounter_two_couriers[0].route_flag_to_be_updated.keys()) - T

                                if encounter_two_couriers[1].route_flag_to_be_updated == {}:
                                    encounter_courier2_all_order_deliver_cost_time_exchange = 0
                                elif max(encounter_two_couriers[1].route_flag_to_be_updated) <= T:
                                    encounter_courier2_all_order_deliver_cost_time_exchange = 0
                                else:
                                    encounter_courier2_all_order_deliver_cost_time_exchange = max(
                                        encounter_two_couriers[1].route_flag_to_be_updated.keys()) - T

                            else:
                                encounter_two_couriers[0].exchange_drop_order(
                                    encounter_to_exchange_order_list[encounter_order_id], T,courier1_huandan_time_lat,
                                            courier1_huandan_time_lon,
                                            courier2_huandan_time_lat,
                                            courier2_huandan_time_lon)
                                encounter_two_couriers[1].exchange_take_order(
                                    encounter_to_exchange_order_list[encounter_order_id], T,courier1_huandan_time_lat,
                                            courier1_huandan_time_lon,
                                            courier2_huandan_time_lat,
                                            courier2_huandan_time_lon)
                                this_order_loc_id = -1
                                for loc_id in range(len(encounter_two_couriers[1].order_list)):
                                    if encounter_to_exchange_order_list[encounter_order_id].order_id == \
                                            encounter_two_couriers[1].order_list[loc_id].order_id:
                                        this_order_loc_id = loc_id
                                if this_order_loc_id == -1:
                                    print('problem')

                                this_order_new_courier_cost_left_time = -9999
                                if encounter_two_couriers[1].route_flag_to_be_updated == {}:
                                    this_order_new_courier_cost_left_time = 0
                                elif max(encounter_two_couriers[1].route_flag_to_be_updated) <= T:
                                    this_order_new_courier_cost_left_time = 0
                                else:
                                    for time_step_id in range(T, max(
                                            encounter_two_couriers[1].route_flag_to_be_updated.keys()) + 1):
                                        for state_exchange_id in range(
                                                len(encounter_two_couriers[1].route_flag_to_be_updated[time_step_id])):
                                            if encounter_two_couriers[1].route_flag_to_be_updated[time_step_id][
                                                state_exchange_id] == (
                                                    this_order_loc_id, 0):
                                                this_order_new_courier_cost_left_time = time_step_id - T
                                                break
                                if this_order_new_courier_cost_left_time == -9999:
                                    print('problem')

                                if encounter_two_couriers[0].route_flag_to_be_updated == {}:
                                    encounter_courier1_all_order_deliver_cost_time_exchange = 0
                                elif max(encounter_two_couriers[0].route_flag_to_be_updated) <= T:
                                    encounter_courier1_all_order_deliver_cost_time_exchange = 0
                                else:
                                    encounter_courier1_all_order_deliver_cost_time_exchange = max(
                                        encounter_two_couriers[0].route_flag_to_be_updated.keys()) - T

                                if encounter_two_couriers[1].route_flag_to_be_updated == {}:
                                    encounter_courier2_all_order_deliver_cost_time_exchange = 0
                                elif max(encounter_two_couriers[1].route_flag_to_be_updated) <= T:
                                    encounter_courier2_all_order_deliver_cost_time_exchange = 0
                                else:
                                    encounter_courier2_all_order_deliver_cost_time_exchange = max(
                                        encounter_two_couriers[1].route_flag_to_be_updated.keys()) - T

                            courier1_courier2_distance = get_distance_hav(encounter_two_couriers[0].lat,
                                                                          encounter_two_couriers[0].lon,
                                                                          encounter_two_couriers[1].lat,
                                                                          encounter_two_couriers[1].lon)
                            courier1_courier2_time = courier1_courier2_distance / 12.11 * (60 * 6) * 2  # 单位：时间步数

                            order_raw_dispatch_time_average = to_exchange_order_raw_courier_cost_left_time
                            order_exchange_dispatch_time_average = this_order_new_courier_cost_left_time + courier1_courier2_time

                            # 超时率(为0，未超时该订单未来将不会超时，为1该订单未来将超时)
                            order_promise_left_delivery_time = encounter_to_exchange_order_list[
                                                                   encounter_order_id].promise_deliver_time - T
                            raw_overdue_order_flag = 0
                            if order_promise_left_delivery_time < order_raw_dispatch_time_average:
                                raw_overdue_order_flag = 1
                            exchange_overdue_order_flag = 0
                            if order_promise_left_delivery_time < order_exchange_dispatch_time_average:
                                exchange_overdue_order_flag = 1

                            # 优化的骑手送完所有订单的平均配送时间
                            raw_courier_dispatch_time_average = (
                                                                            encounter_courier1_all_order_deliver_cost_time + encounter_courier2_all_order_deliver_cost_time) / 2
                            exchange_courier_dispatch_time_average = (
                                                                                 encounter_courier1_all_order_deliver_cost_time_exchange + encounter_courier2_all_order_deliver_cost_time_exchange) / 2

                        else:
                            # 不换单
                            order_raw_dispatch_time_average = to_exchange_order_raw_courier_cost_left_time
                            order_exchange_dispatch_time_average = to_exchange_order_raw_courier_cost_left_time

                            # 超时率(为0，未超时该订单未来将不会超时，为1该订单未来将超时)
                            order_promise_left_delivery_time = encounter_to_exchange_order_list[
                                                                   encounter_order_id].promise_deliver_time - T
                            raw_overdue_order_flag = 0
                            if order_promise_left_delivery_time < order_raw_dispatch_time_average:
                                raw_overdue_order_flag = 1
                            exchange_overdue_order_flag = raw_overdue_order_flag

    if T % 600 == 599:
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
