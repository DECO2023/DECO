from matplotlib.ticker import MultipleLocator
import os
import re
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

plt.rc('font', family='Times New Roman', size=18)
# print('不换单-500')
# # 不换单的超时率
# last_file_name = "D:/exchange/train/optimize-2022-1-19/no-exchange-zh1001/time_step_86399_courier_state.txt"
# state_file = open(last_file_name, "r")
# # 超时率
# overdue_order_num_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
# all_order_num_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
# for line in state_file:
#     line = line.strip('\n')
#     first_item = line.split(',')[0]
#     if first_item == '':
#         order_dispatch_stage = int(line.split(',')[10].split(':')[1])
#         order_create_time = int(line.split(',')[6].split(':')[1])
#         order_deliver_time = int(line.split(',')[8].split(':')[1])
#         promise_deliver_time = int(line.split(',')[9].split(':')[1])
#         if order_dispatch_stage == 0:
#             if promise_deliver_time < order_deliver_time:
#                 overdue_order_num_list[int(order_create_time / 3600)] += 1
#                 # print(line)
#             all_order_num_list[int(order_create_time / 3600)] += 1
# print(overdue_order_num_list)
# print(all_order_num_list)
# overdue_rate = []
# hour_list = []
# for i in range(len(all_order_num_list)):
#     if all_order_num_list[i] != 0:
#         overdue_rate.append(overdue_order_num_list[i] / all_order_num_list[i] / 2)
#         hour_list.append(i + 1)
#     else:
#         overdue_rate.append(0)
#         hour_list.append(i + 1)
#
# print(overdue_rate)
#
# day_overdue_sum = sum(overdue_order_num_list)
# day_all_sum = sum(all_order_num_list)
# day_overdue_rate = day_overdue_sum / day_all_sum
# print(day_overdue_rate)
# 10-20h的超时率
# working_time_overdue_sum = 0
# working_time_order_sum = 0
# for i in range(len(all_order_num_list)):
#     if (0 <= i <12) or (13 <= i < 23):
#         continue
#     else:
#         working_time_overdue_sum += overdue_order_num_list[i]
#         working_time_order_sum += all_order_num_list[i]
# working_time_overdue_rate = working_time_overdue_sum / working_time_order_sum
# print(working_time_overdue_rate)

print('不换单-200')
# 不换单的超时率
last_file_name = "D:/exchange/train/optimize-2022-1-19/no-exchange-zh1001_200/time_step_86399_courier_state.txt"
state_file = open(last_file_name, "r")
# 超时率
overdue_order_num_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
all_order_num_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for line in state_file:
    line = line.strip('\n')
    first_item = line.split(',')[0]
    if first_item == '':
        order_dispatch_stage = int(line.split(',')[10].split(':')[1])
        order_create_time = int(line.split(',')[6].split(':')[1])
        order_deliver_time = int(line.split(',')[8].split(':')[1])
        promise_deliver_time = int(line.split(',')[9].split(':')[1])
        if order_dispatch_stage == 0:
            if promise_deliver_time < order_deliver_time:
                overdue_order_num_list[int(order_create_time / 3600)] += 1
                # print(line)
            all_order_num_list[int(order_create_time / 3600)] += 1
print(overdue_order_num_list)
print(all_order_num_list)
overdue_rate = []
hour_list = []
for i in range(len(all_order_num_list)):
    if all_order_num_list[i] != 0:
        overdue_rate.append(overdue_order_num_list[i] / all_order_num_list[i] / 2)
        hour_list.append(i + 1)
    else:
        overdue_rate.append(0)
        hour_list.append(i + 1)

print(overdue_rate)

