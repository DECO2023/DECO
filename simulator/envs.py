import time
import numpy as np
from simulator.orders import *
from simulator.couriers_update_200_2min import *
from simulator.utility import get_distance_hav

# 更新换单处理时间----符合实际情况

# 对一个商圈Region数据做实验

class Region:
    def __init__(self, courier_init, real_orders):
        self.courier_init = courier_init
        self.real_orders = real_orders
        self.day_orders = []    # 初始化；用于存储对象，后续对这些对象作每个时间步订单配送状态的更新，状态为2，则配送完成则不再管。
        self.day_couriers = []  # 初始化为骑手第一次出现的时间步和位置，后面可以根据预测的路径往里面加后续时间步的位置信息
        self.city_time = 0  # 0- 8640 中的一个值，表示当前所处的时间步
        self.n_step = 86400  # 一天一共的时间步个数
        # self.order_response_rate = 0

        self.couriers_dict = {}  # 用于存储对象，后续对这些对象作每个时间步位置的更新

        # self.day_encounter = [[] for _ in np.arange(self.n_step)]
        self.encounter_exchange_event = []
    # 平台派单（按距离最近派单的逻辑）策略

    def bootstrap_one_day_orders(self):
        # 将订单数据输入加载入模型
        # ['1', '31.255537', '121.45916', '31.25317194', '121.46889204',   0-4
        #  '2020-10-01 11:59:14', '2020-10-01 12:17:56', '37.99', '3.8',  5-8,
        #  '269345', '23487920.0', '2758233.0', '2020-10-01 12:03:56',   9-12
        #  '2020-10-01 12:07:16', '2020-10-01 12:09:06']  13-14
        # 5为创建订单，送达为6，到店为13
        day_orders = [[] for _ in np.arange(self.n_step)]
        count = 0
        for iorder in self.real_orders:
            # 2020-10-1
            order_create_timestep = int((int(time.mktime(time.strptime(iorder[5], "%Y-%m-%d %H:%M:%S"))) - int(
                time.mktime(time.strptime("2020-10-01 00:00:00", "%Y-%m-%d %H:%M:%S")))) )
            # 2020-10-12
            # order_create_timestep = int((int(time.mktime(time.strptime(iorder[5], "%Y-%m-%d %H:%M:%S"))) - int(
            #     time.mktime(time.strptime("2020-10-12 00:00:00", "%Y-%m-%d %H:%M:%S")))))
                # time.mktime(time.strptime("2020-10-12 00:00:00", "%Y-%m-%d %H:%M:%S")))) / 10)
            # if order_create_timestep < 0:
            #     print('debug')

            # 2020-6-6
            # if len(iorder[5].split(':')[-1]) > 2:
            #     order_create_time_str = "2020-06-06 "+iorder[5][:-1]
            # elif len(iorder[5].split(':')[0]) > 2:
            #     order_create_time_str = "2020-06-06 "+iorder[5][1:]
            # elif iorder[5] == '':
            #     continue
            # else:
            #     order_create_time_str = "2020-06-06 "+iorder[5]
            # order_create_timestep = int((int(time.mktime(time.strptime(order_create_time_str, "%Y-%m-%d %H:%M:%S"))) - int(
            #     time.mktime(time.strptime("2020-06-06 00:00:00", "%Y-%m-%d %H:%M:%S")))) / 10)

            # promise_order_deliver_timestep = order_create_timestep + int(int(iorder[15]) / 10)
            promise_order_deliver_timestep = order_create_timestep + int(int(iorder[15]))

            price = float(iorder[7])

            # 处理一下输入：之前7-10有些promise=0 的订单需要过滤；
            if promise_order_deliver_timestep == order_create_timestep:
                continue

            day_orders[order_create_timestep].append(Order(int(iorder[0]), float(iorder[1]), float(iorder[2]),
                                                           float(iorder[3]), float(iorder[4]),
                                                           order_create_timestep, promise_order_deliver_timestep, price))
            count += 1
            # print(count)
        self.day_orders = day_orders

    def bootstrap_one_day_couriers(self):
        # 将骑手数据输入加载入模型
        # ['2758233.0', '31.255537', '121.45916', '2020-10-01 12:07:16']
        day_couriers = [[] for _ in range(self.n_step)]
        for i_couriers in self.courier_init:
            # 这里初始化骑手时可以让id为真实id或者虚拟id
            # 2020-10-1
            first_occur_time_step = int((int(time.mktime(time.strptime(i_couriers[3], "%Y-%m-%d %H:%M:%S"))) - int(
                time.mktime(time.strptime("2020-10-01 00:00:00", "%Y-%m-%d %H:%M:%S")))) )
            # 2020-10-12
            # first_occur_time_step = int((int(time.mktime(time.strptime(i_couriers[3], "%Y-%m-%d %H:%M:%S"))) - int(
            #     time.mktime(time.strptime("2020-10-12 00:00:00", "%Y-%m-%d %H:%M:%S")))))
                # time.mktime(time.strptime("2020-10-12 00:00:00", "%Y-%m-%d %H:%M:%S")))) / 10)
            # 2020-6-6
            # if len(i_couriers[3].split(':')[-1]) > 2:
            #     first_occur_time_str = "2020-06-06 "+i_couriers[3][:-1]
            # elif len(i_couriers[3].split(':')[0]) > 2:
            #     first_occur_time_str = "2020-06-06 "+i_couriers[3][1:]
            # elif i_couriers[3] == '':
            #     continue
            # else:
            #     first_occur_time_str = "2020-06-06 "+i_couriers[3]
            # first_occur_time_step = int((int(time.mktime(time.strptime(first_occur_time_str, "%Y-%m-%d %H:%M:%S"))) - int(
            #     time.mktime(time.strptime("2020-06-06 00:00:00", "%Y-%m-%d %H:%M:%S")))) / 10)

            c = Courier(int(float(i_couriers[0])), float(i_couriers[1]), float(i_couriers[2]), first_occur_time_step)
            day_couriers[first_occur_time_step].append(c)
            self.couriers_dict[int(float(i_couriers[0]))] = c
        self.day_couriers = day_couriers

    def env_initialize(self):
        self.city_time = 0
        self.bootstrap_one_day_orders()
        self.bootstrap_one_day_couriers()
        # self.step_bootstrap_order(self.day_orders[self.city_time], self.city_time)
        # self.step_bootstrap_couriers(self.day_couriers[self.city_time], self.city_time)

    def day_couriers_update(self, order_time):
        # couriers_info_collect 调用的骑手对象
        couriers_list_before_curtime = []
        for time_count in range(order_time + 1):
            for ic in self.day_couriers[time_count]:
                couriers_list_before_curtime.append(ic)
        return couriers_list_before_curtime

    def couriers_info_collect(self, one_order, T):
        order_time_slot = T
        courier_distance = []  # 骑手和商家间的距离
        couriers_ = []  # 该时刻可以接单的骑手列表(在线骑手)
        # cost_time = []  # 计算商家-用户间骑手配送需要的额外时间

        # to do :
        # day_couriers 每个时间步的 骑手信息需要更新，类似 env.step_couriers_state_update函数控制.online状态
        # self.occur_time 为 骑手第一次出现的时刻，就让这个骑手继续接单，在该时刻继续接单，更新day_couriers(根据couriers_dist_time)

        # ——solution:若当前时间步有订单，看系统当前已出现了的骑手的位置（最近时刻记录的位置），将最近的骑手派给他。
        couriers_time_before = self.day_couriers_update(order_time_slot)
        for ic in couriers_time_before:
            # courier.full状态，骑手接一个单时，判断与capacity的大小，满了就不考虑该骑手
            if not ic.full and ic.cur_order_num <= ic.capacity:
                couriers_.append(ic)
                courier_distance.append(get_distance_hav(ic.lat, ic.lon, float(one_order.shop_latitude),
                                                         float(one_order.shop_longitude)))
                # cost_time.append((ic, ic.take_order_temp(one_order)))

        return couriers_, courier_distance
