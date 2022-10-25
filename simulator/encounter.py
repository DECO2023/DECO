class Encounter(object):
    __slots__ = ("encounter_id1",
                 "encounter_id2",
                 "encounter_start_time_slot",
                 "encounter_end_time_slot",
                 "courier1_order_list",
                 "courier1_order_num",
                 "courier2_order_list",
                 "courier2_order_num")

    def __init__(self, encounter_id1, encounter_id2, encounter_time_slot):
        self.encounter_id1 = encounter_id1  # 相遇的骑手1的骑手id
        self.encounter_id2 = encounter_id2  # 相遇的骑手2的骑手id
        self.encounter_start_time_slot = encounter_time_slot  # 两个骑手相遇开始的时间
        self.encounter_end_time_slot = encounter_time_slot  # 两个骑手相遇结束的时间
        # self.has_deal_with = False

        self.courier1_order_list = []
        self.courier2_order_list = []
        self.courier2_order_num = 0
        self.courier1_order_num = 0
