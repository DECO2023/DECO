import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pickle

# 解决画图中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
df_order = pd.read_csv('D:/exchange/data/2W_order20201001.csv').iloc[:, :]

#异常值处理
df_order = df_order.drop(df_order[df_order['shop_latitude'] < 10].index)
df_order = df_order.drop(df_order[df_order['rider_delivery_time'] == 'a'].index)
df_order = df_order.drop(df_order[df_order['promise_delivery_time'] == 0].index)
df_order = df_order.dropna()
df_order.reset_index(drop=True, inplace=True)

#数据格式转换
df_order['rider_pickup_time']=pd.to_datetime(df_order['rider_pickup_time'])
df_order['order_create_time']=pd.to_datetime(df_order['order_create_time'])
df_order['rider_accept_order_time']=pd.to_datetime(df_order['rider_accept_order_time'])
df_order['rider_arrive_restaurant_time']=pd.to_datetime(df_order['rider_arrive_restaurant_time'])
df_order['rider_delivery_time']=pd.to_datetime(df_order['rider_delivery_time'])

#打印骑手数组
rider_id=df_order['rider_id'].unique()

#骑手路径提取函数
def getRoute(rider_id):
    rider_orders = df_order[(df_order['rider_id'] == rider_id)]
    rider_shops=rider_orders[['shop_id','rider_pickup_time','shop_longitude', 'shop_latitude']]
    rider_shops.rename(columns={'shop_id':'loc_id', 'rider_pickup_time':'arrive_time','shop_longitude':'longitude', 'shop_latitude':'latitude'}, inplace = True)
    rider_users=rider_orders[['user_id','rider_delivery_time','user_longitude', 'user_latitude']]
    rider_users.rename(columns={'user_id':'loc_id', 'rider_delivery_time':'arrive_time','user_longitude':'longitude', 'user_latitude':'latitude'}, inplace = True)
    rider_shops['type']=rider_shops.index*0+1
    rider_users['type']=rider_users.index*0
    rider_route=rider_shops.append(rider_users)
    rider_route=rider_route.sort_values(by='arrive_time',ascending=True)
    rider_route.reset_index(drop=True, inplace=True)
    return rider_route

#距离计算
from math import sin, asin, cos, radians, fabs, sqrt
EARTH_RADIUS = 6371  # 地球平均半径，6371km
def hav(theta):
    s = sin(theta / 2)
    return s * s
def get_distance_hav(lng0, lat0, lng1, lat1):
    """
     用haversine公式计算球面两点间的距离
    """
    # 经纬度转换成弧度
    lat0 = radians(lat0)
    lat1 = radians(lat1)
    lng0 = radians(lng0)
    lng1 = radians(lng1)
    dlng = fabs(lng0 - lng1)
    dlat = fabs(lat0 - lat1)
    h = hav(dlat) + cos(lat0) * cos(lat1) * hav(dlng)
    distance = 2 * EARTH_RADIUS * asin(sqrt(h))
    return distance

#生成骑手—骑手路径数据集
rider_route_dict=dict.fromkeys(rider_id)
for r in rider_id:
    rider_route_dict[r]=getRoute(r)

# 骑手速度
SPEED = 1.25