day_overdue_sum = sum(overdue_order_num_list)
day_all_sum = sum(all_order_num_list)
day_overdue_rate = day_overdue_sum / day_all_sum
print(day_overdue_rate)
# 10-20h的超时率
working_time_overdue_sum = 0
working_time_order_sum = 0
for i in range(len(all_order_num_list)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum += overdue_order_num_list[i]
        working_time_order_sum += all_order_num_list[i]
working_time_overdue_rate = working_time_overdue_sum / working_time_order_sum
print(working_time_overdue_rate)




# print('不换单-300')
# # 不换单的超时率
# last_file_name = "D:/exchange/train/optimize-2022-1-19/no-exchange-zh1001_300/time_step_86399_courier_state.txt"
# state_file = open(last_file_name, "r")
# # 超时率
# overdue_order_num_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
# all_order_num_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
# for line in state_file:
#     line = line.strip('\n')
#     first_item = line.split(',')[0]
#     if first_item == '':
#         order_dispatch_stage = int(line.split(',')[10].split(':')[1])
#         order_create_time = int(line.split(',')[6].split(':')[1])
#         order_deliver_time = int(line.split(',')[8].split(':')[1])
#         promise_deliver_time = int(line.split(',')[9].split(':')[1])
#         if order_dispatch_stage == 0:
#             if promise_deliver_time < order_deliver_time:
#                 overdue_order_num_list[int(order_create_time / 3600)] += 1
#                 # print(line)
#             all_order_num_list[int(order_create_time / 3600)] += 1
# print(overdue_order_num_list)
# print(all_order_num_list)
# overdue_rate = []
# hour_list = []
# for i in range(len(all_order_num_list)):
#     if all_order_num_list[i] != 0:
#         overdue_rate.append(overdue_order_num_list[i] / all_order_num_list[i] / 2)
#         hour_list.append(i + 1)
#     else:
#         overdue_rate.append(0)
#         hour_list.append(i + 1)
#
# print(overdue_rate)
#
# day_overdue_sum = sum(overdue_order_num_list)
# day_all_sum = sum(all_order_num_list)
# day_overdue_rate = day_overdue_sum / day_all_sum
# print(day_overdue_rate)
# # 10-20h的超时率
# # working_time_overdue_sum = 0
# # working_time_order_sum = 0
# # for i in range(len(all_order_num_list)):
# #     if (0 <= i <12) or (13 <= i < 23):
# #         continue
# #     else:
# #         working_time_overdue_sum += overdue_order_num_list[i]
# #         working_time_order_sum += all_order_num_list[i]
# # working_time_overdue_rate = working_time_overdue_sum / working_time_order_sum
# # print(working_time_overdue_rate)
#
# print('不换单-400')
# # 不换单的超时率
# last_file_name = "D:/exchange/train/optimize-2022-1-19/no-exchange-zh1001_400/time_step_86399_courier_state.txt"
# state_file = open(last_file_name, "r")
# # 超时率
# overdue_order_num_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
# all_order_num_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
# for line in state_file:
#     line = line.strip('\n')
#     first_item = line.split(',')[0]
#     if first_item == '':
#         order_dispatch_stage = int(line.split(',')[10].split(':')[1])
#         order_create_time = int(line.split(',')[6].split(':')[1])
#         order_deliver_time = int(line.split(',')[8].split(':')[1])
#         promise_deliver_time = int(line.split(',')[9].split(':')[1])
#         if order_dispatch_stage == 0:
#             if promise_deliver_time < order_deliver_time:
#                 overdue_order_num_list[int(order_create_time / 3600)] += 1
#                 # print(line)
#             all_order_num_list[int(order_create_time / 3600)] += 1
# print(overdue_order_num_list)
# print(all_order_num_list)
# overdue_rate = []
# hour_list = []
# for i in range(len(all_order_num_list)):
#     if all_order_num_list[i] != 0:
#         overdue_rate.append(overdue_order_num_list[i] / all_order_num_list[i] / 2)
#         hour_list.append(i + 1)
#     else:
#         overdue_rate.append(0)
#         hour_list.append(i + 1)
#
# print(overdue_rate)
#
# day_overdue_sum = sum(overdue_order_num_list)
# day_all_sum = sum(all_order_num_list)
# day_overdue_rate = day_overdue_sum / day_all_sum
# print(day_overdue_rate)
# 10-20h的超时率
# working_time_overdue_sum = 0
# working_time_order_sum = 0
# for i in range(len(all_order_num_list)):
#     if (0 <= i <12) or (13 <= i < 23):
#         continue
#     else:
#         working_time_overdue_sum += overdue_order_num_list[i]
#         working_time_order_sum += all_order_num_list[i]
# working_time_overdue_rate = working_time_overdue_sum / working_time_order_sum
# print(working_time_overdue_rate)

# print('换单SD rule-based')
# # 不换单的超时率
# exchange_last_file_name1_1 = "D:/exchange/train/optimize-2022-1-19/SD-record/time_step_57599_courier_state.txt"
# exchange_state_file1_1 = open(exchange_last_file_name1_1, "r")
# # 超时率
# exchange_overdue_order_num_list1_1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
# exchange_all_order_num_list1_1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
# for exchange_line in exchange_state_file1_1:
#     exchange_line = exchange_line.strip('\n')
#     exchange_first_item = exchange_line.split(',')[0]
#     if exchange_first_item == '':
#         exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
#         exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
#         exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
#         exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
#         if exchange_order_dispatch_stage == 0:
#             if exchange_promise_deliver_time < exchange_order_deliver_time:
#                 exchange_overdue_order_num_list1_1[int(exchange_order_create_time / 3600)] += 1
#             exchange_all_order_num_list1_1[int(exchange_order_create_time / 3600)] += 1
# print(exchange_overdue_order_num_list1_1)
# print(exchange_all_order_num_list1_1)
# exchange_overdue_rate1_1 = []
# exchange_hour_list1_1 = []
# for i in range(len(exchange_all_order_num_list1_1)):
#     if exchange_all_order_num_list1_1[i] != 0:
#         exchange_overdue_rate1_1.append(exchange_overdue_order_num_list1_1[i] / exchange_all_order_num_list1_1[i] / 2)
#         exchange_hour_list1_1.append(i + 1)
#     else:
#         exchange_overdue_rate1_1.append(0)
#         exchange_hour_list1_1.append(i + 1)
# print(exchange_overdue_rate1_1)
#
# exchange_day_overdue_sum1_1 = sum(exchange_overdue_order_num_list1_1)
# exchange_day_all_sum1_1 = sum(exchange_all_order_num_list1_1)
# exchange_day_overdue_rate1_1 = exchange_day_overdue_sum1_1 / exchange_day_all_sum1_1
# print(exchange_day_overdue_rate1_1)
#
# # 10-20h的超时率
# working_time_overdue_sum1_1 = 0
# working_time_order_sum1_1 = 0
# for i in range(len(exchange_all_order_num_list1_1)):
#     if (0 <= i < 10) or (21 <= i < 23):
#         continue
#     else:
#         working_time_overdue_sum1_1 += exchange_overdue_order_num_list1_1[i]
#         working_time_order_sum1_1 += exchange_all_order_num_list1_1[i]
# working_time_overdue_rate1_1 = working_time_overdue_sum1_1 / working_time_order_sum1_1
# print(working_time_overdue_rate1_1)
#

# print('换单SD rule-based-200')
# # 不换单的超时率
# exchange_last_file_name1_1 = "D:/exchange/train/optimize-2022-1-19/SD-record-200/time_step_57599_courier_state.txt"
# exchange_state_file1_1 = open(exchange_last_file_name1_1, "r")
# # 超时率
# exchange_overdue_order_num_list1_1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
# exchange_all_order_num_list1_1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
# for exchange_line in exchange_state_file1_1:
#     exchange_line = exchange_line.strip('\n')
#     exchange_first_item = exchange_line.split(',')[0]
#     if exchange_first_item == '':
#         exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
#         exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
#         exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
#         exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
#         if exchange_order_dispatch_stage == 0:
#             if exchange_promise_deliver_time < exchange_order_deliver_time:
#                 exchange_overdue_order_num_list1_1[int(exchange_order_create_time / 3600)] += 1
#             exchange_all_order_num_list1_1[int(exchange_order_create_time / 3600)] += 1
# print(exchange_overdue_order_num_list1_1)
# print(exchange_all_order_num_list1_1)
# exchange_overdue_rate1_1 = []
# exchange_hour_list1_1 = []
# for i in range(len(exchange_all_order_num_list1_1)):
#     if exchange_all_order_num_list1_1[i] != 0:
#         exchange_overdue_rate1_1.append(exchange_overdue_order_num_list1_1[i] / exchange_all_order_num_list1_1[i] / 2)
#         exchange_hour_list1_1.append(i + 1)
#     else:
#         exchange_overdue_rate1_1.append(0)
#         exchange_hour_list1_1.append(i + 1)
# print(exchange_overdue_rate1_1)
#
# exchange_day_overdue_sum1_1 = sum(exchange_overdue_order_num_list1_1)
# exchange_day_all_sum1_1 = sum(exchange_all_order_num_list1_1)
# exchange_day_overdue_rate1_1 = exchange_day_overdue_sum1_1 / exchange_day_all_sum1_1
# print(exchange_day_overdue_rate1_1)


print('换单SD rule-based-200_2min')
# 不换单的超时率
exchange_last_file_name1_1 = "D:/exchange/train/optimize-2022-1-19/SD-record-200_2min/time_step_86399_courier_state.txt"
exchange_state_file1_1 = open(exchange_last_file_name1_1, "r")
# 超时率
exchange_overdue_order_num_list1_1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list1_1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file1_1:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list1_1[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list1_1[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list1_1)
print(exchange_all_order_num_list1_1)
exchange_overdue_rate1_1 = []
exchange_hour_list1_1 = []
for i in range(len(exchange_all_order_num_list1_1)):
    if exchange_all_order_num_list1_1[i] != 0:
        exchange_overdue_rate1_1.append(exchange_overdue_order_num_list1_1[i] / exchange_all_order_num_list1_1[i] / 2)
        exchange_hour_list1_1.append(i + 1)
    else:
        exchange_overdue_rate1_1.append(0)
        exchange_hour_list1_1.append(i + 1)
print(exchange_overdue_rate1_1)

exchange_day_overdue_sum1_1 = sum(exchange_overdue_order_num_list1_1)
exchange_day_all_sum1_1 = sum(exchange_all_order_num_list1_1)
exchange_day_overdue_rate1_1 = exchange_day_overdue_sum1_1 / exchange_day_all_sum1_1
print(exchange_day_overdue_rate1_1)

# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list1_1)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list1_1[i]
        working_time_order_sum3_0+=exchange_all_order_num_list1_1[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)



print('换单SD rule-based-200_2min_filter1200')
# 不换单的超时率
exchange_last_file_name1_1 = "D:/exchange/train/optimize-2022-1-19/SD-record-200_2min_filter1200/time_step_86399_courier_state.txt"
exchange_state_file1_1 = open(exchange_last_file_name1_1, "r")
# 超时率
exchange_overdue_order_num_list1_1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list1_1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file1_1:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list1_1[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list1_1[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list1_1)
print(exchange_all_order_num_list1_1)
exchange_overdue_rate1_1 = []
exchange_hour_list1_1 = []
for i in range(len(exchange_all_order_num_list1_1)):
    if exchange_all_order_num_list1_1[i] != 0:
        exchange_overdue_rate1_1.append(exchange_overdue_order_num_list1_1[i] / exchange_all_order_num_list1_1[i] / 2)
        exchange_hour_list1_1.append(i + 1)
    else:
        exchange_overdue_rate1_1.append(0)
        exchange_hour_list1_1.append(i + 1)
print(exchange_overdue_rate1_1)

exchange_day_overdue_sum1_1 = sum(exchange_overdue_order_num_list1_1)
exchange_day_all_sum1_1 = sum(exchange_all_order_num_list1_1)
exchange_day_overdue_rate1_1 = exchange_day_overdue_sum1_1 / exchange_day_all_sum1_1
print(exchange_day_overdue_rate1_1)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list1_1)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list1_1[i]
        working_time_order_sum3_0+=exchange_all_order_num_list1_1[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)
# print('换单Osquare-SD rule-based')
# # 不换单的超时率
# # exchange_last_file_name1 = "D:/exchange/train/baseline/SD-OSquare-record/time_step_42599_courier_state.txt"
# exchange_last_file_name1 = "D:/exchange/train/optimize-2022-1-19/SD-Osquare-record/time_step_57599_courier_state.txt"
# exchange_state_file1 = open(exchange_last_file_name1, "r")
# # 超时率
# exchange_overdue_order_num_list1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
# exchange_all_order_num_list1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
# for exchange_line in exchange_state_file1:
#     exchange_line = exchange_line.strip('\n')
#     exchange_first_item = exchange_line.split(',')[0]
#     if exchange_first_item == '':
#         exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
#         exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
#         exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
#         exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
#         if exchange_order_dispatch_stage == 0:
#             if exchange_promise_deliver_time < exchange_order_deliver_time:
#                 exchange_overdue_order_num_list1[int(exchange_order_create_time / 3600)] += 1
#             exchange_all_order_num_list1[int(exchange_order_create_time / 3600)] += 1
# print(exchange_overdue_order_num_list1)
# print(exchange_all_order_num_list1)
# exchange_overdue_rate1 = []
# exchange_hour_list1 = []
# for i in range(len(exchange_all_order_num_list1)):
#     if exchange_all_order_num_list1[i] != 0:
#         exchange_overdue_rate1.append(exchange_overdue_order_num_list1[i] / exchange_all_order_num_list1[i] / 2)
#         exchange_hour_list1.append(i + 1)
#     else:
#         exchange_overdue_rate1.append(0)
#         exchange_hour_list1.append(i + 1)
# print(exchange_overdue_rate1)
#
# exchange_day_overdue_sum1 = sum(exchange_overdue_order_num_list1)
# exchange_day_all_sum1 = sum(exchange_all_order_num_list1)
# exchange_day_overdue_rate1 = exchange_day_overdue_sum1 / exchange_day_all_sum1
# print(exchange_day_overdue_rate1)
#
# working_time_overdue_sum1 = 0
# working_time_order_sum1 = 0
# for i in range(len(exchange_all_order_num_list1)):
#     if (0 <= i < 10) or (21 <= i < 23):
#         continue
#     else:
#         working_time_overdue_sum1 += exchange_overdue_order_num_list1[i]
#         working_time_order_sum1 += exchange_all_order_num_list1[i]
# working_time_overdue_rate1 = working_time_overdue_sum1 / working_time_order_sum1
# print(working_time_overdue_rate1)


# print('换单Osquare-SD rule-based-200')
# # 不换单的超时率
# # exchange_last_file_name1 = "D:/exchange/train/baseline/SD-OSquare-record/time_step_42599_courier_state.txt"
# exchange_last_file_name1 = "D:/exchange/train/optimize-2022-1-19/SD-Osquare-record-200/time_step_57599_courier_state.txt"
# exchange_state_file1 = open(exchange_last_file_name1, "r")
# # 超时率
# exchange_overdue_order_num_list1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
# exchange_all_order_num_list1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
# for exchange_line in exchange_state_file1:
#     exchange_line = exchange_line.strip('\n')
#     exchange_first_item = exchange_line.split(',')[0]
#     if exchange_first_item == '':
#         exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
#         exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
#         exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
#         exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
#         if exchange_order_dispatch_stage == 0:
#             if exchange_promise_deliver_time < exchange_order_deliver_time:
#                 exchange_overdue_order_num_list1[int(exchange_order_create_time / 3600)] += 1
#             exchange_all_order_num_list1[int(exchange_order_create_time / 3600)] += 1
# print(exchange_overdue_order_num_list1)
# print(exchange_all_order_num_list1)
# exchange_overdue_rate1 = []
# exchange_hour_list1 = []
# for i in range(len(exchange_all_order_num_list1)):
#     if exchange_all_order_num_list1[i] != 0:
#         exchange_overdue_rate1.append(exchange_overdue_order_num_list1[i] / exchange_all_order_num_list1[i] / 2)
#         exchange_hour_list1.append(i + 1)
#     else:
#         exchange_overdue_rate1.append(0)
#         exchange_hour_list1.append(i + 1)
# print(exchange_overdue_rate1)
#
# exchange_day_overdue_sum1 = sum(exchange_overdue_order_num_list1)
# exchange_day_all_sum1 = sum(exchange_all_order_num_list1)
# exchange_day_overdue_rate1 = exchange_day_overdue_sum1 / exchange_day_all_sum1
# print(exchange_day_overdue_rate1)
#
# working_time_overdue_sum1 = 0
# working_time_order_sum1 = 0
# for i in range(len(exchange_all_order_num_list1)):
#     if (0 <= i < 10) or (21 <= i < 23):
#         continue
#     else:
#         working_time_overdue_sum1 += exchange_overdue_order_num_list1[i]
#         working_time_order_sum1 += exchange_all_order_num_list1[i]
# working_time_overdue_rate1 = working_time_overdue_sum1 / working_time_order_sum1
# print(working_time_overdue_rate1)


print('换单Osquare-SD rule-based-200_2min')
# 不换单的超时率
# exchange_last_file_name1 = "D:/exchange/train/baseline/SD-OSquare-record/time_step_42599_courier_state.txt"
exchange_last_file_name1 = "D:/exchange/train/optimize-2022-1-19/SD-Osquare-record-200_2min/time_step_86399_courier_state.txt"
exchange_state_file1 = open(exchange_last_file_name1, "r")
# 超时率
exchange_overdue_order_num_list1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file1:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list1[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list1[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list1)
print(exchange_all_order_num_list1)
exchange_overdue_rate1 = []
exchange_hour_list1 = []
for i in range(len(exchange_all_order_num_list1)):
    if exchange_all_order_num_list1[i] != 0:
        exchange_overdue_rate1.append(exchange_overdue_order_num_list1[i] / exchange_all_order_num_list1[i] / 2)
        exchange_hour_list1.append(i + 1)
    else:
        exchange_overdue_rate1.append(0)
        exchange_hour_list1.append(i + 1)
print(exchange_overdue_rate1)

exchange_day_overdue_sum1 = sum(exchange_overdue_order_num_list1)
exchange_day_all_sum1 = sum(exchange_all_order_num_list1)
exchange_day_overdue_rate1 = exchange_day_overdue_sum1 / exchange_day_all_sum1
print(exchange_day_overdue_rate1)

working_time_overdue_sum1 = 0
working_time_order_sum1 = 0
for i in range(len(exchange_all_order_num_list1)):
    if (0 <= i < 10) or (21 <= i <= 23):
        continue
    else:
        working_time_overdue_sum1 += exchange_overdue_order_num_list1[i]
        working_time_order_sum1 += exchange_all_order_num_list1[i]
working_time_overdue_rate1 = working_time_overdue_sum1 / working_time_order_sum1
print(working_time_overdue_rate1)


print('换单Osquare-SD rule-based-200_2min_filter1200')
# 不换单的超时率
# exchange_last_file_name1 = "D:/exchange/train/baseline/SD-OSquare-record/time_step_42599_courier_state.txt"
exchange_last_file_name1 = "D:/exchange/train/optimize-2022-1-19/SD-Osquare-record-200_2min_filter1200/time_step_86399_courier_state.txt"
exchange_state_file1 = open(exchange_last_file_name1, "r")
# 超时率
exchange_overdue_order_num_list1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file1:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list1[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list1[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list1)
print(exchange_all_order_num_list1)
exchange_overdue_rate1 = []
exchange_hour_list1 = []
for i in range(len(exchange_all_order_num_list1)):
    if exchange_all_order_num_list1[i] != 0:
        exchange_overdue_rate1.append(exchange_overdue_order_num_list1[i] / exchange_all_order_num_list1[i] / 2)
        exchange_hour_list1.append(i + 1)
    else:
        exchange_overdue_rate1.append(0)
        exchange_hour_list1.append(i + 1)
print(exchange_overdue_rate1)

exchange_day_overdue_sum1 = sum(exchange_overdue_order_num_list1)
exchange_day_all_sum1 = sum(exchange_all_order_num_list1)
exchange_day_overdue_rate1 = exchange_day_overdue_sum1 / exchange_day_all_sum1
print(exchange_day_overdue_rate1)

working_time_overdue_sum1 = 0
working_time_order_sum1 = 0
for i in range(len(exchange_all_order_num_list1)):
    if (0 <= i < 10) or (21 <= i <= 23):
        continue
    else:
        working_time_overdue_sum1 += exchange_overdue_order_num_list1[i]
        working_time_order_sum1 += exchange_all_order_num_list1[i]
working_time_overdue_rate1 = working_time_overdue_sum1 / working_time_order_sum1
print(working_time_overdue_rate1)


print('模拟退火')
# 不换单的超时率
# exchange_last_file_name1 = "D:/exchange/train/baseline/SD-OSquare-record/time_step_42599_courier_state.txt"
exchange_last_file_name1 = "D:/exchange/train/optimize-2022-1-19/annealing/time_step_57599_courier_state.txt"
exchange_state_file1 = open(exchange_last_file_name1, "r")
# 超时率
exchange_overdue_order_num_list1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file1:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list1[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list1[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list1)
print(exchange_all_order_num_list1)
exchange_overdue_rate1 = []
exchange_hour_list1 = []
for i in range(len(exchange_all_order_num_list1)):
    if exchange_all_order_num_list1[i] != 0:
        exchange_overdue_rate1.append(exchange_overdue_order_num_list1[i] / exchange_all_order_num_list1[i] / 2)
        exchange_hour_list1.append(i + 1)
    else:
        exchange_overdue_rate1.append(0)
        exchange_hour_list1.append(i + 1)
print(exchange_overdue_rate1)

exchange_day_overdue_sum1 = sum(exchange_overdue_order_num_list1)
exchange_day_all_sum1 = sum(exchange_all_order_num_list1)
exchange_day_overdue_rate1 = exchange_day_overdue_sum1 / exchange_day_all_sum1
print(exchange_day_overdue_rate1)

working_time_overdue_sum1 = 0
working_time_order_sum1 = 0
for i in range(len(exchange_all_order_num_list1)):
    # if (0 <= i < 10) or (21 <= i <= 23):
    #     continue
    # else:
    working_time_overdue_sum1 += exchange_overdue_order_num_list1[i]
    working_time_order_sum1 += exchange_all_order_num_list1[i]
working_time_overdue_rate1 = working_time_overdue_sum1 / working_time_order_sum1
print(working_time_overdue_rate1)



print('模拟退火1200')
# 不换单的超时率
# exchange_last_file_name1 = "D:/exchange/train/baseline/SD-OSquare-record/time_step_42599_courier_state.txt"
exchange_last_file_name1 = "D:/exchange/train/optimize-2022-1-19/annealing_1200/time_step_57599_courier_state.txt"
exchange_state_file1 = open(exchange_last_file_name1, "r")
# 超时率
exchange_overdue_order_num_list1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file1:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list1[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list1[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list1)
print(exchange_all_order_num_list1)
exchange_overdue_rate1 = []
exchange_hour_list1 = []
for i in range(len(exchange_all_order_num_list1)):
    if exchange_all_order_num_list1[i] != 0:
        exchange_overdue_rate1.append(exchange_overdue_order_num_list1[i] / exchange_all_order_num_list1[i] / 2)
        exchange_hour_list1.append(i + 1)
    else:
        exchange_overdue_rate1.append(0)
        exchange_hour_list1.append(i + 1)
print(exchange_overdue_rate1)

exchange_day_overdue_sum1 = sum(exchange_overdue_order_num_list1)
exchange_day_all_sum1 = sum(exchange_all_order_num_list1)
exchange_day_overdue_rate1 = exchange_day_overdue_sum1 / exchange_day_all_sum1
print(exchange_day_overdue_rate1)

working_time_overdue_sum1 = 0
working_time_order_sum1 = 0
for i in range(len(exchange_all_order_num_list1)):
    # if (0 <= i < 10) or (21 <= i <= 23):
    #     continue
    # else:
    working_time_overdue_sum1 += exchange_overdue_order_num_list1[i]
    working_time_order_sum1 += exchange_all_order_num_list1[i]
working_time_overdue_rate1 = working_time_overdue_sum1 / working_time_order_sum1
print(working_time_overdue_rate1)

print('换单DQN_200_2min_filter1200')
# 不换单的超时率
# exchange_last_file_name1 = "D:/exchange/train/baseline/SD-OSquare-record/time_step_42599_courier_state.txt"
exchange_last_file_name1 = "D:/exchange/train/optimize-2022-1-19/dqn/20220319_filter1200/test_zh1001_251/state/time_step_39599_courier_state.txt"
exchange_state_file1 = open(exchange_last_file_name1, "r")
# 超时率
exchange_overdue_order_num_list1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file1:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list1[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list1[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list1)
print(exchange_all_order_num_list1)
exchange_overdue_rate1 = []
exchange_hour_list1 = []
for i in range(len(exchange_all_order_num_list1)):
    if exchange_all_order_num_list1[i] != 0:
        exchange_overdue_rate1.append(exchange_overdue_order_num_list1[i] / exchange_all_order_num_list1[i] / 2)
        exchange_hour_list1.append(i + 1)
    else:
        exchange_overdue_rate1.append(0)
        exchange_hour_list1.append(i + 1)
print(exchange_overdue_rate1)

exchange_day_overdue_sum1 = sum(exchange_overdue_order_num_list1)
exchange_day_all_sum1 = sum(exchange_all_order_num_list1)
exchange_day_overdue_rate1 = exchange_day_overdue_sum1 / exchange_day_all_sum1
print(exchange_day_overdue_rate1)

working_time_overdue_sum1 = 0
working_time_order_sum1 = 0
for i in range(len(exchange_all_order_num_list1)):
    if (0 <= i < 10) or (21 <= i <= 23):
        continue
    else:
        working_time_overdue_sum1 += exchange_overdue_order_num_list1[i]
        working_time_order_sum1 += exchange_all_order_num_list1[i]
working_time_overdue_rate1 = working_time_overdue_sum1 / working_time_order_sum1
print(working_time_overdue_rate1)

print('换单DQN_200_2min_filter1200-ckpt373')
# 不换单的超时率
# exchange_last_file_name1 = "D:/exchange/train/baseline/SD-OSquare-record/time_step_42599_courier_state.txt"
exchange_last_file_name1 = "D:/exchange/train/optimize-2022-1-19/dqn/20220319_filter1200/test_zh1001_373/state/time_step_79199_courier_state.txt"
exchange_state_file1 = open(exchange_last_file_name1, "r")
# 超时率
exchange_overdue_order_num_list1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file1:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list1[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list1[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list1)
print(exchange_all_order_num_list1)
exchange_overdue_rate1 = []
exchange_hour_list1 = []
for i in range(len(exchange_all_order_num_list1)):
    if exchange_all_order_num_list1[i] != 0:
        exchange_overdue_rate1.append(exchange_overdue_order_num_list1[i] / exchange_all_order_num_list1[i] / 2)
        exchange_hour_list1.append(i + 1)
    else:
        exchange_overdue_rate1.append(0)
        exchange_hour_list1.append(i + 1)
print(exchange_overdue_rate1)

exchange_day_overdue_sum1 = sum(exchange_overdue_order_num_list1)
exchange_day_all_sum1 = sum(exchange_all_order_num_list1)
exchange_day_overdue_rate1 = exchange_day_overdue_sum1 / exchange_day_all_sum1
print(exchange_day_overdue_rate1)

working_time_overdue_sum1 = 0
working_time_order_sum1 = 0
for i in range(len(exchange_all_order_num_list1)):
    if (0 <= i < 10) or (21 <= i <= 23):
        continue
    else:
        working_time_overdue_sum1 += exchange_overdue_order_num_list1[i]
        working_time_order_sum1 += exchange_all_order_num_list1[i]
working_time_overdue_rate1 = working_time_overdue_sum1 / working_time_order_sum1
print(working_time_overdue_rate1)

print('换单DDQN_200_2min_filter1200')
# 不换单的超时率
# exchange_last_file_name1 = "D:/exchange/train/baseline/SD-OSquare-record/time_step_42599_courier_state.txt"
exchange_last_file_name1 = "D:/exchange/train/optimize-2022-1-19/dqn/ddqn/test_zh1001/state/time_step_86399_courier_state.txt"
exchange_state_file1 = open(exchange_last_file_name1, "r")
# 超时率
exchange_overdue_order_num_list1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file1:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list1[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list1[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list1)
print(exchange_all_order_num_list1)
exchange_overdue_rate1 = []
exchange_hour_list1 = []
for i in range(len(exchange_all_order_num_list1)):
    if exchange_all_order_num_list1[i] != 0:
        exchange_overdue_rate1.append(exchange_overdue_order_num_list1[i] / exchange_all_order_num_list1[i] / 2)
        exchange_hour_list1.append(i + 1)
    else:
        exchange_overdue_rate1.append(0)
        exchange_hour_list1.append(i + 1)
print(exchange_overdue_rate1)

exchange_day_overdue_sum1 = sum(exchange_overdue_order_num_list1)
exchange_day_all_sum1 = sum(exchange_all_order_num_list1)
exchange_day_overdue_rate1 = exchange_day_overdue_sum1 / exchange_day_all_sum1
print(exchange_day_overdue_rate1)

working_time_overdue_sum1 = 0
working_time_order_sum1 = 0
for i in range(len(exchange_all_order_num_list1)):
    if (0 <= i < 10) or (21 <= i <= 23):
        continue
    else:
        working_time_overdue_sum1 += exchange_overdue_order_num_list1[i]
        working_time_order_sum1 += exchange_all_order_num_list1[i]
working_time_overdue_rate1 = working_time_overdue_sum1 / working_time_order_sum1
print(working_time_overdue_rate1)
#
# print('DQN-no filter')
# # 不换单的超时率
# exchange_last_file_name6_1 = "D:/exchange/train/baseline/DQN-update-record/time_step_75599_courier_state.txt"
# exchange_state_file6_1 = open(exchange_last_file_name6_1, "r")
# # 超时率
# exchange_overdue_order_num_list6_1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
# exchange_all_order_num_list6_1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
# for exchange_line in exchange_state_file6_1:
#     exchange_line = exchange_line.strip('\n')
#     exchange_first_item = exchange_line.split(',')[0]
#     if exchange_first_item == '':
#         exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
#         exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
#         exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
#         exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
#         if exchange_order_dispatch_stage == 0:
#             if exchange_promise_deliver_time < exchange_order_deliver_time:
#                 exchange_overdue_order_num_list6_1[int(exchange_order_create_time / 3600)] += 1
#             exchange_all_order_num_list6_1[int(exchange_order_create_time / 3600)] += 1
# print(exchange_overdue_order_num_list6_1)
# print(exchange_all_order_num_list6_1)
# exchange_overdue_rate6_1 = []
# exchange_hour_list6_1 = []
# for i in range(len(exchange_all_order_num_list6_1)):
#     if exchange_all_order_num_list6_1[i] != 0:
#         exchange_overdue_rate6_1.append(exchange_overdue_order_num_list6_1[i] / exchange_all_order_num_list6_1[i] / 2)
#         exchange_hour_list6_1.append(i + 1)
#     else:
#         exchange_overdue_rate6_1.append(0)
#         exchange_hour_list6_1.append(i + 1)
# print(exchange_overdue_rate6_1)
#
# exchange_day_overdue_sum6_1 = sum(exchange_overdue_order_num_list6_1)
# exchange_day_all_sum6_1 = sum(exchange_all_order_num_list6_1)
# exchange_day_overdue_rate6_1 = exchange_day_overdue_sum6_1 / exchange_day_all_sum6_1
# print(exchange_day_overdue_rate6_1)
#
# working_time_overdue_sum6_1 = 0
# working_time_order_sum6_1 = 0
# for i in range(len(exchange_all_order_num_list6_1)):
#     if (0 <= i < 10) or (21 <= i < 23):
#         continue
#     else:
#         working_time_overdue_sum6_1 += exchange_overdue_order_num_list6_1[i]
#         working_time_order_sum6_1 += exchange_all_order_num_list6_1[i]
# working_time_overdue_rate6_1 = working_time_overdue_sum6_1 / working_time_order_sum6_1
# print(working_time_overdue_rate6_1)
#
# #
# print('DQN-filter')
# # 不换单的超时率
# exchange_last_file_name6 = "D:/exchange/train/baseline/DQN-record/time_step_50399_courier_state.txt"
# exchange_state_file6 = open(exchange_last_file_name6, "r")
# # 超时率
# exchange_overdue_order_num_list6 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
# exchange_all_order_num_list6 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
# for exchange_line in exchange_state_file6:
#     exchange_line = exchange_line.strip('\n')
#     exchange_first_item = exchange_line.split(',')[0]
#     if exchange_first_item == '':
#         exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
#         exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
#         exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
#         exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
#         if exchange_order_dispatch_stage == 0:
#             if exchange_promise_deliver_time < exchange_order_deliver_time:
#                 exchange_overdue_order_num_list6[int(exchange_order_create_time / 3600)] += 1
#             exchange_all_order_num_list6[int(exchange_order_create_time / 3600)] += 1
# print(exchange_overdue_order_num_list6)
# print(exchange_all_order_num_list6)
# exchange_overdue_rate6 = []
# exchange_hour_list6 = []
# for i in range(len(exchange_all_order_num_list6)):
#     if exchange_all_order_num_list6[i] != 0:
#         exchange_overdue_rate6.append(exchange_overdue_order_num_list6[i] / exchange_all_order_num_list6[i] / 2)
#         exchange_hour_list6.append(i + 1)
#     else:
#         exchange_overdue_rate6.append(0)
#         exchange_hour_list6.append(i + 1)
# print(exchange_overdue_rate6)
#
# exchange_day_overdue_sum6 = sum(exchange_overdue_order_num_list6)
# exchange_day_all_sum6 = sum(exchange_all_order_num_list6)
# exchange_day_overdue_rate6 = exchange_day_overdue_sum6 / exchange_day_all_sum6
# print(exchange_day_overdue_rate6)
#
# working_time_overdue_sum6 = 0
# working_time_order_sum6 = 0
# for i in range(len(exchange_all_order_num_list6)):
#     if (0 <= i < 10) or (20 <= i < 23):
#         continue
#     else:
#         working_time_overdue_sum6 += exchange_overdue_order_num_list6[i]
#         working_time_order_sum6 += exchange_all_order_num_list6[i]
# working_time_overdue_rate6 = working_time_overdue_sum6 / working_time_order_sum6
# print(working_time_overdue_rate6)
#
# print('换单A2C,相遇事件不考虑01订单数')
# #  换单
# # exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/test_A2C_buxianzhidanshu/time_step_46999_courier_state.txt"
# exchange_state_file2 = open(exchange_last_file_name2, "r")
# # 超时率
# exchange_overdue_order_num_list2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
# exchange_all_order_num_list2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
# for exchange_line in exchange_state_file2:
#     exchange_line = exchange_line.strip('\n')
#     exchange_first_item = exchange_line.split(',')[0]
#     if exchange_first_item == '':
#         exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
#         exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
#         exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
#         exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
#         if exchange_order_dispatch_stage == 0:
#             if exchange_promise_deliver_time < exchange_order_deliver_time:
#                 exchange_overdue_order_num_list2[int(exchange_order_create_time / 3600)] += 1
#             exchange_all_order_num_list2[int(exchange_order_create_time / 3600)] += 1
# print(exchange_overdue_order_num_list2)
# print(exchange_all_order_num_list2)
# exchange_overdue_rate2 = []
# exchange_hour_list2 = []
# for i in range(len(exchange_all_order_num_list2)):
#     if exchange_all_order_num_list2[i] != 0:
#         exchange_overdue_rate2.append(exchange_overdue_order_num_list2[i] / exchange_all_order_num_list2[i] / 2)
#         exchange_hour_list2.append(i + 1)
#     else:
#         exchange_overdue_rate2.append(0)
#         exchange_hour_list2.append(i + 1)
# print(exchange_overdue_rate2)
#
# exchange_day_overdue_sum2 = sum(exchange_overdue_order_num_list2)
# exchange_day_all_sum2 = sum(exchange_all_order_num_list2)
# exchange_day_overdue_rate2 = exchange_day_overdue_sum2 / exchange_day_all_sum2
# print(exchange_day_overdue_rate2)
#
# working_time_overdue_sum2 = 0
# working_time_order_sum2 = 0
# for i in range(len(exchange_all_order_num_list2)):
#     if (0 <= i < 11) or (21 <= i < 23):
#         continue
#     else:
#         working_time_overdue_sum2 += exchange_overdue_order_num_list2[i]
#         working_time_order_sum2 += exchange_all_order_num_list2[i]
# working_time_overdue_rate2 = working_time_overdue_sum2 / working_time_order_sum2
# print(working_time_overdue_rate2)
#
# print('换单A2C, 相遇事件考虑01订单数据')
# #  换单
# # exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name2_1 = "D:/exchange/train/debug-2021-7-29/A2C_exchange_logs_consider_processint_time/time_step_46999_courier_state.txt"
# exchange_state_file2_1 = open(exchange_last_file_name2_1, "r")
# # 超时率
# exchange_overdue_order_num_list2_1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
# exchange_all_order_num_list2_1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
# for exchange_line in exchange_state_file2_1:
#     exchange_line = exchange_line.strip('\n')
#     exchange_first_item = exchange_line.split(',')[0]
#     if exchange_first_item == '':
#         exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
#         exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
#         exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
#         exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
#         if exchange_order_dispatch_stage == 0:
#             if exchange_promise_deliver_time < exchange_order_deliver_time:
#                 exchange_overdue_order_num_list2_1[int(exchange_order_create_time / 3600)] += 1
#             exchange_all_order_num_list2_1[int(exchange_order_create_time / 3600)] += 1
# print(exchange_overdue_order_num_list2_1)
# print(exchange_all_order_num_list2_1)
# exchange_overdue_rate2_1 = []
# exchange_hour_list2_1 = []
# for i in range(len(exchange_all_order_num_list2_1)):
#     if exchange_all_order_num_list2_1[i] != 0:
#         exchange_overdue_rate2_1.append(exchange_overdue_order_num_list2_1[i] / exchange_all_order_num_list2_1[i] / 2)
#         exchange_hour_list2_1.append(i + 1)
#     else:
#         exchange_overdue_rate2_1.append(0)
#         exchange_hour_list2_1.append(i + 1)
# print(exchange_overdue_rate2_1)
#
# exchange_day_overdue_sum2_1 = sum(exchange_overdue_order_num_list2_1)
# exchange_day_all_sum2_1 = sum(exchange_all_order_num_list2_1)
# exchange_day_overdue_rate2_1 = exchange_day_overdue_sum2_1 / exchange_day_all_sum2_1
# print(exchange_day_overdue_rate2_1)
#
# working_time_overdue_sum2_1 = 0
# working_time_order_sum2_1 = 0
# for i in range(len(exchange_all_order_num_list2_1)):
#     if (0 <= i < 11) or (21 <= i < 23):
#         continue
#     else:
#         working_time_overdue_sum2_1 += exchange_overdue_order_num_list2_1[i]
#         working_time_order_sum2_1 += exchange_all_order_num_list2_1[i]
# working_time_overdue_rate2_1 = working_time_overdue_sum2_1 / working_time_order_sum2_1
# print(working_time_overdue_rate2_1)
#
# print('换单A2C, 相遇事件考虑01订单数据---9-6')
# #  换单
# # exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name2_2 = "D:/exchange/train/A2C-update-reward-20201-9-6/A2C_test_record/time_step_58679_courier_state.txt"
# exchange_state_file2_2 = open(exchange_last_file_name2_2, "r")
# # 超时率
# exchange_overdue_order_num_list2_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
# exchange_all_order_num_list2_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
# for exchange_line in exchange_state_file2_2:
#     exchange_line = exchange_line.strip('\n')
#     exchange_first_item = exchange_line.split(',')[0]
#     if exchange_first_item == '':
#         exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
#         exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
#         exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
#         exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
#         if exchange_order_dispatch_stage == 0:
#             if exchange_promise_deliver_time < exchange_order_deliver_time:
#                 exchange_overdue_order_num_list2_2[int(exchange_order_create_time / 3600)] += 1
#             exchange_all_order_num_list2_2[int(exchange_order_create_time / 3600)] += 1
# print(exchange_overdue_order_num_list2_2)
# print(exchange_all_order_num_list2_2)
# exchange_overdue_rate2_2 = []
# exchange_hour_list2_2 = []
# for i in range(len(exchange_all_order_num_list2_2)):
#     if exchange_all_order_num_list2_2[i] != 0:
#         exchange_overdue_rate2_2.append(exchange_overdue_order_num_list2_2[i] / exchange_all_order_num_list2_2[i] / 2)
#         exchange_hour_list2_2.append(i + 1)
#     else:
#         exchange_overdue_rate2_2.append(0)
#         exchange_hour_list2_2.append(i + 1)
# print(exchange_overdue_rate2_2)
#
# exchange_day_overdue_sum2_2 = sum(exchange_overdue_order_num_list2_2)
# exchange_day_all_sum2_2 = sum(exchange_all_order_num_list2_2)
# exchange_day_overdue_rate2_2 = exchange_day_overdue_sum2_2 / exchange_day_all_sum2_2
# print(exchange_day_overdue_rate2_2)
#
# working_time_overdue_sum2_2 = 0
# working_time_order_sum2_2 = 0
# for i in range(len(exchange_all_order_num_list2_2)):
#     if (0 <= i < 11) or (21 <= i < 23):
#         continue
#     else:
#         working_time_overdue_sum2_2 += exchange_overdue_order_num_list2_2[i]
#         working_time_order_sum2_2 += exchange_all_order_num_list2_2[i]
# working_time_overdue_rate2_2 = working_time_overdue_sum2_2 / working_time_order_sum2_2
# print(working_time_overdue_rate2_2)
#
# print('换单MOOC')
# #  换单
# exchange_last_file_name7 = "D:/exchange/train/baseline/MOOC_record_zxh/time_step_86399_courier_state.txt"
# exchange_state_file7 = open(exchange_last_file_name7, "r")
# # 超时率
# exchange_overdue_order_num_list7 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
# exchange_all_order_num_list7 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
# for exchange_line in exchange_state_file7:
#     exchange_line = exchange_line.strip('\n')
#     exchange_first_item = exchange_line.split(',')[0]
#     if exchange_first_item == '':
#         exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
#         exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
#         exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
#         exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
#         if exchange_order_dispatch_stage == 0:
#             if exchange_promise_deliver_time < exchange_order_deliver_time:
#                 exchange_overdue_order_num_list7[int(exchange_order_create_time / 3600)] += 1
#             exchange_all_order_num_list7[int(exchange_order_create_time / 3600)] += 1
# print(exchange_overdue_order_num_list7)
# print(exchange_all_order_num_list7)
# exchange_overdue_rate7 = []
# exchange_hour_list7 = []
# for i in range(len(exchange_all_order_num_list7)):
#     if exchange_all_order_num_list7[i] != 0:
#         exchange_overdue_rate7.append(exchange_overdue_order_num_list7[i] / exchange_all_order_num_list7[i] / 2)
#         exchange_hour_list7.append(i + 1)
#     else:
#         exchange_overdue_rate7.append(0)
#         exchange_hour_list7.append(i + 1)
# print(exchange_overdue_rate7)
#
# exchange_day_overdue_sum7 = sum(exchange_overdue_order_num_list7)
# exchange_day_all_sum7 = sum(exchange_all_order_num_list7)
# exchange_day_overdue_rate7 = exchange_day_overdue_sum7 / exchange_day_all_sum7
# print(exchange_day_overdue_rate7)
#
#
# working_time_overdue_sum7 = 0
# working_time_order_sum7 = 0
# for i in range(len(exchange_all_order_num_list7)):
#     if (0 <= i < 12) or (16<= i < 23):
#         continue
#     else:
#         working_time_overdue_sum7 += exchange_overdue_order_num_list7[i]
#         working_time_order_sum7 += exchange_all_order_num_list7[i]
# working_time_overdue_rate7 = working_time_overdue_sum7 / working_time_order_sum7
# print(working_time_overdue_rate7)
#
# print('换单HOAC, 相遇事件不考虑01订单数据')
# #  换单
# exchange_last_file_name3 = "D:/exchange/train/update-2021-8-24/exchange_log_20201012_short_time/time_step_50399_courier_state.txt"
# # exchange_last_file_name3 = "D:/exchange/train/update-2021-8-24/exchange_train_HCAC_axis_update_train_time7_test_log/time_step_39599_courier_state.txt"
#
# exchange_state_file3 = open(exchange_last_file_name3, "r")
# # 超时率
# exchange_overdue_order_num_list3 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
# exchange_all_order_num_list3 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
# for exchange_line in exchange_state_file3:
#     exchange_line = exchange_line.strip('\n')
#     exchange_first_item = exchange_line.split(',')[0]
#     if exchange_first_item == '':
#         exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
#         exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
#         exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
#         exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
#         if exchange_order_dispatch_stage == 0:
#             if exchange_promise_deliver_time < exchange_order_deliver_time:
#                 exchange_overdue_order_num_list3[int(exchange_order_create_time / 3600)] += 1
#             exchange_all_order_num_list3[int(exchange_order_create_time / 3600)] += 1
# print(exchange_overdue_order_num_list3)
# print(exchange_all_order_num_list3)
# exchange_overdue_rate3 = []
# exchange_hour_list3 = []
# for i in range(len(exchange_all_order_num_list3)):
#     if exchange_all_order_num_list3[i] != 0:
#         exchange_overdue_rate3.append(exchange_overdue_order_num_list3[i] / exchange_all_order_num_list3[i] / 2)
#         exchange_hour_list3.append(i + 1)
#     else:
#         exchange_overdue_rate3.append(0)
#         exchange_hour_list3.append(i + 1)
# print(exchange_overdue_rate3)
#
# exchange_day_overdue_sum3 = sum(exchange_overdue_order_num_list3)
# exchange_day_all_sum3 = sum(exchange_all_order_num_list3)
# exchange_day_overdue_rate3 = exchange_day_overdue_sum3 / exchange_day_all_sum3
# print(exchange_day_overdue_rate3)
#
# # 10-20h的超时率
# working_time_overdue_sum3 = 0
# working_time_order_sum3 = 0
# for i in range(len(exchange_all_order_num_list3)):
#     if (0 <= i < 11) or ( 13<=i<23):
#         continue
#     else:
#         working_time_overdue_sum3+=exchange_overdue_order_num_list3[i]
#         working_time_order_sum3+=exchange_all_order_num_list3[i]
# working_time_overdue_rate3 = working_time_overdue_sum3 / working_time_order_sum3
# print(working_time_overdue_rate3)
#
# print('换单HOAC, 相遇事件不考虑01订单数据')
# #  换单
# # exchange_last_file_name3 = "D:/exchange/train/update-2021-8-24/exchange_log_20201012_short_time/time_step_50399_courier_state.txt"
# exchange_last_file_name3_0 = "D:/exchange/train/update-2021-8-24/exchange_train_HCAC_axis_update_train_time7_test_log/time_step_46799_courier_state.txt"
#
# exchange_state_file3_0 = open(exchange_last_file_name3_0, "r")
# # 超时率
# exchange_overdue_order_num_list3_0 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
# exchange_all_order_num_list3_0 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
# for exchange_line in exchange_state_file3_0:
#     exchange_line = exchange_line.strip('\n')
#     exchange_first_item = exchange_line.split(',')[0]
#     if exchange_first_item == '':
#         exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
#         exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
#         exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
#         exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
#         if exchange_order_dispatch_stage == 0:
#             if exchange_promise_deliver_time < exchange_order_deliver_time:
#                 exchange_overdue_order_num_list3_0[int(exchange_order_create_time / 3600)] += 1
#             exchange_all_order_num_list3_0[int(exchange_order_create_time / 3600)] += 1
# print(exchange_overdue_order_num_list3_0)
# print(exchange_all_order_num_list3_0)
# exchange_overdue_rate3_0 = []
# exchange_hour_list3_0 = []
# for i in range(len(exchange_all_order_num_list3_0)):
#     if exchange_all_order_num_list3_0[i] != 0:
#         exchange_overdue_rate3_0.append(exchange_overdue_order_num_list3_0[i] / exchange_all_order_num_list3_0[i] / 2)
#         exchange_hour_list3_0.append(i + 1)
#     else:
#         exchange_overdue_rate3_0.append(0)
#         exchange_hour_list3_0.append(i + 1)
# print(exchange_overdue_rate3_0)
#
# exchange_day_overdue_sum3_0 = sum(exchange_overdue_order_num_list3_0)
# exchange_day_all_sum3_0 = sum(exchange_all_order_num_list3_0)
# exchange_day_overdue_rate3_0 = exchange_day_overdue_sum3_0 / exchange_day_all_sum3_0
# print(exchange_day_overdue_rate3_0)
#
# # 10-20h的超时率
# # working_time_overdue_sum3_0 = 0
# # working_time_order_sum3_0 = 0
# # for i in range(len(exchange_all_order_num_list3_0)):
# #     if (0 <= i < 11) or ( 13<=i<23):
# #         continue
# #     else:
# #         working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_0[i]
# #         working_time_order_sum3_0+=exchange_all_order_num_list3_0[i]
# # working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
# # print(working_time_overdue_rate3_0)
#
# print('换单HOAC, 相遇事件考虑01订单数据')
# #  换单
# # exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# # exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# # exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/exchange_train_HCAC_axis_update_train_time7_test_log_filter/time_step_35999_courier_state.txt"
#
# exchange_state_file3_1 = open(exchange_last_file_name3_1, "r")
# # 超时率
# exchange_overdue_order_num_list3_1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
# exchange_all_order_num_list3_1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
# for exchange_line in exchange_state_file3_1:
#     exchange_line = exchange_line.strip('\n')
#     exchange_first_item = exchange_line.split(',')[0]
#     if exchange_first_item == '':
#         exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
#         exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
#         exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
#         exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
#         if exchange_order_dispatch_stage == 0:
#             if exchange_promise_deliver_time < exchange_order_deliver_time:
#                 exchange_overdue_order_num_list3_1[int(exchange_order_create_time / 3600)] += 1
#             exchange_all_order_num_list3_1[int(exchange_order_create_time / 3600)] += 1
# print(exchange_overdue_order_num_list3_1)
# print(exchange_all_order_num_list3_1)
# exchange_overdue_rate3_1 = []
# exchange_hour_list3_1 = []
# for i in range(len(exchange_all_order_num_list3_1)):
#     if exchange_all_order_num_list3_1[i] != 0:
#         exchange_overdue_rate3_1.append(exchange_overdue_order_num_list3_1[i] / exchange_all_order_num_list3_1[i] / 2)
#         exchange_hour_list3_1.append(i + 1)
#     else:
#         exchange_overdue_rate3_1.append(0)
#         exchange_hour_list3_1.append(i + 1)
# print(exchange_overdue_rate3_1)
#
# exchange_day_overdue_sum3_1 = sum(exchange_overdue_order_num_list3_1)
# exchange_day_all_sum3_1 = sum(exchange_all_order_num_list3_1)
# exchange_day_overdue_rate3_1 = exchange_day_overdue_sum3_1 / exchange_day_all_sum3_1
# print(exchange_day_overdue_rate3_1)
#
# # 10-20h的超时率
# working_time_overdue_sum3_1 = 0
# working_time_order_sum3_1 = 0
# for i in range(len(exchange_all_order_num_list3_1)):
#     if (0 <= i < 11) or ( 14<=i<23):
#         continue
#     else:
#         working_time_overdue_sum3_1+=exchange_overdue_order_num_list3_1[i]
#         working_time_order_sum3_1+=exchange_all_order_num_list3_1[i]
# working_time_overdue_rate3_1 = working_time_overdue_sum3_1 / working_time_order_sum3_1
# print(working_time_overdue_rate3_1)
#
# print('换单HOAC, 13test-订单')
# #  换单
# # exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# # exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# # exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20220129_attention_conv_times_batch_50/time_step_64799_courier_state.txt"
#
# exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# # 超时率
# exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
# exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
# for exchange_line in exchange_state_file3_2:
#     exchange_line = exchange_line.strip('\n')
#     exchange_first_item = exchange_line.split(',')[0]
#     if exchange_first_item == '':
#         exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
#         exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
#         exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
#         exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
#         if exchange_order_dispatch_stage == 0:
#             if exchange_promise_deliver_time < exchange_order_deliver_time:
#                 exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
#             exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
# print(exchange_overdue_order_num_list3_2)
# print(exchange_all_order_num_list3_2)
# exchange_overdue_rate3_2 = []
# exchange_hour_list3_2 = []
# for i in range(len(exchange_all_order_num_list3_2)):
#     if exchange_all_order_num_list3_2[i] != 0:
#         exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
#         exchange_hour_list3_2.append(i + 1)
#     else:
#         exchange_overdue_rate3_2.append(0)
#         exchange_hour_list3_2.append(i + 1)
# print(exchange_overdue_rate3_2)
#
# exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
# exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
# exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
# print(exchange_day_overdue_rate3_2)

# print('换单HOAC, 14test-棋手')
# #  换单
# # exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# # exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# # exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20220129_attention_conv_times_batch_50_courier_reward/time_step_64799_courier_state.txt"
#
# exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# # 超时率
# exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
# exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
# for exchange_line in exchange_state_file3_2:
#     exchange_line = exchange_line.strip('\n')
#     exchange_first_item = exchange_line.split(',')[0]
#     if exchange_first_item == '':
#         exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
#         exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
#         exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
#         exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
#         if exchange_order_dispatch_stage == 0:
#             if exchange_promise_deliver_time < exchange_order_deliver_time:
#                 exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
#             exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
# print(exchange_overdue_order_num_list3_2)
# print(exchange_all_order_num_list3_2)
# exchange_overdue_rate3_2 = []
# exchange_hour_list3_2 = []
# for i in range(len(exchange_all_order_num_list3_2)):
#     if exchange_all_order_num_list3_2[i] != 0:
#         exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
#         exchange_hour_list3_2.append(i + 1)
#     else:
#         exchange_overdue_rate3_2.append(0)
#         exchange_hour_list3_2.append(i + 1)
# print(exchange_overdue_rate3_2)
#
# exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
# exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
# exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
# print(exchange_day_overdue_rate3_2)
#
print('换单HOAC, 17test-订单')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20220201_attention_conv_times_batch_50/time_step_50399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('换单HOAC, 20test-qishou,lon2有bug')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20220201_attention_conv_times_batch_50_courier_reward/lr=10-4/time_step_64799_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)

# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('换单HOAC, jt_weight0219-qishou,lon2有bug')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20220219_attention_conv_times_batch_50_courier_reward_jt/time_step_53999_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)

# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('换单DDPG_200_2min_filter1200')
# 不换单的超时率
# exchange_last_file_name1 = "D:/exchange/train/baseline/SD-OSquare-record/time_step_42599_courier_state.txt"
exchange_last_file_name1 = "D:/exchange/train/optimize-2022-1-19/a2c/ddpg/test_zh1001/state/time_step_86399_courier_state.txt"
exchange_state_file1 = open(exchange_last_file_name1, "r")
# 超时率
exchange_overdue_order_num_list1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file1:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list1[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list1[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list1)
print(exchange_all_order_num_list1)
exchange_overdue_rate1 = []
exchange_hour_list1 = []
for i in range(len(exchange_all_order_num_list1)):
    if exchange_all_order_num_list1[i] != 0:
        exchange_overdue_rate1.append(exchange_overdue_order_num_list1[i] / exchange_all_order_num_list1[i] / 2)
        exchange_hour_list1.append(i + 1)
    else:
        exchange_overdue_rate1.append(0)
        exchange_hour_list1.append(i + 1)
print(exchange_overdue_rate1)

exchange_day_overdue_sum1 = sum(exchange_overdue_order_num_list1)
exchange_day_all_sum1 = sum(exchange_all_order_num_list1)
exchange_day_overdue_rate1 = exchange_day_overdue_sum1 / exchange_day_all_sum1
print(exchange_day_overdue_rate1)

working_time_overdue_sum1 = 0
working_time_order_sum1 = 0
for i in range(len(exchange_all_order_num_list1)):
    if (0 <= i < 10) or (21 <= i <= 23):
        continue
    else:
        working_time_overdue_sum1 += exchange_overdue_order_num_list1[i]
        working_time_order_sum1 += exchange_all_order_num_list1[i]
working_time_overdue_rate1 = working_time_overdue_sum1 / working_time_order_sum1
print(working_time_overdue_rate1)
print('换单A2C, a2c-two_item0.5_filter1200')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/a2c/0223A2C/test1001/time_step_86399_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/a2c/0223A2C_all_time/test_zh1001/state/time_step_86399_courier_state.txt"
exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)
# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('换单A2C, a2c-three_item_filter1200')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/a2c/0223A2C_all_time_3item/test_zh1001/state/time_step_86399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)

# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)


print('换单A2C, 2item_without filter_test')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/a2c/0223A2C_all_time_without_filter/test_zh1001/state/time_step_86399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)

# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('换单A2C, 2item_without filter_test_filter1200')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/a2c/0223A2C_all_time_without_filter/test_zh1001filter/state/time_step_86399_courier_state.txt"
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/a2c/0223A2C_3/test1001/time_step_86399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)

print('换单A2C, 2item_without filter_test_filter600')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/a2c/0223A2C_all_time_without_filter/test_zh1001filter2/state/time_step_86399_courier_state.txt"
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/a2c/0223A2C_4/test1001/time_step_86399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)

# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)


print('换单A2C, 2item_without filter_test_filter300')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/a2c/0223A2C_all_time_without_filter/test_zh1001filter3/state/time_step_86399_courier_state.txt"
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/a2c/0223A2C_5/test1001/time_step_86399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)

# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('HCAC-1')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward/before/test_zh1001/state/time_step_61199_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)

# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)
print('HCAC-1-909')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward/test_zh1001_before_909/state/time_step_86399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)
# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
if working_time_order_sum3_0 != 0:
    working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
    print(working_time_overdue_rate3_0)

print('HCAC-1-before509')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward/test_zh1001_before_590/state/time_step_86399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)

# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
if working_time_order_sum3_0 != 0:
    working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
    print(working_time_overdue_rate3_0)

print('HCAC-1-before140')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward/test_zh1001_before_140/state/time_step_75599_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)

# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
if working_time_order_sum3_0 != 0:
    working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
    print(working_time_overdue_rate3_0)

print('HCAC-1-before145')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward/test_zh1001_before_145/state/time_step_86399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)

# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
if working_time_order_sum3_0 != 0:
    working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
    print(working_time_overdue_rate3_0)

print('HCAC-1-before206')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward/test_zh1001_before_206/state/time_step_86399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)

# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
if working_time_order_sum3_0 != 0:
    working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
    print(working_time_overdue_rate3_0)
print('HCAC-1-before206_hopnum')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward/test_zh1001_before_206_hopnum/state/time_step_53999_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)

# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
if working_time_order_sum3_0 != 0:
    working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
    print(working_time_overdue_rate3_0)
print('HCAC-1-before210')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward/test_zh1001_before_210/state/time_step_75599_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)

# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
if working_time_order_sum3_0 != 0:
    working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
    print(working_time_overdue_rate3_0)

print('HCAC-1-before438')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward/test_zh1001_before_438/state/time_step_86399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)

# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
if working_time_order_sum3_0 != 0:
    working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
    print(working_time_overdue_rate3_0)

print('HCAC-1--ckpt160_20220321')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward/before2/test_zh1001/state/time_step_50399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)

# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)
print('HCAC-1--ckpt218_20220321')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward/before3/test_zh1001/state/time_step_57599_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)

# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)
print('HCAC-1--ckpt216_20220322')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward/test_zh1001/state/time_step_57599_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)

# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('HCAC-1--ckpt203_20220322')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward/before2/test_zh1001_205/state/time_step_57599_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)
# 20200307_0.5_0.5_without_filter\test_zh1001_filter3\state

print('HCAC-1-1200-state-DDPG-660')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward_state_DDPG/test_zh1001_660/state/time_step_86399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)


print('HCAC-1-1200-state-AC-无GRU-单层attention-582')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward_state_network/test_zh1001_582/state/time_step_86399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)


print('HCAC-1-1200-state-DDPG-单层attetion-620')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward_state_DDPG_attention/test_zh1001_620/state/time_step_86399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('HCAC-1-1200-state-AC-GRU-MHA-25')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward_state_MHA_GRU/test_zh1001_25/state/time_step_68399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('HCAC-1-1200-state-AC-GRU-MHA-151')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward_state_MHA_GRU/test_zh1001_151/state/time_step_86399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('HCAC-1-1200-state-AC-GRU-MHA-212')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward_state_MHA_GRU/test_zh1001_212/state/time_step_68399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('HCAC-1-1200-state-AC-GRU-MHA-225')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward_state_MHA_GRU/test_zh1001_225/state/time_step_68399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)
print('HCAC-1-1200-state-AC-GRU-MHA-271')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward_state_MHA_GRU/test_zh1001_271/state/time_step_68399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)
print('HCAC-1-1200-state-AC-GRU-MHA-285')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward_state_MHA_GRU/test_zh1001_285/state/time_step_86399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)


