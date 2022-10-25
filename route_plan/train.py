import pickle
import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import roc_auc_score, auc
from sklearn import metrics
'''
[0 1 0 ... 0 1 0]
4844
5992
0.8084112149532711
'''

test_set = []
eval_set = []
eval_set2 = []
test_group = []
eval_group = []

f = open('train_data.pckl', 'rb')
the_data= pickle.load(f)
f.close()

#划分训练集
sep = int(0.7 * len(the_data))
train_list = the_data[:sep]
test_list = the_data[sep:]

#eval_group初始化
for i in test_list:
    eval_group.append(len(i))
#list转换为dataframe
train_data=pd.DataFrame()
train_data=train_data.append(train_list)
test_data=pd.DataFrame()
test_data=test_data.append(test_list)



dtrain = np.array(test_data)[:, 6:17]
dtarget = np.array(test_data)[:, 17:]
dtarget= dtarget.astype(int)
dtrain_eval = np.array(train_data)[:, 6:17]
dtarget_eval = np.array(train_data)[:, 17:]
dtarget_eval= dtarget_eval.astype(int)

gdbt = GradientBoostingClassifier(random_state=10)
#gdbt = GradientBoostingClassifier(learning_rate=0.1, n_estimators=60, max_depth=7, min_samples_leaf=60,
                                  #min_samples_split=1200, max_features='sqrt', subsample=0.8, random_state=10)
gdbt.fit(dtrain, dtarget)
y_pred = gdbt.predict(dtrain_eval)
y_probs = gdbt.predict_proba(dtrain_eval)[:,1]


fpr, tpr, thresholds = metrics.roc_curve(dtarget_eval, y_probs)
roc_auc = auc(fpr, tpr)  #auc为Roc曲线下的面积
#开始画ROC曲线
plt.plot(fpr, tpr, 'b',label='AUC = %0.2f'% roc_auc)
plt.show()
print(y_pred)

index = 0
count = 0
t = [[] for _ in range(len(eval_group))]
d = [[] for _ in range(len(eval_group))]

for i in range(len(eval_group)):
    t[i] = y_pred[index:index+eval_group[i]]
    d[i] = dtarget_eval[index:index+eval_group[i]]

    if len(t[i]) > 0:
        # print(np.argmax(np.array(t[i])), np.argmax(np.array(d[i])))
        max_1 = np.argmax(np.array(t[i]))
        max_2 = np.argmax(np.array(d[i]))

        if max_1 == max_2:
            count += 1
    index += eval_group[i]

print(count)
print(len(eval_group))
print(count/len(eval_group))