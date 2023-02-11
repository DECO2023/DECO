# 两个actor，2个critic
# 时间步变短，lr变快

'''
1、处理一下输入：之前7-10有些promise=0 的订单需要过滤；
2、至少先保证没换单前【两个结果一致】
'''
import math
import os
import pickle
import tensorflow as tf

from simulator.encounter import Encounter
from simulator.envs_zh_1001_update_200_2min import *
import numpy as np
from algorithm.HOAC_optimize_fusion_axis_batch_memory2_attention_conv_batch256_norm_new_jt_multi_head_conv_3 import *
from algorithm.alg_utility import *
import itertools
import copy

# 【近铁区域】
# 经度：121.354-121.40939 纬度：31.214287- 31.260757
# 中环内小区域：
# lon_min=121.440130,lon_max=121.49999，lat_min=31.210006,lat_max=31.269933

min_lon = 121.44013
min_lat = 31.210006
max_lon = 121.49999
max_lat = 31.269933

# 时间步:10s，平台派单(根据距离最近)
# 时间步: 遍历检查是否存在相遇可换单事件：判断可换单的逻辑

order_real = pickle.load(open("D:/exchange/dataProcessing/all_orders_target_20201001.pkl", 'rb'))
# 10.12骑手第一次出现的时间及地点, 未转网格，未转时间步
couriers_init = pickle.load(open("D:/exchange/dataProcessing/courier_init_20201001.pkl", 'rb'))

# 全局参数的初始化
global_step = 0
low_level_global_step = 0
repeat_time = 10000
gamma = 0.9  # RL中计算未来reward的 折扣因子

learning_rate_Hierarical_Actor = 1e-4
learning_rate_Actor = 1e-4
learning_rate_Hierarchical_Critic = 1e-4
learning_rate_Critic = 1e-4

max_iter = 60 * 60 * 24  # 10s一个时间步=8640，可能有很多空白时间点-----10min

# 骑手当前订单数,预测的骑手的下一站经纬度.送完手中所有单还需时间,所持订单【其他状态：相遇骑手的状态】--最多6个订单
state_dim = 13+2
action_dim = 2
h_state_dim = 19+2 + 4
h_action_dim = 2

# critic_action_dim = action_dim

max_train_step = 1000

tf.compat.v1.set_random_seed(1)
# 实际网络
# log_dir = "D:/exchange/train/update-2021-8-24/HAC_train_logs/"

# 新训练模型
sess = tf.compat.v1.Session()
hierachical_actor = High_Level_Network(sess, h_state_dim, h_action_dim, learning_rate_Hierarical_Actor)
actor = Actor(sess, state_dim, action_dim, learning_rate_Actor)
hierachical_critic = High_Level_Critic(sess, h_state_dim, learning_rate_Critic)
critic = Critic(sess, state_dim, learning_rate_Critic)
sess.run(tf.compat.v1.global_variables_initializer())
saver = tf.compat.v1.train.Saver()

