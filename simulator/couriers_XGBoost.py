import copy

from simulator.utility import get_distance_hav
from collections import defaultdict


class Loc:

    def __init__(self, latitude, longitude):
        self.lat = latitude
        self.lon = longitude


class Courier(object):
    __slots__ = ("occur_time", "cur_time",
                 "courier_id",
                 "lon", "lat",
                 "order_list", "cur_order_num",
                 "full", "capacity", "online",
                 "user_loc_list", "available_loc", "order_stage_flag",
                 "merchant_loc_list", "available_loc_real_time",
                 "available_flag", "route_distance", "cost_time",
                 "route_time_step", "next_stop", "next_stop_arrive_time",
                 "route_plan_merchant_user_loc", "route_flag_to_be_updated",
                 "dispatch_in_state",
                 "overdue_order_num",
                 "encounter_before_finished_orders",
                 "cur_route_generation")

    def __init__(self, courier_id, lat, lon, occur_time):
        self.occur_time = occur_time
        self.cur_time = 0  # 实时的时刻
        self.courier_id = courier_id
        self.lon = lon
        self.lat = lat

        self.encounter_before_finished_orders = []
        self.order_list = []
        self.cur_order_num = 0  # 骑手实时拥有的订单数
        self.capacity = 6
        self.full = False
        self.online = False

        # 用于real_time
        self.user_loc_list = []  # 骑手手中订单的用户位置列表
        self.merchant_loc_list = []  # 骑手手中订单的商家位置列表
        self.order_stage_flag = []  # 手里每个个订单的阶段【更新】
        self.available_loc_real_time = []
        # self.real_time_next_stop_loc = 0  # 用于policy_rebalancing换单时计算距离最近原则【后面可删除】

        # 用于route plan
        self.available_loc = []  # 每个订单的 当前下一个配送站点的位置(可以为商家，也可为用户)【更新】
        self.available_flag = []  # 手里每个个订单的阶段【更新】
        # 骑手在当前位置---骑手到达商家位置， order_stage_flag = 1(一接单就将order_stage_flag=1【初始化订单时就将flag=1】)
        # 骑手到达商家位置就 将order_stage_flag = 2，----后面的目标地点为用户位置
        # 骑手到达用户位置就将order_stage_flag = 0，-----订单完成

        # 用于real_time
        self.route_distance = 0  # 骑手一天的配送距离总和，可以换算成 配送时间(评估指标)
        self.cost_time = 0  # 配送完手中所有订单的所需配送时间和（评估指标）
        # 每接单一次就更新路线规划。
        self.route_time_step = {}  # 存储每个时间步的骑手位置:（time_step---- courier_loc）
        self.route_flag_to_be_updated = defaultdict(list)  # 存储每个时间步 对哪个订单 的订单阶段在变。time----order_loc_id__stage

        self.overdue_order_num = 0
        self.cur_route_generation = 0
        # # 到达路径中的下一站的时间和下一站的位置
        # self.next_stop = 0
        # self.next_stop_arrive_time = 0

    def next_stop_generation(self, avail_loc, avail_flag, plan_time, plan_start_loc,
                             cur_generation_count):  # route_plan
        '''
            :param avail_loc: 每个订单当前的目的地站点（可以是用户，也可以是商家【根据订单目前的进度不断变化】）
            :param avail_flag: 目前手中订单的配送阶段（手里每个个订单的阶段(2\1\0：刚接单\到了商家\送到用户（订单结束）)
            :return:
        '''
        # 找 目前所有订单可去的目的地中距离最近的一个站点去
        _distance = []
        for order_count in range(len(avail_loc)):
            if avail_flag[order_count] != 0:  # 该订单还未规划送到用户处
                _distance.append((order_count, get_distance_hav(plan_start_loc.lat, plan_start_loc.lon,
                                                                avail_loc[order_count].lat,
                                                                avail_loc[order_count].lon)))
        _distance.sort(key=lambda x: x[1])
        min_loc_id = _distance[0][0]  # distance 改成 features， 决策树
        min_dis = _distance[0][1]  # 单位：km
        # cost_time = int(min_dis / 12.11 * (60 * 6))  # 骑手骑行平均时间：12.11km/h,3m/s====所用的时间步数，
        # cost_time = int(min_dis / 12.11 * (60 * 60))
        # 前100m and 后100m 步行 1m/s 3.6km/h
        if min_dis > 0.1:
            buxingsudu = 12.11 / 3
            buxing_time = 0.1 / buxingsudu * (60 * 60)  # 单位秒，200m，1m/s，为骑行速度的三分之一，则同样的距离下，原来要1s，现在要3s
            qixing_time = (min_dis - 0.1) / 12.11 * (60 * 60)
            cost_time = int(buxing_time + qixing_time)
            raw_cost_time = min_dis / 12.11 * (60 * 60)
        else:
            buxingsudu = 12.11 / 3
            buxing_time = min_dis / buxingsudu * (60 * 60)  # 单位秒，200m，1m/s，为骑行速度的三分之一，则同样的距离下，原来要1s，现在要3s
            qixing_time = 0
            cost_time = int(buxing_time)
            raw_cost_time = buxing_time

        # self.cost_time += cost_time
        # self.route_distance += min_dis

        if cost_time == 0:
            # 用户就在站点处，就直接不用计算骑手的中间位置
            next_stop_start_time = plan_time + cost_time
            next_stop_start_loc = plan_start_loc

            if avail_flag[min_loc_id] == 1:
                self.route_time_step[next_stop_start_time] = next_stop_start_loc
                hasExistedItem = False
                loc_id_existed = False
                for item in self.route_flag_to_be_updated[next_stop_start_time]:
                    # if item[0] == min_loc_id and item[1] != 2:
                    #     self.route_flag_to_be_updated[next_stop_start_time].remove(item)
                    if item == (min_loc_id, 2):
                        hasExistedItem = True
                        break
                if not hasExistedItem:
                    self.route_flag_to_be_updated[next_stop_start_time].append((min_loc_id, 2))
                # self.order_list[min_loc_id].dispatch_stage = 2
                # self.order_list[min_loc_id].arrive_merchant_time = next_stop_start_time
            elif avail_flag[min_loc_id] == 2:
                self.route_time_step[next_stop_start_time] = next_stop_start_loc
                hasExistedItem = False
                for item in self.route_flag_to_be_updated[next_stop_start_time]:
                    # if item[0] == min_loc_id and item[1] != 0:
                    #     self.route_flag_to_be_updated[next_stop_start_time].remove(item)
                    if item == (min_loc_id, 0):
                        hasExistedItem = True
                        break
                if not hasExistedItem:
                    self.route_flag_to_be_updated[next_stop_start_time].append((min_loc_id, 0))
                # self.order_list[min_loc_id].dispatch_stage = 0
                # self.order_list[min_loc_id].order_deliver_time = next_stop_start_time
        else:
            start_lat = plan_start_loc.lat
            start_lon = plan_start_loc.lon
            end_lat = avail_loc[min_loc_id].lat
            end_lon = avail_loc[min_loc_id].lon
            one_step_lat = (end_lat - start_lat) / raw_cost_time
            one_step_lon = (end_lon - start_lon) / raw_cost_time
            qishou_cur_lat = start_lat
            qishou_cur_lon = start_lon

            # if plan_time in self.route_flag_to_be_updated.keys():
            # if self.route_flag_to_be_updated != {} and plan_time in self.route_flag_to_be_updated.keys():
            #     for time_step in range(plan_time + 1, plan_time + cost_time + 1):
            #         self.route_time_step[time_step] = Loc(start_lat + one_step_lat * (time_step - plan_time),
            #                                               start_lon + one_step_lon * (time_step - plan_time))
            #         if time_step == (plan_time + cost_time):
            #             if avail_flag[min_loc_id] == 1:
            #                 self.route_flag_to_be_updated[time_step] = [(min_loc_id, 2)]
            #             elif avail_flag[min_loc_id] == 2:
            #                 self.route_flag_to_be_updated[time_step] = [(min_loc_id, 0)]
            #         else:
            #             self.route_flag_to_be_updated[time_step] = [(min_loc_id, avail_flag[min_loc_id])]
            # else:
            for time_step in range(plan_time, plan_time + cost_time + 1):
                if time_step < plan_time + buxing_time / 2 or time_step > plan_time + buxing_time / 2 + qixing_time:
                    if time_step == plan_time:
                        self.route_time_step[time_step] = Loc(start_lat, start_lon)
                    else:
                        qishou_cur_lat = qishou_cur_lat + one_step_lat / 3
                        qishou_cur_lon = qishou_cur_lon + one_step_lat / 3
                        self.route_time_step[time_step] = Loc(qishou_cur_lat, qishou_cur_lon)
                else:
                    qishou_cur_lat = qishou_cur_lat + one_step_lat
                    qishou_cur_lon += one_step_lon
                    self.route_time_step[time_step] = Loc(qishou_cur_lat, qishou_cur_lon)
                # self.route_time_step[time_step] = Loc(start_lat + one_step_lat * (time_step - plan_time),
                #                                       start_lon + one_step_lon * (time_step - plan_time))

                if time_step == (plan_time + cost_time):
                    if avail_flag[min_loc_id] == 1:
                        # self.route_flag_to_be_updated[time_step] = [(min_loc_id, 2)]
                        hasExistedItem = False
                        for item in self.route_flag_to_be_updated[time_step]:
                            # if item[0] == min_loc_id and item[1] != 1:
                            #     self.route_flag_to_be_updated[time_step].remove(item)
                            if item == (min_loc_id, 1):
                                hasExistedItem = True
                                break
                        if not hasExistedItem:
                            self.route_flag_to_be_updated[time_step].append((min_loc_id, 2))
                    elif avail_flag[min_loc_id] == 2:
                        hasExistedItem = False
                        for item in self.route_flag_to_be_updated[time_step]:
                            # if item[0] == min_loc_id and item[1] == 1:
                            #     self.route_flag_to_be_updated[time_step].remove(item)
                            if item == (min_loc_id, 2):
                                hasExistedItem = True
                                break
                        if not hasExistedItem:
                            # self.route_flag_to_be_updated[time_step] = [(min_loc_id, 0)]
                            self.route_flag_to_be_updated[time_step].append((min_loc_id, 0))
                # elif time_step == plan_time:
                #     hasExisted = False
                #     for item in self.route_flag_to_be_updated[time_step]:
                #         if item == (min_loc_id, avail_flag[min_loc_id]):
                #             hasExisted = True
                #             break
                #     if not hasExisted:
                #         self.route_flag_to_be_updated[time_step].append((min_loc_id, avail_flag[min_loc_id]))
                else:
                    if time_step == plan_time:
                        hasExistedItem = False
                        for item in self.route_flag_to_be_updated[time_step]:
                            if item == (min_loc_id, avail_flag[min_loc_id]):
                                hasExistedItem = True
                                break
                        if not hasExistedItem:
                            self.route_flag_to_be_updated[time_step].append((min_loc_id, avail_flag[min_loc_id]))
                    else:
                        self.route_flag_to_be_updated[time_step] = [(min_loc_id, avail_flag[min_loc_id])]

            # if end_lon != qishou_cur_lon or end_lat != qishou_cur_lat:
            #     print('debug')
            next_stop_start_time = plan_time + cost_time
            next_stop_start_loc = Loc(avail_loc[min_loc_id].lat, avail_loc[min_loc_id].lon)

        return min_loc_id, next_stop_start_time, next_stop_start_loc

    def generate_future_route(self, plan_time):  # route_plan
        # 针对拥有的所有订单，直至把针对手中所有订单都安排了顺序就停止，安排完成
        cur_generate_count = self.cur_route_generation
        cur_plan_time = plan_time
        cur_plan_courier_loc = Loc(self.lat, self.lon)
        # 来新订单后新作路径更新，更新self.available_loc, self.available_flag
        self.available_loc = copy.deepcopy(self.available_loc_real_time)
        self.available_flag = copy.deepcopy(self.order_stage_flag)
        self.cur_route_generation = True
        # if sum(self.available_flag) == 0:
        if self.route_flag_to_be_updated != {}:
            route_flag_start_time_step_to_remove_max = max(self.route_flag_to_be_updated.keys())
            if self.route_time_step != {}:
                route_time_step_to_remove_max = max(self.route_time_step.keys())
            else:
                print('debug')
            for route_flag_to_remove_time_step in range(plan_time, route_flag_start_time_step_to_remove_max + 1):
                if route_flag_to_remove_time_step in self.route_flag_to_be_updated.keys():
                    self.route_flag_to_be_updated.pop(route_flag_to_remove_time_step)
            for route_time_step_to_remove_time_id in range(plan_time, route_time_step_to_remove_max + 1):
                self.route_time_step.pop(route_time_step_to_remove_time_id)
        while sum(self.available_flag) != 0:
            # 1次针对所有订单的当前目的地选择先去的第一个站点
            loc_id, next_stop_time, next_stop_loc = self.next_stop_generation(self.available_loc, self.available_flag,
                                                                              cur_plan_time, cur_plan_courier_loc,
                                                                              cur_generate_count)
            cur_plan_time = next_stop_time
            cur_plan_courier_loc = next_stop_loc
            if self.available_flag[loc_id] == 1:
                # (一接单就将order_stage_flag=1【初始化订单时就将flag=1】)骑手在当前位置---骑手到达商家位置
                # 下一阶段：即将去往用位置，stage=2
                self.available_loc[loc_id] = self.user_loc_list[loc_id]
                self.available_flag[loc_id] = 2
            elif self.available_flag[loc_id] == 2:  # 骑手到达用户位置就将order_stage_flag = 0，-----订单完成
                self.available_flag[loc_id] = 0
                self.available_loc[loc_id] = 0  # 订单完成
            elif self.available_flag[loc_id] == 0:
                pass
        # max_route_prediction_time_step = max(self.route_flag_to_be_updated.keys())
        # # if plan_time == max_route_prediction_time_step:
        # #     # 由于cost_time==0，不会进入到下一时间步的update状态，所以当前时间步直接更新骑手及订单状态
        # #     self.order_stage_flag[loc_id] = 0
        # #     self.order_list[loc_id].dispatch_stage = 0
        # #     self.cur_order_num -= 1
        # #     self.cost_time += self.cur_time - self.order_list[loc_id].arrive_merchant_time
        # #     self.order_list[loc_id].order_deliver_time = self.cur_time
        # #     if self.cur_time > self.order_list[loc_id].promise_deliver_time:
        # #         self.overdue_order_num += 1
        # # 用于drop_order后的原来预测信息清理
        # if cur_plan_time < max_route_prediction_time_step:
        #     route_flag_start_time_step_to_remove_max = max(self.route_flag_to_be_updated.keys())
        #     route_time_step_to_remove_max = max(self.route_time_step.keys())
        #     for route_flag_to_remove_time_step in range(cur_plan_time + 1, route_flag_start_time_step_to_remove_max + 1):
        #         self.route_flag_to_be_updated.pop(route_flag_to_remove_time_step)
        #     for route_time_step_to_remove_time_id in range(cur_plan_time + 1, route_time_step_to_remove_max + 1):
        #         self.route_time_step.pop(route_time_step_to_remove_time_id)
        self.cur_route_generation += 1

    def take_order(self, order, real_time):  # real_time
        self.order_list.append(order)
        self.cur_order_num += 1
        if self.cur_order_num >= self.capacity:
            self.full = True
        # self.available_loc_real_time.append(Loc(order.shop_latitude, order.shop_longitude))
        if order.dispatch_stage == 1:
            self.available_loc_real_time.append(Loc(order.shop_latitude, order.shop_longitude))
        elif order.dispatch_stage == 2:
            self.available_loc_real_time.append(Loc(order.user_latitude, order.user_longitude))
        self.user_loc_list.append(Loc(order.user_latitude, order.user_longitude))
        self.merchant_loc_list.append(Loc(order.shop_latitude, order.shop_longitude))
        self.order_stage_flag.append(order.dispatch_stage)  # 骑手刚接单时该订单的订单状态

        # 每次派新单都跑一次---新预测路径----会有问题吗？
        # self.route_plan_merchant_user_loc = Route(self.available_merchant_loc, self.user_loc_list,
        #                                           Loc(self.lat, self.lon), self.cur_time, self.order_stage_flag)
        # dis, self.route, c_time, self.route_flag_list = self.route_plan.route_generation()
        # 返回 他们后面每个时间步 的 位置列表，用于后面step更新
        self.generate_future_route(real_time)

    def exchange_take_order(self, order, real_time, courier1_huandan_time_lat, courier1_huandan_time_lon,
                            courier2_huandan_time_lat, courier2_huandan_time_lon):
        self.order_list.append(order)
        self.cur_order_num += 1
        if self.cur_order_num >= self.capacity:
            self.full = True
        if order.dispatch_stage == 1:
            self.available_loc_real_time.append(Loc(order.shop_latitude, order.shop_longitude))
        elif order.dispatch_stage == 2:
            self.available_loc_real_time.append(Loc(order.user_latitude, order.user_longitude))
        self.user_loc_list.append(Loc(order.user_latitude, order.user_longitude))
        self.merchant_loc_list.append(Loc(order.shop_latitude, order.shop_longitude))
        self.order_stage_flag.append(order.dispatch_stage)  # 骑手刚接单时该订单的订单状态
        # 添加换单处理时间的位置处理
        encounter_start_lat = self.lat
        encounter_start_lon = self.lon
        encounter_end_lat = (courier1_huandan_time_lat + courier2_huandan_time_lat) / 2
        encounter_end_lon = (courier1_huandan_time_lon + courier2_huandan_time_lon) / 2
        encounter_sudu = 12.11 / 2

        courier1_courier2_distance = get_distance_hav(courier1_huandan_time_lat,
                                                      courier1_huandan_time_lon,
                                                      courier2_huandan_time_lat,
                                                      courier2_huandan_time_lon) / 2
        courier1_courier2_time = courier1_courier2_distance / encounter_sudu * (
                60 * 60)
        if courier1_courier2_time != 0:
            one_encounter_step_lat = (encounter_end_lat - encounter_start_lat) / courier1_courier2_time
            one_encounter_step_lon = (encounter_end_lon - encounter_start_lon) / courier1_courier2_time
        else:
            one_encounter_step_lat = encounter_end_lat - encounter_start_lat
            one_encounter_step_lon = encounter_end_lon - encounter_start_lon

        for encounter_time_step in range(real_time, real_time + int(courier1_courier2_time) + 1):
            self.route_time_step[encounter_time_step] = Loc(
                encounter_start_lat + one_encounter_step_lat * (encounter_time_step - real_time),
                encounter_start_lon + one_encounter_step_lon * (
                        encounter_time_step - real_time))
        for encounter_time_step in range(real_time + int(courier1_courier2_time) + 1, real_time + int(courier1_courier2_time) + 31):
            self.route_time_step[encounter_time_step] = self.route_time_step[real_time + int(courier1_courier2_time)]
        for encounter_time_step in range(real_time, real_time + int(courier1_courier2_time) + 31):
            self.route_flag_to_be_updated[encounter_time_step] = self.route_flag_to_be_updated[real_time - 1]
        # + 30  # 单位：时间步数,考虑换单停下来的交换时间，用户的反应时间
        begin_route_plan_time = real_time + int(courier1_courier2_time) + 30
        self.generate_future_route(begin_route_plan_time)

    def exchange_drop_order(self, order, real_time, courier1_huandan_time_lat, courier1_huandan_time_lon,
                            courier2_huandan_time_lat, courier2_huandan_time_lon):
        remain_order_stage = self.route_flag_to_be_updated[real_time - 1]
        remain_dispatch_order_id_list = []
        for remain_dispatch_order_item in remain_order_stage:
            order_id = self.order_list[remain_dispatch_order_item[0]].order_id
            remain_dispatch_order_id_list.append(order_id)

        drop_order_loc_id = 0
        for order_loc_id in range(len(self.order_list)):
            if order.order_id == self.order_list[order_loc_id].order_id:
                drop_order_loc_id = order_loc_id
                break
        self.order_list.pop(drop_order_loc_id)
        self.cur_order_num -= 1
        self.available_loc_real_time.pop(drop_order_loc_id)
        self.user_loc_list.pop(drop_order_loc_id)
        self.merchant_loc_list.pop(drop_order_loc_id)
        self.order_stage_flag.pop(drop_order_loc_id)
        max_route_prediction_time_step = max(self.route_flag_to_be_updated.keys())

        for time_step in range(self.cur_time, max_route_prediction_time_step + 1):
            if time_step in self.route_flag_to_be_updated.keys():
                self.route_flag_to_be_updated.pop(time_step)
            # for route_flag_item in self.route_flag_to_be_updated[time_step]:
            # if route_flag_item[0] == drop_order_loc_id:
            # self.route_flag_to_be_updated[time_step].remove(route_flag_item)
        # 添加换单处理时间的位置处理
        encounter_start_lat = self.lat
        encounter_start_lon = self.lon
        encounter_end_lat = (courier1_huandan_time_lat + courier2_huandan_time_lat) / 2
        encounter_end_lon = (courier1_huandan_time_lon + courier2_huandan_time_lon) / 2
        encounter_sudu = 12.11 / 2

        courier1_courier2_distance = get_distance_hav(courier1_huandan_time_lat,
                                                      courier1_huandan_time_lon,
                                                      courier2_huandan_time_lat,
                                                      courier2_huandan_time_lon) / 2
        courier1_courier2_time = courier1_courier2_distance / encounter_sudu * (
                60 * 60)
        if courier1_courier2_time != 0:
            one_encounter_step_lat = (encounter_end_lat - encounter_start_lat) / courier1_courier2_time
            one_encounter_step_lon = (encounter_end_lon - encounter_start_lon) / courier1_courier2_time
        else:
            one_encounter_step_lat = encounter_end_lat - encounter_start_lat
            one_encounter_step_lon = encounter_end_lon - encounter_start_lon

        for encounter_time_step in range(real_time, real_time + int(courier1_courier2_time) + 1):
            self.route_time_step[encounter_time_step] = Loc(
                encounter_start_lat + one_encounter_step_lat * (encounter_time_step - real_time),
                encounter_start_lon + one_encounter_step_lon * (
                        encounter_time_step - real_time))
        for encounter_time_step in range(real_time + int(courier1_courier2_time) + 1, real_time + int(courier1_courier2_time) + 31):
            self.route_time_step[encounter_time_step] = self.route_time_step[real_time + int(courier1_courier2_time)]

        after_exchange_remain_order_stage = []
        for remain_dispatch_order_id in range(len(remain_dispatch_order_id_list)):
            for cur_order_list_item_id in range(len(self.order_list)):
                if self.order_list[cur_order_list_item_id].order_id == remain_dispatch_order_id_list[remain_dispatch_order_id]:
                    after_exchange_remain_order_stage.append((cur_order_list_item_id,
                                                              remain_order_stage[remain_dispatch_order_id][1]))
                    # remain_order_stage[remain_dispatch_order_id][0] = cur_order_list_item_id
                    break

        for encounter_time_step in range(real_time - 1, real_time + int(courier1_courier2_time) + 31):
            self.route_flag_to_be_updated[encounter_time_step] = after_exchange_remain_order_stage
        # + 30  # 单位：时间步数,考虑换单停下来的交换时间，用户的反应时间
        begin_route_plan_time = real_time + int(courier1_courier2_time) + 30
        self.generate_future_route(begin_route_plan_time)

    def update_courier_state(self):  # real_time
        # 每个时间步更新一次
        #     # 更新后面骑手每个时间步的位置、订单的配送阶段（骑手对象、订单对象都有该属性）-----订单列表、订单数目
        #     print('更新骑手状态')
        # 更新上一时间步的骑手及相关订单的信息。
        # if self.courier_id == 2053730:
        #     print('debug')
        if self.cur_time >= self.occur_time:
            self.online = True  # 不online，位置不可用

        if self.cur_time in self.route_time_step.keys() and self.online:
            self.lat = self.route_time_step[self.cur_time].lat
            self.lon = self.route_time_step[self.cur_time].lon

            for route_flag_list_id in range(len(self.route_flag_to_be_updated[self.cur_time])):
                order_loc_id = self.route_flag_to_be_updated[self.cur_time][route_flag_list_id][0]
                order_stage = self.route_flag_to_be_updated[self.cur_time][route_flag_list_id][1]

                # if self.order_stage_flag[order_loc_id] == order_stage: # 中间阶段
                if len(self.order_stage_flag) >= order_loc_id + 1:
                    if self.order_stage_flag[order_loc_id] != order_stage:  # 到达商家、到达用户位置
                        # 配送阶段改变的时间点
                        # self.order_stage_flag[order_loc_id] = order_stage
                        if self.order_stage_flag[order_loc_id] == 1:
                            # 进入要送往 用户的配送阶段。
                            if order_stage == 2:
                                self.order_stage_flag[order_loc_id] = 2
                                self.order_list[order_loc_id].dispatch_stage = 2
                                self.available_loc_real_time[order_loc_id] = self.user_loc_list[order_loc_id]
                                self.cost_time += self.cur_time - self.order_list[order_loc_id].order_create_time
                                self.order_list[order_loc_id].arrive_merchant_time = self.cur_time
                            elif order_stage == 0:
                                self.order_stage_flag[order_loc_id] = 0
                                self.order_list[order_loc_id].dispatch_stage = 0
                                self.cur_order_num -= 1
                                self.available_loc_real_time[order_loc_id] = 0
                                self.cost_time += self.cur_time - self.order_list[order_loc_id].arrive_merchant_time
                                self.order_list[order_loc_id].order_deliver_time = self.cur_time
                                if self.cur_time > self.order_list[order_loc_id].promise_deliver_time:
                                    self.overdue_order_num += 1

                        elif self.order_stage_flag[order_loc_id] == 2:
                            if order_stage != 0:
                                print('debug')
                            else:
                                # 当前这个订单送达用户，订单完成了。
                                self.order_stage_flag[order_loc_id] = 0
                                self.order_list[order_loc_id].dispatch_stage = 0
                                self.cur_order_num -= 1
                                self.available_loc_real_time[order_loc_id] = 0
                                self.cost_time += self.cur_time - self.order_list[order_loc_id].arrive_merchant_time
                                self.order_list[order_loc_id].order_deliver_time = self.cur_time
                                if self.cur_time > self.order_list[order_loc_id].promise_deliver_time:
                                    self.overdue_order_num += 1
                else:
                    print('debug')
            if self.cur_order_num < self.capacity:
                self.full = False
            # if sum(self.order_stage_flag) == 0:
            # self.order_list = []
            # self.order_stage_flag = []
            # self.merchant_loc_list = []
            # self.user_loc_list = []
            # self.cur_order_num = 0
            # self.route_time_step = {}
            # self.route_flag_to_be_updated = {}
            # self.available_loc_real_time = []

            # 用于route plan
            # self.available_loc = []  # 每个订单的 当前下一个配送站点的位置(可以为商家，也可为用户)【更新】
            # self.available_flag = []  # 手里每个个订单的阶段【更新】
            # 骑手在当前位置---骑手到达商家位置， order_stage_flag = 1(一接单就将order_stage_flag=1【初始化订单时就将flag=1】)
            # 骑手到达商家位置就 将order_stage_flag = 2，----后面的目标地点为用户位置
            # 骑手到达用户位置就将order_stage_flag = 0，-----订单完成

        to_dispatch_order_num = 0
        for order_count in self.order_list:
            if order_count.dispatch_stage != 0:
                to_dispatch_order_num = to_dispatch_order_num + 1
        if to_dispatch_order_num != self.cur_order_num:
            self.cur_order_num = to_dispatch_order_num
        self.cur_time += 1
