class Order(object):
    __slots__ = ("order_id",
                 "shop_longitude", "shop_latitude",
                 "user_longitude", "user_latitude",
                 "order_create_time", "order_deliver_time", "arrive_merchant_time", "promise_deliver_time",
                 "dispatch_stage",
                 "hop_num", "order_price")

    def __init__(self, order_id, shop_lat, shop_lon, user_lat, user_lon,
                 order_create_time, promise_order_deliver_time,price):
        self.order_id = order_id

        self.shop_longitude = shop_lon
        self.shop_latitude = shop_lat
        self.user_longitude = user_lon
        self.user_latitude = user_lat

        self.order_create_time = order_create_time
        self.arrive_merchant_time = 0
        self.order_deliver_time = 0

        self.promise_deliver_time = promise_order_deliver_time  # 用于计算超时率

        self.dispatch_stage = 1  # 手里每个订单的阶段
        # 骑手在当前位置---骑手到达商家位置， order_stage_flag = 1(一接单就将order_stage_flag=1【初始化订单时就将flag=1】)
        # 骑手到达商家位置就 将order_stage_flag = 2，----后面的目标地点为用户位置
        # 骑手到达用户位置就将order_stage_flag = 0，-----订单完成

        # 跳数
        self.hop_num = 0

        self.order_price = price