print('HCAC-1-1200-state-AC-GRU-MHA-285-64799')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward_state_MHA_GRU/test_zh1001_285/state/time_step_64799_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('HCAC-1-1200-state-AC-GRU-MHA-425')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward_state_MHA_GRU/test_zh1001_425/state/time_step_86399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('HCAC-1-1200-state-AC-GRU-MHA-540')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward_state_MHA_GRU/test_zh1001_540/state/time_step_64799_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('HCAC-1-1200-state-AC-GRU-MHA-696')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward_state_MHA_GRU/test_zh1001_696/state/time_step_64799_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('HCAC-1-1200-state-AC-GRU-MHA-conv-173')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward_state_MHA_GRU_conv/test_zh1001_173/state/time_step_86399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('HCAC-1-1200-state-AC-GRU-MHA-conv-255')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward_state_MHA_GRU_conv/test_zh1001_255/state/time_step_86399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('HCAC-1-1200-state-AC-GRU-MHA-conv-440')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward_state_MHA_GRU_conv/test_zh1001_440/state/time_step_86399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)


print('HCAC-1-1200-state-AC-GRU-MHA-conv-495')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward_state_MHA_GRU_conv/test_zh1001_495/state/time_step_86399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)


print('HCAC-1-1200-state-AC-GRU-MHA-conv-575')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward_state_MHA_GRU_conv/test_zh1001_575/state/time_step_71999_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('HCAC-1-1200-state-AC-GRU-MHA-conv-245')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward_state_MHA_GRU_conv/test_zh1001_245/state/time_step_86399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('HCAC-1-1200-state-AC-GRU-MHA-conv-272')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward_state_MHA_GRU_conv/test_zh1001_272/state/time_step_64799_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('HCAC-1-1200-state-AC-GRU-MHA-conv-277')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward_state_MHA_GRU_conv/test_zh1001_277/state/time_step_64799_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('HCAC-1-1200-state-AC-GRU-MHA-conv-357')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward_state_MHA_GRU_conv/test_zh1001_357/state/time_step_71999_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('HCAC-1-1200-state-AC-GRU-MHA-conv-437')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward_state_MHA_GRU_conv/test_zh1001_437/state/time_step_86399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)


