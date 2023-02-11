import pickle
import tensorflow as tf
from simulator.encounter import Encounter
from simulator.envs import *
import numpy as np
from algorithm.A2C import *
from algorithm.alg_utility import *
import itertools
import copy
from train.visulize_debug import *

# 输入
# 一天的所有订单10.12,未转网格，未转时间步
order_real = pickle.load(open("D:/exchange/dataProcessing/all_orders_target_20201012.pkl", 'rb'))
# 10.12骑手第一次出现的时间及地点, 未转网格，未转时间步
couriers_init = pickle.load(open("D:/exchange/dataProcessing/courier_init_20201012.pkl", 'rb'))

# 全局参数的初始化
global_step = 0
# repeat_time = 10000
gamma = 0.9  # RL中计算未来reward的 折扣因子
max_iter = 86400  # 10s一个时间步=8640，可能有很多空白时间点-----10min

# 骑手当前订单数,预测的骑手的下一站经纬度.送完手中所有单还需时间,所持订单【其他状态：相遇骑手的状态】--最多6个订单
state_dim = 13
action_dim = 2

learning_rate_Actor = 1e-5
learning_rate_Critic = 1e-3

# max_train_step = 1000

tf.compat.v1.set_random_seed(1)
# 实际网络

# 新训练模型
# sess = tf.compat.v1.Session()
# sess.run(tf.compat.v1.global_variables_initializer())
# saver = tf.compat.v1.train.Saver()

# 用跑过的模型继续训练
sess = tf.compat.v1.Session()
actor = Actor(sess, state_dim, action_dim, learning_rate_Actor)
critic = Critic(sess, state_dim, learning_rate_Critic)
saver = tf.compat.v1.train.Saver()
saver.restore(sess, 'D:/exchange/train/debug-2021-7-29/A2C_train_logs/model.ckpt')

# while True:
#
#     ep_track_r = []
#
#     env = Region(couriers_init, order_real)
#     env_state = env.env_initialize()
#
#     order_to_wait_to_next_timestep = []  # 当前时间步未得到分派的订单
#
#     event_id = 0
#     episode_id = 0
#     end = False
#     # train:10.12
#     T = 0
#     # 只搞一个事件