# in:骑手id,时间,位置
# out:骑手当前可访问地点集合（包含特征）
def getAvailableLoc(rider_id, time, rider_lng, rider_lat):
    rider_orders = df_order[(df_order['rider_id'] == rider_id)
                            & (df_order['rider_accept_order_time'] < time)]
    rider_shops = rider_orders[['shop_id', 'rider_pickup_time', 'food_total_amt', 'shop_longitude', 'shop_latitude']]
    rider_shops.rename(columns={'shop_id': 'loc_id', 'rider_pickup_time': 'arrive_time', 'shop_longitude': 'longitude',
                                'shop_latitude': 'latitude'}, inplace=True)
    rider_shops['shop_id'] = rider_shops['loc_id']
    # 位置距离（D_sd）、订单距离（D_mc）、订单超时时间（T_ToD）、时间预算（T_budget）
    rider_shops['D_sd'] = rider_orders[['shop_longitude', 'shop_latitude']].apply(
        lambda x: (get_distance_hav(x['shop_longitude'], x['shop_latitude'], rider_lng, rider_lat)), axis=1)
    rider_shops['D_mc'] = rider_orders[['shop_longitude', 'shop_latitude', 'user_longitude', 'user_latitude']].apply(
        lambda x: (get_distance_hav(x['shop_longitude'], x['shop_latitude'], x['user_longitude'], x['user_latitude'])),
        axis=1)
    rider_shops['T_ToD'] = rider_orders['promise_delivery_time'] - rider_orders[['order_create_time']].apply(
        lambda x: (time - x['order_create_time']).total_seconds(), axis=1)
    rider_shops['T_budget'] = rider_shops['T_ToD'] - rider_shops['D_mc'] * 1000 / SPEED

    rider_users = rider_orders[
        ['user_id', 'rider_delivery_time', 'food_total_amt', 'user_longitude', 'user_latitude', 'shop_id']]
    rider_users.rename(
        columns={'user_id': 'loc_id', 'rider_delivery_time': 'arrive_time', 'user_longitude': 'longitude',
                 'user_latitude': 'latitude'}, inplace=True)
    # 位置距离、订单距离、订单超时时间、时间预算
    rider_users['D_sd'] = rider_orders[['user_longitude', 'user_latitude']].apply(
        lambda x: (get_distance_hav(x['user_longitude'], x['user_latitude'], rider_lng, rider_lat)), axis=1)
    rider_users['D_mc'] = rider_orders[['shop_longitude', 'shop_latitude', 'user_longitude', 'user_latitude']].apply(
        lambda x: (get_distance_hav(x['shop_longitude'], x['shop_latitude'], x['user_longitude'], x['user_latitude'])),
        axis=1)
    rider_users['T_ToD'] = rider_orders['promise_delivery_time'] - rider_orders[['order_create_time']].apply(
        lambda x: (time - x['order_create_time']).total_seconds(), axis=1)
    rider_users['T_budget'] = rider_shops['T_ToD']
    # 位置类型
    rider_shops['type'] = rider_shops.index * 0 + 1
    rider_users['type'] = rider_users.index * 0
    # 商户客户数据合并
    rider_available_loc = rider_shops.append(rider_users)
    rider_available_loc = rider_available_loc[(rider_available_loc['arrive_time'] > time)]
    # 重置index
    rider_available_loc.index = np.arange(len(rider_available_loc))
    # 可访问位置数量（N_d）、相同位置类型数量（N_sameType）、最近标记（B_nearest）、紧急标记（B_urgent）、紧急程度（T_left）
    rider_available_loc['N_d'] = rider_available_loc.index * 0 + len(rider_available_loc)
    rider_available_loc['N_sameType'] = rider_available_loc[['type']].apply(
        lambda x: (len(rider_available_loc[(rider_available_loc['type'] == x['type'])])), axis=1)
    rider_available_loc['B_nearest'] = rider_available_loc[['D_sd']].apply(
        lambda x: rider_available_loc.D_sd.min() == x['D_sd'], axis=1)
    rider_available_loc.B_nearest[rider_available_loc['B_nearest'] == True] = 1
    rider_available_loc.B_nearest[rider_available_loc['B_nearest'] == False] = 0
    rider_available_loc['B_urgent'] = rider_available_loc[['T_ToD']].apply(
        lambda x: rider_available_loc.T_ToD.min() == x['T_ToD'], axis=1)
    rider_available_loc.B_urgent[rider_available_loc['B_urgent'] == True] = 1
    rider_available_loc.B_urgent[rider_available_loc['B_urgent'] == False] = 0
    rider_available_loc['T_left'] = rider_available_loc[['T_budget']].apply(
        lambda x: rider_available_loc.T_budget.max() - x['T_budget'], axis=1)
    # To_all距离（D_other）
    rider_available_loc['D_other'] = rider_available_loc.index * 0
    for i in range(len(rider_available_loc)):
        d2other = 0
        for j in range(len(rider_available_loc)):
            d2other += get_distance_hav(rider_available_loc.loc[i, ['longitude']][0],
                                        rider_available_loc.loc[i, ['latitude']][0],
                                        rider_available_loc.loc[j, ['longitude']][0],
                                        rider_available_loc.loc[j, ['latitude']][0])
        rider_available_loc.loc[i, ['D_other']] = d2other
    return rider_available_loc

#给骑手当前可访问地点集合（包含特征）添加标签
#in:可访问地点集合、骑手下一站id、骑手下一站类型
#out:带标签的可访问地点集合
def addAvailableLocLabel(rider_available_loc):
    rider_available_loc['Label']=rider_available_loc[['arrive_time']].apply(lambda x: (rider_available_loc.arrive_time.min()==x['arrive_time']), axis=1)
    rider_available_loc.Label[rider_available_loc['Label']==True]=1
    rider_available_loc.Label[rider_available_loc['Label']==False]=0
    return rider_available_loc


#根据骑手—骑手路径数据集 生成 训练数据集
train_data=[]
for key, item in rider_route_dict.items():
    if len(item)>1:
        r_id=key
        rider_route1=item
        for i in range(len(item)-1):
            available_loc=getAvailableLoc(r_id,rider_route1.loc[i,['arrive_time']][0],rider_route1.loc[i,['longitude']][0],rider_route1.loc[i,['latitude']][0])
            if len(available_loc)>1:
                available_loc=addAvailableLocLabel(available_loc)
                train_data.append(available_loc)

#导出
import pickle
f = open('train_data.pckl', 'wb')
pickle.dump(train_data, f)
f.close()