print('HCAC-1-1200-state-AC-GRU-MHA-conv-540')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward_state_MHA_GRU_conv/test_zh1001_540/state/time_step_57599_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('HCAC-1-1200-state-AC-GRU-MHA-conv3-125')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward_state_MHA_GRU_conv_3/test_zh1001_125/state/time_step_86399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('HCAC-1-1200-state-AC-GRU-MHA-conv3-175')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward_state_MHA_GRU_conv_3/test_zh1001_175/state/time_step_86399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('HCAC-1-1200-state-AC-GRU-MHA-conv3-230')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward_state_MHA_GRU_conv_3/test_zh1001_230/state/time_step_57599_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('HCAC-1-1200-state-AC-GRU-MHA-conv3-235')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward_state_MHA_GRU_conv_3/test_zh1001_235/state/time_step_82799_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)


print('HCAC-1-1200-state-AC-GRU-MHA-conv3-270')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward_state_MHA_GRU_conv_3/test_zh1001_270/state/time_step_86399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('HCAC-1-1200-state-AC-GRU-MHA-conv3-265')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward_state_MHA_GRU_conv_3/test_zh1001_265/state/time_step_86399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('HCAC-1-1200-state-AC-GRU-MHA-conv3-283')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward_state_MHA_GRU_conv_3/test_zh1001_283/state/time_step_71999_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('HCAC-1-1200-state-AC-GRU-MHA-conv3-440')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward_state_MHA_GRU_conv_3/test_zh1001_440/state/time_step_86399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('DDPG-AC-48')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/DDPG_AC/test_zh1001_48/state/time_step_86399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('DDPG-AC-128')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/DDPG_AC/test_zh1001_128/state/time_step_75599_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('DDPG-AC-175')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/DDPG_AC/test_zh1001_175/state/time_step_68399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)