if __name__ == "__main__":
    env = Region(couriers_init, order_real)
    env_state = env.env_initialize()

    order_to_wait_to_next_timestep = []  # 当前时间步未得到分派的订单
    event_id = 0
    episode_id = 0
    # end = False
    T = 0
    while T < max_iter:
        # while T < max_iter and not end:

        # *********************1********************平台派单（按10min 按批派单）(根据距离最近),来一个新订单就派单
        time_step_courier_state_file_name_exchange = "D:/exchange/train/debug-2021-7-29/A2C_exchange_logs_consider_processint_time/time_step_" + str(
            T) + "_courier_state.txt"
        # time_step_courier_state_file_name_encounter = "D:/exchange/train/debug-2021-7-29/A2C_exchange_logs_consider_processint_time" \
        #                                               "/time_step_" + str(T) + "_encounter.txt"
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
                if courier_encounter_distance <= 0.015 and \
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
                        env.encounter_exchange_event.append(courier_encounter_event)
                        cur_time_step_encounter_events.append(courier_encounter_event)
                    # courier_encounter_event = Encounter(online_couriers[online_courier_count_x].courier_id,
                    #                                     online_couriers[online_courier_count_y].courier_id, T)
                    # cur_time_step_encounter_events.append(courier_encounter_event)

        # *****************3*******************换单逻辑（主要）A2C [一时刻的多个相遇事件,然后对每个相遇事件的订单做处理]
        # compute cur_state、action【由于机遇式相遇，每个时间步不一定有相遇事件，有就计算，没有就算了】
        if len(cur_time_step_encounter_events) > 0:
            combine_action_list = []
            # with open(time_step_courier_state_file_name_encounter, "a") as file:
            for i_encounter in cur_time_step_encounter_events:
                encounter_two_couriers = [
                    env.couriers_dict[i_encounter.encounter_id1],
                    env.couriers_dict[i_encounter.encounter_id2]]
                print('encounterEvent:', T, 'courier_id1:', i_encounter.encounter_id1,
                      'courier_id2:', i_encounter.encounter_id2)
                # file.writelines('time:' + str(T) +
                #                 ', courier_id1:' + str(i_encounter.encounter_id1) +
                #                 ', courier1_loc: (' + str(encounter_two_couriers[0].lat) + ',' +
                #                 str(encounter_two_couriers[0].lon) +
                #                 '), courier_id2:' + str(i_encounter.encounter_id2) +
                #                 ', courier2_loc: (' + str(encounter_two_couriers[1].lat) + ',' +
                #                 str(encounter_two_couriers[1].lon) + ')' + '\n'
                #                 )
                courier1_id = i_encounter.encounter_id1
                courier2_id = i_encounter.encounter_id2
                # file.writelines('courier1, id:' + str(courier1_id) + ',order_list:' + '\n')
                # for order in env.couriers_dict[courier1_id].order_list:
                #     file.writelines(',order_id:' + str(order.order_id) +
                #                     ',shop_loc:' + str(order.shop_latitude) + ',' + str(
                #         order.shop_longitude) +
                #                     ',user_loc:' + str(order.user_latitude) + ',' + str(
                #         order.user_longitude) +
                #                     ',order_create_time:' + str(order.order_create_time) +
                #                     ',arrive_merchant_time:' + str(order.arrive_merchant_time) +
                #                     ',order_deliver_time:' + str(order.order_deliver_time) +
                #                     ',promise_deliver_time:' + str(order.promise_deliver_time) +
                #                     ', dispatch_stage:' + str(order.dispatch_stage) +
                #                     '\n')
                # file.writelines('courier2, id:' + str(courier2_id) + ',order_list:' + '\n')
                # for order in env.couriers_dict[courier2_id].order_list:
                #     file.writelines(',order_id:' + str(order.order_id) +
                #                     ',shop_loc:' + str(order.shop_latitude) + ',' + str(
                #         order.shop_longitude) +
                #                     ',user_loc:' + str(order.user_latitude) + ',' + str(
                #         order.user_longitude) +
                #                     ',order_create_time:' + str(order.order_create_time) +
                #                     ',arrive_merchant_time:' + str(order.arrive_merchant_time) +
                #                     ',order_deliver_time:' + str(order.order_deliver_time) +
                #                     ',promise_deliver_time:' + str(order.promise_deliver_time) +
                #                     ', dispatch_stage:' + str(order.dispatch_stage) +
                #                     '\n')

                # 先迭代训练该换单事件(还在训练的过程中时，仅在copy的对象上作操作)，等收敛了再真正drop_take订单
                train_step = 0
                # 获取相遇骑手对的订单信息
                encounter_to_exchange_order_list = []  # 要筛选掉已送完的订单
                encounter_order_next_stop_location = []
                to_exchange_order_raw_courier_id_list = []
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
                                encounter_two_couriers[0].route_flag_to_be_updated[T + detect_time_added + 1] != []:
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

                    if encounter_two_couriers[0].available_loc_real_time[courier1_next_stop_order_loc_id] == 0:
                        courier1_next_stop_location_lat = encounter_two_couriers[0].lat
                        courier1_next_stop_location_lon = encounter_two_couriers[0].lon
                    else:
                        courier1_next_stop_location_lat = encounter_two_couriers[0].available_loc_real_time[
                            courier1_next_stop_order_loc_id].lat
                        courier1_next_stop_location_lon = encounter_two_couriers[0].available_loc_real_time[
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
                                encounter_two_couriers[1].route_flag_to_be_updated[T + detect_time_added + 1] != []:
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

                    if encounter_two_couriers[1].available_loc_real_time[courier2_next_stop_order_loc_id] == 0:
                        courier2_next_stop_location_lat = encounter_two_couriers[1].lat
                        courier2_next_stop_location_lon = encounter_two_couriers[1].lon
                    else:
                        courier2_next_stop_location_lat = encounter_two_couriers[1].available_loc_real_time[
                            courier2_next_stop_order_loc_id].lat
                        courier2_next_stop_location_lon = encounter_two_couriers[1].available_loc_real_time[
                            courier2_next_stop_order_loc_id] .lon

                track_reward = []  # 某一次针对 该相遇事件 换单后的效果
                for encounter_order_id in range(len(encounter_to_exchange_order_list)):

                    if encounter_to_exchange_order_list[encounter_order_id].hop_num > 3:
                        continue

                    order_similarity = 0
                    order_similarity2 = 0
                    if encounter_to_exchange_order_list[encounter_order_id].dispatch_stage == 1:
                        cur_order_next_stop_lon = encounter_to_exchange_order_list[encounter_order_id].shop_longitude
                        cur_order_next_stop_lat = encounter_to_exchange_order_list[encounter_order_id].shop_latitude
                    elif encounter_to_exchange_order_list[encounter_order_id].dispatch_stage == 2:
                        cur_order_next_stop_lon = encounter_to_exchange_order_list[encounter_order_id].user_longitude
                        cur_order_next_stop_lat = encounter_to_exchange_order_list[encounter_order_id].user_latitude
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

                                for change_state_id1 in range(
                                        len(encounter_two_couriers[1].route_flag_to_be_updated[time_step_id])):
                                    if encounter_two_couriers[1].route_flag_to_be_updated[time_step_id][
                                        change_state_id1] == (
                                            cur_this_order_loc_id, 0):
                                        to_exchange_order_raw_courier_cost_left_time = time_step_id - T
                                        break

                    if to_exchange_order_raw_courier_cost_left_time == -9999:
                        print('debug')

                    # 筛选长订单（到达当前目的地还需超过30min = 30 * 60s = 1800s = 180个时间步,20min--120个时间步）
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
                                order_similarity = cosine_dis(np.array([cur_order_next_stop_lat - cur_order_cur_lat,
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
                            elif encounter_two_couriers[1].order_list[shunludan_id2].dispatch_stage == 2:
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

                    state_input = [encounter_two_couriers[raw_courier_id].lat,
                                   encounter_two_couriers[raw_courier_id].lon,
                                   to_exchange_order_raw_courier_cost_left_time,
                                   courier1_next_stop_location_lat, courier1_next_stop_location_lon,
                                   encounter_two_couriers[0].cur_order_num, courier1_shunludan_num,
                                   encounter_courier1_all_order_deliver_cost_time,
                                   courier2_next_stop_location_lat, courier2_next_stop_location_lon,
                                   encounter_two_couriers[1].cur_order_num, courier2_shunludan_num,
                                   encounter_courier2_all_order_deliver_cost_time
                                   ]

                    chosen_courier_id = actor.choose_action(np.array(state_input))  # 输出了0/1
                    combine_action_list.append(chosen_courier_id)

                    if encounter_two_couriers[chosen_courier_id].cur_order_num >= 6:
                        # 该谁的还是谁的，没变化，也不用来更新换单模型
                        continue

                    if chosen_courier_id != to_exchange_order_raw_courier_id_list[encounter_order_id]:
                        # 出现换单
                        encounter_to_exchange_order_list[encounter_order_id].hop_num += 1
                        # file.writelines('exchanged order_id:'+
                        #                 str(encounter_to_exchange_order_list[encounter_order_id].order_id) +'\n')

                        if chosen_courier_id == 0:
                            encounter_two_couriers[0].exchange_take_order(
                                encounter_to_exchange_order_list[encounter_order_id], T, courier1_huandan_time_lat,
                                courier1_huandan_time_lon, courier2_huandan_time_lat, courier2_huandan_time_lon)
                            encounter_two_couriers[1].exchange_drop_order(
                                encounter_to_exchange_order_list[encounter_order_id], T, courier1_huandan_time_lat,
                                courier1_huandan_time_lon, courier2_huandan_time_lat, courier2_huandan_time_lon)
                            # if encounter_two_couriers[0].cur_order_num > 6 or encounter_two_couriers[1].cur_order_num == 0:
                            # out_capacity = True

                            courier1_shunludan_num += 1
                            # 根据env返回状态
                            # debug原因，take_order/drop_order会影响order_list中的loc_id
                            # solution: 到骑手中order_list找出loc_id再赋值
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
                                        for flag_item in encounter_two_couriers[0].route_flag_to_be_updated[T + 1]:
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
                                    courier1_next_stop_location_lat = encounter_two_couriers[0].available_loc_real_time[
                                        encounter_two_couriers[0].route_flag_to_be_updated[T + 1][0][0]].lat
                                    courier1_next_stop_location_lon = encounter_two_couriers[0].available_loc_real_time[
                                        encounter_two_couriers[0].route_flag_to_be_updated[T + 1][0][0]].lon

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
                                        for flag_item in encounter_two_couriers[1].route_flag_to_be_updated[T + 1]:
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
                                    courier2_next_stop_location_lat = encounter_two_couriers[1].available_loc_real_time[
                                        encounter_two_couriers[1].route_flag_to_be_updated[T + 1][0][0]].lat
                                    courier2_next_stop_location_lon = encounter_two_couriers[1].available_loc_real_time[
                                        encounter_two_couriers[1].route_flag_to_be_updated[T + 1][0][0]].lon

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
                            # if encounter_two_couriers[1].courier_id == 103401162:
                            #     print('debug')
                            # elif encounter_two_couriers[0].courier_id == 103401162:
                            #     print('debug')
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
                            encounter_two_couriers[0].exchange_drop_order(
                                encounter_to_exchange_order_list[encounter_order_id], T, courier1_huandan_time_lat,
                                courier1_huandan_time_lon, courier2_huandan_time_lat, courier2_huandan_time_lon)
                            encounter_two_couriers[1].exchange_take_order(
                                encounter_to_exchange_order_list[encounter_order_id], T, courier1_huandan_time_lat,
                                courier1_huandan_time_lon, courier2_huandan_time_lat, courier2_huandan_time_lon)
                            # if encounter_two_couriers[1].cur_order_num > 6 or encounter_two_couriers[0].cur_order_num == 0:
                            #     out_capacity = True

                            courier2_shunludan_num += 1

                            this_order_loc_id = -1
                            for loc_id in range(len(encounter_two_couriers[1].order_list)):
                                if encounter_to_exchange_order_list[encounter_order_id].order_id == \
                                        encounter_two_couriers[1].order_list[loc_id].order_id:
                                    this_order_loc_id = loc_id
                            if this_order_loc_id == -1:
                                print('problem')

                            # this_order_new_courier_cost_left_time = list(encounter_two_couriers[1].route_flag_to_be_updated.keys())[
                            #                                             list(encounter_two_couriers[1].route_flag_to_be_updated.values()).index((this_order_loc_id, 0))] - T

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
                                    # for flag_item in encounter_two_couriers[0].route_flag_to_be_updated[T + 1]:
                                    #     for next_time_flag_item in \
                                    #     encounter_two_couriers[0].route_flag_to_be_updated[T + 2]:
                                    #         if flag_item == next_time_flag_item:
                                    #             courier1_next_stop_order_loc_id = next_time_flag_item[0]
                                    #             if next_time_flag_item[1] == 0:
                                    #                 print('debug')
                                    #             break
                                    # if courier1_next_stop_order_loc_id == -1 and \
                                    #         encounter_two_couriers[0].route_flag_to_be_updated[T + 3] != []:
                                    #     print('debug')
                                    #     for flag_item in encounter_two_couriers[0].route_flag_to_be_updated[T + 2]:
                                    #         for next_time_flag_item in \
                                    #         encounter_two_couriers[0].route_flag_to_be_updated[T + 3]:
                                    #             if flag_item == next_time_flag_item:
                                    #                 courier1_next_stop_order_loc_id = next_time_flag_item[0]
                                    #                 if next_time_flag_item[1] == 0:
                                    #                     print('debug')
                                    #                 break
                                    if courier1_next_stop_order_loc_id == -1:
                                        # 都是快送完的单
                                        for flag_item in encounter_two_couriers[0].route_flag_to_be_updated[T + 1]:
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
                                    courier1_next_stop_location_lat = encounter_two_couriers[0].lat
                                    courier1_next_stop_location_lon = encounter_two_couriers[0].lon
                                else:
                                    courier1_next_stop_location_lat = encounter_two_couriers[0].available_loc_real_time[
                                        encounter_two_couriers[0].route_flag_to_be_updated[T + 1][0][0]].lat
                                    courier1_next_stop_location_lon = encounter_two_couriers[0].available_loc_real_time[
                                        encounter_two_couriers[0].route_flag_to_be_updated[T + 1][0][0]].lon

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
                                        for flag_item in encounter_two_couriers[1].route_flag_to_be_updated[T + 1]:
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
                                    courier2_next_stop_location_lat = encounter_two_couriers[1].available_loc_real_time[
                                        encounter_two_couriers[1].route_flag_to_be_updated[T + 1][0][0]].lat
                                    courier2_next_stop_location_lon = encounter_two_couriers[1].available_loc_real_time[
                                        encounter_two_couriers[1].route_flag_to_be_updated[T + 1][0][0]].lon

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

                            # 根据env返回状态
                        if this_order_new_courier_cost_left_time < 0 or encounter_courier1_all_order_deliver_cost_time_exchange < 0 or encounter_courier2_all_order_deliver_cost_time_exchange < 0:
                            print('debug')

                        # 换完单，顺路单数要变吗
                        next_s = [encounter_two_couriers[chosen_courier_id].lat,
                                  encounter_two_couriers[chosen_courier_id].lon,
                                  this_order_new_courier_cost_left_time,
                                  courier1_next_stop_location_lat, courier1_next_stop_location_lon,
                                  encounter_two_couriers[0].cur_order_num, courier1_shunludan_num,
                                  encounter_courier1_all_order_deliver_cost_time_exchange,
                                  courier2_next_stop_location_lat, courier2_next_stop_location_lon,
                                  encounter_two_couriers[1].cur_order_num, courier2_shunludan_num,
                                  encounter_courier2_all_order_deliver_cost_time_exchange
                                  ]
                        # 需要预测*****这个单在换到别人手里 送完-T
                        # 预测该订单的超时率
                        courier1_courier2_distance = get_distance_hav(encounter_two_couriers[0].lat,
                                                                      encounter_two_couriers[0].lon,
                                                                      encounter_two_couriers[1].lat,
                                                                      encounter_two_couriers[1].lon)
                        courier1_courier2_time = courier1_courier2_distance / 12.11 * (60 * 6) * 2  # 单位：时间步数
                        reward = gamma * (to_exchange_order_raw_courier_cost_left_time - (
                            this_order_new_courier_cost_left_time)) + \
                                 (-encounter_courier1_all_order_deliver_cost_time_exchange +
                                  encounter_courier1_all_order_deliver_cost_time -
                                  encounter_courier2_all_order_deliver_cost_time_exchange +
                                  encounter_courier2_all_order_deliver_cost_time) * (1 - gamma)
                        # reward = gamma * (to_exchange_order_raw_courier_cost_left_time - (
                        #         this_order_new_courier_cost_left_time + courier1_courier2_time)) + \
                        #          (-encounter_courier1_all_order_deliver_cost_time_exchange +
                        #           encounter_courier1_all_order_deliver_cost_time -
                        #           encounter_courier2_all_order_deliver_cost_time_exchange +
                        #           encounter_courier2_all_order_deliver_cost_time) * (1 - gamma)
                        # reward = to_exchange_order_raw_courier_cost_left_time - (
                        #         this_order_new_courier_cost_left_time + courier1_courier2_time)
                        if reward < 0:
                            print('not ok ')
                    else:
                        # 还派给了原骑手，env不更新
                        next_s = state_input
                        reward = 0  # 负的最不好，正的较好
                    track_reward.append(reward)
                    # ep_track_r.append(reward)
                    encounter_order_id += 1

                if len(track_reward) > 0:
                    ep_rs_sum = sum(track_reward) / len(track_reward)
                    if 'running_reward' not in globals():
                        running_reward = ep_rs_sum
                    else:
                        running_reward = ep_rs_sum
                    print("event:", event_id, ', len(deal_with_orders)', len(track_reward), ", average reward:",
                          int(running_reward))
                # print('episode:', global_step, ',len(ep_track_r):', len(ep_track_r), ',ep_average_reward', running_reward_ep)

                # train_step += 1
                event_id += 1

                # if event_id >= 100:
                #     end = True
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

    # ep_rs_sum1 = sum(ep_track_r) / len(ep_track_r)
    # running_reward_ep = ep_rs_sum1
    # print('episode:', global_step, ',len(ep_track_r):', len(ep_track_r), ',ep_average_reward', running_reward_ep)

    global_step += 1
    # 觉得差不多了（ep_reward/reward上升到稳定；loss稳定，单看loss不行）就手动save模型去训练

# saver.save(sess, log_dir + "model.ckpt")
