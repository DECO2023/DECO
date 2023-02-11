'''
1、处理一下输入：之前7-10有些promise=0 的订单需要过滤；
2、至少先保证没换单前【两个结果一致】
'''
import math
import pickle
import tensorflow as tf
from simulator.encounter import Encounter
from simulator.envs import *
import numpy as np
from algorithm.DQN import *
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
# get_distance_hav(online_couriers[online_courier_count_x].lat,
#                                                               online_couriers[online_courier_count_x].lon,
#                                                               online_couriers[online_courier_count_y].lat,
#                                                               online_couriers[online_courier_count_y].lon)


# 输入
# 一天的所有订单10.12,未转网格，未转时间步
order_real = pickle.load(open("D:/exchange/dataProcessing/all_orders_target_20201012.pkl", 'rb'))
# 10.12骑手第一次出现的时间及地点, 未转网格，未转时间步
couriers_init = pickle.load(open("D:/exchange/dataProcessing/courier_init_20201012.pkl", 'rb'))

# 时间步:10s，平台派单(根据距离最近)
# 时间步: 遍历检查是否存在相遇可换单事件：判断可换单的逻辑

# 全局参数的初始化
global_step = 0
repeat_time = 10000
gamma = 0.9  # RL中计算未来reward的 折扣因子

# learning_rate_Hierarical_Actor = 1e-5
# learning_rate_Actor = 1e-5
# learning_rate_Critic = 1e-3

max_iter = 86400  # 10s一个时间步=8640，可能有很多空白时间点-----10min

# 骑手当前订单数,预测的骑手的下一站经纬度.送完手中所有单还需时间,所持订单【其他状态：相遇骑手的状态】--最多6个订单
state_dim = 13
action_dim = 2
# h_state_dim = 19
# h_action_dim = 2

max_train_step = 1000

tf.compat.v1.set_random_seed(1)
# 实际网络
log_dir = "D:/exchange/train/baseline/DQN_train_logs/DQN_train_logs/"

# 新训练模型
# sess = tf.compat.v1.Session()
# # hierachical_network = High_Level_Network(sess, h_state_dim, h_action_dim, learning_rate_Hierarical_Actor)
# # actor = Actor(sess, state_dim, action_dim, learning_rate_Actor)
# # critic = Critic(sess, state_dim, learning_rate_Critic)
DQN = DeepQNetwork(action_dim, state_dim, learning_rate=0.01, reward_decay=0.9, e_greedy=0.9,
                   replace_target_iter=200, memory_size=2000)
# sess.run(tf.compat.v1.global_variables_initializer())
# saver = tf.compat.v1.train.Saver()