# saver = tf.compat.v1.train.Saver()
# saver.restore(sess,'D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward/before/1105/model_1105.ckpt')
# saver.restore(sess,'D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward/218/model_218.ckpt')
# D:\exchange\train\optimize-2022-1-19\main\20200306_attention_conv_times_batch_50_courier_reward\before2\high_checkpoint\203
# 用跑过的模型继续训练
# sess = tf.compat.v1.Session()
# # saver = tf.compat.v1.train.import_meta_graph('D:/exchange/train/run2021-7-1/DQN_train_logs/model.ckpt.meta')
# # saver.restore(sess, 'D:/exchange/train/run2021-7-1/DQN_train_logs/model.ckpt')
# saver = tf.compat.v1.train.Saver()
# saver.restore(sess,'D:/exchange/train/run2021-7-1/DQN_train_logs/model.ckpt')
episode_ep_reward = []
episode_ep_average_reward = []
# deal_with_data_count = 0
while True:

    ep_track_r = []
    low_level_ep_track_r = []
    # 一天的所有订单10.12,未转网格，未转时间步

    # order_real = pickle.load(
    #     open("D:/exchange/dataProcessing/all_orders_target_jt_202010" + str(deal_with_data_count % 7 + 15) + ".pkl",
    #          'rb'))
    # # 10.12骑手第一次出现的时间及地点, 未转网格，未转时间步
    # couriers_init = pickle.load(
    #     open("D:/exchange/dataProcessing/courier_init_jt_202010" + str(deal_with_data_count % 7 + 15) + ".pkl", 'rb'))

    env = Region(couriers_init, order_real)
    env_state = env.env_initialize()
    # env_state = env.env_initialize(deal_with_data_count % 7 + 15)
    # deal_with_data_count += 1

    order_to_wait_to_next_timestep = []  # 当前时间步未得到分派的订单

    event_id = 0
    episode_id = 0
    # end = False
    # train:10.12
    # T = 3600*10
    T = 0
    # max_iter = 60 * 60 * 6

    while T < max_iter:

        # *********************1********************平台派单（按10min 按批派单）(根据距离最近),来一个新订单就派单
        # time_step_courier_state_file_name_exchange = "D:/exchange/train/run2021-7-1/exchange_DQN_20201012_train/time_step_" + str(
        #     T) + "_courier_state.txt"
        # 每一个时间步，用txt文档记录，骑手状态及分派状态的记录。
        print(str(global_step) +':'+ str(T))
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

        # 模拟可获取的beacon序列
        online_couriers = []  # 存储骑手对象的在线骑手列表
        for courier_id in env.couriers_dict:
            if env.couriers_dict[courier_id].online:
                online_couriers.append(env.couriers_dict[courier_id])
        cur_time_step_encounter_events = []  # 当前时间步要处理的相遇事件
        cur_time_step_exchange_events = []  # 当前时间步要处理的换单事件
        # cur_time_step_exchange_events_state_input_list = []
        cur_time_step_encounter_event_high_level_state_input_list = []
        cur_time_step_encounter_event_high_level_next_state_list = []
        cur_time_step_encounter_event_high_level_action_list = []
        cur_time_step_encounter_event_high_level_reward_list = []

        high_level_reward_track = []
        # 将遍历得到相遇的骑手(id1,id2)[相遇对象]存入day_encounter[time_step],依次对每个时间步的encounter对象做换单决策
        for online_courier_count_x in range(len(online_couriers)):
            for online_courier_count_y in range(online_courier_count_x + 1, len(online_couriers)):
                # 1）模拟beacon检测到了相遇
                courier_encounter_distance = get_distance_hav(online_couriers[online_courier_count_x].lat,
                                                              online_couriers[online_courier_count_x].lon,
                                                              online_couriers[online_courier_count_y].lat,
                                                              online_couriers[online_courier_count_y].lon)
                if courier_encounter_distance < 0.01 and \
                        not (online_couriers[online_courier_count_x].cur_order_num == 0 and
                             online_couriers[online_courier_count_y].cur_order_num == 0) and \
                        not (online_couriers[online_courier_count_x].cur_order_num == 1 and
                             online_couriers[online_courier_count_y].cur_order_num == 1) and \
                        not (online_couriers[online_courier_count_x].cur_order_num == 1 and
                             online_couriers[online_courier_count_y].cur_order_num == 0) and \
                        not (online_couriers[online_courier_count_x].cur_order_num == 0 and
                             online_couriers[online_courier_count_y].cur_order_num == 1):  # beacon检测到
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
                        # print(T)
                        # print('new encounter event:')
                        # print('courier1_id:', online_couriers[online_courier_count_x].courier_id, ', courier2_id:',
                        # online_couriers[online_courier_count_y].courier_id)
                        # encounter state_input preprocess
                        encounter_start_time = T
                        encounter_start_courier1_lat = online_couriers[online_courier_count_x].lat
                        encounter_start_courier1_lon = online_couriers[online_courier_count_x].lon
                        encounter_start_courier2_lat = online_couriers[online_courier_count_y].lat
                        encounter_start_courier2_lon = online_couriers[online_courier_count_y].lon
                        encounter_start_courier1_next_stop_lat = 0
                        encounter_start_courier1_next_stop_lon = 0
                        encounter_start_courier2_next_stop_lat = 0
                        encounter_start_courier2_next_stop_lon = 0
                        encounter_courier1_cur_order_cur_stage_remaining_time = 0
                        encounter_courier2_cur_order_cur_stage_remaining_time = 0

                        if T + 1 not in online_couriers[online_courier_count_x].route_flag_to_be_updated.keys() or \
                                online_couriers[online_courier_count_x].cur_order_num == 0 or len(
                            online_couriers[online_courier_count_x].route_flag_to_be_updated[T + 1]) == 0:
                            encounter_start_courier1_next_stop_lat = online_couriers[online_courier_count_x].lat
                            encounter_start_courier1_next_stop_lon = online_couriers[online_courier_count_x].lon
                            encounter_courier1_cur_order_cur_stage_remaining_time = 0
                        else:
                            if len(online_couriers[online_courier_count_x].route_flag_to_be_updated[T + 1]) > 1 and \
                                    online_couriers[online_courier_count_x].route_flag_to_be_updated[T + 2] != []:
                                courier1_next_stop_order_loc_id = -1
                                detect_time_added = 1
                                while courier1_next_stop_order_loc_id == -1 and \
                                        online_couriers[online_courier_count_x].route_flag_to_be_updated[
                                            T + detect_time_added + 1] != []:
                                    for flag_item in online_couriers[online_courier_count_x].route_flag_to_be_updated[
                                        T + detect_time_added]:
                                        for next_time_flag_item in \
                                                online_couriers[online_courier_count_x].route_flag_to_be_updated[
                                                    T + detect_time_added + 1]:
                                            if flag_item == next_time_flag_item:
                                                courier1_next_stop_order_loc_id = next_time_flag_item[0]
                                                break
                                    detect_time_added += 1
                                if courier1_next_stop_order_loc_id == -1:
                                    # 都是快送完的单
                                    for flag_item in online_couriers[online_courier_count_x].route_flag_to_be_updated[
                                        T + 1]:
                                        if flag_item[1] != 2:
                                            courier1_next_stop_order_loc_id = flag_item[0]
                                            break
                                    if courier1_next_stop_order_loc_id == -1:
                                        print('debug')
                            else:
                                courier1_next_stop_order_loc_id = \
                                    online_couriers[online_courier_count_x].route_flag_to_be_updated[T + 1][0][0]

                            if courier1_next_stop_order_loc_id > len(
                                    online_couriers[online_courier_count_x].available_loc_real_time):
                                print('debug')
                            if online_couriers[online_courier_count_x].available_loc_real_time[
                                courier1_next_stop_order_loc_id] == 0:
                                # 该单下一时刻送完了
                                encounter_start_courier1_next_stop_lat = online_couriers[online_courier_count_x].lat
                                encounter_start_courier1_next_stop_lon = online_couriers[online_courier_count_x].lon
                                encounter_courier1_cur_order_cur_stage_remaining_time = 1
                            else:
                                encounter_start_courier1_next_stop_lat = \
                                    online_couriers[online_courier_count_x].available_loc_real_time[
                                        courier1_next_stop_order_loc_id].lat
                                encounter_start_courier1_next_stop_lon = \
                                    online_couriers[online_courier_count_x].available_loc_real_time[
                                        courier1_next_stop_order_loc_id].lon
                                # encounter_start_courier1_next_stop_lat = \
                                #     online_couriers[online_courier_count_x].available_loc_real_time[
                                #         online_couriers[online_courier_count_x].route_flag_to_be_updated[T + 1][0][
                                #             0]].lat
                                # encounter_start_courier1_next_stop_lon = \
                                #     online_couriers[online_courier_count_x].available_loc_real_time[
                                #         online_couriers[online_courier_count_x].route_flag_to_be_updated[T + 1][0][
                                #             0]].lon

                                cur_order_id_in_courier_order_list = \
                                    online_couriers[online_courier_count_x].route_flag_to_be_updated[T + 1][0][0]
                                cur_order_stage_in_courier_order_list = \
                                    online_couriers[online_courier_count_x].route_flag_to_be_updated[T + 1][0][1]
                                objective_order_flag = -1
                                if cur_order_stage_in_courier_order_list == 1:
                                    objective_order_flag = 2
                                else:
                                    objective_order_flag = 0

                                objective_route_flag_item = (cur_order_id_in_courier_order_list, objective_order_flag)

                                cur_time = T + 1
                                order_next_step_need_time = 0
                                while cur_time > T:
                                    route_flag_item = online_couriers[online_courier_count_x].route_flag_to_be_updated[
                                        cur_time]
                                    if objective_route_flag_item in route_flag_item:
                                        order_next_step_need_time = cur_time
                                        break
                                    cur_time += 1
                                if order_next_step_need_time == 0:
                                    print('debug')
                                encounter_courier1_cur_order_cur_stage_remaining_time = order_next_step_need_time - T

                        if T + 1 not in online_couriers[online_courier_count_y].route_flag_to_be_updated.keys() or \
                                online_couriers[online_courier_count_y].cur_order_num == 0 or len(
                            online_couriers[online_courier_count_y].route_flag_to_be_updated[T + 1]) == 0:
                            encounter_start_courier2_next_stop_lat = online_couriers[online_courier_count_y].lat
                            encounter_start_courier2_next_stop_lon = online_couriers[online_courier_count_y].lon
                            encounter_courier2_cur_order_cur_stage_remaining_time = 0
                        else:
                            if len(online_couriers[online_courier_count_y].route_flag_to_be_updated[T + 1]) > 1 and \
                                    online_couriers[online_courier_count_y].route_flag_to_be_updated[T + 2] != []:
                                courier2_next_stop_order_loc_id = -1
                                detect_time_added = 1
                                while courier2_next_stop_order_loc_id == -1 and \
                                        online_couriers[online_courier_count_y].route_flag_to_be_updated[
                                            T + detect_time_added + 1] != []:
                                    for flag_item in \
                                            online_couriers[online_courier_count_y].route_flag_to_be_updated[
                                                T + detect_time_added]:
                                        for next_time_flag_item in \
                                                online_couriers[online_courier_count_y].route_flag_to_be_updated[
                                                    T + detect_time_added + 1]:
                                            if flag_item == next_time_flag_item:
                                                courier2_next_stop_order_loc_id = next_time_flag_item[0]
                                                break
                                    detect_time_added += 1
                                if courier2_next_stop_order_loc_id == -1:
                                    # 都是快送完的单
                                    for flag_item in \
                                            online_couriers[online_courier_count_y].route_flag_to_be_updated[
                                                T + 1]:
                                        if flag_item[1] != 2:
                                            courier2_next_stop_order_loc_id = flag_item[0]
                                            break
                                    if courier2_next_stop_order_loc_id == -1:
                                        print('debug')
                            else:
                                courier2_next_stop_order_loc_id = \
                                    online_couriers[online_courier_count_y].route_flag_to_be_updated[T + 1][0][0]

                            if courier2_next_stop_order_loc_id > len(
                                    online_couriers[online_courier_count_y].available_loc_real_time):
                                print('debug')
                            if online_couriers[online_courier_count_y].available_loc_real_time[
                                courier2_next_stop_order_loc_id] == 0:
                                # 该单下一时刻送完了
                                encounter_start_courier2_next_stop_lat = online_couriers[online_courier_count_y].lat
                                encounter_start_courier2_next_stop_lon = online_couriers[online_courier_count_y].lon
                                encounter_courier2_cur_order_cur_stage_remaining_time = 1
                            else:
                                # encounter_start_courier2_next_stop_lat = \
                                #     online_couriers[online_courier_count_y].available_loc_real_time[
                                #         online_couriers[online_courier_count_y].route_flag_to_be_updated[T + 1][0][
                                #             0]].lat
                                # encounter_start_courier2_next_stop_lon = \
                                #     online_couriers[online_courier_count_y].available_loc_real_time[
                                #         online_couriers[online_courier_count_y].route_flag_to_be_updated[T + 1][0][
                                #             0]].lon
                                encounter_start_courier2_next_stop_lat = \
                                    online_couriers[online_courier_count_y].available_loc_real_time[
                                        courier2_next_stop_order_loc_id].lat
                                encounter_start_courier2_next_stop_lon = \
                                    online_couriers[online_courier_count_y].available_loc_real_time[
                                        courier2_next_stop_order_loc_id].lon

                                cur_order_id_in_courier_order_list = \
                                    online_couriers[online_courier_count_y].route_flag_to_be_updated[T + 1][0][0]
                                cur_order_stage_in_courier_order_list = \
                                    online_couriers[online_courier_count_y].route_flag_to_be_updated[T + 1][0][1]
                                objective_order_flag = -1
                                if cur_order_stage_in_courier_order_list == 1:
                                    objective_order_flag = 2
                                else:
                                    objective_order_flag = 0

                                objective_route_flag_item = (cur_order_id_in_courier_order_list, objective_order_flag)

                                cur_time = T + 1
                                order_next_step_need_time = 0
                                while cur_time > T:
                                    route_flag_item = online_couriers[online_courier_count_y].route_flag_to_be_updated[
                                        cur_time]
                                    if objective_route_flag_item in route_flag_item:
                                        order_next_step_need_time = cur_time
                                        break
                                    cur_time += 1
                                if order_next_step_need_time == 0:
                                    print('debug')
                                encounter_courier2_cur_order_cur_stage_remaining_time = order_next_step_need_time - T

                        # courier-order state_input preprocess
                        courier1_max_order_remaining_time = 0  # estimated deliver time - cur time
                        # courier1_max_order_promise_remaining_time = 0  # promise_deliver time - current time
                        courier1_min_real_time_promise_variance_order_remaining_time = 9999999999  # 越小越好
                        courier1_order_num = online_couriers[online_courier_count_x].cur_order_num
                        if courier1_order_num > 0:
                            for order_item_id in range(len(online_couriers[online_courier_count_x].order_list)):

                                if online_couriers[online_courier_count_x].order_list[
                                    order_item_id].dispatch_stage != 0:
                                    cur_order_promise_remaining_time = \
                                        online_couriers[online_courier_count_x].order_list[
                                            order_item_id].promise_deliver_time - T
                                    order_item_cost_left_time = -9999
                                    if online_couriers[online_courier_count_x].route_flag_to_be_updated == {}:
                                        order_item_cost_left_time = 0
                                    elif max(online_couriers[
                                                 online_courier_count_x].route_flag_to_be_updated.keys()) <= T:
                                        order_item_cost_left_time = 0
                                    else:
                                        for time_step_id in range(T, max(
                                                online_couriers[
                                                    online_courier_count_x].route_flag_to_be_updated.keys()) + 1):
                                            for state_change_id in range(
                                                    len(online_couriers[
                                                            online_courier_count_x].route_flag_to_be_updated[
                                                            time_step_id])):
                                                if online_couriers[
                                                    online_courier_count_x].route_flag_to_be_updated[
                                                    time_step_id][
                                                    state_change_id] == (
                                                        order_item_id, 0):
                                                    order_item_cost_left_time = time_step_id - T
                                                    break

                                    if order_item_cost_left_time == -9999:
                                        print('debug')

                                    if courier1_min_real_time_promise_variance_order_remaining_time > \
                                            cur_order_promise_remaining_time - order_item_cost_left_time:
                                        courier1_min_real_time_promise_variance_order_remaining_time = \
                                            cur_order_promise_remaining_time - order_item_cost_left_time
                                    if courier1_max_order_remaining_time < order_item_cost_left_time:
                                        courier1_max_order_remaining_time = order_item_cost_left_time
                        else:
                            courier1_min_real_time_promise_variance_order_remaining_time = 0

                        courier2_max_order_remaining_time = 0  # estimated deliver time - cur time
                        # courier2_max_order_promise_remaining_time = 0  # promise_deliver time - current time
                        courier2_min_real_time_promise_variance_order_remaining_time = 9999999999  # 越小越好
                        courier2_order_num = online_couriers[online_courier_count_y].cur_order_num
                        if courier2_order_num > 0:
                            for order_item_id in range(len(online_couriers[online_courier_count_y].order_list)):
                                if online_couriers[online_courier_count_y].order_list[
                                    order_item_id].dispatch_stage != 0:
                                    cur_order_promise_remaining_time = \
                                        online_couriers[online_courier_count_y].order_list[
                                            order_item_id].promise_deliver_time - T
                                    order_item_cost_left_time = -9999
                                    if online_couriers[online_courier_count_y].route_flag_to_be_updated == {}:
                                        order_item_cost_left_time = 0
                                    elif max(online_couriers[
                                                 online_courier_count_y].route_flag_to_be_updated.keys()) <= T:
                                        order_item_cost_left_time = 0
                                    else:
                                        for time_step_id in range(T, max(
                                                online_couriers[
                                                    online_courier_count_y].route_flag_to_be_updated.keys()) + 1):
                                            for state_change_id in range(
                                                    len(online_couriers[
                                                            online_courier_count_y].route_flag_to_be_updated[
                                                            time_step_id])):
                                                if \
                                                        online_couriers[
                                                            online_courier_count_y].route_flag_to_be_updated[
                                                            time_step_id][
                                                            state_change_id] == (
                                                                order_item_id, 0):
                                                    order_item_cost_left_time = time_step_id - T
                                                    break

                                    if order_item_cost_left_time == -9999:
                                        print('debug')
                                    if courier2_min_real_time_promise_variance_order_remaining_time > \
                                            cur_order_promise_remaining_time - order_item_cost_left_time:
                                        courier2_min_real_time_promise_variance_order_remaining_time = \
                                            cur_order_promise_remaining_time - order_item_cost_left_time
                                    if courier2_max_order_remaining_time < order_item_cost_left_time:
                                        courier2_max_order_remaining_time = order_item_cost_left_time
                        else:
                            courier2_min_real_time_promise_variance_order_remaining_time = 0

                        # courier-order whole similarity preprocess
                        courier1_self_order_similarity = 0
                        courier1_self_order_similarity_list = []
                        courier1_courier2_order_similarity = 0
                        courier1_courier2_order_similarity_list = []

                        courier2_self_order_similarity = 0
                        courier2_self_order_similarity_list = []
                        courier2_courier1_order_similarity = 0
                        courier2_courier1_order_similarity_list = []

                        courier1_order_next_stop_list = []
                        for courier1_order_item in range(len(online_couriers[online_courier_count_x].order_list)):
                            if online_couriers[online_courier_count_x].order_list[
                                courier1_order_item].dispatch_stage != 0:
                                if online_couriers[online_courier_count_x].order_list[
                                    courier1_order_item].dispatch_stage == 1:
                                    courier1_order_next_stop_list.append(Loc(
                                        online_couriers[online_courier_count_x].order_list[
                                            courier1_order_item].shop_latitude,
                                        online_couriers[online_courier_count_x].order_list[
                                            courier1_order_item].shop_longitude))
                                elif online_couriers[online_courier_count_x].order_list[
                                    courier1_order_item].dispatch_stage == 2:
                                    courier1_order_next_stop_list.append(Loc(
                                        online_couriers[online_courier_count_x].order_list[
                                            courier1_order_item].user_latitude,
                                        online_couriers[online_courier_count_x].order_list[
                                            courier1_order_item].user_longitude))
                        courier2_order_next_stop_list = []
                        for courier2_order_item in range(len(online_couriers[online_courier_count_y].order_list)):
                            if online_couriers[online_courier_count_y].order_list[
                                courier2_order_item].dispatch_stage != 0:
                                if online_couriers[online_courier_count_y].order_list[
                                    courier2_order_item].dispatch_stage == 1:
                                    courier2_order_next_stop_list.append(Loc(
                                        online_couriers[online_courier_count_y].order_list[
                                            courier2_order_item].shop_latitude,
                                        online_couriers[online_courier_count_y].order_list[
                                            courier2_order_item].shop_longitude))
                                elif online_couriers[online_courier_count_y].order_list[
                                    courier2_order_item].dispatch_stage == 2:
                                    courier2_order_next_stop_list.append(Loc(
                                        online_couriers[online_courier_count_y].order_list[
                                            courier2_order_item].user_latitude,
                                        online_couriers[online_courier_count_y].order_list[
                                            courier2_order_item].user_longitude))

                        if courier1_order_num > 1:
                            for courier1_compute_similarity_id1 in range(0, len(courier1_order_next_stop_list)):
                                for courier1_compute_similarity_id2 in range(courier1_compute_similarity_id1 + 1,
                                                                             len(courier1_order_next_stop_list)):
                                    cur_simi = 0
                                    cur_order_next_stop_lat = courier1_order_next_stop_list[
                                        courier1_compute_similarity_id1].lat
                                    cur_order_next_stop_lon = courier1_order_next_stop_list[
                                        courier1_compute_similarity_id1].lon
                                    cur_order_cur_lat = encounter_start_courier1_lat
                                    cur_order_cur_lon = encounter_start_courier1_lon
                                    this_order_next_stop_lat = courier1_order_next_stop_list[
                                        courier1_compute_similarity_id2].lat
                                    this_order_next_stop_lon = courier1_order_next_stop_list[
                                        courier1_compute_similarity_id2].lon
                                    this_order_cur_lat = encounter_start_courier1_lat
                                    this_order_cur_lon = encounter_start_courier1_lon
                                    if (
                                            cur_order_next_stop_lat - cur_order_cur_lat == 0 and cur_order_next_stop_lon - cur_order_cur_lon == 0) or \
                                            (
                                                    this_order_next_stop_lat - this_order_cur_lat == 0 and this_order_next_stop_lon - this_order_cur_lon == 0):
                                        cur_simi = 0
                                    else:
                                        cur_simi = cosine_dis(np.array([cur_order_next_stop_lat - cur_order_cur_lat,
                                                                        cur_order_next_stop_lon - cur_order_cur_lon]),
                                                              np.array(
                                                                  [this_order_next_stop_lat - this_order_cur_lat,
                                                                   this_order_next_stop_lon - this_order_cur_lon]))
                                    courier1_self_order_similarity_list.append(cur_simi)
                            courier1_self_order_similarity = np.sum(courier1_self_order_similarity_list) / len(
                                courier1_self_order_similarity_list)
                        else:
                            courier1_self_order_similarity = 0

                        if courier1_order_num > 0 and courier2_order_num > 0:
                            for courier1_courier2_compute_similarity_c1 in range(len(courier1_order_next_stop_list)):
                                cur_order_exchange_simi = []
                                for courier1_courier2_compute_similarity_c2 in range(
                                        len(courier2_order_next_stop_list)):
                                    cur_simi = 0
                                    cur_order_next_stop_lat = courier1_order_next_stop_list[
                                        courier1_courier2_compute_similarity_c1].lat
                                    cur_order_next_stop_lon = courier1_order_next_stop_list[
                                        courier1_courier2_compute_similarity_c1].lon
                                    cur_order_cur_lat = encounter_start_courier1_lat
                                    cur_order_cur_lon = encounter_start_courier1_lon
                                    this_order_next_stop_lat = courier2_order_next_stop_list[
                                        courier1_courier2_compute_similarity_c2].lat
                                    this_order_next_stop_lon = courier2_order_next_stop_list[
                                        courier1_courier2_compute_similarity_c2].lon
                                    this_order_cur_lat = encounter_start_courier2_lat
                                    this_order_cur_lon = encounter_start_courier2_lon
                                    if (
                                            cur_order_next_stop_lat - cur_order_cur_lat == 0 and cur_order_next_stop_lon - cur_order_cur_lon == 0) or \
                                            (
                                                    this_order_next_stop_lat - this_order_cur_lat == 0 and this_order_next_stop_lon - this_order_cur_lon == 0):
                                        cur_simi = 0
                                    else:
                                        cur_simi = cosine_dis(np.array([cur_order_next_stop_lat - cur_order_cur_lat,
                                                                        cur_order_next_stop_lon - cur_order_cur_lon]),
                                                              np.array(
                                                                  [this_order_next_stop_lat - this_order_cur_lat,
                                                                   this_order_next_stop_lon - this_order_cur_lon]))
                                    cur_order_exchange_simi.append(cur_simi)
                                courier1_courier2_order_similarity_list.append(
                                    np.sum(cur_order_exchange_simi) / len(cur_order_exchange_simi))
                            courier1_courier2_order_similarity = np.sum(courier1_courier2_order_similarity_list) / len(
                                courier1_courier2_order_similarity_list)
                        else:
                            courier1_courier2_order_similarity = 0

                        # 骑手2 相关的 相似度计算
                        if courier2_order_num > 1:
                            for courier2_compute_similarity_id1 in range(0, len(courier2_order_next_stop_list)):
                                for courier2_compute_similarity_id2 in range(courier2_compute_similarity_id1 + 1,
                                                                             len(courier2_order_next_stop_list)):
                                    cur_simi = 0
                                    cur_order_next_stop_lat = courier2_order_next_stop_list[
                                        courier2_compute_similarity_id1].lat
                                    cur_order_next_stop_lon = courier2_order_next_stop_list[
                                        courier2_compute_similarity_id1].lon
                                    cur_order_cur_lat = encounter_start_courier2_lat
                                    cur_order_cur_lon = encounter_start_courier2_lon
                                    this_order_next_stop_lat = courier2_order_next_stop_list[
                                        courier2_compute_similarity_id2].lat
                                    this_order_next_stop_lon = courier2_order_next_stop_list[
                                        courier2_compute_similarity_id2].lon
                                    this_order_cur_lat = encounter_start_courier2_lat
                                    this_order_cur_lon = encounter_start_courier2_lon
                                    if (
                                            cur_order_next_stop_lat - cur_order_cur_lat == 0 and cur_order_next_stop_lon - cur_order_cur_lon == 0) or \
                                            (
                                                    this_order_next_stop_lat - this_order_cur_lat == 0 and this_order_next_stop_lon - this_order_cur_lon == 0):
                                        cur_simi = 0
                                    else:
                                        cur_simi = cosine_dis(np.array([cur_order_next_stop_lat - cur_order_cur_lat,
                                                                        cur_order_next_stop_lon - cur_order_cur_lon]),
                                                              np.array(
                                                                  [this_order_next_stop_lat - this_order_cur_lat,
                                                                   this_order_next_stop_lon - this_order_cur_lon]))
                                    courier2_self_order_similarity_list.append(cur_simi)
                            courier2_self_order_similarity = np.sum(courier2_self_order_similarity_list) / len(
                                courier2_self_order_similarity_list)
                        else:
                            courier2_self_order_similarity = 0
                        if courier1_order_num > 0 and courier2_order_num > 0:
                            for courier2_courier1_compute_similarity_c2 in range(len(courier2_order_next_stop_list)):
                                cur_order_exchange_simi = []
                                for courier2_courier1_compute_similarity_c1 in range(
                                        len(courier1_order_next_stop_list)):
                                    cur_simi = 0
                                    cur_order_next_stop_lat = courier2_order_next_stop_list[
                                        courier2_courier1_compute_similarity_c2].lat
                                    cur_order_next_stop_lon = courier2_order_next_stop_list[
                                        courier2_courier1_compute_similarity_c2].lon
                                    cur_order_cur_lat = encounter_start_courier2_lat
                                    cur_order_cur_lon = encounter_start_courier2_lon
                                    this_order_next_stop_lat = courier1_order_next_stop_list[
                                        courier2_courier1_compute_similarity_c1].lat
                                    this_order_next_stop_lon = courier1_order_next_stop_list[
                                        courier2_courier1_compute_similarity_c1].lon
                                    this_order_cur_lat = encounter_start_courier1_lat
                                    this_order_cur_lon = encounter_start_courier1_lon
                                    if (
                                            cur_order_next_stop_lat - cur_order_cur_lat == 0 and cur_order_next_stop_lon - cur_order_cur_lon == 0) or \
                                            (
                                                    this_order_next_stop_lat - this_order_cur_lat == 0 and this_order_next_stop_lon - this_order_cur_lon == 0):
                                        cur_simi = 0
                                    else:
                                        cur_simi = cosine_dis(np.array([cur_order_next_stop_lat - cur_order_cur_lat,
                                                                        cur_order_next_stop_lon - cur_order_cur_lon]),
                                                              np.array(
                                                                  [this_order_next_stop_lat - this_order_cur_lat,
                                                                   this_order_next_stop_lon - this_order_cur_lon]))
                                    cur_order_exchange_simi.append(cur_simi)
                                courier2_courier1_order_similarity_list.append(
                                    np.sum(cur_order_exchange_simi) / len(cur_order_exchange_simi))
                            courier2_courier1_order_similarity = np.sum(courier2_courier1_order_similarity_list) / len(
                                courier2_courier1_order_similarity_list)
                        else:
                            courier2_courier1_order_similarity = 0

                        # two_couriers_exchange_order_similarity = (courier1_courier2_order_similarity +
                        #                                           courier2_courier1_order_similarity) / 2
                        encounter_courier_rssi = []
                        for time_id in range(T-30*3,T+30,30):
                            print(T)
                            print(time_id)
                            if time_id in online_couriers[online_courier_count_x].route_time_step.keys():
                                courier1_encounter_history_time_lat = online_couriers[online_courier_count_x].route_time_step[time_id].lat
                                courier1_encounter_history_time_lon = online_couriers[online_courier_count_x].route_time_step[time_id].lon
                            else:
                                courier1_encounter_history_time_lat = online_couriers[online_courier_count_x].lat
                                courier1_encounter_history_time_lon = online_couriers[online_courier_count_x].lon

                            if time_id in online_couriers[online_courier_count_y].route_time_step.keys():
                                courier2_encounter_history_time_lat = online_couriers[online_courier_count_y].route_time_step[time_id].lat
                                courier2_encounter_history_time_lon = online_couriers[online_courier_count_y].route_time_step[time_id].lon
                            else:
                                courier2_encounter_history_time_lat = online_couriers[online_courier_count_y].lat
                                courier2_encounter_history_time_lon = online_couriers[online_courier_count_y].lon

                            temp_distance = get_distance_hav(courier1_encounter_history_time_lat,
                                                             courier1_encounter_history_time_lon,
                                                             courier2_encounter_history_time_lat,
                                                             courier2_encounter_history_time_lon)
                            # temp_distance = get_distance_hav(online_couriers[online_courier_count_x].route_time_step[time_id].lat,
                            #                                  online_couriers[online_courier_count_x].route_time_step[time_id].lon,
                            #                                  online_couriers[online_courier_count_y].route_time_step[time_id].lat,
                            #                                  online_couriers[online_courier_count_y].route_time_step[time_id].lon)
                            # rssi = - (55 + 4 * 10 * math.log10(temp_distance*1000))
                            encounter_courier_rssi.append(temp_distance)
                            # distance = np.power(10, abs(rssi + 55) / (4 * 10))
                            # 这里环境因子取值为4，tx_power取值为55

                        high_level_state_input = [
                            encounter_start_time/3600,  # encounter:11个state
                            encounter_start_courier1_lat,
                            encounter_start_courier1_lon,
                            encounter_start_courier2_lat,
                            encounter_start_courier2_lon,
                            encounter_start_courier1_next_stop_lat,
                            encounter_start_courier1_next_stop_lon,
                            encounter_start_courier2_next_stop_lat,
                            encounter_start_courier2_next_stop_lon,
                            encounter_courier1_cur_order_cur_stage_remaining_time/60,
                            encounter_courier2_cur_order_cur_stage_remaining_time/60,
                            # order-state: 8 个
                            courier1_max_order_remaining_time/60,
                            courier1_min_real_time_promise_variance_order_remaining_time/60,
                            courier1_order_num,
                            courier1_self_order_similarity,
                            courier1_courier2_order_similarity,
                            courier2_max_order_remaining_time/60,
                            courier2_min_real_time_promise_variance_order_remaining_time/60,
                            courier2_order_num,
                            courier2_self_order_similarity,
                            courier2_courier1_order_similarity,
                            encounter_courier_rssi[0],
                            encounter_courier_rssi[1],
                            encounter_courier_rssi[2],
                            encounter_courier_rssi[3],

                        ]





                        h_network_output = hierachical_actor.choose_action(
                            np.array(high_level_state_input))  # 0 不换，1 换
                        print('high_level_state_input', high_level_state_input, ',action:',h_network_output)

                        courier_encounter_event = Encounter(online_couriers[online_courier_count_x].courier_id,
                                                            online_couriers[online_courier_count_y].courier_id,
                                                            T)
                        env.encounter_exchange_event.append(courier_encounter_event)

                        if online_couriers[online_courier_count_x].route_flag_to_be_updated == {}:
                            raw_encounter_courier1_all_order_deliver_cost_time = 0
                        elif max(online_couriers[online_courier_count_x].route_flag_to_be_updated.keys()) <= T:
                            raw_encounter_courier1_all_order_deliver_cost_time = 0
                        else:
                            raw_encounter_courier1_all_order_deliver_cost_time = max(
                                online_couriers[online_courier_count_x].route_flag_to_be_updated.keys()) - T

                        if online_couriers[online_courier_count_y].route_flag_to_be_updated == {}:
                            raw_encounter_courier2_all_order_deliver_cost_time = 0
                        elif max(online_couriers[online_courier_count_y].route_flag_to_be_updated.keys()) <= T:
                            raw_encounter_courier2_all_order_deliver_cost_time = 0
                        else:
                            raw_encounter_courier2_all_order_deliver_cost_time = max(
                                online_couriers[online_courier_count_y].route_flag_to_be_updated.keys()) - T

                        high_level_next_s = []

                        high_level_reward = 1
                        # 供低层订单作决策
                        # cur_time_step_encounter_events.append(courier_encounter_event)
                        #
                        # if h_network_output == 1:
                        #     cur_time_step_exchange_events.append(courier_encounter_event)
                        #     cur_time_step_exchange_events_state_input.append(high_level_state_input)
                        #
                        # # 供高层骑手作决策
                        # cur_time_step_encounter_event_state_input.append(high_level_state_input)
                        # cur_time_step_encounter_event_action.append(h_network_output)
                        encounter_two_couriers = [
                            online_couriers[online_courier_count_x],
                            online_couriers[online_courier_count_y]]
                        encounter_to_exchange_order_list = []  # 要筛选掉已送完的订单
                        encounter_order_next_stop_location = []
                        to_exchange_order_raw_courier_id_list = []
                        if encounter_two_couriers[0].cur_order_num > encounter_two_couriers[1].cur_order_num:
                            for encounter_order1_id in range(len(encounter_two_couriers[0].order_list)):
                                if encounter_two_couriers[0].order_list[
                                    encounter_order1_id].dispatch_stage != 0:
                                    encounter_to_exchange_order_list.append(
                                        encounter_two_couriers[0].order_list[encounter_order1_id])
                                    encounter_order_next_stop_location.append(
                                        encounter_two_couriers[0].available_loc_real_time[encounter_order1_id])
                                    to_exchange_order_raw_courier_id_list.append(0)
                                    # to_exchange_order_raw_courier_cost_left_time.append(list(encounter_two_couriers[0].route_flag_to_be_updated.keys())[
                                    #                                                         list(encounter_two_couriers[0].route_flag_to_be_updated.values()).index((encounter_order1_id,0))] - T)
                            for encounter_order2_id in range(len(encounter_two_couriers[1].order_list)):
                                if encounter_two_couriers[1].order_list[
                                    encounter_order2_id].dispatch_stage != 0:
                                    encounter_to_exchange_order_list.append(
                                        encounter_two_couriers[1].order_list[encounter_order2_id])
                                    encounter_order_next_stop_location.append(
                                        encounter_two_couriers[1].available_loc_real_time[encounter_order2_id])
                                    to_exchange_order_raw_courier_id_list.append(1)
                                    # to_exchange_order_raw_courier_cost_left_time.append(list(encounter_two_couriers[1].route_flag_to_be_updated.keys())[
                                    #                                                         list(encounter_two_couriers[1].route_flag_to_be_updated.values()).index((encounter_order2_id,0))] -T)
                        else:
                            for encounter_order2_id in range(len(encounter_two_couriers[1].order_list)):
                                if encounter_two_couriers[1].order_list[
                                    encounter_order2_id].dispatch_stage != 0:
                                    encounter_to_exchange_order_list.append(
                                        encounter_two_couriers[1].order_list[encounter_order2_id])
                                    encounter_order_next_stop_location.append(
                                        encounter_two_couriers[1].available_loc_real_time[encounter_order2_id])
                                    to_exchange_order_raw_courier_id_list.append(1)
                            for encounter_order1_id in range(len(encounter_two_couriers[0].order_list)):
                                if encounter_two_couriers[0].order_list[
                                    encounter_order1_id].dispatch_stage != 0:
                                    encounter_to_exchange_order_list.append(
                                        encounter_two_couriers[0].order_list[encounter_order1_id])
                                    encounter_order_next_stop_location.append(
                                        encounter_two_couriers[0].available_loc_real_time[encounter_order1_id])
                                    to_exchange_order_raw_courier_id_list.append(0)
                        if len(encounter_to_exchange_order_list) == 0:
                            continue
                        # low-level decision
                        raw_revenue_list = []
                        raw_order_dispatch_time_list = []
                        for encounter_order_id in range(len(encounter_to_exchange_order_list)):
                            #  换了单之后会影响后面订单还需的配送时间，求当前订单要送完所需的时间
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
                                                len(encounter_two_couriers[0].route_flag_to_be_updated[
                                                        time_step_id])):
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

                                        for change_state_id1 in range(
                                                len(encounter_two_couriers[1].route_flag_to_be_updated[
                                                        time_step_id])):
                                            if encounter_two_couriers[1].route_flag_to_be_updated[time_step_id][
                                                change_state_id1] == (
                                                    cur_this_order_loc_id, 0):
                                                to_exchange_order_raw_courier_cost_left_time = time_step_id - T
                                                break

                            if to_exchange_order_raw_courier_cost_left_time == -9999:
                                print('debug')
                            # print('high_level_time:',to_exchange_order_raw_courier_cost_left_time)
                            raw_order_dispatch_time_list.append(to_exchange_order_raw_courier_cost_left_time / 60)
                            order_price = encounter_to_exchange_order_list[encounter_order_id].order_price
                            promise_order_time = encounter_to_exchange_order_list[
                                encounter_order_id].promise_deliver_time
                            # exchange_deliver_time_overdue_condition = exchange_order_dispatch_time + courier1_courier2_time - promise_order_time
                            raw_deliver_time_overdue_condition = to_exchange_order_raw_courier_cost_left_time - promise_order_time
                            if raw_deliver_time_overdue_condition <= 0:
                                # 没超时，全额得到订单价格
                                raw_revenue = order_price
                            else:
                                overdue_time = raw_deliver_time_overdue_condition / 60  # 超时的分钟数
                                if overdue_time <= 10:
                                    raw_revenue = 0.95 * order_price
                                elif 10 < overdue_time <= 15:
                                    raw_revenue = 0.9 * order_price
                                elif 15 < overdue_time <= 30:
                                    raw_revenue = 0.7 * order_price
                                else:
                                    raw_revenue = 0.3 * order_price
                            raw_revenue_list.append(raw_revenue)

                        if h_network_output == 1:

                            # 最多12个单，11*12个状态空间=>调整一下，当前订单所在哪个骑手就把哪个骑手的状态放在前面
                            buhuan_count = 0
                            # raw_order_dispatch_time_list=[]
                            exchanged_order_dispatch_time_list = []
                            # raw_revenue_list = []
                            exchanged_revenue_list = []
                            exchanged_order_raw_courier_id_list = to_exchange_order_raw_courier_id_list

                            courier1_huandan_time_lat = 0
                            courier1_huandan_time_lon = 0
                            courier2_huandan_time_lat = 0
                            courier2_huandan_time_lon = 0
                            if T + 30 in encounter_two_couriers[0].route_time_step.keys():
                                courier1_huandan_time_lat = encounter_two_couriers[0].route_time_step[
                                    T + 30].lat
                                courier1_huandan_time_lon = encounter_two_couriers[0].route_time_step[
                                    T + 30].lon
                            else:
                                courier1_huandan_time_lat = encounter_two_couriers[0].lat
                                courier1_huandan_time_lon = encounter_two_couriers[0].lon

                            if T + 30 in encounter_two_couriers[1].route_time_step.keys():
                                courier2_huandan_time_lat = encounter_two_couriers[1].route_time_step[
                                    T + 30].lat
                                courier2_huandan_time_lon = encounter_two_couriers[1].route_time_step[
                                    T + 30].lon
                            else:
                                courier2_huandan_time_lat = encounter_two_couriers[1].lat
                                courier2_huandan_time_lon = encounter_two_couriers[1].lon

                            for encounter_order_id in range(len(encounter_to_exchange_order_list)):
                                if encounter_to_exchange_order_list[encounter_order_id].hop_num > 1:
                                    continue
                                # 骑手的下一站位置的经纬度
                                if T + 1 not in encounter_two_couriers[0].route_flag_to_be_updated.keys() or \
                                        encounter_two_couriers[0].cur_order_num == 0 or len(
                                    encounter_two_couriers[0].route_flag_to_be_updated[T + 1]) == 0:
                                    courier1_next_stop_location_lat = encounter_two_couriers[0].lat
                                    courier1_next_stop_location_lon = encounter_two_couriers[0].lon
                                else:
                                    if len(encounter_two_couriers[0].route_flag_to_be_updated[T + 1]) > 1 and \
                                            encounter_two_couriers[0].route_flag_to_be_updated[T + 2] != []:
                                        courier1_next_stop_order_loc_id = -1
                                        detect_time_added = 1
                                        while courier1_next_stop_order_loc_id == -1 and \
                                                encounter_two_couriers[0].route_flag_to_be_updated[
                                                    T + detect_time_added + 1] != []:
                                            for flag_item in encounter_two_couriers[0].route_flag_to_be_updated[
                                                T + detect_time_added]:
                                                for next_time_flag_item in \
                                                        encounter_two_couriers[0].route_flag_to_be_updated[
                                                            T + detect_time_added + 1]:
                                                    if flag_item == next_time_flag_item:
                                                        courier1_next_stop_order_loc_id = next_time_flag_item[0]
                                                        break
                                            detect_time_added += 1

                                        if courier1_next_stop_order_loc_id == -1:
                                            for flag_item in encounter_two_couriers[0].route_flag_to_be_updated[T + 1]:
                                                if flag_item[1] != 2:
                                                    courier1_next_stop_order_loc_id = flag_item[0]
                                                    break
                                            if courier1_next_stop_order_loc_id == -1:
                                                print('debug')
                                    else:
                                        courier1_next_stop_order_loc_id = \
                                            encounter_two_couriers[0].route_flag_to_be_updated[T + 1][0][0]

                                    if encounter_two_couriers[0].available_loc_real_time[
                                        courier1_next_stop_order_loc_id] == 0:
                                        courier1_next_stop_location_lat = encounter_two_couriers[0].lat
                                        courier1_next_stop_location_lon = encounter_two_couriers[0].lon
                                    else:
                                        courier1_next_stop_location_lat = \
                                            encounter_two_couriers[0].available_loc_real_time[
                                                courier1_next_stop_order_loc_id].lat
                                        courier1_next_stop_location_lon = \
                                            encounter_two_couriers[0].available_loc_real_time[
                                                courier1_next_stop_order_loc_id].lon

                                if T + 1 not in encounter_two_couriers[1].route_flag_to_be_updated.keys() or \
                                        encounter_two_couriers[1].cur_order_num == 0 or len(
                                    encounter_two_couriers[1].route_flag_to_be_updated[T + 1]) == 0:
                                    courier2_next_stop_location_lat = encounter_two_couriers[1].lat
                                    courier2_next_stop_location_lon = encounter_two_couriers[1].lon
                                else:
                                    if len(encounter_two_couriers[1].route_flag_to_be_updated[T + 1]) > 1 and \
                                            encounter_two_couriers[1].route_flag_to_be_updated[T + 2] != []:
                                        courier2_next_stop_order_loc_id = -1
                                        detect_time_added = 1
                                        while courier2_next_stop_order_loc_id == -1 and \
                                                encounter_two_couriers[1].route_flag_to_be_updated[
                                                    T + detect_time_added + 1] != []:
                                            for flag_item in encounter_two_couriers[1].route_flag_to_be_updated[
                                                T + detect_time_added]:
                                                for next_time_flag_item in \
                                                        encounter_two_couriers[1].route_flag_to_be_updated[
                                                            T + detect_time_added + 1]:
                                                    if flag_item == next_time_flag_item:
                                                        courier2_next_stop_order_loc_id = next_time_flag_item[0]
                                                        break
                                            detect_time_added += 1

                                        if courier2_next_stop_order_loc_id == -1:
                                            for flag_item in encounter_two_couriers[1].route_flag_to_be_updated[T + 1]:
                                                if flag_item[1] != 2:
                                                    courier2_next_stop_order_loc_id = flag_item[0]
                                                    break
                                            if courier2_next_stop_order_loc_id == -1:
                                                print('debug')
                                    else:
                                        courier2_next_stop_order_loc_id = \
                                            encounter_two_couriers[1].route_flag_to_be_updated[T + 1][0][0]

                                    if encounter_two_couriers[1].available_loc_real_time[
                                        courier2_next_stop_order_loc_id] == 0:
                                        courier2_next_stop_location_lat = encounter_two_couriers[1].lat
                                        courier2_next_stop_location_lon = encounter_two_couriers[1].lon
                                    else:
                                        courier2_next_stop_location_lat = \
                                            encounter_two_couriers[1].available_loc_real_time[
                                                courier2_next_stop_order_loc_id].lat
                                        courier2_next_stop_location_lon = \
                                            encounter_two_couriers[1].available_loc_real_time[
                                                courier2_next_stop_order_loc_id].lon
                                        # courier2_next_stop_location_lat = \
                                        #     encounter_two_couriers[1].available_loc_real_time[
                                        #         encounter_two_couriers[1].route_flag_to_be_updated[T + 1][0][0]].lat
                                        # courier2_next_stop_location_lon = \
                                        #     encounter_two_couriers[1].available_loc_real_time[
                                        #         encounter_two_couriers[1].route_flag_to_be_updated[T + 1][0][0]].lon
                                order_similarity = 0
                                order_similarity2 = 0
                                if encounter_to_exchange_order_list[encounter_order_id].dispatch_stage == 1:
                                    cur_order_next_stop_lon = encounter_to_exchange_order_list[
                                        encounter_order_id].shop_longitude
                                    cur_order_next_stop_lat = encounter_to_exchange_order_list[
                                        encounter_order_id].shop_latitude
                                elif encounter_to_exchange_order_list[encounter_order_id].dispatch_stage == 2:
                                    cur_order_next_stop_lon = encounter_to_exchange_order_list[
                                        encounter_order_id].user_longitude
                                    cur_order_next_stop_lat = encounter_to_exchange_order_list[
                                        encounter_order_id].user_latitude
                                else:
                                    continue

                                #  换了单之后会影响后面订单还需的配送时间，求当前订单要送完所需的时间
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
                                                    len(encounter_two_couriers[0].route_flag_to_be_updated[
                                                            time_step_id])):
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

                                            for change_state_id1 in range(
                                                    len(encounter_two_couriers[1].route_flag_to_be_updated[
                                                            time_step_id])):
                                                if encounter_two_couriers[1].route_flag_to_be_updated[time_step_id][
                                                    change_state_id1] == (
                                                        cur_this_order_loc_id, 0):
                                                    to_exchange_order_raw_courier_cost_left_time = time_step_id - T
                                                    break

                                if to_exchange_order_raw_courier_cost_left_time == -9999:
                                    print('debug')

                                if to_exchange_order_raw_courier_cost_left_time <= 1200:
                                    continue

                                raw_courier_id = to_exchange_order_raw_courier_id_list[encounter_order_id]

                                cur_order_cur_lat = encounter_two_couriers[raw_courier_id].lat
                                cur_order_cur_lon = encounter_two_couriers[raw_courier_id].lon

                                # 订单相似度定义：与当前订单顺路的顺路单数
                                # 与骑手1持有的的所有订单相似度，计数>0.8的个数
                                courier1_shunludan_num = 0
                                courier1_cur_order_num = 0
                                for shunludan_id in range(len(encounter_two_couriers[0].order_list)):
                                    if encounter_two_couriers[0].order_list[shunludan_id].dispatch_stage != 0:
                                        courier1_cur_order_num += 1
                                        if encounter_two_couriers[0].order_list[shunludan_id].order_id == \
                                                encounter_to_exchange_order_list[encounter_order_id].order_id:
                                            continue
                                        this_order_cur_lon = encounter_two_couriers[0].lon
                                        this_order_cur_lat = encounter_two_couriers[0].lat
                                        if encounter_two_couriers[0].order_list[shunludan_id].dispatch_stage == 1:
                                            this_order_next_stop_lon = encounter_two_couriers[0].order_list[
                                                shunludan_id].shop_longitude
                                            this_order_next_stop_lat = encounter_two_couriers[0].order_list[
                                                shunludan_id].shop_latitude
                                        elif encounter_two_couriers[0].order_list[shunludan_id].dispatch_stage == 2:
                                            this_order_next_stop_lon = encounter_two_couriers[0].order_list[
                                                shunludan_id].user_longitude
                                            this_order_next_stop_lat = encounter_two_couriers[0].order_list[
                                                shunludan_id].user_latitude
                                        # 计算相似度
                                        #     order_similarity = cosine_dis(np.array([cur_order_cur_lat, cur_order_cur_lon,
                                        #                                             cur_order_next_stop_lat, cur_order_next_stop_lon]),
                                        #                                   np.array([this_order_cur_lat, this_order_cur_lon,
                                        #                                             this_order_next_stop_lat, this_order_next_stop_lon]))
                                        if (
                                                cur_order_next_stop_lat - cur_order_cur_lat == 0 and cur_order_next_stop_lon - cur_order_cur_lon == 0) or \
                                                (
                                                        this_order_next_stop_lat - this_order_cur_lat == 0 and this_order_next_stop_lon - this_order_cur_lon == 0):
                                            order_similarity = 0
                                        else:
                                            order_similarity = cosine_dis(
                                                np.array([cur_order_next_stop_lat - cur_order_cur_lat,
                                                          cur_order_next_stop_lon - cur_order_cur_lon]),
                                                np.array([this_order_next_stop_lat - this_order_cur_lat,
                                                          this_order_next_stop_lon - this_order_cur_lon]))
                                        if order_similarity > 0:
                                            courier1_shunludan_num += 1

                                # 骑手2的订单相似度
                                courier2_shunludan_num = 0
                                courier2_cur_order_num = 0
                                for shunludan_id2 in range(len(encounter_two_couriers[1].order_list)):

                                    if encounter_two_couriers[1].order_list[shunludan_id2].dispatch_stage != 0:
                                        courier2_cur_order_num += 1
                                        if encounter_two_couriers[1].order_list[shunludan_id2].order_id == \
                                                encounter_to_exchange_order_list[encounter_order_id].order_id:
                                            continue
                                        this_order_cur_lon2 = encounter_two_couriers[1].lon
                                        this_order_cur_lat2 = encounter_two_couriers[1].lat
                                        if encounter_two_couriers[1].order_list[shunludan_id2].dispatch_stage == 1:
                                            this_order_next_stop_lon2 = encounter_two_couriers[1].order_list[
                                                shunludan_id2].shop_longitude
                                            this_order_next_stop_lat2 = encounter_two_couriers[1].order_list[
                                                shunludan_id2].shop_latitude
                                        elif encounter_two_couriers[1].order_list[
                                            shunludan_id2].dispatch_stage == 2:
                                            this_order_next_stop_lon2 = encounter_two_couriers[1].order_list[
                                                shunludan_id2].user_longitude
                                            this_order_next_stop_lat2 = encounter_two_couriers[1].order_list[
                                                shunludan_id2].user_latitude
                                        # 计算相似度
                                        # order_similarity2 = cosine_dis(np.array([cur_order_cur_lat, cur_order_cur_lon,
                                        #                                         cur_order_next_stop_lat,
                                        #                                         cur_order_next_stop_lon]),
                                        #                               np.array([this_order_cur_lat2, this_order_cur_lon2,
                                        #                                         this_order_next_stop_lat2,
                                        #                                         this_order_next_stop_lon2]))
                                        if (
                                                cur_order_next_stop_lat - cur_order_cur_lat == 0 and cur_order_next_stop_lon - cur_order_cur_lon == 0) or \
                                                (
                                                        this_order_next_stop_lat2 - this_order_cur_lat2 == 0 and this_order_next_stop_lon2 - this_order_cur_lon2 == 0):
                                            order_similarity2 = 0
                                        else:
                                            order_similarity2 = cosine_dis(
                                                np.array([cur_order_next_stop_lat - cur_order_cur_lat,
                                                          cur_order_next_stop_lon - cur_order_cur_lon]),
                                                np.array([this_order_next_stop_lat2 - this_order_cur_lat2,
                                                          this_order_next_stop_lon2 - this_order_cur_lon2]))
                                        if order_similarity2 > 0:
                                            courier2_shunludan_num += 1

                                # 当前骑手送完手里单还需的时间
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

                                low_level_state_input = []
                                state_input = [cur_order_next_stop_lat,
                                               cur_order_next_stop_lon,
                                               # encounter_two_couriers[raw_courier_id].lat,
                                               # encounter_two_couriers[raw_courier_id].lon,
                                               to_exchange_order_raw_courier_cost_left_time/60,
                                               courier1_next_stop_location_lat, courier1_next_stop_location_lon,
                                               get_distance_hav(cur_order_next_stop_lat, cur_order_next_stop_lon,
                                                                courier1_next_stop_location_lat,
                                                                courier1_next_stop_location_lon),
                                               encounter_two_couriers[0].cur_order_num, courier1_shunludan_num,
                                               encounter_courier1_all_order_deliver_cost_time/60,
                                               courier2_next_stop_location_lat, courier2_next_stop_location_lon,
                                               get_distance_hav(cur_order_next_stop_lat, cur_order_next_stop_lon,
                                                                courier2_next_stop_location_lat,
                                                                courier2_next_stop_location_lon),

                                               encounter_two_couriers[1].cur_order_num, courier2_shunludan_num,
                                               encounter_courier2_all_order_deliver_cost_time/60
                                               ]
                                # if raw_courier_id == 0:
                                #     state_input = [cur_order_next_stop_lat,
                                #                    cur_order_next_stop_lon,
                                #                    # encounter_two_couriers[raw_courier_id].lat,
                                #                    #            encounter_two_couriers[raw_courier_id].lon,
                                #                    to_exchange_order_raw_courier_cost_left_time / 60,
                                #                    courier1_next_stop_location_lat, courier1_next_stop_location_lon,
                                #                    encounter_two_couriers[0].cur_order_num, courier1_shunludan_num,
                                #                    encounter_courier1_all_order_deliver_cost_time / 60,
                                #                    courier2_next_stop_location_lat, courier2_next_stop_location_lon,
                                #                    encounter_two_couriers[1].cur_order_num, courier2_shunludan_num,
                                #                    encounter_courier2_all_order_deliver_cost_time / 60]
                                # else:
                                #     state_input = [cur_order_next_stop_lat,
                                #                    cur_order_next_stop_lon,
                                #                    # encounter_two_couriers[raw_courier_id].lat,
                                #                    #            encounter_two_couriers[raw_courier_id].lon,
                                #                    to_exchange_order_raw_courier_cost_left_time / 60,
                                #                    courier2_next_stop_location_lat, courier2_next_stop_location_lon,
                                #                    encounter_two_couriers[1].cur_order_num, courier2_shunludan_num,
                                #                    encounter_courier2_all_order_deliver_cost_time / 60,
                                #                    courier1_next_stop_location_lat, courier1_next_stop_location_lon,
                                #                    encounter_two_couriers[0].cur_order_num, courier1_shunludan_num,
                                #                    encounter_courier1_all_order_deliver_cost_time / 60]
                                low_level_state_input = state_input


                                if to_exchange_order_raw_courier_cost_left_time < 0:
                                    print('debug')
                                low_level_action = actor.choose_action(np.array(low_level_state_input))
                                print('low_level_state', low_level_state_input)
                                print('raw courier id:', raw_courier_id,',choose_action:',low_level_action)

                                if encounter_two_couriers[low_level_action].cur_order_num >= 6:
                                    # 该谁的还是谁的，没变化，也不用来更新换单模型
                                    continue

                                if low_level_action != to_exchange_order_raw_courier_id_list[encounter_order_id]:
                                    # 该单发生换单
                                    # to be adjusted: 要不要考虑骑手反应时间（与相遇持续时长有关）
                                    if low_level_action == 1:
                                        # 订单原骑手为骑手0
                                        # print(courier1_huandan_time_lat,
                                        # courier1_huandan_time_lon,
                                        # courier2_huandan_time_lat,
                                        # courier2_huandan_time_lon)
                                        encounter_two_couriers[1].exchange_take_order(
                                            encounter_to_exchange_order_list[encounter_order_id], T,
                                            courier1_huandan_time_lat,
                                            courier1_huandan_time_lon,
                                            courier2_huandan_time_lat,
                                            courier2_huandan_time_lon)
                                        encounter_two_couriers[0].exchange_drop_order(
                                            encounter_to_exchange_order_list[encounter_order_id], T,
                                            courier1_huandan_time_lat,
                                            courier1_huandan_time_lon,
                                            courier2_huandan_time_lat,
                                            courier2_huandan_time_lon)
                                        exchanged_order_raw_courier_id_list[encounter_order_id] = 1

                                        exchanged_order_courier_cost_left_time = -9999
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
                                            exchanged_order_courier_cost_left_time = 0
                                        elif max(encounter_two_couriers[1].route_flag_to_be_updated.keys()) <= T:
                                            exchanged_order_courier_cost_left_time = 0
                                        else:
                                            for time_step_id in range(T, max(
                                                    encounter_two_couriers[1].route_flag_to_be_updated.keys()) + 1):

                                                for change_state_id1 in range(
                                                        len(encounter_two_couriers[1].route_flag_to_be_updated[
                                                                time_step_id])):
                                                    if encounter_two_couriers[1].route_flag_to_be_updated[
                                                        time_step_id][
                                                        change_state_id1] == (
                                                            cur_this_order_loc_id, 0):
                                                        exchanged_order_courier_cost_left_time = time_step_id - T
                                                        break
                                        if exchanged_order_courier_cost_left_time == -9999:
                                            print('debug')

                                        huandan_courier_id = 1

                                    else:
                                        # 订单原骑手为骑手1
                                        # print(courier1_huandan_time_lat,
                                        #     courier1_huandan_time_lon,
                                        #     courier2_huandan_time_lat,
                                        #     courier2_huandan_time_lon)
                                        encounter_two_couriers[0].exchange_take_order(
                                            encounter_to_exchange_order_list[encounter_order_id], T,
                                            courier1_huandan_time_lat,
                                            courier1_huandan_time_lon,
                                            courier2_huandan_time_lat,
                                            courier2_huandan_time_lon)
                                        encounter_two_couriers[1].exchange_drop_order(
                                            encounter_to_exchange_order_list[encounter_order_id], T,
                                            courier1_huandan_time_lat,
                                            courier1_huandan_time_lon,
                                            courier2_huandan_time_lat,
                                            courier2_huandan_time_lon)
                                        exchanged_order_raw_courier_id_list[encounter_order_id] = 0

                                        exchanged_order_courier_cost_left_time = -9999
                                        cur_this_order_loc_id = -1
                                        for loc_id in range(len(encounter_two_couriers[0].order_list)):
                                            if encounter_to_exchange_order_list[encounter_order_id].order_id == \
                                                    encounter_two_couriers[0].order_list[loc_id].order_id:
                                                cur_this_order_loc_id = loc_id
                                                break
                                        if cur_this_order_loc_id == -1:
                                            print('problem')
                                        if encounter_two_couriers[0].route_flag_to_be_updated == {}:
                                            exchanged_order_courier_cost_left_time = 0
                                        elif max(encounter_two_couriers[0].route_flag_to_be_updated.keys()) <= T:
                                            exchanged_order_courier_cost_left_time = 0
                                        else:
                                            for time_step_id in range(T, max(
                                                    encounter_two_couriers[0].route_flag_to_be_updated.keys()) + 1):
                                                for state_change_id in range(
                                                        len(encounter_two_couriers[0].route_flag_to_be_updated[
                                                                time_step_id])):
                                                    if encounter_two_couriers[0].route_flag_to_be_updated[
                                                        time_step_id][
                                                        state_change_id] == (
                                                            cur_this_order_loc_id, 0):
                                                        exchanged_order_courier_cost_left_time = time_step_id - T
                                                        break
                                        if exchanged_order_courier_cost_left_time == -9999:
                                            print('debug')
                                        huandan_courier_id = 0

                                    if T + 1 not in encounter_two_couriers[0].route_flag_to_be_updated.keys() or \
                                            encounter_two_couriers[0].cur_order_num == 0 or len(
                                        encounter_two_couriers[0].route_flag_to_be_updated[T + 1]) == 0:
                                        courier1_next_stop_location_lat = encounter_two_couriers[0].lat
                                        courier1_next_stop_location_lon = encounter_two_couriers[0].lon
                                    else:
                                        if len(encounter_two_couriers[0].route_flag_to_be_updated[T + 1]) > 1 and \
                                                encounter_two_couriers[0].route_flag_to_be_updated[T + 2] != []:
                                            courier1_next_stop_order_loc_id = -1
                                            detect_time_added = 1
                                            while courier1_next_stop_order_loc_id == -1 and \
                                                    encounter_two_couriers[0].route_flag_to_be_updated[
                                                        T + detect_time_added + 1] != []:
                                                for flag_item in encounter_two_couriers[0].route_flag_to_be_updated[
                                                    T + detect_time_added]:
                                                    for next_time_flag_item in \
                                                            encounter_two_couriers[0].route_flag_to_be_updated[
                                                                T + detect_time_added + 1]:
                                                        if flag_item == next_time_flag_item:
                                                            courier1_next_stop_order_loc_id = next_time_flag_item[0]
                                                            break
                                                detect_time_added += 1
                                            if courier1_next_stop_order_loc_id == -1:
                                                # 都是快送完的单
                                                for flag_item in encounter_two_couriers[0].route_flag_to_be_updated[
                                                    T + 1]:
                                                    if flag_item[1] != 2:
                                                        courier1_next_stop_order_loc_id = flag_item[0]
                                                        break
                                                if courier1_next_stop_order_loc_id == -1:
                                                    print('debug')
                                        else:
                                            courier1_next_stop_order_loc_id = \
                                                encounter_two_couriers[0].route_flag_to_be_updated[T + 1][0][0]

                                        if courier1_next_stop_order_loc_id > len(
                                                encounter_two_couriers[0].available_loc_real_time):
                                            print('debug')
                                        if encounter_two_couriers[0].available_loc_real_time[
                                            courier1_next_stop_order_loc_id] == 0:
                                            # 该单下一时刻送完了
                                            courier1_next_stop_location_lat = encounter_two_couriers[0].lat
                                            courier1_next_stop_location_lon = encounter_two_couriers[0].lon
                                        else:
                                            courier1_next_stop_location_lat = \
                                            encounter_two_couriers[0].available_loc_real_time[
                                                courier1_next_stop_order_loc_id].lat
                                            courier1_next_stop_location_lon = \
                                            encounter_two_couriers[0].available_loc_real_time[
                                                courier1_next_stop_order_loc_id].lon

                                    if T + 1 not in encounter_two_couriers[1].route_flag_to_be_updated.keys() or \
                                            encounter_two_couriers[1].cur_order_num == 0 or len(
                                        encounter_two_couriers[1].route_flag_to_be_updated[T + 1]) == 0:
                                        courier2_next_stop_location_lat = encounter_two_couriers[1].lat
                                        courier2_next_stop_location_lon = encounter_two_couriers[1].lon
                                    else:
                                        if len(encounter_two_couriers[1].route_flag_to_be_updated[T + 1]) > 1 and \
                                                encounter_two_couriers[1].route_flag_to_be_updated[T + 2] != []:
                                            courier2_next_stop_order_loc_id = -1
                                            detect_time_added = 1
                                            while courier2_next_stop_order_loc_id == -1 and \
                                                    encounter_two_couriers[1].route_flag_to_be_updated[
                                                        T + detect_time_added + 1] != []:
                                                for flag_item in encounter_two_couriers[1].route_flag_to_be_updated[
                                                    T + detect_time_added]:
                                                    for next_time_flag_item in \
                                                            encounter_two_couriers[1].route_flag_to_be_updated[
                                                                T + detect_time_added + 1]:
                                                        if flag_item == next_time_flag_item:
                                                            courier2_next_stop_order_loc_id = next_time_flag_item[0]
                                                            if next_time_flag_item[1] == 0:
                                                                print('debug')
                                                            break
                                                detect_time_added += 1
                                            # for flag_item in encounter_two_couriers[1].route_flag_to_be_updated[T + 1]:
                                            #     for next_time_flag_item in \
                                            #     encounter_two_couriers[1].route_flag_to_be_updated[T + 2]:
                                            #         if flag_item == next_time_flag_item:
                                            #             courier2_next_stop_order_loc_id = next_time_flag_item[0]
                                            #             if next_time_flag_item[1] == 0:
                                            #                 print('debug')
                                            #             break
                                            # if courier2_next_stop_order_loc_id == -1 and \
                                            #         encounter_two_couriers[1].route_flag_to_be_updated[T + 3] != []:
                                            #     print('debug')
                                            #     for flag_item in encounter_two_couriers[1].route_flag_to_be_updated[T + 2]:
                                            #         for next_time_flag_item in \
                                            #         encounter_two_couriers[1].route_flag_to_be_updated[T + 3]:
                                            #             if flag_item == next_time_flag_item:
                                            #                 courier2_next_stop_order_loc_id = next_time_flag_item[0]
                                            #                 if next_time_flag_item[1] == 0:
                                            #                     print('debug')
                                            #                 break
                                            if courier2_next_stop_order_loc_id == -1:
                                                # 都是快送完的单
                                                for flag_item in encounter_two_couriers[1].route_flag_to_be_updated[
                                                    T + 1]:
                                                    if flag_item[1] != 2:
                                                        courier2_next_stop_order_loc_id = flag_item[0]
                                                        break
                                                if courier2_next_stop_order_loc_id == -1:
                                                    print('debug')
                                        else:
                                            courier2_next_stop_order_loc_id = \
                                                encounter_two_couriers[1].route_flag_to_be_updated[T + 1][0][0]
                                        if courier2_next_stop_order_loc_id > len(
                                                encounter_two_couriers[1].available_loc_real_time):
                                            print('debug')
                                        if encounter_two_couriers[1].available_loc_real_time[
                                            courier2_next_stop_order_loc_id] == 0:
                                            # 该单下一时刻送完了
                                            courier2_next_stop_location_lat = encounter_two_couriers[1].lat
                                            courier2_next_stop_location_lon = encounter_two_couriers[1].lon
                                        else:
                                            courier2_next_stop_location_lat = \
                                            encounter_two_couriers[1].available_loc_real_time[
                                                courier2_next_stop_order_loc_id].lat
                                            courier2_next_stop_location_lon = \
                                            encounter_two_couriers[1].available_loc_real_time[
                                                courier2_next_stop_order_loc_id].lon
                                    order_similarity = 0
                                    order_similarity2 = 0
                                    if encounter_to_exchange_order_list[encounter_order_id].dispatch_stage == 1:
                                        cur_order_next_stop_lon = encounter_to_exchange_order_list[
                                            encounter_order_id].shop_longitude
                                        cur_order_next_stop_lat = encounter_to_exchange_order_list[
                                            encounter_order_id].shop_latitude
                                    elif encounter_to_exchange_order_list[encounter_order_id].dispatch_stage == 2:
                                        cur_order_next_stop_lon = encounter_to_exchange_order_list[
                                            encounter_order_id].user_longitude
                                        cur_order_next_stop_lat = encounter_to_exchange_order_list[
                                            encounter_order_id].user_latitude
                                    else:
                                        continue
                                    cur_order_cur_lat = encounter_two_couriers[huandan_courier_id].lat
                                    cur_order_cur_lon = encounter_two_couriers[huandan_courier_id].lon

                                    # 订单相似度定义：与当前订单顺路的顺路单数
                                    # 与骑手1持有的的所有订单相似度，计数>0.8的个数
                                    courier1_shunludan_num = 0
                                    courier1_cur_order_num = 0
                                    for shunludan_id in range(len(encounter_two_couriers[0].order_list)):
                                        if encounter_two_couriers[0].order_list[shunludan_id].dispatch_stage != 0:
                                            courier1_cur_order_num += 1
                                            if encounter_two_couriers[0].order_list[shunludan_id].order_id == \
                                                    encounter_to_exchange_order_list[encounter_order_id].order_id:
                                                continue
                                            this_order_cur_lon = encounter_two_couriers[0].lon
                                            this_order_cur_lat = encounter_two_couriers[0].lat
                                            if encounter_two_couriers[0].order_list[
                                                shunludan_id].dispatch_stage == 1:
                                                this_order_next_stop_lon = encounter_two_couriers[0].order_list[
                                                    shunludan_id].shop_longitude
                                                this_order_next_stop_lat = encounter_two_couriers[0].order_list[
                                                    shunludan_id].shop_latitude
                                            elif encounter_two_couriers[0].order_list[
                                                shunludan_id].dispatch_stage == 2:
                                                this_order_next_stop_lon = encounter_two_couriers[0].order_list[
                                                    shunludan_id].user_longitude
                                                this_order_next_stop_lat = encounter_two_couriers[0].order_list[
                                                    shunludan_id].user_latitude
                                            # 计算相似度
                                            #     order_similarity = cosine_dis(np.array([cur_order_cur_lat, cur_order_cur_lon,
                                            #                                             cur_order_next_stop_lat, cur_order_next_stop_lon]),
                                            #                                   np.array([this_order_cur_lat, this_order_cur_lon,
                                            #                                             this_order_next_stop_lat, this_order_next_stop_lon]))
                                            if (
                                                    cur_order_next_stop_lat - cur_order_cur_lat == 0 and cur_order_next_stop_lon - cur_order_cur_lon == 0) or \
                                                    (
                                                            this_order_next_stop_lat - this_order_cur_lat == 0 and this_order_next_stop_lon - this_order_cur_lon == 0):
                                                order_similarity = 0
                                            else:
                                                order_similarity = cosine_dis(
                                                    np.array([cur_order_next_stop_lat - cur_order_cur_lat,
                                                              cur_order_next_stop_lon - cur_order_cur_lon]),
                                                    np.array([this_order_next_stop_lat - this_order_cur_lat,
                                                              this_order_next_stop_lon - this_order_cur_lon]))
                                            if order_similarity > 0:
                                                courier1_shunludan_num += 1

                                    # 骑手2的订单相似度
                                    courier2_shunludan_num = 0
                                    courier2_cur_order_num = 0
                                    for shunludan_id2 in range(len(encounter_two_couriers[1].order_list)):

                                        if encounter_two_couriers[1].order_list[shunludan_id2].dispatch_stage != 0:
                                            courier2_cur_order_num += 1
                                            if encounter_two_couriers[1].order_list[shunludan_id2].order_id == \
                                                    encounter_to_exchange_order_list[encounter_order_id].order_id:
                                                continue
                                            this_order_cur_lon2 = encounter_two_couriers[1].lon
                                            this_order_cur_lat2 = encounter_two_couriers[1].lat
                                            if encounter_two_couriers[1].order_list[
                                                shunludan_id2].dispatch_stage == 1:
                                                this_order_next_stop_lon2 = encounter_two_couriers[1].order_list[
                                                    shunludan_id2].shop_longitude
                                                this_order_next_stop_lat2 = encounter_two_couriers[1].order_list[
                                                    shunludan_id2].shop_latitude
                                            elif encounter_two_couriers[1].order_list[
                                                shunludan_id2].dispatch_stage == 2:
                                                this_order_next_stop_lon2 = encounter_two_couriers[1].order_list[
                                                    shunludan_id2].user_longitude
                                                this_order_next_stop_lat2 = encounter_two_couriers[1].order_list[
                                                    shunludan_id2].user_latitude
                                            # 计算相似度
                                            # order_similarity2 = cosine_dis(np.array([cur_order_cur_lat, cur_order_cur_lon,
                                            #                                         cur_order_next_stop_lat,
                                            #                                         cur_order_next_stop_lon]),
                                            #                               np.array([this_order_cur_lat2, this_order_cur_lon2,
                                            #                                         this_order_next_stop_lat2,
                                            #                                         this_order_next_stop_lon2]))
                                            if (
                                                    cur_order_next_stop_lat - cur_order_cur_lat == 0 and cur_order_next_stop_lon - cur_order_cur_lon == 0) or \
                                                    (
                                                            this_order_next_stop_lat2 - this_order_cur_lat2 == 0 and this_order_next_stop_lon2 - this_order_cur_lon2 == 0):
                                                order_similarity2 = 0
                                            else:
                                                order_similarity2 = cosine_dis(
                                                    np.array([cur_order_next_stop_lat - cur_order_cur_lat,
                                                              cur_order_next_stop_lon - cur_order_cur_lon]),
                                                    np.array([this_order_next_stop_lat2 - this_order_cur_lat2,
                                                              this_order_next_stop_lon2 - this_order_cur_lon2]))
                                            if order_similarity2 > 0:
                                                courier2_shunludan_num += 1

                                    # 当前骑手送完手里单还需的时间
                                    if encounter_two_couriers[0].route_flag_to_be_updated == {}:
                                        encounter_courier1_all_order_deliver_cost_time_exchange = 0
                                    elif max(encounter_two_couriers[0].route_flag_to_be_updated.keys()) <= T:
                                        encounter_courier1_all_order_deliver_cost_time_exchange = 0
                                    else:
                                        encounter_courier1_all_order_deliver_cost_time_exchange = max(
                                            encounter_two_couriers[0].route_flag_to_be_updated.keys()) - T

                                    if encounter_two_couriers[1].route_flag_to_be_updated == {}:
                                        encounter_courier2_all_order_deliver_cost_time_exchange = 0
                                    elif max(encounter_two_couriers[1].route_flag_to_be_updated.keys()) <= T:
                                        encounter_courier2_all_order_deliver_cost_time_exchange = 0
                                    else:
                                        encounter_courier2_all_order_deliver_cost_time_exchange = max(
                                            encounter_two_couriers[1].route_flag_to_be_updated.keys()) - T
                                    if exchanged_order_courier_cost_left_time < 0 or encounter_courier1_all_order_deliver_cost_time_exchange < 0 or encounter_courier2_all_order_deliver_cost_time_exchange < 0:
                                        print('debug')

                                    low_level_next_s = []
                                    next_s = [cur_order_next_stop_lat,
                                              cur_order_next_stop_lon,
                                              # encounter_two_couriers[chosen_courier_id].lat,
                                              # encounter_two_couriers[chosen_courier_id].lon,
                                              exchanged_order_courier_cost_left_time/60,
                                              courier1_next_stop_location_lat, courier1_next_stop_location_lon,
                                              get_distance_hav(cur_order_next_stop_lat, cur_order_next_stop_lon,
                                                               courier1_next_stop_location_lat,
                                                               courier1_next_stop_location_lon),
                                              encounter_two_couriers[0].cur_order_num, courier1_shunludan_num,
                                              encounter_courier1_all_order_deliver_cost_time_exchange/60,
                                              courier2_next_stop_location_lat, courier2_next_stop_location_lon,
                                              get_distance_hav(cur_order_next_stop_lat, cur_order_next_stop_lon,
                                                               courier2_next_stop_location_lat,
                                                               courier2_next_stop_location_lon),
                                              encounter_two_couriers[1].cur_order_num, courier2_shunludan_num,
                                              encounter_courier2_all_order_deliver_cost_time_exchange/60
                                              ]
                                    # if huandan_courier_id == 0:
                                    #     next_state = [cur_order_next_stop_lat,
                                    #                   cur_order_next_stop_lon,
                                    #                   # encounter_two_couriers[raw_courier_id].lat,
                                    #                   #            encounter_two_couriers[raw_courier_id].lon,
                                    #                   exchanged_order_courier_cost_left_time / 60,
                                    #                   courier1_next_stop_location_lat,
                                    #                   courier1_next_stop_location_lon,
                                    #                   encounter_two_couriers[0].cur_order_num,
                                    #                   courier1_shunludan_num,
                                    #                   encounter_courier1_all_order_deliver_cost_time / 60,
                                    #                   courier2_next_stop_location_lat,
                                    #                   courier2_next_stop_location_lon,
                                    #                   encounter_two_couriers[1].cur_order_num,
                                    #                   courier2_shunludan_num,
                                    #                   encounter_courier2_all_order_deliver_cost_time / 60]
                                    # else:
                                    #     next_state = [cur_order_next_stop_lat,
                                    #                   cur_order_next_stop_lon,
                                    #                   # encounter_two_couriers[raw_courier_id].lat,
                                    #                   #            encounter_two_couriers[raw_courier_id].lon,
                                    #                   exchanged_order_courier_cost_left_time / 60,
                                    #                   courier2_next_stop_location_lat,
                                    #                   courier2_next_stop_location_lon,
                                    #                   encounter_two_couriers[1].cur_order_num,
                                    #                   courier2_shunludan_num,
                                    #                   encounter_courier2_all_order_deliver_cost_time / 60,
                                    #                   courier1_next_stop_location_lat,
                                    #                   courier1_next_stop_location_lon,
                                    #                   encounter_two_couriers[0].cur_order_num,
                                    #                   courier1_shunludan_num,
                                    #                   encounter_courier1_all_order_deliver_cost_time / 60]
                                    low_level_next_s = next_s
                                    print('low_level next_s:',low_level_next_s)

                                    raw_order_dispatch_time = low_level_state_input[2]
                                    # raw_order_dispatch_time_list.append(raw_order_dispatch_time)
                                    exchange_order_dispatch_time = low_level_next_s[2]
                                    # exchanged_order_dispatch_time_list.append(exchange_order_dispatch_time)
                                    # print('low_level_raw:',raw_order_dispatch_time,',exchange:',exchange_order_dispatch_time)

                                    # revenue computation
                                    order_price = encounter_to_exchange_order_list[encounter_order_id].order_price
                                    promise_order_time = encounter_to_exchange_order_list[
                                        encounter_order_id].promise_deliver_time
                                    raw_deliver_time_overdue_condition1 = raw_order_dispatch_time - promise_order_time
                                    raw_revenue = 0
                                    # exchange_revenue = 0
                                    if raw_deliver_time_overdue_condition1 <= 0:
                                        # 没超时，全额得到订单价格
                                        raw_revenue = order_price
                                    else:
                                        overdue_time = raw_deliver_time_overdue_condition1 / 60  # 超时的分钟数
                                        if overdue_time <= 10:
                                            raw_revenue = 0.95 * order_price
                                        elif 10 < overdue_time <= 15:
                                            raw_revenue = 0.9 * order_price
                                        elif 15 < overdue_time <= 30:
                                            raw_revenue = 0.7 * order_price
                                        else:
                                            raw_revenue = 0.3 * order_price
                                    # raw_revenue_list.append(raw_revenue)
                                    exchange_deliver_time_overdue_condition = exchange_order_dispatch_time - promise_order_time
                                    if exchange_deliver_time_overdue_condition <= 0:
                                        # 没超时，全额得到订单价格
                                        exchange_revenue = order_price
                                    else:
                                        overdue_time = exchange_deliver_time_overdue_condition / 60  # 超时的分钟数
                                        if overdue_time <= 10:
                                            exchange_revenue = 0.95 * order_price
                                        elif 10 < overdue_time <= 15:
                                            exchange_revenue = 0.9 * order_price
                                        elif 15 < overdue_time <= 30:
                                            exchange_revenue = 0.7 * order_price
                                        else:
                                            exchange_revenue = 0.3 * order_price
                                    # exchanged_revenue_list.append(exchange_revenue)

                                    low_level_reward = 0.1* (raw_order_dispatch_time / exchange_order_dispatch_time) + (
                                            exchange_revenue / raw_revenue)*0.9

                                else:
                                    low_level_next_s = low_level_state_input
                                    low_level_reward = 1
                                    buhuan_count += 1

                                    # raw_order_dispatch_time = low_level_state_input[2]
                                    # # raw_order_dispatch_time_list.append(raw_order_dispatch_time)
                                    # # exchanged_order_dispatch_time_list.append(raw_order_dispatch_time)
                                    # # revenue computation
                                    # order_price = encounter_to_exchange_order_list[encounter_order_id].order_price
                                    # promise_order_time = encounter_to_exchange_order_list[
                                    #     encounter_order_id].promise_deliver_time
                                    # raw_deliver_time_overdue_condition = raw_order_dispatch_time - promise_order_time
                                    # raw_revenue = 0
                                    # # exchange_revenue = 0
                                    # if raw_deliver_time_overdue_condition <= 0:
                                    #     # 没超时，全额得到订单价格
                                    #     raw_revenue = order_price
                                    # else:
                                    #     overdue_time = raw_deliver_time_overdue_condition / 60  # 超时的分钟数
                                    #     if overdue_time <= 10:
                                    #         raw_revenue = 0.95 * order_price
                                    #     elif 10 < overdue_time <= 15:
                                    #         raw_revenue = 0.9 * order_price
                                    #     elif 15 < overdue_time <= 30:
                                    #         raw_revenue = 0.7 * order_price
                                    #     else:
                                    #         raw_revenue = 0.3 * order_price
                                    # raw_revenue_list.append(raw_revenue)
                                    # exchanged_revenue_list.append(raw_revenue)
                                print('low_level_reward:', low_level_reward)
                                low_level_ep_track_r.append(low_level_reward)
                                critic.store_transition(low_level_state_input,
                                                        low_level_action,
                                                        low_level_reward,
                                                        low_level_next_s)
                                if critic.memory_counter > critic.memory_size:
                                    sample_index = np.random.choice(critic.memory_size, size=critic.batch_size)
                                else:
                                    sample_index = np.random.choice(critic.memory_counter, size=critic.batch_size)

                                batch_memory = critic.memory[sample_index, :]
                                s = batch_memory[:, :critic.n_features]  # 32*13
                                _s = batch_memory[:, -critic.n_features:]  # 32*13
                                a = batch_memory[:, critic.n_features]  # 32*1
                                r = batch_memory[:, critic.n_features + 1]  # 32*1

                                td_error = critic.learn(s, r, _s)
                                actor.learn(s, a, td_error)
                                low_episode_times = len(low_level_ep_track_r)

                                if low_episode_times >= 50:
                                    low_level_ep_rs_sum = sum(low_level_ep_track_r)
                                    if 'low_level_running_reward_ep' not in globals():
                                        low_level_running_reward_ep = low_level_ep_rs_sum
                                    else:
                                        low_level_running_reward_ep = low_level_running_reward_ep * 0.95 + low_level_ep_rs_sum * 0.05
                                    print("low_episode:", low_level_global_step, "  low level reward:",
                                          low_level_running_reward_ep)

                                    low_level_ep_rs_average = sum(low_level_ep_track_r) / len(low_level_ep_track_r)
                                    # running_reward_ep = ep_rs_sum1
                                    print('low_episode:', low_level_global_step, ',len(low_level_ep_track_r):',
                                          len(low_level_ep_track_r),
                                          ',low level ep_average_reward', low_level_ep_rs_average)

                                    low_level_global_step += 1
                                    # 觉得差不多了（ep_reward/reward上升到稳定；loss稳定，单看loss不行）就手动save模型去训练
                                    with open(
                                            "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward_state_MHA_GRU_conv_3/low_train_log/train_20220125_time_iter7_to_14.txt",
                                            'a+') as logf:

                                        print('low_episode:', low_level_global_step, ",low_level_reward:",
                                              low_level_running_reward_ep,
                                              ',len(ep_track_r):',
                                              len(low_level_ep_track_r), ',low level ep_average_reward',
                                              low_level_ep_rs_average, file=logf)
                                    low_critic_loss_record = open(
                                        'D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward_state_MHA_GRU_conv_3/low_c_loss.txt',
                                        'a')
                                    low_critic_loss_record.write(str(critic.cost_his[-50:]) + '\n')
                                    low_critic_loss_record.close()
                                    # critic.cost_his = []

                                    low_actor_loss_record = open(
                                        'D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward_state_MHA_GRU_conv_3/low_a_loss.txt',
                                        'a')
                                    low_actor_loss_record.write(str(actor.cost_his[-50:]) + '\n')
                                    low_actor_loss_record.close()
                                    # actor.cost_his = []

                                    if (low_level_ep_rs_average >= 1) or low_level_global_step % 5 == 0:
                                        os.mkdir(
                                            "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward_state_MHA_GRU_conv_3/low_checkpoint/{}".format(
                                                low_level_global_step))
                                        saver.save(sess,
                                                   "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward_state_MHA_GRU_conv_3/low_checkpoint/{}/".format(
                                                       low_level_global_step) + "model_{}.ckpt".format(
                                                       low_level_global_step))
                                        print("save: ",
                                              "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward_state_MHA_GRU_conv_3/low_checkpoint/{}/".format(
                                                  low_level_global_step) + "model_{}.ckpt".format(
                                                  low_level_global_step))

                                    low_level_ep_track_r = []

                                # low_level_state_input.append(state_input)
                                # for state_input_id in range(len(state_input)):
                                #     low_level_state_input.append(state_input[state_input_id])

                            encounter_start_time = T
                            encounter_start_courier1_lat = encounter_two_couriers[0].lat
                            encounter_start_courier1_lon = encounter_two_couriers[0].lon
                            encounter_start_courier2_lat = encounter_two_couriers[1].lat
                            encounter_start_courier2_lon = encounter_two_couriers[1].lon
                            encounter_start_courier1_next_stop_lat = 0
                            encounter_start_courier1_next_stop_lon = 0
                            encounter_start_courier2_next_stop_lat = 0
                            encounter_start_courier2_next_stop_lon = 0
                            encounter_courier1_cur_order_cur_stage_remaining_time = 0
                            encounter_courier2_cur_order_cur_stage_remaining_time = 0

                            if T + 1 not in online_couriers[
                                online_courier_count_x].route_flag_to_be_updated.keys() or \
                                    online_couriers[online_courier_count_x].cur_order_num == 0 or len(
                                online_couriers[online_courier_count_x].route_flag_to_be_updated[T + 1]) == 0:
                                encounter_start_courier1_next_stop_lat = online_couriers[
                                    online_courier_count_x].lat
                                encounter_start_courier1_next_stop_lon = online_couriers[
                                    online_courier_count_x].lon
                                encounter_courier1_cur_order_cur_stage_remaining_time = 0
                            else:
                                if len(online_couriers[online_courier_count_x].route_flag_to_be_updated[
                                           T + 1]) > 1 and \
                                        online_couriers[online_courier_count_x].route_flag_to_be_updated[
                                            T + 2] != []:
                                    courier1_next_stop_order_loc_id = -1
                                    detect_time_added = 1
                                    while courier1_next_stop_order_loc_id == -1 and \
                                            online_couriers[online_courier_count_x].route_flag_to_be_updated[
                                                T + detect_time_added + 1] != []:
                                        for flag_item in \
                                                online_couriers[
                                                    online_courier_count_x].route_flag_to_be_updated[
                                                    T + detect_time_added]:
                                            for next_time_flag_item in \
                                                    online_couriers[
                                                        online_courier_count_x].route_flag_to_be_updated[
                                                        T + detect_time_added + 1]:
                                                if flag_item == next_time_flag_item:
                                                    courier1_next_stop_order_loc_id = next_time_flag_item[0]
                                                    break
                                        detect_time_added += 1
                                    if courier1_next_stop_order_loc_id == -1:
                                        # 都是快送完的单
                                        for flag_item in \
                                                online_couriers[
                                                    online_courier_count_x].route_flag_to_be_updated[
                                                    T + 1]:
                                            if flag_item[1] != 2:
                                                courier1_next_stop_order_loc_id = flag_item[0]
                                                break
                                        if courier1_next_stop_order_loc_id == -1:
                                            print('debug')
                                else:
                                    courier1_next_stop_order_loc_id = \
                                        online_couriers[online_courier_count_x].route_flag_to_be_updated[T + 1][
                                            0][
                                            0]

                                if courier1_next_stop_order_loc_id > len(
                                        online_couriers[online_courier_count_x].available_loc_real_time):
                                    print('debug')
                                if online_couriers[online_courier_count_x].available_loc_real_time[
                                    courier1_next_stop_order_loc_id] == 0:
                                    # 该单下一时刻送完了
                                    encounter_start_courier1_next_stop_lat = online_couriers[
                                        online_courier_count_x].lat
                                    encounter_start_courier1_next_stop_lon = online_couriers[
                                        online_courier_count_x].lon
                                    encounter_courier1_cur_order_cur_stage_remaining_time = 1
                                else:
                                    encounter_start_courier1_next_stop_lat = \
                                        online_couriers[online_courier_count_x].available_loc_real_time[
                                            courier1_next_stop_order_loc_id].lat
                                    encounter_start_courier1_next_stop_lon = \
                                        online_couriers[online_courier_count_x].available_loc_real_time[
                                            courier1_next_stop_order_loc_id].lon
                                    # encounter_start_courier1_next_stop_lat = \
                                    #     online_couriers[online_courier_count_x].available_loc_real_time[
                                    #         online_couriers[online_courier_count_x].route_flag_to_be_updated[
                                    #             T + 1][
                                    #             0][
                                    #             0]].lat
                                    # encounter_start_courier1_next_stop_lon = \
                                    #     online_couriers[online_courier_count_x].available_loc_real_time[
                                    #         online_couriers[online_courier_count_x].route_flag_to_be_updated[
                                    #             T + 1][
                                    #             0][
                                    #             0]].lon

                                    cur_order_id_in_courier_order_list = \
                                        online_couriers[online_courier_count_x].route_flag_to_be_updated[T + 1][
                                            0][
                                            0]
                                    cur_order_stage_in_courier_order_list = \
                                        online_couriers[online_courier_count_x].route_flag_to_be_updated[T + 1][
                                            0][
                                            1]
                                    objective_order_flag = -1
                                    if cur_order_stage_in_courier_order_list == 1:
                                        objective_order_flag = 2
                                    else:
                                        objective_order_flag = 0

                                    objective_route_flag_item = (
                                        cur_order_id_in_courier_order_list, objective_order_flag)

                                    cur_time = T + 1
                                    order_next_step_need_time = 0
                                    while cur_time > T:
                                        route_flag_item = \
                                            online_couriers[online_courier_count_x].route_flag_to_be_updated[
                                                cur_time]
                                        if objective_route_flag_item in route_flag_item:
                                            order_next_step_need_time = cur_time
                                            break
                                        cur_time += 1
                                    if order_next_step_need_time == 0:
                                        print('debug')
                                    encounter_courier1_cur_order_cur_stage_remaining_time = order_next_step_need_time - T

                            if T + 1 not in online_couriers[
                                online_courier_count_y].route_flag_to_be_updated.keys() or \
                                    online_couriers[online_courier_count_y].cur_order_num == 0 or len(
                                online_couriers[online_courier_count_y].route_flag_to_be_updated[T + 1]) == 0:
                                encounter_start_courier2_next_stop_lat = online_couriers[
                                    online_courier_count_y].lat
                                encounter_start_courier2_next_stop_lon = online_couriers[
                                    online_courier_count_y].lon
                                encounter_courier2_cur_order_cur_stage_remaining_time = 0
                            else:
                                if len(online_couriers[online_courier_count_y].route_flag_to_be_updated[
                                           T + 1]) > 1 and \
                                        online_couriers[online_courier_count_y].route_flag_to_be_updated[
                                            T + 2] != []:
                                    courier2_next_stop_order_loc_id = -1
                                    detect_time_added = 1
                                    while courier2_next_stop_order_loc_id == -1 and \
                                            online_couriers[online_courier_count_y].route_flag_to_be_updated[
                                                T + detect_time_added + 1] != []:
                                        for flag_item in \
                                                online_couriers[
                                                    online_courier_count_y].route_flag_to_be_updated[
                                                    T + detect_time_added]:
                                            for next_time_flag_item in \
                                                    online_couriers[
                                                        online_courier_count_y].route_flag_to_be_updated[
                                                        T + detect_time_added + 1]:
                                                if flag_item == next_time_flag_item:
                                                    courier2_next_stop_order_loc_id = next_time_flag_item[0]
                                                    break
                                        detect_time_added += 1
                                    if courier2_next_stop_order_loc_id == -1:
                                        # 都是快送完的单
                                        for flag_item in \
                                                online_couriers[
                                                    online_courier_count_y].route_flag_to_be_updated[
                                                    T + 1]:
                                            if flag_item[1] != 2:
                                                courier2_next_stop_order_loc_id = flag_item[0]
                                                break
                                        if courier2_next_stop_order_loc_id == -1:
                                            print('debug')
                                else:
                                    courier2_next_stop_order_loc_id = \
                                        online_couriers[online_courier_count_y].route_flag_to_be_updated[T + 1][
                                            0][
                                            0]

                                if courier2_next_stop_order_loc_id > len(
                                        online_couriers[online_courier_count_y].available_loc_real_time):
                                    print('debug')
                                if online_couriers[online_courier_count_y].available_loc_real_time[
                                    courier2_next_stop_order_loc_id] == 0:
                                    # 该单下一时刻送完了
                                    encounter_start_courier2_next_stop_lat = online_couriers[
                                        online_courier_count_y].lat
                                    encounter_start_courier2_next_stop_lon = online_couriers[
                                        online_courier_count_y].lon
                                    encounter_courier2_cur_order_cur_stage_remaining_time = 1
                                else:
                                    encounter_start_courier2_next_stop_lat = \
                                        online_couriers[online_courier_count_y].available_loc_real_time[
                                            courier2_next_stop_order_loc_id].lat
                                    encounter_start_courier2_next_stop_lon = \
                                        online_couriers[online_courier_count_y].available_loc_real_time[
                                            courier2_next_stop_order_loc_id].lon
                                    # encounter_start_courier2_next_stop_lat = \
                                    #     online_couriers[online_courier_count_y].available_loc_real_time[
                                    #         online_couriers[online_courier_count_y].route_flag_to_be_updated[
                                    #             T + 1][
                                    #             0][
                                    #             0]].lat
                                    # encounter_start_courier2_next_stop_lon = \
                                    #     online_couriers[online_courier_count_y].available_loc_real_time[
                                    #         online_couriers[online_courier_count_y].route_flag_to_be_updated[
                                    #             T + 1][
                                    #             0][
                                    #             0]].lon

                                    cur_order_id_in_courier_order_list = \
                                        online_couriers[online_courier_count_y].route_flag_to_be_updated[T + 1][
                                            0][
                                            0]
                                    cur_order_stage_in_courier_order_list = \
                                        online_couriers[online_courier_count_y].route_flag_to_be_updated[T + 1][
                                            0][
                                            1]
                                    objective_order_flag = -1
                                    if cur_order_stage_in_courier_order_list == 1:
                                        objective_order_flag = 2
                                    else:
                                        objective_order_flag = 0

                                    objective_route_flag_item = (
                                        cur_order_id_in_courier_order_list, objective_order_flag)

                                    cur_time = T + 1
                                    order_next_step_need_time = 0
                                    while cur_time > T:
                                        route_flag_item = \
                                            online_couriers[online_courier_count_y].route_flag_to_be_updated[
                                                cur_time]
                                        if objective_route_flag_item in route_flag_item:
                                            order_next_step_need_time = cur_time
                                            break
                                        cur_time += 1
                                    if order_next_step_need_time == 0:
                                        print('debug')
                                    encounter_courier2_cur_order_cur_stage_remaining_time = order_next_step_need_time - T

                            # courier-order state_input preprocess
                            courier1_max_order_remaining_time = 0  # estimated deliver time - cur time
                            # courier1_max_order_promise_remaining_time = 0  # promise_deliver time - current time
                            courier1_min_real_time_promise_variance_order_remaining_time = 9999999999  # 越小越好
                            courier1_order_num = online_couriers[online_courier_count_x].cur_order_num
                            if courier1_order_num > 0:
                                for order_item_id in range(
                                        len(online_couriers[online_courier_count_x].order_list)):

                                    if online_couriers[online_courier_count_x].order_list[
                                        order_item_id].dispatch_stage != 0:
                                        cur_order_promise_remaining_time = \
                                            online_couriers[online_courier_count_x].order_list[
                                                order_item_id].promise_deliver_time - T
                                        order_item_cost_left_time = -9999
                                        if online_couriers[
                                            online_courier_count_x].route_flag_to_be_updated == {}:
                                            order_item_cost_left_time = 0
                                        elif max(online_couriers[
                                                     online_courier_count_x].route_flag_to_be_updated.keys()) <= T:
                                            order_item_cost_left_time = 0
                                        else:
                                            for time_step_id in range(T, max(
                                                    online_couriers[
                                                        online_courier_count_x].route_flag_to_be_updated.keys()) + 1):
                                                for state_change_id in range(
                                                        len(online_couriers[
                                                                online_courier_count_x].route_flag_to_be_updated[
                                                                time_step_id])):
                                                    if \
                                                            online_couriers[
                                                                online_courier_count_x].route_flag_to_be_updated[
                                                                time_step_id][
                                                                state_change_id] == (
                                                                    order_item_id, 0):
                                                        order_item_cost_left_time = time_step_id - T
                                                        break

                                        if order_item_cost_left_time == -9999:
                                            print('debug')

                                        if courier1_min_real_time_promise_variance_order_remaining_time > \
                                                cur_order_promise_remaining_time - order_item_cost_left_time:
                                            courier1_min_real_time_promise_variance_order_remaining_time = \
                                                cur_order_promise_remaining_time - order_item_cost_left_time
                                        if courier1_max_order_remaining_time < order_item_cost_left_time:
                                            courier1_max_order_remaining_time = order_item_cost_left_time
                            else:
                                courier1_min_real_time_promise_variance_order_remaining_time = 0

                            courier2_max_order_remaining_time = 0  # estimated deliver time - cur time
                            # courier2_max_order_promise_remaining_time = 0  # promise_deliver time - current time
                            courier2_min_real_time_promise_variance_order_remaining_time = 9999999999  # 越小越好
                            courier2_order_num = online_couriers[online_courier_count_y].cur_order_num
                            if courier2_order_num > 0:
                                for order_item_id in range(
                                        len(online_couriers[online_courier_count_y].order_list)):
                                    if online_couriers[online_courier_count_y].order_list[
                                        order_item_id].dispatch_stage != 0:
                                        cur_order_promise_remaining_time = \
                                            online_couriers[online_courier_count_y].order_list[
                                                order_item_id].promise_deliver_time - T
                                        order_item_cost_left_time = -9999
                                        if online_couriers[
                                            online_courier_count_y].route_flag_to_be_updated == {}:
                                            order_item_cost_left_time = 0
                                        elif max(online_couriers[
                                                     online_courier_count_y].route_flag_to_be_updated.keys()) <= T:
                                            order_item_cost_left_time = 0
                                        else:
                                            for time_step_id in range(T, max(
                                                    online_couriers[
                                                        online_courier_count_y].route_flag_to_be_updated.keys()) + 1):
                                                for state_change_id in range(
                                                        len(online_couriers[
                                                                online_courier_count_y].route_flag_to_be_updated[
                                                                time_step_id])):
                                                    if \
                                                            online_couriers[
                                                                online_courier_count_y].route_flag_to_be_updated[
                                                                time_step_id][
                                                                state_change_id] == (
                                                                    order_item_id, 0):
                                                        order_item_cost_left_time = time_step_id - T
                                                        break

                                        if order_item_cost_left_time == -9999:
                                            print('debug')
                                        if courier2_min_real_time_promise_variance_order_remaining_time > \
                                                cur_order_promise_remaining_time - order_item_cost_left_time:
                                            courier2_min_real_time_promise_variance_order_remaining_time = \
                                                cur_order_promise_remaining_time - order_item_cost_left_time
                                        if courier2_max_order_remaining_time < order_item_cost_left_time:
                                            courier2_max_order_remaining_time = order_item_cost_left_time
                            else:
                                courier2_min_real_time_promise_variance_order_remaining_time = 0

                            # courier-order whole similarity preprocess
                            courier1_self_order_similarity = 0
                            courier1_self_order_similarity_list = []
                            courier1_courier2_order_similarity = 0
                            courier1_courier2_order_similarity_list = []

                            courier2_self_order_similarity = 0
                            courier2_self_order_similarity_list = []
                            courier2_courier1_order_similarity = 0
                            courier2_courier1_order_similarity_list = []

                            courier1_order_next_stop_list = []
                            for courier1_order_item in range(
                                    len(online_couriers[online_courier_count_x].order_list)):
                                if online_couriers[online_courier_count_x].order_list[
                                    courier1_order_item].dispatch_stage != 0:
                                    if online_couriers[online_courier_count_x].order_list[
                                        courier1_order_item].dispatch_stage == 1:
                                        courier1_order_next_stop_list.append(Loc(
                                            online_couriers[online_courier_count_x].order_list[
                                                courier1_order_item].shop_latitude,
                                            online_couriers[online_courier_count_x].order_list[
                                                courier1_order_item].shop_longitude))
                                    elif online_couriers[online_courier_count_x].order_list[
                                        courier1_order_item].dispatch_stage == 2:
                                        courier1_order_next_stop_list.append(Loc(
                                            online_couriers[online_courier_count_x].order_list[
                                                courier1_order_item].user_latitude,
                                            online_couriers[online_courier_count_x].order_list[
                                                courier1_order_item].user_longitude))
                            courier2_order_next_stop_list = []
                            for courier2_order_item in range(
                                    len(online_couriers[online_courier_count_y].order_list)):
                                if online_couriers[online_courier_count_y].order_list[
                                    courier2_order_item].dispatch_stage != 0:
                                    if online_couriers[online_courier_count_y].order_list[
                                        courier2_order_item].dispatch_stage == 1:
                                        courier2_order_next_stop_list.append(Loc(
                                            online_couriers[online_courier_count_y].order_list[
                                                courier2_order_item].shop_latitude,
                                            online_couriers[online_courier_count_y].order_list[
                                                courier2_order_item].shop_longitude))
                                    elif online_couriers[online_courier_count_y].order_list[
                                        courier2_order_item].dispatch_stage == 2:
                                        courier2_order_next_stop_list.append(Loc(
                                            online_couriers[online_courier_count_y].order_list[
                                                courier2_order_item].user_latitude,
                                            online_couriers[online_courier_count_y].order_list[
                                                courier2_order_item].user_longitude))

                            if courier1_order_num > 1:
                                for courier1_compute_similarity_id1 in range(0, len(
                                        courier1_order_next_stop_list)):
                                    for courier1_compute_similarity_id2 in range(
                                            courier1_compute_similarity_id1 + 1,
                                            len(courier1_order_next_stop_list)):
                                        cur_simi = 0
                                        cur_order_next_stop_lat = courier1_order_next_stop_list[
                                            courier1_compute_similarity_id1].lat
                                        cur_order_next_stop_lon = courier1_order_next_stop_list[
                                            courier1_compute_similarity_id1].lon
                                        cur_order_cur_lat = encounter_start_courier1_lat
                                        cur_order_cur_lon = encounter_start_courier1_lon
                                        this_order_next_stop_lat = courier1_order_next_stop_list[
                                            courier1_compute_similarity_id2].lat
                                        this_order_next_stop_lon = courier1_order_next_stop_list[
                                            courier1_compute_similarity_id2].lon
                                        this_order_cur_lat = encounter_start_courier1_lat
                                        this_order_cur_lon = encounter_start_courier1_lon
                                        if (
                                                cur_order_next_stop_lat - cur_order_cur_lat == 0 and cur_order_next_stop_lon - cur_order_cur_lon == 0) or \
                                                (
                                                        this_order_next_stop_lat - this_order_cur_lat == 0 and this_order_next_stop_lon - this_order_cur_lon == 0):
                                            cur_simi = 0
                                        else:
                                            cur_simi = cosine_dis(
                                                np.array([cur_order_next_stop_lat - cur_order_cur_lat,
                                                          cur_order_next_stop_lon - cur_order_cur_lon]),
                                                np.array(
                                                    [this_order_next_stop_lat - this_order_cur_lat,
                                                     this_order_next_stop_lon - this_order_cur_lon]))
                                        courier1_self_order_similarity_list.append(cur_simi)
                                courier1_self_order_similarity = np.sum(
                                    courier1_self_order_similarity_list) / len(
                                    courier1_self_order_similarity_list)
                            else:
                                courier1_self_order_similarity = 0

                            if courier1_order_num > 0 and courier2_order_num > 0:
                                for courier1_courier2_compute_similarity_c1 in range(
                                        len(courier1_order_next_stop_list)):
                                    cur_order_exchange_simi = []
                                    for courier1_courier2_compute_similarity_c2 in range(
                                            len(courier2_order_next_stop_list)):
                                        cur_simi = 0
                                        cur_order_next_stop_lat = courier1_order_next_stop_list[
                                            courier1_courier2_compute_similarity_c1].lat
                                        cur_order_next_stop_lon = courier1_order_next_stop_list[
                                            courier1_courier2_compute_similarity_c1].lon
                                        cur_order_cur_lat = encounter_start_courier1_lat
                                        cur_order_cur_lon = encounter_start_courier1_lon
                                        this_order_next_stop_lat = courier2_order_next_stop_list[
                                            courier1_courier2_compute_similarity_c2].lat
                                        this_order_next_stop_lon = courier2_order_next_stop_list[
                                            courier1_courier2_compute_similarity_c2].lon
                                        this_order_cur_lat = encounter_start_courier2_lat
                                        this_order_cur_lon = encounter_start_courier2_lon
                                        if (
                                                cur_order_next_stop_lat - cur_order_cur_lat == 0 and cur_order_next_stop_lon - cur_order_cur_lon == 0) or \
                                                (
                                                        this_order_next_stop_lat - this_order_cur_lat == 0 and this_order_next_stop_lon - this_order_cur_lon == 0):
                                            cur_simi = 0
                                        else:
                                            cur_simi = cosine_dis(
                                                np.array([cur_order_next_stop_lat - cur_order_cur_lat,
                                                          cur_order_next_stop_lon - cur_order_cur_lon]),
                                                np.array(
                                                    [this_order_next_stop_lat - this_order_cur_lat,
                                                     this_order_next_stop_lon - this_order_cur_lon]))
                                        cur_order_exchange_simi.append(cur_simi)
                                    courier1_courier2_order_similarity_list.append(
                                        np.sum(cur_order_exchange_simi) / len(cur_order_exchange_simi))
                                courier1_courier2_order_similarity = np.sum(
                                    courier1_courier2_order_similarity_list) / len(
                                    courier1_courier2_order_similarity_list)
                            else:
                                courier1_courier2_order_similarity = 0

                            # 骑手2 相关的 相似度计算
                            if courier2_order_num > 1:
                                for courier2_compute_similarity_id1 in range(0, len(
                                        courier2_order_next_stop_list)):
                                    for courier2_compute_similarity_id2 in range(
                                            courier2_compute_similarity_id1 + 1,
                                            len(courier2_order_next_stop_list)):
                                        cur_simi = 0
                                        cur_order_next_stop_lat = courier2_order_next_stop_list[
                                            courier2_compute_similarity_id1].lat
                                        cur_order_next_stop_lon = courier2_order_next_stop_list[
                                            courier2_compute_similarity_id1].lon
                                        cur_order_cur_lat = encounter_start_courier2_lat
                                        cur_order_cur_lon = encounter_start_courier2_lon
                                        this_order_next_stop_lat = courier2_order_next_stop_list[
                                            courier2_compute_similarity_id2].lat
                                        this_order_next_stop_lon = courier2_order_next_stop_list[
                                            courier2_compute_similarity_id2].lon
                                        this_order_cur_lat = encounter_start_courier2_lat
                                        this_order_cur_lon = encounter_start_courier2_lon
                                        if (
                                                cur_order_next_stop_lat - cur_order_cur_lat == 0 and cur_order_next_stop_lon - cur_order_cur_lon == 0) or \
                                                (
                                                        this_order_next_stop_lat - this_order_cur_lat == 0 and this_order_next_stop_lon - this_order_cur_lon == 0):
                                            cur_simi = 0
                                        else:
                                            cur_simi = cosine_dis(
                                                np.array([cur_order_next_stop_lat - cur_order_cur_lat,
                                                          cur_order_next_stop_lon - cur_order_cur_lon]),
                                                np.array(
                                                    [this_order_next_stop_lat - this_order_cur_lat,
                                                     this_order_next_stop_lon - this_order_cur_lon]))
                                        courier2_self_order_similarity_list.append(cur_simi)
                                courier2_self_order_similarity = np.sum(
                                    courier2_self_order_similarity_list) / len(
                                    courier2_self_order_similarity_list)
                            else:
                                courier2_self_order_similarity = 0
                            if courier1_order_num > 0 and courier2_order_num > 0:
                                for courier2_courier1_compute_similarity_c2 in range(
                                        len(courier2_order_next_stop_list)):
                                    cur_order_exchange_simi = []
                                    for courier2_courier1_compute_similarity_c1 in range(
                                            len(courier1_order_next_stop_list)):
                                        cur_simi = 0
                                        cur_order_next_stop_lat = courier2_order_next_stop_list[
                                            courier2_courier1_compute_similarity_c2].lat
                                        cur_order_next_stop_lon = courier2_order_next_stop_list[
                                            courier2_courier1_compute_similarity_c2].lon
                                        cur_order_cur_lat = encounter_start_courier2_lat
                                        cur_order_cur_lon = encounter_start_courier2_lon
                                        this_order_next_stop_lat = courier1_order_next_stop_list[
                                            courier2_courier1_compute_similarity_c1].lat
                                        this_order_next_stop_lon = courier1_order_next_stop_list[
                                            courier2_courier1_compute_similarity_c1].lon
                                        this_order_cur_lat = encounter_start_courier1_lat
                                        this_order_cur_lon = encounter_start_courier1_lon
                                        if (
                                                cur_order_next_stop_lat - cur_order_cur_lat == 0 and cur_order_next_stop_lon - cur_order_cur_lon == 0) or \
                                                (
                                                        this_order_next_stop_lat - this_order_cur_lat == 0 and this_order_next_stop_lon - this_order_cur_lon == 0):
                                            cur_simi = 0
                                        else:
                                            cur_simi = cosine_dis(
                                                np.array([cur_order_next_stop_lat - cur_order_cur_lat,
                                                          cur_order_next_stop_lon - cur_order_cur_lon]),
                                                np.array(
                                                    [this_order_next_stop_lat - this_order_cur_lat,
                                                     this_order_next_stop_lon - this_order_cur_lon]))
                                        cur_order_exchange_simi.append(cur_simi)
                                    courier2_courier1_order_similarity_list.append(
                                        np.sum(cur_order_exchange_simi) / len(cur_order_exchange_simi))
                                courier2_courier1_order_similarity = np.sum(
                                    courier2_courier1_order_similarity_list) / len(
                                    courier2_courier1_order_similarity_list)
                            else:
                                courier2_courier1_order_similarity = 0

                            high_level_next_s = [
                                encounter_start_time / 3600,  # encounter:11个state
                                encounter_start_courier1_lat,
                                encounter_start_courier1_lon,
                                encounter_start_courier2_lat,
                                encounter_start_courier2_lon,
                                encounter_start_courier1_next_stop_lat,
                                encounter_start_courier1_next_stop_lon,
                                encounter_start_courier2_next_stop_lat,
                                encounter_start_courier2_next_stop_lon,
                                encounter_courier1_cur_order_cur_stage_remaining_time / 60,
                                encounter_courier2_cur_order_cur_stage_remaining_time / 60,
                                # order-state: 8 个
                                courier1_max_order_remaining_time/60,
                                courier1_min_real_time_promise_variance_order_remaining_time / 60,
                                courier1_order_num,
                                courier1_self_order_similarity,
                                courier1_courier2_order_similarity,
                                courier2_max_order_remaining_time/60,
                                courier2_min_real_time_promise_variance_order_remaining_time / 60,
                                courier2_order_num,
                                courier2_self_order_similarity,
                                courier2_courier1_order_similarity,
                                encounter_courier_rssi[0],
                                encounter_courier_rssi[1],
                                encounter_courier_rssi[2],
                                encounter_courier_rssi[3],
                            ]

                            # high_level_1==>low_level[0,0,0] 的处理
                            print('high_level next_s:',high_level_next_s)

                            if buhuan_count == len(to_exchange_order_raw_courier_id_list):
                                # 添加惩罚引子，reward = -10
                                # high_level_reward = -1
                                high_level_reward = 1

                            else:
                                exchanged_revenue_list = []
                                exchanged_order_dispatch_time_list = []
                                for encounter_order_id in range(len(encounter_to_exchange_order_list)):
                                    exchanged_order_raw_courier_cost_left_time = -9999
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
                                            exchanged_order_raw_courier_cost_left_time = 0
                                        elif max(encounter_two_couriers[0].route_flag_to_be_updated.keys()) <= T:
                                            exchanged_order_raw_courier_cost_left_time = 0
                                        else:
                                            for time_step_id in range(T, max(
                                                    encounter_two_couriers[0].route_flag_to_be_updated.keys()) + 1):
                                                for state_change_id in range(
                                                        len(encounter_two_couriers[0].route_flag_to_be_updated[
                                                                time_step_id])):
                                                    if encounter_two_couriers[0].route_flag_to_be_updated[time_step_id][
                                                        state_change_id] == (
                                                            cur_this_order_loc_id, 0):
                                                        exchanged_order_raw_courier_cost_left_time = time_step_id - T
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
                                            exchanged_order_raw_courier_cost_left_time = 0
                                        elif max(encounter_two_couriers[1].route_flag_to_be_updated.keys()) <= T:
                                            exchanged_order_raw_courier_cost_left_time = 0
                                        else:
                                            for time_step_id in range(T, max(
                                                    encounter_two_couriers[1].route_flag_to_be_updated.keys()) + 1):

                                                for change_state_id1 in range(
                                                        len(encounter_two_couriers[1].route_flag_to_be_updated[
                                                                time_step_id])):
                                                    if encounter_two_couriers[1].route_flag_to_be_updated[time_step_id][
                                                        change_state_id1] == (
                                                            cur_this_order_loc_id, 0):
                                                        exchanged_order_raw_courier_cost_left_time = time_step_id - T
                                                        break

                                    if exchanged_order_raw_courier_cost_left_time == -9999:
                                        print('debug')
                                    # print('high_level_exchange:',exchanged_order_raw_courier_cost_left_time)
                                    exchanged_order_dispatch_time_list.append(
                                        exchanged_order_raw_courier_cost_left_time / 60)
                                    order_price = encounter_to_exchange_order_list[encounter_order_id].order_price
                                    promise_order_time = encounter_to_exchange_order_list[
                                        encounter_order_id].promise_deliver_time
                                    # exchange_deliver_time_overdue_condition = exchange_order_dispatch_time + courier1_courier2_time - promise_order_time
                                    exchange_deliver_time_overdue_condition = exchanged_order_raw_courier_cost_left_time - promise_order_time
                                    if exchange_deliver_time_overdue_condition <= 0:
                                        # 没超时，全额得到订单价格
                                        exchange_revenue = order_price
                                    else:
                                        overdue_time = exchange_deliver_time_overdue_condition / 60  # 超时的分钟数
                                        if overdue_time <= 10:
                                            exchange_revenue = 0.95 * order_price
                                        elif 10 < overdue_time <= 15:
                                            exchange_revenue = 0.9 * order_price
                                        elif 15 < overdue_time <= 30:
                                            exchange_revenue = 0.7 * order_price
                                        else:
                                            exchange_revenue = 0.3 * order_price
                                    exchanged_revenue_list.append(exchange_revenue)
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
                                high_level_reward = ((raw_encounter_courier1_all_order_deliver_cost_time +
                                                      raw_encounter_courier2_all_order_deliver_cost_time) /
                                                     (encounter_courier1_all_order_deliver_cost_time +
                                                      encounter_courier2_all_order_deliver_cost_time)) * 0.1 + 0.9* \
                                                    (sum(exchanged_revenue_list) / sum(raw_revenue_list))
                                # * (sum(raw_order_dispatch_time_list)/sum(exchanged_order_dispatch_time_list))
                                print('high_level_reward:', high_level_reward)
                                # reward = (sum(raw_order_dispatch_time_list)/sum(exchanged_order_dispatch_time_list
                                #                                                 )) * \
                                #          (sum(exchanged_revenue_list) / sum(raw_revenue_list))
                                # revenue_variance = sum(revenue_variance_list)
                                # reward = math.exp(-order_dispatch_time_variance/1000) * math.exp(revenue_variance/50)
                                # reward = (math.exp(-sum(exchanged_order_dispatch_time_list) / 3600) *
                                #           sum(exchanged_revenue_list) / 50) - \
                                #          (math.exp(-sum(raw_order_dispatch_time_list) / 3600) * sum(
                                #              raw_revenue_list) / 50)
                                # reward = -sum(exchanged_order_dispatch_time_list) + sum(raw_order_dispatch_time_list)
                                # reward = (math.exp(reward) - math.exp(-reward)) / (math.exp(reward) + math.exp(-reward))
                                # low_level_reward = reward
                        else:
                            high_level_reward = 1
                            # low_level_reward = 0
                            high_level_next_s = high_level_state_input

                        hierachical_critic.store_transition(high_level_state_input, h_network_output,
                                                            high_level_reward, high_level_next_s)
                        if hierachical_critic.memory_counter > hierachical_critic.memory_size:
                            hierachical_sample_index = np.random.choice(hierachical_critic.memory_size,
                                                                        size=hierachical_critic.batch_size)
                        else:
                            hierachical_sample_index = np.random.choice(hierachical_critic.memory_counter,
                                                                        size=hierachical_critic.batch_size)

                        hierachical_batch_memory = hierachical_critic.memory[hierachical_sample_index, :]
                        hierachical_s = hierachical_batch_memory[:, :hierachical_critic.n_features]  # 32*13
                        hierachical__s = hierachical_batch_memory[:, -hierachical_critic.n_features:]  # 32*13
                        hierachical_a = hierachical_batch_memory[:, hierachical_critic.n_features]  # 32*1
                        hierachical_r = hierachical_batch_memory[:, hierachical_critic.n_features + 1]  # 32*1

                        hierachical_td_error = hierachical_critic.learn(hierachical_s, hierachical_r, hierachical__s)
                        hierachical_actor.learn(hierachical_s, hierachical_a, hierachical_td_error)

                        # td_error = critic.learn(s, r, _s)
                        # actor.learn(s, a, td_error)

                        # td_error = critic.learn(np.array(s),
                        #                         r, np.array(_s))
                        # h_network_output_list = []
                        # h_network_output_list.append(h_network_output)
                        # hierachical_actor.learn(np.array(s[:, :h_state_dim]), a_h, td_error)
                        # # if h_network_output == 1:
                        # actor.learn(np.array(s[:, h_state_dim:h_state_dim + state_dim]), a, td_error)
                        ep_track_r.append(high_level_reward)
                        # print('huandan_state:', high_level_state_input, ', option:', h_network_output, 'huandan_reward',
                        # high_level_reward)
                        event_id += 1
                        # 修改了 每个回合训练的个数，原来是event_id <=100（导致每次的reward序列长度不同）
                        episode_times = len(ep_track_r)

                        if episode_times >= 50:
                            ep_rs_sum1 = sum(ep_track_r)
                            if 'running_reward_ep' not in globals():
                                running_reward_ep = ep_rs_sum1
                            else:
                                running_reward_ep = running_reward_ep * 0.95 + ep_rs_sum1 * 0.05
                            print("episode:", global_step, "  reward:", running_reward_ep)
                            episode_ep_reward.append(running_reward_ep)

                            # hierachical_network.learn()

                            ep_rs_average = sum(ep_track_r) / len(ep_track_r)
                            # running_reward_ep = ep_rs_sum1
                            print('episode:', global_step, ',len(ep_track_r):', len(ep_track_r), ',ep_average_reward',
                                  ep_rs_average)
                            episode_ep_average_reward.append(ep_rs_average)

                            if len(low_level_ep_track_r) > 0:
                                low_level_ep_rs_average1 = sum(low_level_ep_track_r) / len(low_level_ep_track_r)
                                # running_reward_ep = ep_rs_sum1
                                print('len(low_level_ep_track_r):',
                                      len(low_level_ep_track_r),
                                      ',low level ep_average_reward', low_level_ep_rs_average1)

                            # 觉得差不多了（ep_reward/reward上升到稳定；loss稳定，单看loss不行）就手动save模型去训练
                            global_step += 1
                            with open(
                                    "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward_state_MHA_GRU_conv_3/high_train_log/train_20220125_time_iter7_to_14.txt",
                                    'a+') as logf:
                                print("episode:", global_step, ",reward:", running_reward_ep, ',len(ep_track_r):',
                                      len(ep_track_r),
                                      ',ep_average_reward', ep_rs_average, file=logf)
                                if len(low_level_ep_track_r) > 0:
                                    print('len(low_level_ep_track_r):',
                                          len(low_level_ep_track_r), ',low level ep_average_reward',
                                          low_level_ep_rs_average1, file=logf)

                            if (ep_rs_average >= 1) or global_step % 5 == 0:
                                os.mkdir(
                                    "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward_state_MHA_GRU_conv_3/high_checkpoint/{}".format(
                                        global_step))
                                saver.save(sess,
                                           "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward_state_MHA_GRU_conv_3/high_checkpoint/{}/".format(
                                               global_step) + "model_{}.ckpt".format(global_step))
                                print("save: ",
                                      "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward_state_MHA_GRU_conv_3/high_checkpoint/{}/".format(
                                          global_step) + "model_{}.ckpt".format(global_step))

                            high_critic_loss_record = open(
                                'D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward_state_MHA_GRU_conv_3/high_c_loss.txt',
                                'a')
                            high_critic_loss_record.write(str(hierachical_critic.cost_his[-50:]) + '\n')
                            high_critic_loss_record.close()

                            high_actor_loss_record = open(
                                'D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward_state_MHA_GRU_conv_3/high_a_loss.txt',
                                'a')
                            high_actor_loss_record.write(str(hierachical_actor.cost_his[-50:]) + '\n')
                            high_actor_loss_record.close()
                            ep_track_r = []

        T = T + 1

    # ep_rs_sum1 = sum(ep_track_r)
    # if 'running_reward_ep' not in globals():
    #     running_reward_ep = ep_rs_sum1
    # else:
    #     running_reward_ep = running_reward_ep * 0.95 + ep_rs_sum1 * 0.05
    # print("episode:", global_step, "  reward:", running_reward_ep)
    # episode_ep_reward.append(running_reward_ep)
    #
    # # hierachical_network.learn()
    #
    # ep_rs_average = sum(ep_track_r) / len(ep_track_r)
    # # running_reward_ep = ep_rs_sum1
    # print('episode:', global_step, ',len(ep_track_r):', len(ep_track_r), ',ep_average_reward', ep_rs_average)
    # episode_ep_average_reward.append(ep_rs_average)
    #
    # low_level_ep_rs_average = sum(low_level_ep_track_r)/len(low_level_ep_track_r)
    # if 'low_level_running_reward_ep' not in globals():
    #     low_level_running_reward_ep = low_level_ep_rs_average
    # else:
    #     low_level_running_reward_ep = low_level_running_reward_ep * 0.95 + low_level_ep_rs_average * 0.05
    # print("episode:", global_step, "  low level reward:", low_level_running_reward_ep)
    #
    # # running_reward_ep = ep_rs_sum1
    # print('episode:', global_step, ',len(ep_track_r):', len(low_level_ep_track_r), ',low level ep_average_reward', low_level_ep_rs_average)
    #
    # global_step += 1
    # # 觉得差不多了（ep_reward/reward上升到稳定；loss稳定，单看loss不行）就手动save模型去训练
    # with open(
    #         "D:/exchange/train/optimize-2022-1-19/main/20220204_attention_conv_times_batch_50_courier_reward/h=10-3 l=10-2/train_log/train_20220125_time_iter7_to_14.txt",
    #         'a+') as logf:
    #     print("episode:", global_step, ",reward:", running_reward_ep, ',len(ep_track_r):', len(ep_track_r),
    #           ',ep_average_reward', ep_rs_average, file=logf)
    #     print('episode:', global_step, ",low_level_reward:", low_level_running_reward_ep, ',len(ep_track_r):',
    #           len(low_level_ep_track_r), ',low level ep_average_reward',
    #           low_level_ep_rs_average, file=logf)
    #
    # if (ep_rs_average>=1 and low_level_ep_rs_average>=1) or global_step % 5 == 0:
    #     os.mkdir(
    #         "D:/exchange/train/optimize-2022-1-19/main/20220204_attention_conv_times_batch_50_courier_reward/h=10-3 l=10-2/checkpoint/{}".format(
    #             global_step))
    #     saver.save(sess,
    #                "D:/exchange/train/optimize-2022-1-19/main/20220204_attention_conv_times_batch_50_courier_reward/h=10-3 l=10-2/checkpoint/{}/".format(
    #                    global_step) + "model_{}.ckpt".format(global_step))
    #     print("save: ",
    #           "D:/exchange/train/optimize-2022-1-19/main/20220204_attention_conv_times_batch_50_courier_reward/h=10-3 l=10-2/checkpoint/{}/".format(
    #               global_step) + "model_{}.ckpt".format(global_step))
    #
    #     high_critic_loss_record = open('D:/exchange/train/optimize-2022-1-19/main/20220204_attention_conv_times_batch_50_courier_reward/h=10-3 l=10-2/high_c_loss.txt','a')
    #     high_critic_loss_record.write(str(hierachical_critic.cost_his)+'\n')
    #
    #     high_actor_loss_record = open('D:/exchange/train/optimize-2022-1-19/main/20220204_attention_conv_times_batch_50_courier_reward/h=10-3 l=10-2/high_a_loss.txt','a')
    #     high_actor_loss_record.write(str(hierachical_actor.cost_his)+'\n')
    #
    #     low_critic_loss_record = open('D:/exchange/train/optimize-2022-1-19/main/20220204_attention_conv_times_batch_50_courier_reward/h=10-3 l=10-2/low_c_loss.txt','a')
    #     low_critic_loss_record.write(str(critic.cost_his)+'\n')
    #
    #     low_actor_loss_record = open('D:/exchange/train/optimize-2022-1-19/main/20220204_attention_conv_times_batch_50_courier_reward/h=10-3 l=10-2/low_a_loss.txt','a')
    #     low_actor_loss_record.write(str(actor.cost_his)+'\n')