print('DDPG-AC-240')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/DDPG_AC/test_zh1001_240/state/time_step_57599_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('DDPG-AC-242')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/DDPG_AC/test_zh1001_242/state/time_step_86399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)


print('DDPG-AC-250')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/DDPG_AC/test_zh1001_250/state/time_step_50399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)


print('HCAC-1-1200-state-AC-GRU-MHA-network-196')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/AC_state_MHA_GRU_network/test_zh1001_196/state/time_step_64799_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('HCAC-1-1200-state-AC-GRU-MHA-network-268')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/AC_state_MHA_GRU_network/test_zh1001_268/state/time_step_57599_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
# working_time_overdue_sum3_0 = 0
# working_time_order_sum3_0 = 0
# for i in range(len(exchange_all_order_num_list3_2)):
#     if (0 <= i <=9) or (20 < i <= 23):
#         continue
#     else:
#         working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
#         working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
# working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
# print(working_time_overdue_rate3_0)

print('HCAC-1-1200-state-AC-GRU-MHA-gamma-244')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/AC_state_MHA_GRU_gamma/test_zh1001_244/state/time_step_64799_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('HCAC-1-1200-state-AC-GRU-MHA-reward-177')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/AC_state_MHA_GRU_reward/test_zh1001_177/state/time_step_64799_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('HCAC-1-1200-state-AC-GRU-MHA-lr-305')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/AC_state_MHA_GRU_lr/test_zh1001_305/state/time_step_64799_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('HCAC-1-1200-state-DDPG-GRU-MHA-153')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/MHA_DDPG/test_zh1001_153/state/time_step_86399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('HCAC-1-1200-state-DDPG-GRU-MHA-200')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/MHA_DDPG/test_zh1001_200/state/time_step_64799_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('HCAC-1-1200-state-DDPG-GRU-MHA-245')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/MHA_DDPG/test_zh1001_245/state/time_step_86399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)


print('HCAC-1-1200-state-DDPG-GRU-MHA-275')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/MHA_DDPG/test_zh1001_275/state/time_step_64799_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)


print('HCAC-1-1200-state-DDPG-GRU-MHA-430')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/MHA_DDPG/test_zh1001_430/state/time_step_86399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)


print('HCAC-1-1200-state-98')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward_state/test_zh1001_98/state/time_step_86399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('HCAC-1-1200-state-190')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward_state/test_zh1001_190/state/time_step_86399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('HCAC-1-1200-state-190-64799')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward_state/test_zh1001_190/state/time_step_64799_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('HCAC-1-1200-test_zh1001_low_46')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward_state/test_zh1001_low_46/state/time_step_50399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('HCAC-1-1200-state-99')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward_state/test_zh1001_99/state/time_step_64799_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('HCAC-1-1200-state-100')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward_state/test_zh1001_100/state/time_step_75599_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)


print('HCAC-1-1200-state-195')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward_state/test_zh1001_195/state/time_step_50399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('HCAC-1-1200-state-200')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward_state/test_zh1001_200/state/time_step_86399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('HCAC-1-1200-state-205')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward_state/test_zh1001_205/state/time_step_50399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)
print('HCAC-1-1200-state-280')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward_state/test_zh1001_280/state/time_step_50399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('HCAC-1-1200-state-425')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward_state/test_zh1001_425/state/time_step_82799_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)


print('HCAC-1-1200-state-565')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward_state/test_zh1001_565/state/time_step_82799_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('HCAC-1-1200-state-795')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward_state/test_zh1001_795/state/time_step_50399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('HCAC-1-1200-state-889')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward_state/test_zh1001_889/state/time_step_50399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('HCAC-1-batch256-filter600_139')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_256_courier_reward_filter600/test_zh1001_139/state/time_step_50399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)
print('HCAC-1-batch256-filter600_220')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_256_courier_reward_filter600/test_zh1001_220/state/time_step_50399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)


print('HCAC-1-batch256-filter600_410')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_256_courier_reward_filter600/test_zh1001_410/state/time_step_79199_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('HCAC-1-batch256-filter600_465')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_256_courier_reward_filter600/test_zh1001_465/state/time_step_57599_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('HCAC-1-batch256-filter600_620')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_256_courier_reward_filter600/test_zh1001_620/state/time_step_86399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('HCAC-1-batch256-filter600_745')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_256_courier_reward_filter600/test_zh1001_745/state/time_step_50399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)


print('HCAC-1-batch256-filter600_870')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_256_courier_reward_filter600/test_zh1001_870/state/time_step_50399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('HCAC-1-batch256-filter600_1018')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_256_courier_reward_filter600/test_zh1001_1018/state/time_step_82799_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)


print('HCAC-1-batch256-filter600_1190')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_256_courier_reward_filter600/test_zh1001_1190/state/time_step_50399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('HCAC-1-batch256-filter300_235')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward_filter300/test_zh1001_before2_235/state/time_step_75599_courier_state.txt"
exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)


print('HCAC-1-batch64-filter300_210')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_64_courier_reward_filter300/test_zh1001_before210/state/time_step_75599_courier_state.txt"
exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('HCAC-1--batch64_filter600_623')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_64_courier_reward_filter600/test_zh1001_623/state/time_step_57599_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('HCAC-1--batch64_filter600_930')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_64_courier_reward_filter600/test_zh1001_930/state/time_step_64799_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)


print('HCAC-1--batch64_filter600_1145')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_64_courier_reward_filter600/test_zh1001_1145/state/time_step_50399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('HCAC-1--batch64_filter600_1185')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_64_courier_reward_filter600/test_zh1001_1185/state/time_step_50399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('HCAC-1--batch64_filter600_before_123')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_64_courier_reward_filter600/test_zh1001_before_123/state/time_step_50399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('HCAC-1--batch64_filter600_before_210')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_64_courier_reward_filter600/test_zh1001_before_210/state/time_step_50399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('HCAC-1--batch64_filter600_395')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_64_courier_reward_filter600/test_zh1001_623/state/time_step_50399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)


# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)
print('HCAC-2-before-140')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200307_0.5_0.5/test_zh1001_before140/state/time_step_50399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)
# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)