# 用跑过的模型继续训练
sess = tf.compat.v1.Session()
# saver = tf.compat.v1.train.import_meta_graph('D:/exchange/train/run2021-7-1/DQN_train_logs/model.ckpt.meta')
# saver.restore(sess, 'D:/exchange/train/run2021-7-1/DQN_train_logs/model.ckpt')
# # saver.restore(sess, 'D:/exchange/train/run2021-7-1/DQN_train_logs/model.ckpt')
saver = tf.compat.v1.train.Saver()
saver.restore(sess,'D:/exchange/train/baseline/DQN_train_logs/DQN_train_logs/model.ckpt')
# episode_ep_reward = []
# episode_ep_average_reward = []
# train_DQN_count = 0
# while True:
#
#     ep_track_r = []
if __name__ == "__main__":
    env = Region(couriers_init, order_real)
    env_state = env.env_initialize()

    order_to_wait_to_next_timestep = []  # 当前时间步未得到分派的订单

    event_id = 0
    episode_id = 0
    end = False
    # train:10.12
    T = 0
    while T < max_iter:

        # *********************1********************平台派单（按10min 按批派单）(根据距离最近),来一个新订单就派单
        time_step_courier_state_file_name_exchange = "D:/exchange/train/baseline/DQN-record/time_step_" + str(
            T) + "_courier_state.txt"
        # 每一个时间步，用txt文档记录，骑手状态及分派状态的记录。
        print(T)
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
                # if chosen_courier.courier_id == 2053730:
                #     print('debug')
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
        # cur_time_step_encounter_event_high_level_state_input_list = []
        # cur_time_step_encounter_event_high_level_next_state_list = []
        # cur_time_step_encounter_event_high_level_action_list = []
        # cur_time_step_encounter_event_high_level_reward_list = []

        # high_level_reward_track = []
        # 将遍历得到相遇的骑手(id1,id2)[相遇对象]存入day_encounter[time_step],依次对每个时间步的encounter对象做换单决策
        for online_courier_count_x in range(len(online_couriers)):
            for online_courier_count_y in range(online_courier_count_x + 1, len(online_couriers)):
                # 1）模拟beacon检测到了相遇
                courier_encounter_distance = get_distance_hav(online_couriers[online_courier_count_x].lat,
                                                              online_couriers[online_courier_count_x].lon,
                                                              online_couriers[online_courier_count_y].lat,
                                                              online_couriers[online_courier_count_y].lon)
                if courier_encounter_distance < 0.015:  # beacon检测到
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
                        # encounter_start_time = T
                        # encounter_start_courier1_lat = online_couriers[online_courier_count_x].lat
                        # encounter_start_courier1_lon = online_couriers[online_courier_count_x].lon
                        # encounter_start_courier2_lat = online_couriers[online_courier_count_y].lat
                        # encounter_start_courier2_lon = online_couriers[online_courier_count_y].lon
                        # encounter_start_courier1_next_stop_lat = 0
                        # encounter_start_courier1_next_stop_lon = 0
                        # encounter_start_courier2_next_stop_lat = 0
                        # encounter_start_courier2_next_stop_lon = 0
                        # encounter_courier1_cur_order_cur_stage_remaining_time = 0
                        # encounter_courier2_cur_order_cur_stage_remaining_time = 0
                        #
                        # if T + 1 not in online_couriers[online_courier_count_x].route_flag_to_be_updated.keys() or \
                        #         online_couriers[online_courier_count_x].cur_order_num == 0 or len(
                        #     online_couriers[online_courier_count_x].route_flag_to_be_updated[T + 1]) == 0:
                        #     encounter_start_courier1_next_stop_lat = online_couriers[online_courier_count_x].lat
                        #     encounter_start_courier1_next_stop_lon = online_couriers[online_courier_count_x].lon
                        #     encounter_courier1_cur_order_cur_stage_remaining_time = 0
                        # else:
                        #     if len(online_couriers[online_courier_count_x].route_flag_to_be_updated[T + 1]) > 1 and \
                        #             online_couriers[online_courier_count_x].route_flag_to_be_updated[T + 2] != []:
                        #         courier1_next_stop_order_loc_id = -1
                        #         detect_time_added = 1
                        #         while courier1_next_stop_order_loc_id == -1 and \
                        #                 online_couriers[online_courier_count_x].route_flag_to_be_updated[
                        #                     T + detect_time_added + 1] != []:
                        #             for flag_item in online_couriers[online_courier_count_x].route_flag_to_be_updated[
                        #                 T + detect_time_added]:
                        #                 for next_time_flag_item in \
                        #                         online_couriers[online_courier_count_x].route_flag_to_be_updated[
                        #                             T + detect_time_added + 1]:
                        #                     if flag_item == next_time_flag_item:
                        #                         courier1_next_stop_order_loc_id = next_time_flag_item[0]
                        #                         break
                        #             detect_time_added += 1
                        #         if courier1_next_stop_order_loc_id == -1:
                        #             # 都是快送完的单
                        #             for flag_item in online_couriers[online_courier_count_x].route_flag_to_be_updated[
                        #                 T + 1]:
                        #                 if flag_item[1] != 2:
                        #                     courier1_next_stop_order_loc_id = flag_item[0]
                        #                     break
                        #             if courier1_next_stop_order_loc_id == -1:
                        #                 print('debug')
                        #     else:
                        #         courier1_next_stop_order_loc_id = \
                        #             online_couriers[online_courier_count_x].route_flag_to_be_updated[T + 1][0][0]
                        #
                        #     if courier1_next_stop_order_loc_id > len(
                        #             online_couriers[online_courier_count_x].available_loc_real_time):
                        #         print('debug')
                        #     if online_couriers[online_courier_count_x].available_loc_real_time[
                        #         courier1_next_stop_order_loc_id] == 0:
                        #         # 该单下一时刻送完了
                        #         encounter_start_courier1_next_stop_lat = online_couriers[online_courier_count_x].lat
                        #         encounter_start_courier1_next_stop_lon = online_couriers[online_courier_count_x].lon
                        #         encounter_courier1_cur_order_cur_stage_remaining_time = 1
                        #     else:
                        #         encounter_start_courier1_next_stop_lat = \
                        #             online_couriers[online_courier_count_x].available_loc_real_time[
                        #                 online_couriers[online_courier_count_x].route_flag_to_be_updated[T + 1][0][
                        #                     0]].lat
                        #         encounter_start_courier1_next_stop_lon = \
                        #             online_couriers[online_courier_count_x].available_loc_real_time[
                        #                 online_couriers[online_courier_count_x].route_flag_to_be_updated[T + 1][0][
                        #                     0]].lon
                        #
                        #         cur_order_id_in_courier_order_list = \
                        #             online_couriers[online_courier_count_x].route_flag_to_be_updated[T + 1][0][0]
                        #         cur_order_stage_in_courier_order_list = \
                        #             online_couriers[online_courier_count_x].route_flag_to_be_updated[T + 1][0][1]
                        #         objective_order_flag = -1
                        #         if cur_order_stage_in_courier_order_list == 1:
                        #             objective_order_flag = 2
                        #         else:
                        #             objective_order_flag = 0
                        #
                        #         objective_route_flag_item = (cur_order_id_in_courier_order_list, objective_order_flag)
                        #
                        #         cur_time = T + 1
                        #         order_next_step_need_time = 0
                        #         while cur_time > T:
                        #             route_flag_item = online_couriers[online_courier_count_x].route_flag_to_be_updated[
                        #                 cur_time]
                        #             if objective_route_flag_item in route_flag_item:
                        #                 order_next_step_need_time = cur_time
                        #                 break
                        #             cur_time += 1
                        #         encounter_courier1_cur_order_cur_stage_remaining_time = order_next_step_need_time - T
                        #
                        # if T + 1 not in online_couriers[online_courier_count_y].route_flag_to_be_updated.keys() or \
                        #         online_couriers[online_courier_count_y].cur_order_num == 0 or len(
                        #     online_couriers[online_courier_count_y].route_flag_to_be_updated[T + 1]) == 0:
                        #     encounter_start_courier2_next_stop_lat = online_couriers[online_courier_count_y].lat
                        #     encounter_start_courier2_next_stop_lon = online_couriers[online_courier_count_y].lon
                        #     encounter_courier2_cur_order_cur_stage_remaining_time = 0
                        # else:
                        #     if len(online_couriers[online_courier_count_y].route_flag_to_be_updated[T + 1]) > 1 and \
                        #             online_couriers[online_courier_count_y].route_flag_to_be_updated[T + 2] != []:
                        #         courier2_next_stop_order_loc_id = -1
                        #         detect_time_added = 1
                        #         while courier2_next_stop_order_loc_id == -1 and \
                        #                 online_couriers[online_courier_count_y].route_flag_to_be_updated[
                        #                     T + detect_time_added + 1] != []:
                        #             for flag_item in \
                        #                     online_couriers[online_courier_count_y].route_flag_to_be_updated[
                        #                         T + detect_time_added]:
                        #                 for next_time_flag_item in \
                        #                         online_couriers[online_courier_count_y].route_flag_to_be_updated[
                        #                             T + detect_time_added + 1]:
                        #                     if flag_item == next_time_flag_item:
                        #                         courier2_next_stop_order_loc_id = next_time_flag_item[0]
                        #                         break
                        #             detect_time_added += 1
                        #         if courier2_next_stop_order_loc_id == -1:
                        #             # 都是快送完的单
                        #             for flag_item in \
                        #                     online_couriers[online_courier_count_y].route_flag_to_be_updated[
                        #                         T + 1]:
                        #                 if flag_item[1] != 2:
                        #                     courier2_next_stop_order_loc_id = flag_item[0]
                        #                     break
                        #             if courier2_next_stop_order_loc_id == -1:
                        #                 print('debug')
                        #     else:
                        #         courier2_next_stop_order_loc_id = \
                        #             online_couriers[online_courier_count_y].route_flag_to_be_updated[T + 1][0][0]
                        #
                        #     if courier2_next_stop_order_loc_id > len(
                        #             online_couriers[online_courier_count_y].available_loc_real_time):
                        #         print('debug')
                        #     if online_couriers[online_courier_count_y].available_loc_real_time[
                        #         courier2_next_stop_order_loc_id] == 0:
                        #         # 该单下一时刻送完了
                        #         encounter_start_courier2_next_stop_lat = online_couriers[online_courier_count_y].lat
                        #         encounter_start_courier2_next_stop_lon = online_couriers[online_courier_count_y].lon
                        #         encounter_courier2_cur_order_cur_stage_remaining_time = 1
                        #     else:
                        #         encounter_start_courier2_next_stop_lat = \
                        #             online_couriers[online_courier_count_y].available_loc_real_time[
                        #                 online_couriers[online_courier_count_y].route_flag_to_be_updated[T + 1][0][
                        #                     0]].lat
                        #         encounter_start_courier2_next_stop_lon = \
                        #             online_couriers[online_courier_count_y].available_loc_real_time[
                        #                 online_couriers[online_courier_count_y].route_flag_to_be_updated[T + 1][0][
                        #                     0]].lon
                        #
                        #         cur_order_id_in_courier_order_list = \
                        #             online_couriers[online_courier_count_y].route_flag_to_be_updated[T + 1][0][0]
                        #         cur_order_stage_in_courier_order_list = \
                        #             online_couriers[online_courier_count_y].route_flag_to_be_updated[T + 1][0][1]
                        #         objective_order_flag = -1
                        #         if cur_order_stage_in_courier_order_list == 1:
                        #             objective_order_flag = 2
                        #         else:
                        #             objective_order_flag = 0
                        #
                        #         objective_route_flag_item = (cur_order_id_in_courier_order_list, objective_order_flag)
                        #
                        #         cur_time = T + 1
                        #         order_next_step_need_time = 0
                        #         while cur_time > T:
                        #             route_flag_item = online_couriers[online_courier_count_y].route_flag_to_be_updated[
                        #                 cur_time]
                        #             if objective_route_flag_item in route_flag_item:
                        #                 order_next_step_need_time = cur_time
                        #                 break
                        #             cur_time += 1
                        #         encounter_courier2_cur_order_cur_stage_remaining_time = order_next_step_need_time - T
                        #
                        # # courier-order state_input preprocess
                        # courier1_max_order_remaining_time = 0  # estimated deliver time - cur time
                        # # courier1_max_order_promise_remaining_time = 0  # promise_deliver time - current time
                        # courier1_min_real_time_promise_variance_order_remaining_time = 9999999999  # 越小越好
                        # courier1_order_num = online_couriers[online_courier_count_x].cur_order_num
                        # if courier1_order_num > 0:
                        #     for order_item_id in range(len(online_couriers[online_courier_count_x].order_list)):
                        #
                        #         if online_couriers[online_courier_count_x].order_list[
                        #             order_item_id].dispatch_stage != 0:
                        #             cur_order_promise_remaining_time = \
                        #                 online_couriers[online_courier_count_x].order_list[
                        #                     order_item_id].promise_deliver_time - T
                        #             order_item_cost_left_time = -9999
                        #             if online_couriers[online_courier_count_x].route_flag_to_be_updated == {}:
                        #                 order_item_cost_left_time = 0
                        #             elif max(online_couriers[
                        #                          online_courier_count_x].route_flag_to_be_updated.keys()) <= T:
                        #                 order_item_cost_left_time = 0
                        #             else:
                        #                 for time_step_id in range(T, max(
                        #                         online_couriers[
                        #                             online_courier_count_x].route_flag_to_be_updated.keys()) + 1):
                        #                     for state_change_id in range(
                        #                             len(online_couriers[
                        #                                     online_courier_count_x].route_flag_to_be_updated[
                        #                                     time_step_id])):
                        #                         if \
                        #                                 online_couriers[
                        #                                     online_courier_count_x].route_flag_to_be_updated[
                        #                                     time_step_id][
                        #                                     state_change_id] == (
                        #                                         order_item_id, 0):
                        #                             order_item_cost_left_time = time_step_id - T
                        #                             break
                        #
                        #             if order_item_cost_left_time == -9999:
                        #                 print('debug')
                        #
                        #             if courier1_min_real_time_promise_variance_order_remaining_time > \
                        #                     cur_order_promise_remaining_time - order_item_cost_left_time:
                        #                 courier1_min_real_time_promise_variance_order_remaining_time = \
                        #                     cur_order_promise_remaining_time - order_item_cost_left_time
                        #             if courier1_max_order_remaining_time < order_item_cost_left_time:
                        #                 courier1_max_order_remaining_time = order_item_cost_left_time
                        # else:
                        #     courier1_min_real_time_promise_variance_order_remaining_time = 0
                        #
                        # courier2_max_order_remaining_time = 0  # estimated deliver time - cur time
                        # # courier2_max_order_promise_remaining_time = 0  # promise_deliver time - current time
                        # courier2_min_real_time_promise_variance_order_remaining_time = 9999999999  # 越小越好
                        # courier2_order_num = online_couriers[online_courier_count_y].cur_order_num
                        # if courier2_order_num > 0:
                        #     for order_item_id in range(len(online_couriers[online_courier_count_y].order_list)):
                        #         if online_couriers[online_courier_count_y].order_list[
                        #             order_item_id].dispatch_stage != 0:
                        #             cur_order_promise_remaining_time = \
                        #                 online_couriers[online_courier_count_y].order_list[
                        #                     order_item_id].promise_deliver_time - T
                        #             order_item_cost_left_time = -9999
                        #             if online_couriers[online_courier_count_y].route_flag_to_be_updated == {}:
                        #                 order_item_cost_left_time = 0
                        #             elif max(online_couriers[
                        #                          online_courier_count_y].route_flag_to_be_updated.keys()) <= T:
                        #                 order_item_cost_left_time = 0
                        #             else:
                        #                 for time_step_id in range(T, max(
                        #                         online_couriers[
                        #                             online_courier_count_y].route_flag_to_be_updated.keys()) + 1):
                        #                     for state_change_id in range(
                        #                             len(online_couriers[
                        #                                     online_courier_count_y].route_flag_to_be_updated[
                        #                                     time_step_id])):
                        #                         if \
                        #                                 online_couriers[
                        #                                     online_courier_count_y].route_flag_to_be_updated[
                        #                                     time_step_id][
                        #                                     state_change_id] == (
                        #                                         order_item_id, 0):
                        #                             order_item_cost_left_time = time_step_id - T
                        #                             break
                        #
                        #             if order_item_cost_left_time == -9999:
                        #                 print('debug')
                        #             if courier2_min_real_time_promise_variance_order_remaining_time > \
                        #                     cur_order_promise_remaining_time - order_item_cost_left_time:
                        #                 courier2_min_real_time_promise_variance_order_remaining_time = \
                        #                     cur_order_promise_remaining_time - order_item_cost_left_time
                        #             if courier2_max_order_remaining_time < order_item_cost_left_time:
                        #                 courier2_max_order_remaining_time = order_item_cost_left_time
                        # else:
                        #     courier2_min_real_time_promise_variance_order_remaining_time = 0
                        #
                        # # courier-order whole similarity preprocess
                        # courier1_self_order_similarity = 0
                        # courier1_self_order_similarity_list = []
                        # courier1_courier2_order_similarity = 0
                        # courier1_courier2_order_similarity_list = []
                        #
                        # courier2_self_order_similarity = 0
                        # courier2_self_order_similarity_list = []
                        # courier2_courier1_order_similarity = 0
                        # courier2_courier1_order_similarity_list = []
                        #
                        # courier1_order_next_stop_list = []
                        # for courier1_order_item in range(len(online_couriers[online_courier_count_x].order_list)):
                        #     if online_couriers[online_courier_count_x].order_list[
                        #         courier1_order_item].dispatch_stage != 0:
                        #         if online_couriers[online_courier_count_x].order_list[
                        #             courier1_order_item].dispatch_stage == 1:
                        #             courier1_order_next_stop_list.append(Loc(
                        #                 online_couriers[online_courier_count_x].order_list[
                        #                     courier1_order_item].shop_latitude,
                        #                 online_couriers[online_courier_count_x].order_list[
                        #                     courier1_order_item].shop_longitude))
                        #         elif online_couriers[online_courier_count_x].order_list[
                        #             courier1_order_item].dispatch_stage == 2:
                        #             courier1_order_next_stop_list.append(Loc(
                        #                 online_couriers[online_courier_count_x].order_list[
                        #                     courier1_order_item].user_latitude,
                        #                 online_couriers[online_courier_count_x].order_list[
                        #                     courier1_order_item].user_longitude))
                        # courier2_order_next_stop_list = []
                        # for courier2_order_item in range(len(online_couriers[online_courier_count_y].order_list)):
                        #     if online_couriers[online_courier_count_y].order_list[
                        #         courier2_order_item].dispatch_stage != 0:
                        #         if online_couriers[online_courier_count_y].order_list[
                        #             courier2_order_item].dispatch_stage == 1:
                        #             courier2_order_next_stop_list.append(Loc(
                        #                 online_couriers[online_courier_count_y].order_list[
                        #                     courier2_order_item].shop_latitude,
                        #                 online_couriers[online_courier_count_y].order_list[
                        #                     courier2_order_item].shop_longitude))
                        #         elif online_couriers[online_courier_count_y].order_list[
                        #             courier2_order_item].dispatch_stage == 2:
                        #             courier2_order_next_stop_list.append(Loc(
                        #                 online_couriers[online_courier_count_y].order_list[
                        #                     courier2_order_item].user_latitude,
                        #                 online_couriers[online_courier_count_y].order_list[
                        #                     courier2_order_item].user_longitude))
                        #
                        # if courier1_order_num > 1:
                        #     for courier1_compute_similarity_id1 in range(0, len(courier1_order_next_stop_list)):
                        #         for courier1_compute_similarity_id2 in range(courier1_compute_similarity_id1 + 1,
                        #                                                      len(courier1_order_next_stop_list)):
                        #             cur_simi = 0
                        #             cur_order_next_stop_lat = courier1_order_next_stop_list[
                        #                 courier1_compute_similarity_id1].lat
                        #             cur_order_next_stop_lon = courier1_order_next_stop_list[
                        #                 courier1_compute_similarity_id1].lon
                        #             cur_order_cur_lat = encounter_start_courier1_lat
                        #             cur_order_cur_lon = encounter_start_courier1_lon
                        #             this_order_next_stop_lat = courier1_order_next_stop_list[
                        #                 courier1_compute_similarity_id2].lat
                        #             this_order_next_stop_lon = courier1_order_next_stop_list[
                        #                 courier1_compute_similarity_id2].lon
                        #             this_order_cur_lat = encounter_start_courier1_lat
                        #             this_order_cur_lon = encounter_start_courier1_lon
                        #             if (
                        #                     cur_order_next_stop_lat - cur_order_cur_lat == 0 and cur_order_next_stop_lon - cur_order_cur_lon == 0) or \
                        #                     (
                        #                             this_order_next_stop_lat - this_order_cur_lat == 0 and this_order_next_stop_lon - this_order_cur_lon == 0):
                        #                 cur_simi = 0
                        #             else:
                        #                 cur_simi = cosine_dis(np.array([cur_order_next_stop_lat - cur_order_cur_lat,
                        #                                                 cur_order_next_stop_lon - cur_order_cur_lon]),
                        #                                       np.array(
                        #                                           [this_order_next_stop_lat - this_order_cur_lat,
                        #                                            this_order_next_stop_lon - this_order_cur_lon]))
                        #             courier1_self_order_similarity_list.append(cur_simi)
                        #     courier1_self_order_similarity = np.sum(courier1_self_order_similarity_list) / len(
                        #         courier1_self_order_similarity_list)
                        # else:
                        #     courier1_self_order_similarity = 0
                        #
                        # if courier1_order_num > 0 and courier2_order_num > 0:
                        #     for courier1_courier2_compute_similarity_c1 in range(len(courier1_order_next_stop_list)):
                        #         cur_order_exchange_simi = []
                        #         for courier1_courier2_compute_similarity_c2 in range(
                        #                 len(courier2_order_next_stop_list)):
                        #             cur_simi = 0
                        #             cur_order_next_stop_lat = courier1_order_next_stop_list[
                        #                 courier1_courier2_compute_similarity_c1].lat
                        #             cur_order_next_stop_lon = courier1_order_next_stop_list[
                        #                 courier1_courier2_compute_similarity_c1].lon
                        #             cur_order_cur_lat = encounter_start_courier1_lat
                        #             cur_order_cur_lon = encounter_start_courier1_lon
                        #             this_order_next_stop_lat = courier2_order_next_stop_list[
                        #                 courier1_courier2_compute_similarity_c2].lat
                        #             this_order_next_stop_lon = courier2_order_next_stop_list[
                        #                 courier1_courier2_compute_similarity_c2].lon
                        #             this_order_cur_lat = encounter_start_courier2_lat
                        #             this_order_cur_lon = encounter_start_courier2_lon
                        #             if (
                        #                     cur_order_next_stop_lat - cur_order_cur_lat == 0 and cur_order_next_stop_lon - cur_order_cur_lon == 0) or \
                        #                     (
                        #                             this_order_next_stop_lat - this_order_cur_lat == 0 and this_order_next_stop_lon - this_order_cur_lon == 0):
                        #                 cur_simi = 0
                        #             else:
                        #                 cur_simi = cosine_dis(np.array([cur_order_next_stop_lat - cur_order_cur_lat,
                        #                                                 cur_order_next_stop_lon - cur_order_cur_lon]),
                        #                                       np.array(
                        #                                           [this_order_next_stop_lat - this_order_cur_lat,
                        #                                            this_order_next_stop_lon - this_order_cur_lon]))
                        #             cur_order_exchange_simi.append(cur_simi)
                        #         courier1_courier2_order_similarity_list.append(
                        #             np.sum(cur_order_exchange_simi) / len(cur_order_exchange_simi))
                        #     courier1_courier2_order_similarity = np.sum(courier1_courier2_order_similarity_list) / len(
                        #         courier1_courier2_order_similarity_list)
                        # else:
                        #     courier1_courier2_order_similarity = 0
                        #
                        # # 骑手2 相关的 相似度计算
                        # if courier2_order_num > 1:
                        #     for courier2_compute_similarity_id1 in range(0, len(courier2_order_next_stop_list)):
                        #         for courier2_compute_similarity_id2 in range(courier2_compute_similarity_id1 + 1,
                        #                                                      len(courier2_order_next_stop_list)):
                        #             cur_simi = 0
                        #             cur_order_next_stop_lat = courier2_order_next_stop_list[
                        #                 courier2_compute_similarity_id1].lat
                        #             cur_order_next_stop_lon = courier2_order_next_stop_list[
                        #                 courier2_compute_similarity_id1].lon
                        #             cur_order_cur_lat = encounter_start_courier2_lat
                        #             cur_order_cur_lon = encounter_start_courier2_lon
                        #             this_order_next_stop_lat = courier2_order_next_stop_list[
                        #                 courier2_compute_similarity_id2].lat
                        #             this_order_next_stop_lon = courier2_order_next_stop_list[
                        #                 courier2_compute_similarity_id2].lon
                        #             this_order_cur_lat = encounter_start_courier2_lat
                        #             this_order_cur_lon = encounter_start_courier2_lon
                        #             if (
                        #                     cur_order_next_stop_lat - cur_order_cur_lat == 0 and cur_order_next_stop_lon - cur_order_cur_lon == 0) or \
                        #                     (
                        #                             this_order_next_stop_lat - this_order_cur_lat == 0 and this_order_next_stop_lon - this_order_cur_lon == 0):
                        #                 cur_simi = 0
                        #             else:
                        #                 cur_simi = cosine_dis(np.array([cur_order_next_stop_lat - cur_order_cur_lat,
                        #                                                 cur_order_next_stop_lon - cur_order_cur_lon]),
                        #                                       np.array(
                        #                                           [this_order_next_stop_lat - this_order_cur_lat,
                        #                                            this_order_next_stop_lon - this_order_cur_lon]))
                        #             courier2_self_order_similarity_list.append(cur_simi)
                        #     courier2_self_order_similarity = np.sum(courier2_self_order_similarity_list) / len(
                        #         courier2_self_order_similarity_list)
                        # else:
                        #     courier2_self_order_similarity = 0
                        # if courier1_order_num > 0 and courier2_order_num > 0:
                        #     for courier2_courier1_compute_similarity_c2 in range(len(courier2_order_next_stop_list)):
                        #         cur_order_exchange_simi = []
                        #         for courier2_courier1_compute_similarity_c1 in range(
                        #                 len(courier1_order_next_stop_list)):
                        #             cur_simi = 0
                        #             cur_order_next_stop_lat = courier2_order_next_stop_list[
                        #                 courier2_courier1_compute_similarity_c2].lat
                        #             cur_order_next_stop_lon = courier2_order_next_stop_list[
                        #                 courier2_courier1_compute_similarity_c2].lon
                        #             cur_order_cur_lat = encounter_start_courier2_lat
                        #             cur_order_cur_lon = encounter_start_courier2_lon
                        #             this_order_next_stop_lat = courier1_order_next_stop_list[
                        #                 courier2_courier1_compute_similarity_c1].lat
                        #             this_order_next_stop_lon = courier1_order_next_stop_list[
                        #                 courier2_courier1_compute_similarity_c1].lon
                        #             this_order_cur_lat = encounter_start_courier1_lat
                        #             this_order_cur_lon = encounter_start_courier1_lon
                        #             if (
                        #                     cur_order_next_stop_lat - cur_order_cur_lat == 0 and cur_order_next_stop_lon - cur_order_cur_lon == 0) or \
                        #                     (
                        #                             this_order_next_stop_lat - this_order_cur_lat == 0 and this_order_next_stop_lon - this_order_cur_lon == 0):
                        #                 cur_simi = 0
                        #             else:
                        #                 cur_simi = cosine_dis(np.array([cur_order_next_stop_lat - cur_order_cur_lat,
                        #                                                 cur_order_next_stop_lon - cur_order_cur_lon]),
                        #                                       np.array(
                        #                                           [this_order_next_stop_lat - this_order_cur_lat,
                        #                                            this_order_next_stop_lon - this_order_cur_lon]))
                        #             cur_order_exchange_simi.append(cur_simi)
                        #         courier2_courier1_order_similarity_list.append(
                        #             np.sum(cur_order_exchange_simi) / len(cur_order_exchange_simi))
                        #     courier2_courier1_order_similarity = np.sum(courier2_courier1_order_similarity_list) / len(
                        #         courier2_courier1_order_similarity_list)
                        # else:
                        #     courier2_courier1_order_similarity = 0
                        #
                        # # two_couriers_exchange_order_similarity = (courier1_courier2_order_similarity +
                        # #                                           courier2_courier1_order_similarity) / 2
                        #
                        # high_level_state_input = [
                        #     encounter_start_time,  # encounter:11个state
                        #     encounter_start_courier1_lat,
                        #     encounter_start_courier1_lon,
                        #     encounter_start_courier2_lat,
                        #     encounter_start_courier2_lon,
                        #     encounter_start_courier1_next_stop_lat,
                        #     encounter_start_courier1_next_stop_lon,
                        #     encounter_start_courier2_next_stop_lat,
                        #     encounter_start_courier2_next_stop_lon,
                        #     encounter_courier1_cur_order_cur_stage_remaining_time,
                        #     encounter_courier2_cur_order_cur_stage_remaining_time,
                        #     # order-state: 8 个
                        #     # courier1_max_order_remaining_time,
                        #     courier1_min_real_time_promise_variance_order_remaining_time,
                        #     courier1_order_num,
                        #     courier1_self_order_similarity,
                        #     courier1_courier2_order_similarity,
                        #     # courier2_max_order_remaining_time,
                        #     courier2_min_real_time_promise_variance_order_remaining_time,
                        #     courier2_order_num,
                        #     courier2_self_order_similarity,
                        #     courier2_courier1_order_similarity
                        # ]
                        #
                        # h_network_output = hierachical_network.choose_action(
                        #     np.array(high_level_state_input))  # 0 不换，1 换
                        # print('stateinput', high_level_state_input)
                        courier_encounter_event = Encounter(online_couriers[online_courier_count_x].courier_id,
                                                            online_couriers[online_courier_count_y].courier_id,
                                                            T)
                        env.encounter_exchange_event.append(courier_encounter_event)

                        # high_level_next_s = []
                        # high_level_reward = 0
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

                        # low-level decision
                        low_level_state_input = []
                        low_level_action_list = []
                        # if h_network_output == 1:
                        # track_reward = []
                        # # low_level_train_times = 0
                        # end = False
                        # while True and not end:
                        # low_level_state_input = []
                        # *****************3*******************换单逻辑（主要）A2C [一时刻的多个相遇事件,然后对每个相遇事件的订单做处理]
                        # compute cur_state、action【由于机遇式相遇，每个时间步不一定有相遇事件，有就计算，没有就算了】

                        # if len(cur_time_step_exchange_events) > 0:
                        #     for i_encounter_id in range(len(cur_time_step_exchange_events)):
                        #         raoxing_time = 0  # 两人绕行需要的时间
                        encounter_two_couriers = [
                            online_couriers[online_courier_count_x],
                            online_couriers[online_courier_count_y]]



                        # 先迭代训练该换单事件(还在训练的过程中时，仅在copy的对象上作操作)，等收敛了再真正drop_take订单
                        train_step = 0
                        # 获取相遇骑手对的订单信息
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

                        # track_reward = []  # 某一次针对 该相遇事件 换单后的效果
                        # low level state_input preprocess

                        # 最多12个单，11*12个状态空间=>调整一下，当前订单所在哪个骑手就把哪个骑手的状态放在前面
                        for encounter_order_id in range(len(encounter_to_exchange_order_list)):
                            # if encounter_to_exchange_order_list[encounter_order_id].hop_num > 3:
                            #     continue
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

                            # if to_exchange_order_raw_courier_cost_left_time <= 1200:
                            #     continue

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
                                    this_order_cur_lon2 = encounter_two_couriers[1].lat
                                    this_order_cur_lat2 = encounter_two_couriers[1].lon
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
                            state_input = []
                            if raw_courier_id == 0:
                                state_input = [cur_order_next_stop_lat,
                                               cur_order_next_stop_lon,
                                               # encounter_two_couriers[raw_courier_id].lat,
                                               #            encounter_two_couriers[raw_courier_id].lon,
                                               to_exchange_order_raw_courier_cost_left_time,
                                               courier1_next_stop_location_lat, courier1_next_stop_location_lon,
                                               encounter_two_couriers[0].cur_order_num, courier1_shunludan_num,
                                               encounter_courier1_all_order_deliver_cost_time,
                                               courier2_next_stop_location_lat, courier2_next_stop_location_lon,
                                               encounter_two_couriers[1].cur_order_num, courier2_shunludan_num,
                                               encounter_courier2_all_order_deliver_cost_time]
                            else:
                                state_input = [cur_order_next_stop_lat,
                                               cur_order_next_stop_lon,
                                               # encounter_two_couriers[raw_courier_id].lat,
                                               #            encounter_two_couriers[raw_courier_id].lon,
                                               to_exchange_order_raw_courier_cost_left_time,
                                               courier2_next_stop_location_lat, courier2_next_stop_location_lon,
                                               encounter_two_couriers[1].cur_order_num, courier2_shunludan_num,
                                               encounter_courier2_all_order_deliver_cost_time,
                                               courier1_next_stop_location_lat, courier1_next_stop_location_lon,
                                               encounter_two_couriers[0].cur_order_num, courier1_shunludan_num,
                                               encounter_courier1_all_order_deliver_cost_time]
                            low_level_state_input.append(state_input)
                            # for state_input_id in range(len(state_input)):
                            #     low_level_state_input.append(state_input[state_input_id])
                        # 状态空间补全
                        # for xunhuan_id in range((12 - len(encounter_to_exchange_order_list)) * 13):
                        #     low_level_state_input.append(0)
                        # for xunhuan_id in range(12 - len(encounter_to_exchange_order_list)):
                        #     state_input = []
                        #     for buquan_id in range(13):
                        #         state_input.append(0)
                        #     low_level_state_input.append(state_input)

                        # 由网络告诉怎么选择action【0不换，1换】* 12【省略的地方为0】
                        print('state_num:', len(low_level_state_input),',low_level_state:', low_level_state_input)
                        if len(low_level_state_input) > 12:
                            continue
                        low_level_action_list = DQN.choose_action(np.array(low_level_state_input))  # 输出了0/1
                        print('low_level_action:', low_level_action_list)

                        # action filter(骑手订单数max < 6 ，骑手一段时间内的换单次数) to be adjusted
                        # 后面几个订单 action=1 就过滤  Q 值加一个限制条件！！！
                        # if encounter_two_couriers[chosen_courier_id].cur_order_num >= 6:
                        #     # 该谁的还是谁的，没变化，也不用来更新换单模型
                        #     continue
                        for xunhuan_id in range(len(encounter_to_exchange_order_list)):
                            if encounter_to_exchange_order_list[xunhuan_id].hop_num > 2:
                                low_level_action_list[xunhuan_id] = 0
                            if low_level_state_input[xunhuan_id][2] <= 1200:  # 20min = 20*60s = 1200s
                                low_level_action_list[xunhuan_id] = 0
                        print('low_level_filtered_action:', low_level_action_list)

                        buhuan_count = 0
                        exchanged_order_raw_courier_id_list = to_exchange_order_raw_courier_id_list
                        for chose_id in range(len(to_exchange_order_raw_courier_id_list)):
                            cur_order_next_state = []
                            if low_level_action_list[chose_id] == 1:
                                # 该单发生换单
                                # to be adjusted: 要不要考虑骑手反应时间（与相遇持续时长有关）
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

                                if to_exchange_order_raw_courier_id_list[chose_id] == 0:
                                    # 订单原骑手为骑手0
                                    # if encounter_two_couriers[1].courier_id == 2053730:
                                    #     print('debug')
                                    # if encounter_two_couriers[0].courier_id == 2053730:
                                    #     print('debug')
                                    encounter_two_couriers[1].exchange_take_order(
                                        encounter_to_exchange_order_list[chose_id], T,
                                        courier1_huandan_time_lat,
                                        courier1_huandan_time_lon,
                                        courier2_huandan_time_lat,
                                        courier2_huandan_time_lon)
                                    encounter_two_couriers[0].exchange_drop_order(
                                        encounter_to_exchange_order_list[chose_id], T,
                                        courier1_huandan_time_lat,
                                        courier1_huandan_time_lon,
                                        courier2_huandan_time_lat,
                                        courier2_huandan_time_lon)
                                    exchanged_order_raw_courier_id_list[chose_id] = 1
                                else:
                                    # 订单原骑手为骑手1
                                    # if encounter_two_couriers[1].courier_id == 2053730:
                                    #     print('debug')
                                    # if encounter_two_couriers[0].courier_id == 2053730:
                                    #     print('debug')
                                    encounter_two_couriers[0].exchange_take_order(
                                        encounter_to_exchange_order_list[chose_id], T,
                                        courier1_huandan_time_lat,
                                        courier1_huandan_time_lon,
                                        courier2_huandan_time_lat,
                                        courier2_huandan_time_lon)
                                    encounter_two_couriers[1].exchange_drop_order(
                                        encounter_to_exchange_order_list[chose_id], T,
                                        courier1_huandan_time_lat,
                                        courier1_huandan_time_lon,
                                        courier2_huandan_time_lat,
                                        courier2_huandan_time_lon)
                                    exchanged_order_raw_courier_id_list[chose_id] = 0
                            else:
                                buhuan_count += 1

                        low_level_next_s = []
                        low_level_reward = 0
                        # high_level_1==>low_level[0,0,0] 的处理
                        if buhuan_count == len(to_exchange_order_raw_courier_id_list):
                            # 添加惩罚引子，reward = -10
                            # high_level_reward = -1
                            # high_level_next_s = high_level_state_input
                            low_level_next_s = low_level_state_input
                            low_level_reward = 0

                        else:
                            # compute low_level next state (顺序要和之前的一样)
                            for encounter_order_id in range(len(encounter_to_exchange_order_list)):
                                # if encounter_to_exchange_order_list[encounter_order_id].hop_num > 3:
                                #     continue
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
                                exchanged_order_courier_cost_left_time = -9999
                                if exchanged_order_raw_courier_id_list[encounter_order_id] == 0:
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

                                # if to_exchange_order_raw_courier_cost_left_time <= 1200:
                                #     continue

                                huandan_courier_id = exchanged_order_raw_courier_id_list[encounter_order_id]

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
                                        this_order_cur_lon2 = encounter_two_couriers[1].lat
                                        this_order_cur_lat2 = encounter_two_couriers[1].lon
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
                                state_input = []
                                if huandan_courier_id == 0:
                                    state_input = [cur_order_next_stop_lat,
                                                   cur_order_next_stop_lon,
                                                   # encounter_two_couriers[raw_courier_id].lat,
                                                   #            encounter_two_couriers[raw_courier_id].lon,
                                                   exchanged_order_courier_cost_left_time,
                                                   courier1_next_stop_location_lat,
                                                   courier1_next_stop_location_lon,
                                                   encounter_two_couriers[0].cur_order_num,
                                                   courier1_shunludan_num,
                                                   encounter_courier1_all_order_deliver_cost_time,
                                                   courier2_next_stop_location_lat,
                                                   courier2_next_stop_location_lon,
                                                   encounter_two_couriers[1].cur_order_num,
                                                   courier2_shunludan_num,
                                                   encounter_courier2_all_order_deliver_cost_time]
                                else:
                                    state_input = [cur_order_next_stop_lat,
                                                   cur_order_next_stop_lon,
                                                   # encounter_two_couriers[raw_courier_id].lat,
                                                   #            encounter_two_couriers[raw_courier_id].lon,
                                                   exchanged_order_courier_cost_left_time,
                                                   courier2_next_stop_location_lat,
                                                   courier2_next_stop_location_lon,
                                                   encounter_two_couriers[1].cur_order_num,
                                                   courier2_shunludan_num,
                                                   encounter_courier2_all_order_deliver_cost_time,
                                                   courier1_next_stop_location_lat,
                                                   courier1_next_stop_location_lon,
                                                   encounter_two_couriers[0].cur_order_num,
                                                   courier1_shunludan_num,
                                                   encounter_courier1_all_order_deliver_cost_time]
                                low_level_next_s.append(state_input)
                                # for state_input_id in range(len(state_input)):
                                #     low_level_next_s.append(state_input[state_input_id])

                            # compute high_level next_state
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

                            # high_level_next_s = [
                            #     encounter_start_time,  # encounter:11个state
                            #     encounter_start_courier1_lat,
                            #     encounter_start_courier1_lon,
                            #     encounter_start_courier2_lat,
                            #     encounter_start_courier2_lon,
                            #     encounter_start_courier1_next_stop_lat,
                            #     encounter_start_courier1_next_stop_lon,
                            #     encounter_start_courier2_next_stop_lat,
                            #     encounter_start_courier2_next_stop_lon,
                            #     encounter_courier1_cur_order_cur_stage_remaining_time,
                            #     encounter_courier2_cur_order_cur_stage_remaining_time,
                            #     # order-state: 8 个
                            #     # courier1_max_order_remaining_time,
                            #     courier1_min_real_time_promise_variance_order_remaining_time,
                            #     courier1_order_num,
                            #     courier1_self_order_similarity,
                            #     courier1_courier2_order_similarity,
                            #     # courier2_max_order_remaining_time,
                            #     courier2_min_real_time_promise_variance_order_remaining_time,
                            #     courier2_order_num,
                            #     courier2_self_order_similarity,
                            #     courier2_courier1_order_similarity
                            # ]

                            # compute reward
                            # 时间： 订单配送时长差 -  骑手中转距离（10s） - 换单处理时间（30s）
                            # order_dispatch_time_variance_list = []
                            # order_dispatch_time_variance = 0
                            raw_order_dispatch_time_list = []
                            exchanged_order_dispatch_time_list = []
                            # 订单价格：- 超时钱数  收益差(从全局平台角度看)
                            # revenue_variance = 0
                            # revenue_variance_list = []
                            raw_revenue_list = []
                            exchanged_revenue_list = []
                            for encounter_order_id in range(len(exchanged_order_raw_courier_id_list)):

                                raw_order_dispatch_time = low_level_state_input[encounter_order_id][2]
                                exchange_order_dispatch_time = low_level_next_s[encounter_order_id][2]
                                raw_order_dispatch_time_list.append(raw_order_dispatch_time)
                                exchanged_order_dispatch_time_list.append(exchange_order_dispatch_time)
                                # to be adjusted: 要不要考虑骑手反应时间（与相遇持续时长有关）
                                # courier1_huandan_time_lat = 0
                                # courier1_huandan_time_lon = 0
                                # courier2_huandan_time_lat = 0
                                # courier2_huandan_time_lon = 0
                                # if T + 5 in encounter_two_couriers[0].route_time_step.keys():
                                #     courier1_huandan_time_lat = encounter_two_couriers[0].route_time_step[T + 5].lat
                                #     courier1_huandan_time_lon = encounter_two_couriers[0].route_time_step[T + 5].lon
                                # else:
                                #     courier1_huandan_time_lat = encounter_two_couriers[1].lat
                                #     courier1_huandan_time_lon = encounter_two_couriers[1].lon
                                #
                                # if T + 5 in encounter_two_couriers[1].route_time_step.keys():
                                #     courier2_huandan_time_lat = encounter_two_couriers[1].route_time_step[T + 5].lat
                                #     courier2_huandan_time_lon = encounter_two_couriers[1].route_time_step[T + 5].lon
                                # else:
                                #     courier2_huandan_time_lat = encounter_two_couriers[1].lat
                                #     courier2_huandan_time_lon = encounter_two_couriers[1].lon
                                #
                                # courier1_courier2_distance = get_distance_hav(courier1_huandan_time_lat,
                                #                                               courier1_huandan_time_lon,
                                #                                               courier2_huandan_time_lat,
                                #                                               courier2_huandan_time_lon) / 2
                                # courier1_courier2_time = courier1_courier2_distance / (12.11 / 2) * (
                                #         60 * 60) + 30  # 单位：时间步数,考虑换单停下来的交换时间，用户的反应时间
                                # encounter_order_dispatch_time_variance = exchange_order_dispatch_time + \
                                #                                          courier1_courier2_time - raw_order_dispatch_time

                                # encounter_order_dispatch_time_variance = exchange_order_dispatch_time - raw_order_dispatch_time
                                # order_dispatch_time_variance_list.append(encounter_order_dispatch_time_variance)

                                # revenue computation
                                order_price = encounter_to_exchange_order_list[encounter_order_id].order_price
                                promise_order_time = encounter_to_exchange_order_list[
                                    encounter_order_id].promise_deliver_time
                                raw_deliver_time_overdue_condition = raw_order_dispatch_time - promise_order_time
                                raw_revenue = 0
                                # exchange_revenue = 0
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
                                # exchange_deliver_time_overdue_condition = exchange_order_dispatch_time + courier1_courier2_time - promise_order_time
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
                                exchanged_revenue_list.append(exchange_revenue)
                                # cur_revenue_variance = exchange_revenue - raw_revenue
                                # revenue_variance_list.append(cur_revenue_variance)
                            # order_dispatch_time_variance = sum(order_dispatch_time_variance_list)

                            # revenue_variance = sum(revenue_variance_list)
                            # reward = math.exp(-order_dispatch_time_variance/1000) * math.exp(revenue_variance/50)
                            reward = (math.exp(-sum(exchanged_order_dispatch_time_list) / 3600) *
                                      sum(exchanged_revenue_list) / 50) - \
                                     (math.exp(-sum(raw_order_dispatch_time_list) / 3600) * sum(
                                         raw_revenue_list) / 50)
                            reward = (math.exp(reward) - math.exp(-reward)) / (math.exp(reward) + math.exp(-reward))
                            low_level_reward = reward
                            # high_level_reward = reward

                        # update low-level actor

                        # max_track_reward = max(track_reward)
                        # if max_track_reward == track_reward[-1] and low_level_train_times >=

                        # track_reward.append(low_level_reward)
                        # td_error = critic.learn(low_level_state_input, low_level_reward, low_level_next_s)
                        # actor.learn(low_level_state_input, chosen_courier_id_list, td_error)

                        # low_level_train_times += 1

                        # track_reward.append(reward)
                        # ep_track_r.append(reward)
                        # critic.store_transition(np.array(low_level_state_input), chosen_courier_id_list, low_level_reward, np.array(low_level_next_s))
                        # # encounter_order_id += 1

                        # if critic.memory_counter > critic.memory_size:
                        #     sample_index = np.random.choice(critic.memory_size, size=critic.batch_size)
                        # else:
                        #     sample_index = np.random.choice(critic.memory_counter, size=critic.batch_size)
                        # batch_memory = critic.memory[sample_index, :]
                        # s = batch_memory[:, :critic.n_features]  # 32*13
                        # _s = batch_memory[:, -critic.n_features:]  # 32*13
                        # a = batch_memory[:, critic.n_features]  # 32*1
                        # r = batch_memory[:, critic.n_features + 1]  # 32*1

                        # td_error = critic.learn(s, r, _s)
                        # actor.learn(s, a, td_error)

                        # hierachical_network.store_transition()
                        # print(track_reward)
                        # if len(DQN.cost_his) > 0:
                        #     print('T:',T, ", event:", event_id, 'cur_loss', DQN.cost_his[-1])
                        # done = True
                        # for r in track_reward:
                        #     if r<0:
                        #         done = False
                        #         break
                        #
                        # if done or train_step >= max_train_step:
                        # ep_rs_sum = sum(track_reward)
                        # if 'running_reward' not in globals():
                        #     running_reward = ep_rs_sum
                        # else:
                        #     running_reward = running_reward * 0.95 + ep_rs_sum * 0.05
                        # print("event:", event_id, "  reward:", int(running_reward))
                        # train_step += 1
                        # event_id += 1
                        # # 修改了 每个回合训练的个数，原来是event_id <=100（导致每次的reward序列长度不同）
                        # episode_times = len(ep_track_r)
                        # if episode_times >= 100:
                        #     end = True
                        # else:
                        #     high_level_reward = 0
                        #     high_level_next_s = high_level_state_input

                        # hierachical_network.store_transition(high_level_state_input, h_network_output,
                        #                                      high_level_reward)
                        # DQN.store_transition(np.array(low_level_state_input), low_level_action_list,
                        #                      low_level_reward, np.array(low_level_next_s))
                        # train_DQN_count += 1
                        # h_network_output_list = []
                        # h_network_output_list.append(h_network_output)
                        # hierachical_network.learn(np.array(high_level_state_input), h_network_output_list, td_error)
                        # if h_network_output == 1:
                        # actor.learn(np.array(low_level_state_input), low_level_action_list, td_error)
                        # ep_track_r.append(low_level_reward)
                        # print('huandan_state:', high_level_state_input, ', option:', h_network_output, 'huandan_reward',
                        # high_level_reward)
        # if train_DQN_count > 0:
        #     DQN.learn()
        if T % 100 == 99:
            with open(time_step_courier_state_file_name_exchange, "w") as file:
                for courier_id in env.couriers_dict:
                    if env.couriers_dict[courier_id].online:
                        file.writelines('time:' + str(env.couriers_dict[courier_id].cur_time) +
                                        ',courier_id:' + str(courier_id) + ',courier_lon:' +
                                        str(env.couriers_dict[courier_id].lon) + ', courier_lat:' +
                                        str(env.couriers_dict[courier_id].lat) + ', orders_num:' +
                                        str(env.couriers_dict[courier_id].cur_order_num) +
                                        ', used_time:' + str(env.couriers_dict[courier_id].cost_time) +
                                        ',day_all_order_num:' + str(len(env.couriers_dict[courier_id].order_list) +
                                                                    len(env.couriers_dict[courier_id].
                                                                        encounter_before_finished_orders)) +
                                        ',overdue_order_num' + str(
                            env.couriers_dict[courier_id].overdue_order_num) + '\n')
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

    # ep_rs_sum1 = sum(ep_track_r)
    # if 'running_reward_ep' not in globals():
    #     running_reward_ep = ep_rs_sum1
    # else:
    #     running_reward_ep = running_reward_ep * 0.95 + ep_rs_sum1 * 0.05
    # print("episode:", global_step, "  reward:", running_reward_ep)
    # episode_ep_reward.append(running_reward_ep)

    # hierachical_network.learn()

    # ep_rs_average = sum(ep_track_r) / len(ep_track_r)
    # # running_reward_ep = ep_rs_sum1
    # print('episode:', global_step, ',len(ep_track_r):', len(ep_track_r), ',ep_average_reward', ep_rs_average)
    # episode_ep_average_reward.append(ep_rs_average)

    # global_step += 1
    # 觉得差不多了（ep_reward/reward上升到稳定；loss稳定，单看loss不行）就手动save模型去训练

# saver.save(sess, log_dir + "model.ckpt")