# 骑手间距离的变化趋势---机遇式相遇特征distance_variance_k_list[变成action filter--返回结果时仍可检测到]
# # 2.1) action_filter
# # 距离单位为km，10m=0.01km
# x_gps_10s_location_list = []  # len=6
# y_gps_10s_location_list = []
# # 映射10s内的轨迹细粒度化
# if T - 1 in online_couriers[online_courier_count_x].route_time_step.keys():
#     last_10s_gps_lon = online_couriers[online_courier_count_x].route_time_step[T - 1].lon
#     last_10s_gps_lat = online_couriers[online_courier_count_x].route_time_step[T - 1].lat
#     cur_10s_gps_lon = online_couriers[online_courier_count_x].lon
#     cur_10s_gps_lat = online_couriers[online_courier_count_x].lat
#
#     lon_variation = (cur_order_next_stop_lon - last_10s_gps_lon) / 10
#     lat_variation = (cur_order_next_stop_lat - last_10s_gps_lat) / 10
#
#     for count_loc in range(0, 11):
#         x_gps_10s_location_list.append(Loc(last_10s_gps_lat + count_loc * lat_variation,
#                                            last_10s_gps_lon + count_loc * lon_variation))
# else:
#     for count_loc in range(0, 11):
#         x_gps_10s_location_list.append(online_couriers[online_courier_count_x])
# if T - 1 in online_couriers[online_courier_count_y].route_time_step.keys():
#     last_10s_gps_lon = online_couriers[online_courier_count_y].route_time_step[T - 1].lon
#     last_10s_gps_lat = online_couriers[online_courier_count_y].route_time_step[T - 1].lat
#     cur_10s_gps_lon = online_couriers[online_courier_count_y].lon
#     cur_10s_gps_lat = online_couriers[online_courier_count_y].lat
#
#     lon_variation = (cur_order_next_stop_lon - last_10s_gps_lon) / 10
#     lat_variation = (cur_order_next_stop_lat - last_10s_gps_lat) / 10
#
#     for count_loc in range(0, 11):
#         y_gps_10s_location_list.append(Loc(last_10s_gps_lat + count_loc * lat_variation,
#                                            last_10s_gps_lon + count_loc * lon_variation))
# else:
#     for count_loc in range(0, 11):
#         y_gps_10s_location_list.append(online_couriers[online_courier_count_y])
# distance_list = []
# for loc_item_id in range(len(x_gps_10s_location_list)):
#     temp_dis = get_distance_hav(x_gps_10s_location_list[loc_item_id].lat,
#                                 x_gps_10s_location_list[loc_item_id].lon,
#                                 y_gps_10s_location_list[loc_item_id].lat,
#                                 y_gps_10s_location_list[loc_item_id].lon)
#     distance_list.append(temp_dis)
# # 骑手间距离的变化趋势
# distance_variance_k_list = []
# for distance_item_id in range(len(distance_list)):
#     k = distance_variance_k_list[distance_item_id + 1] - distance_variance_k_list[distance_item_id]
#     distance_variance_k_list.append(k)
# 2)对 相遇作决策，看两个人要不要换