print('HCAC-2-before-209')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200307_0.5_0.5/test_zh1001_before209/state/time_step_86399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)
# # 10-20h的超时率
# working_time_overdue_sum3_0 = 0
# working_time_order_sum3_0 = 0
# for i in range(len(exchange_all_order_num_list3_2)):
#     if (0 <= i <=9) or (20 < i <= 23):
#         continue
#     else:
#         working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
#         working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
# working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
# print(working_time_overdue_rate3_0)

print('HCAC-2-before-1146')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200307_0.5_0.5/before/test_zh1001/state/time_step_61199_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)
# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)
print('HCAC-2-ckpt278')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200307_0.5_0.5/test_zh1001/state/time_step_57599_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)

# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('HCAC-2-without_filter-test')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200307_0.5_0.5_without_filter/test_zh1001/state/time_step_86399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)

# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('HCAC-2-without_filter-test-filter1200')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200307_0.5_0.5_without_filter/test_zh1001_filter/state/time_step_86399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)
# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)
print('HCAC-3filter600')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200307_0.5_0.5_without_filter/test_zh1001_filter2/state/time_step_71999_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)

# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('HCAC-3filter300')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200307_0.5_0.5_without_filter/test_zh1001_filter3/state/time_step_68399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)

# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('HCAC-2-without_filter-test,-ckpt1750')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200307_0.5_0.5_without_filter/test_zh1001_1750/state/time_step_68399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)

# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('HCAC-2-without_filter-test-filter1200,-ckpt1750')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200307_0.5_0.5_without_filter/test_zh1001_filter_1750/state/time_step_68399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)

# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('HCAC-3filter600,-ckpt1750')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200307_0.5_0.5_without_filter/test_zh1001_filter2_1750/state/time_step_68399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)

# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('HCAC-3filter300,-ckpt1750')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200307_0.5_0.5_without_filter/test_zh1001_filter3/state/time_step_50399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)

# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('HCAC-3-3item-1148')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward_3item/test_zh1001/state/time_step_86399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)

# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('HCAC-3-3item-146')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward_3item/test_zh1001_146/state/time_step_86399_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)

# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)

print('HCAC-3-3item-210')
#  换单
# exchange_last_file_name2 = "D:/exchange/train/update-2021-8-24/A2C_exchange_logs_consider_processint_time/time_step_7199_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/update-2021-8-24/test_HOAC_xianzhidanshu_zxh/time_step_86399_courier_state.txt"
# exchange_last_file_name3_1 = "D:/exchange/train/short_HOAC_2021-9-11/test_HOAC_xianzhidanshu/time_step_43149_courier_state.txt"
exchange_last_file_name3_2 = "D:/exchange/train/optimize-2022-1-19/main/20200306_attention_conv_times_batch_50_courier_reward_3item/test_zh1001_210/state/time_step_57599_courier_state.txt"

exchange_state_file3_2 = open(exchange_last_file_name3_2, "r")
# 超时率
exchange_overdue_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
exchange_all_order_num_list3_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # *24
for exchange_line in exchange_state_file3_2:
    exchange_line = exchange_line.strip('\n')
    exchange_first_item = exchange_line.split(',')[0]
    if exchange_first_item == '':
        exchange_order_dispatch_stage = int(exchange_line.split(',')[10].split(':')[1])
        exchange_order_create_time = int(exchange_line.split(',')[6].split(':')[1])
        exchange_order_deliver_time = int(exchange_line.split(',')[8].split(':')[1])
        exchange_promise_deliver_time = int(exchange_line.split(',')[9].split(':')[1])
        if exchange_order_dispatch_stage == 0:
            if exchange_promise_deliver_time < exchange_order_deliver_time:
                exchange_overdue_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
            exchange_all_order_num_list3_2[int(exchange_order_create_time / 3600)] += 1
print(exchange_overdue_order_num_list3_2)
print(exchange_all_order_num_list3_2)
exchange_overdue_rate3_2 = []
exchange_hour_list3_2 = []
for i in range(len(exchange_all_order_num_list3_2)):
    if exchange_all_order_num_list3_2[i] != 0:
        exchange_overdue_rate3_2.append(exchange_overdue_order_num_list3_2[i] / exchange_all_order_num_list3_2[i] / 2)
        exchange_hour_list3_2.append(i + 1)
    else:
        exchange_overdue_rate3_2.append(0)
        exchange_hour_list3_2.append(i + 1)
print(exchange_overdue_rate3_2)

exchange_day_overdue_sum3_2 = sum(exchange_overdue_order_num_list3_2)
exchange_day_all_sum3_2 = sum(exchange_all_order_num_list3_2)
exchange_day_overdue_rate3_2 = exchange_day_overdue_sum3_2 / exchange_day_all_sum3_2
print(exchange_day_overdue_rate3_2)

# 10-20h的超时率
working_time_overdue_sum3_0 = 0
working_time_order_sum3_0 = 0
for i in range(len(exchange_all_order_num_list3_2)):
    if (0 <= i <=9) or (20 < i <= 23):
        continue
    else:
        working_time_overdue_sum3_0+=exchange_overdue_order_num_list3_2[i]
        working_time_order_sum3_0+=exchange_all_order_num_list3_2[i]
working_time_overdue_rate3_0 = working_time_overdue_sum3_0 / working_time_order_sum3_0
print(working_time_overdue_rate3_0)
# # 折线图
# x = ['NE',
#      'E-SD',
#      # 'DQN',
#      # 'E-AC-',
#      # 'E-AC',
#      # 'AC-96',
#      'E-HOAC-',
#      'E-HOAC']
#
# plt.plot(hour_list, overdue_rate, color='green', marker='s', ms=5, label='NT')
# plt.plot(exchange_hour_list1, exchange_overdue_rate1, color='blue', marker='*', ms=5, label='SD-Osquare')
# plt.plot(exchange_hour_list3, exchange_overdue_rate3, color='black', marker='x', ms=5, label='HCAC-w.o.F')
# plt.plot(exchange_hour_list3_1, exchange_overdue_rate3_1, color='red', marker='x', ms=5, label='HCAC')
# # plt.xtick(9,19)
# plt.ylim(0, 0.08)
# plt.xlim(10, 20)
# plt.legend(ncol=2, loc='upper center')  # 显示图例
# #
# plt.xticks(size=20)
# plt.yticks(size=20)
# plt.xlabel('Hour of Day', size=25)
# plt.ylabel('Overdue Rate', size=25)
# #
# # x_major_locator = MultipleLocator(1)
# # ax = plt.gca()
# # ax.xaxis.set_major_locator(x_major_locator)
# # # plt.xlim(0, 10)
# plt.tight_layout()
# plt.savefig('time_overdue1120_2.pdf', bbox_inches='tight')
# plt.show()

# 矩形图
# plt.title('exchange VS no-exchange overdue rate')
# plt.plot(hour_list, overdue_rate, color='green', marker='s', ms=5, label='no-exchange')
# # plt.plot(exchange_hour_list, exchange_overdue_rate, color='blue', marker='*', ms=5, label='exchange-policy')
# # plt.plot(exchange_hour_list1, exchange_overdue_rate1, color='yellow', marker='*', ms=5, label='exchange-DQN')
# plt.plot(exchange_hour_list2_1, exchange_overdue_rate2_1, color='red', marker='*', ms=5, label='exchange-A2C')
# plt.plot(exchange_hour_list3_1, exchange_overdue_rate3_1, color='red', marker='*', ms=5, label='exchange-HOAC')
# x = list(range(len(hour_list) - 1))
# totoal_width = 0.8
# n = 3
# width = totoal_width / n
# plt.bar(x, overdue_rate[:-1], width=width, label='no-exchange', fc='green')
# for i in range(len(x)):
#     x[i] = x[i] + width
# plt.bar(x, exchange_overdue_rate2_1[:-1], width=width, label='exchange-A2C', fc='blue')
# for i in range(len(x)):
#     x[i] = x[i] + width
# plt.bar(x,exchange_overdue_rate3_1[:-1],width=width, label = 'exchange-HOAC', fc = 'red')
# for i in range(len(x)):
#     x[i] = x[i] + width
# plt.bar(x,exchange_overdue_rate2[:-1],width=width, label = 'this project', fc = 'black')

# plt.legend()  # 显示图例
#
# # plt.xlabel('Order Create Time')
# plt.ylabel('Overdue Rate')
#
# x_major_locator = MultipleLocator(1)
# ax = plt.gca()
# ax.xaxis.set_major_locator(x_major_locator)
# # plt.xlim(0, 10)
# plt.show()

# plt.title('exchange VS no-exchange revenue')
# plt.plot(hour_list, overdue_rate, color='green', marker='s', ms=5, label='no-exchange')
# plt.plot(exchange_hour_list, exchange_overdue_rate, color='blue', marker='*', ms=5, label='exchange-policy')
# plt.plot(exchange_hour_list1, exchange_overdue_rate1, color='yellow', marker='*', ms=5, label='exchange-DQN')
# plt.plot(exchange_hour_list2, exchange_overdue_rate2, color='red', marker='*', ms=5, label='exchange-A2C')
# x = list(range(len(hour_list)))
# fig, ax = plt.subplot()xing
# plt.rc('font',  family= 'Times New Roman', size= 14)
# x = ['NE',
#      'E-SD',
#      'DQN',
#      'E-AC-',
#      'E-AC',
#      'AC-96',
#      'E-HOAC-',
#      'E-HOAC']
# overdue_rate = [day_overdue_rate,
#                 exchange_day_overdue_rate1,
#                 exchange_day_overdue_rate6,
#                 exchange_day_overdue_rate2,
#                 exchange_day_overdue_rate2_1,
#                 exchange_day_overdue_rate2_2,
#                 exchange_day_overdue_rate3,
#                 exchange_day_overdue_rate3_1]
#
# # width = 0.8
#
# # rect1 = ax.bar(x -width/4,overdue_rate,width,label= 'no-exchange')
# # rect2 = ax.bar(x -2*width/4, exchange_overdue_rate, label='exchange-policy')
# # rect3 = ax.bar(x-3*width/4, exchange_overdue_rate1, label='exchange-DQN')
# # rect4 = ax.bar(x+width/4, exchange_overdue_rate2, label='exchange-A2C')
# # def autolabel(rects):
# #  for rect in rects:
# #   height = rect.get_height()
# #   height = rect.get_height()
# #   plt.text(rect.get_x()+rect.get_width()/2.-0.2, 1.03*height, '%s' % float(height))
#
# a = plt.bar(x, overdue_rate, fc='green')
#
# # autolabel(a)
# # plt.xticks(fontsize=20)
# # plt.legend(font1)  # 显示图例
#
# # plt.xlabel('Order Create Time')
# plt.ylabel('Overdue Rate')
# # plt.xlabel()
#
# # x_major_locator = MultipleLocator(1)
# # ax = plt.gca()
# # ax.xaxis.set_major_locator(x_major_locator)
# # plt.xlim(0, 10)
# plt.show()