#                         # 考虑相遇的换单  ————————相遇模块的处理
#                         # 1.（历史数据+检测的位置）骑手间距离的变化趋势---机遇式相遇特征distance_variance_k_list[变成action filter--返回结果时仍可检测到]
#                         # 2.订单相似度
#                         # 3.两人的订单数
#                         # 4、相遇位置的安全性[用个表----作为路段得安全性矩阵表---事故易发地]
#                         # 5、是否存在即将超时单（由于会先送其他单），但只有一个单的就别换了！
#
#                         # 相遇时间，地点(后面看是否要归一化)---粗略的位置，融合gps数据
#                         encounter_location_lat = (online_couriers[online_courier_count_x].lat +
#                                                   online_couriers[online_courier_count_y].lat) / 2
#                         encounter_location_lon = (online_couriers[online_courier_count_x].lon +
#                                                   online_couriers[online_courier_count_y].lon) / 2
#
#                         # 距离单位为km，10m=0.01km__相遇倾向
#                         x_gps_1s_location_list = []  # len=3
#                         y_gps_1s_location_list = []
#                         # 映射10s内的轨迹细粒度化
#                         if T - 1 in online_couriers[online_courier_count_x].route_time_step.keys():
#                             last_1s_gps_lon = online_couriers[online_courier_count_x].route_time_step[T - 1].lon
#                             last_1s_gps_lat = online_couriers[online_courier_count_x].route_time_step[T - 1].lat
#                             cur_1s_gps_lon = online_couriers[online_courier_count_x].lon
#                             cur_1s_gps_lat = online_couriers[online_courier_count_x].lat
#
#                             lon_variation = (cur_1s_gps_lon - last_1s_gps_lon) / 3
#                             lat_variation = (cur_1s_gps_lat - last_1s_gps_lat) / 3
#
#                             for count_loc in range(0, 4):
#                                 x_gps_1s_location_list.append(Loc(last_1s_gps_lat + count_loc * lat_variation,
#                                                                   last_1s_gps_lon + count_loc * lon_variation))
#                         else:
#                             for count_loc in range(0, 4):
#                                 x_gps_1s_location_list.append(online_couriers[online_courier_count_x])
#                         if T - 1 in online_couriers[online_courier_count_y].route_time_step.keys():
#                             last_1s_gps_lon = online_couriers[online_courier_count_y].route_time_step[T - 1].lon
#                             last_1s_gps_lat = online_couriers[online_courier_count_y].route_time_step[T - 1].lat
#                             cur_1s_gps_lon = online_couriers[online_courier_count_y].lon
#                             cur_1s_gps_lat = online_couriers[online_courier_count_y].lat
#
#                             lon_variation = (cur_1s_gps_lon - last_1s_gps_lon) / 3
#                             lat_variation = (cur_1s_gps_lat - last_1s_gps_lat) / 3
#
#                             for count_loc in range(0, 4):
#                                 y_gps_1s_location_list.append(Loc(last_1s_gps_lat + count_loc * lat_variation,
#                                                                   last_1s_gps_lon + count_loc * lon_variation))
#                         else:
#                             for count_loc in range(0, 4):
#                                 y_gps_1s_location_list.append(Loc(online_couriers[online_courier_count_y].lat,
#                                                                   online_couriers[online_courier_count_y].lon))
#                         distance_list = []
#                         for loc_item_id in range(len(x_gps_1s_location_list)):
#                             temp_dis = get_distance_hav(x_gps_1s_location_list[loc_item_id].lat,
#                                                         x_gps_1s_location_list[loc_item_id].lon,
#                                                         y_gps_1s_location_list[loc_item_id].lat,
#                                                         y_gps_1s_location_list[loc_item_id].lon)
#                             distance_list.append(temp_dis)
#                         # 骑手间距离的变化趋势
#                         # distance_variance_k_list = []
#                         # for distance_item_id in range(len(distance_list)):
#                         #     k = distance_variance_k_list[distance_item_id + 1] - distance_variance_k_list[distance_item_id]
#                         #     distance_variance_k_list.append(k)
#                         # high_level_state_input.append(k)
#
#                         courier1_max_order_predicted_remaining_time = 0  # estimated deliver time - cur time
#                         courier1_max_order_remaining_time = 0  # promise_deliver time - current time
#                         courier1_order_num = online_couriers[online_courier_count_x].cur_order_num
#
#                         for order_item in online_couriers[online_courier_count_x].order_list:
#                             if order_item.dispatch_stage != 0:
#                                 order_item_cost_left_time = -9999
#                                 if online_couriers[online_courier_count_x].route_flag_to_be_updated == {}:
#                                     order_item_cost_left_time = 0
#                                 elif max(online_couriers[online_courier_count_x].route_flag_to_be_updated.keys()) <= T:
#                                     order_item_cost_left_time = 0
#                                 else:
#                                     for time_step_id in range(T, max(
#                                             online_couriers[
#                                                 online_courier_count_x].route_flag_to_be_updated.keys()) + 1):
#                                         for state_change_id in range(
#                                                 len(online_couriers[online_courier_count_x].route_flag_to_be_updated[
#                                                         time_step_id])):
#                                             if \
#                                                     online_couriers[online_courier_count_x].route_flag_to_be_updated[
#                                                         time_step_id][
#                                                         state_change_id] == (
#                                                             cur_this_order_loc_id, 0):
#                                                 order_item_cost_left_time = time_step_id - T
#                                                 break
#
#                                 if order_item_cost_left_time == -9999:
#                                     print('debug')
#
#                                 if courier1_max_order_remaining_time < order_item_cost_left_time:
#                                     courier1_max_order_remaining_time = order_item_cost_left_time
#
#                         courier2_max_order_predicted_remaining_time = 0  # estimated deliver time - cur time
#                         courier2_max_order_remaining_time = 0  # promise_deliver time - current time
#                         courier2_order_num = online_couriers[online_courier_count_y].cur_order_num
#
#                         for order_item in online_couriers[online_courier_count_y].order_list:
#                             if order_item.dispatch_stage != 0:
#                                 order_item_cost_left_time = -9999
#                                 if online_couriers[online_courier_count_y].route_flag_to_be_updated == {}:
#                                     order_item_cost_left_time = 0
#                                 elif max(online_couriers[online_courier_count_y].route_flag_to_be_updated.keys()) <= T:
#                                     order_item_cost_left_time = 0
#                                 else:
#                                     for time_step_id in range(T, max(
#                                             online_couriers[
#                                                 online_courier_count_y].route_flag_to_be_updated.keys()) + 1):
#                                         for state_change_id in range(
#                                                 len(online_couriers[online_courier_count_y].route_flag_to_be_updated[
#                                                         time_step_id])):
#                                             if \
#                                                     online_couriers[online_courier_count_y].route_flag_to_be_updated[
#                                                         time_step_id][
#                                                         state_change_id] == (
#                                                             cur_this_order_loc_id, 0):
#                                                 order_item_cost_left_time = time_step_id - T
#                                                 break
#
#                                 if order_item_cost_left_time == -9999:
#                                     print('debug')
#
#                                 if courier2_max_order_remaining_time < order_item_cost_left_time:
#                                     courier2_max_order_remaining_time = order_item_cost_left_time
#
#                         high_level_state_input = [T, encounter_location_lat, encounter_location_lon,
#                                                   distance_list[0], distance_list[1], distance_list[2],
#                                                   distance_list[3],
#                                                   courier1_max_order_remaining_time, courier1_order_num,
#                                                   courier2_max_order_remaining_time, courier2_order_num
#                                                   ]
#
#                         exchange_willingness = hierachical_network.choose_action(high_level_state_input)  # 0 不换，1 换
#
#                         courier_encounter_event = Encounter(online_couriers[online_courier_count_x].courier_id,
#                                                             online_couriers[online_courier_count_y].courier_id,
#                                                             T)
#                         env.encounter_exchange_event.append(courier_encounter_event)
#
#                         # 供低层订单作决策
#                         cur_time_step_encounter_events.append(courier_encounter_event)
#                         if exchange_willingness == 1:
#                             cur_time_step_exchange_events.append(courier_encounter_event)
#                             cur_time_step_exchange_events_state_input.append(high_level_state_input)
#
#                         # 供高层骑手作决策
#                         cur_time_step_encounter_event_state_input.append(high_level_state_input)
#                         cur_time_step_encounter_event_action.append(exchange_willingness)
