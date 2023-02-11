import tensorflow as tf
import numpy as np
# import gym
# import time


np.random.seed(1)
tf.set_random_seed(1)

#####################  hyper parameters  ####################

# MAX_EPISODES = 200
# MAX_EP_STEPS = 200
# LR_A = 0.001    # learning rate for actor
# LR_C = 0.001    # learning rate for critic
GAMMA = 0.9     # reward discount
REPLACEMENT = [
    dict(name='soft', tau=0.01),
    dict(name='hard', rep_iter_a=600, rep_iter_c=500)
][0]            # you can try different target replacement strategies
# MEMORY_CAPACITY = 10000
BATCH_SIZE = 32

# RENDER = False
# OUTPUT_GRAPH = True
# ENV_NAME = 'Pendulum-v0'
state_dim = 13+2
action_dim = 2
h_state_dim = 19+2
h_action_dim = 2

# all placeholder for tf
with tf.name_scope('S'):
    S = tf.placeholder(tf.float32, shape=[None, state_dim], name='s')
with tf.name_scope('R'):
    R = tf.placeholder(tf.float32, [None, ], name='r')
with tf.name_scope('S_'):
    S_ = tf.placeholder(tf.float32, shape=[None, state_dim], name='s_')

# all placeholder for tf
with tf.name_scope('h_S'):
    high_S = tf.placeholder(tf.float32, shape=[None, h_state_dim], name='h_s')
with tf.name_scope('h_R'):
    high_R = tf.placeholder(tf.float32, [None, ], name='h_r')
with tf.name_scope('h_S_'):
    high_S_ = tf.placeholder(tf.float32, shape=[None, h_state_dim], name='h_s_')

###############################  Actor  ####################################
class High_Level_Network(object):
    def __init__(self, sess, n_features, n_actions, lr=0.001, batch_size=256):
        self.sess = sess
        self.batch_size = batch_size
        self.n_actions = n_actions
        self.n_features = n_features
        self.lr = lr
        self.gamma = GAMMA

        # self.ep_obs, self.ep_as, self.ep_rs = [], [], []

        self.s = tf.compat.v1.placeholder(tf.float32, [None, self.n_features], "state")
        self.a = tf.compat.v1.placeholder(tf.int32, [None, ], "act")
        self.td_error = tf.compat.v1.placeholder(tf.float32, None, "td_error")

        self.cost_his = []

        with tf.compat.v1.variable_scope('h_Actor'):
            # to be adjusted
            # activ = tf.nn.relu
            # encoding1 = activ(conv(self.s[:6], 'c1', n_filters=32, filter_size=4, stride=2))
            #
            # encoding2 = activ(conv(self.s[7:], 'c2', n_filters=32, filter_size=4, stride=2))
            # encoding1 = activ(linear(self.s[:11], 'e1', n_hidden=32))
            # encoding2 = activ(linear(self.s[12:], 'e2', n_hidden=32))

            # fusion1 = encoding1 * encoding2

            # decoding1 = activ(linear(fusion1, 'fc1', n_hidden=n_actions, init_scale=np.sqrt(2)))

            # layer_3 = activ(conv(layer_2, 'c3', n_filters=64, filter_size=3, stride=1))
            # layer_3 = conv_to_fc(layer_3)
            # return activ(linear(layer_3, 'fc1', n_hidden=512, init_scale=np.sqrt(2)))

            # encoding1 = tf.compat.v1.layers.dense(
            #     inputs=self.s[:,:11],
            #     units=32,  # number of hidden units
            #     activation=tf.nn.relu,
            #     kernel_initializer=tf.random_normal_initializer(0., .1),  # weights
            #     bias_initializer=tf.constant_initializer(0.1),  # biases
            #     name='h_l1'
            # )
            # encoding2 = tf.compat.v1.layers.dense(
            #     inputs=self.s[:,11:],
            #     units=32,  # number of hidden units
            #     activation=tf.nn.relu,
            #     kernel_initializer=tf.random_normal_initializer(0., .1),  # weights
            #     bias_initializer=tf.constant_initializer(0.1),  # biases
            #     name='h_l2'
            # )
            # # 卷积提取分别 相遇场景特征 和相遇订单特征
            # # 合并
            # # 求意愿度
            # fusion1 = tf.concat([encoding1, encoding2], 1)
            # bn1 = tf.layers.batch_normalization(self.s, training=True)
            out = tf.compat.v1.layers.dense(
                inputs=self.s,
                units=n_features,  # number of hidden units
                activation=tf.nn.relu,
                kernel_initializer=tf.random_normal_initializer(0., .1),  # weights
                bias_initializer=tf.constant_initializer(0.1),  # biases
                name='o1'
            )
            s_up_dim = tf.reshape(out, [-1, self.n_features, 1])

            u = tf.compat.v1.layers.dense(
                inputs=s_up_dim,
                units=1,  # number of hidden units
                activation=tf.nn.tanh,
                kernel_initializer=tf.random_normal_initializer(0., .1),  # weights
                bias_initializer=tf.constant_initializer(0.1),  # biases
                name='u'
            )

            att = tf.compat.v1.layers.dense(
                inputs=u,
                units=1,  # number of hidden units
                # activation=tf.nn.softmax,
                kernel_initializer=tf.random_normal_initializer(0., .1),  # weights
                bias_initializer=tf.constant_initializer(0.1),  # biases
                name='att'
            )
            att = tf.reshape(att, [-1, self.n_features])
            att_softmax = tf.nn.softmax(att)
            att_softmax = tf.reshape(att_softmax, [-1, self.n_features, 1])
            self.att = att_softmax
            score_x = s_up_dim * att_softmax

            score_x = tf.reshape(score_x, [-1, self.n_features])

            w1 = tf.constant(1, shape=(1, self.n_features, 32), dtype=tf.float32,
                             name='h_w1')  # shape=(filter_width,in_channels,out_channels)
            w2 = tf.constant(1, shape=(1, 32, 64), dtype=tf.float32,
                             name='h_w2')  # shape=(filter_width,in_channels,out_channels)
            w3 = tf.constant(1, shape=(1, 64, 128), dtype=tf.float32,
                             name='h_w3')  # shape=(filter_width,in_channels,out_channels)

            conv1 = tf.nn.conv1d(score_x[np.newaxis, :], w1, 1, 'VALID')
            bn2 = tf.layers.batch_normalization(conv1, training=True)
            conv1_relu = tf.nn.relu(bn2)
            pool1 = tf.layers.max_pooling1d(conv1_relu, pool_size=1, strides=1)

            conv2 = tf.nn.conv1d(pool1, w2, 1, 'VALID')
            bn3 = tf.layers.batch_normalization(conv2, training=True)
            conv2_relu = tf.nn.relu(bn3)
            pool2 = tf.layers.max_pooling1d(conv2_relu, pool_size=1, strides=1)

            # conv3 = tf.nn.conv1d(pool2, w3, 1, 'VALID')
            # bn4 = tf.layers.batch_normalization(conv3, training=True)
            # conv4_relu = tf.nn.relu(bn4)
            # pool3 = tf.layers.max_pooling1d(conv4_relu, pool_size=1, strides=1)
            # pool3 = pool3[0, :, :]

            pool2 = pool2[0,:,:]

            # fusion1 = tf.compat.v1.layers.dense(
            #     inputs=pool3,
            #     units=64,  # number of hidden units
            #     activation=tf.nn.relu,
            #     kernel_initializer=tf.random_normal_initializer(0., .1),  # weights
            #     bias_initializer=tf.constant_initializer(0.1),  # biases
            #     name='dense1'
            # )
            # fusion2 = tf.compat.v1.layers.dense(
            #     inputs=fusion1,
            #     units=32,  # number of hidden units
            #     activation=tf.nn.relu,
            #     kernel_initializer=tf.random_normal_initializer(0., .1),  # weights
            #     bias_initializer=tf.constant_initializer(0.1),  # biases
            #     name='dense2'
            # )
            fusion2 = tf.compat.v1.layers.dense(
                inputs=pool2,
                units=32,  # number of hidden units
                activation=tf.nn.relu,
                kernel_initializer=tf.random_normal_initializer(0., .1),  # weights
                bias_initializer=tf.constant_initializer(0.1),  # biases
                name='dense2'
            )
            self.decoding1 = tf.compat.v1.layers.dense(
                inputs=fusion2,
                units=n_actions,  # output units
                activation=tf.nn.relu,  # get action probabilities
                kernel_initializer=tf.random_normal_initializer(0., .1),  # weights
                bias_initializer=tf.constant_initializer(0.1),  # biases
                name='h_acts_prob'
            )
            # self.all_act_prob = tf.nn.softmax(self.acts_prob,
            #                                   name='h_act_prob')  # use softmax to convert to probability
            self.all_act_prob = tf.clip_by_value(tf.nn.softmax(self.decoding1,
                                                               name='h_act_prob'), 0.0,
                                                 1.0)  # use softmax to convert to probability

        with tf.compat.v1.variable_scope('h_loss'):
            neg_log_prob = - tf.compat.v1.nn.sparse_softmax_cross_entropy_with_logits(logits=self.decoding1,
                                                                                      labels=self.a)  # this is negative log of chosen action
            # or in this way:
            # neg_log_prob = tf.reduce_sum(-tf.log(self.all_act_prob)*tf.one_hot(self.tf_acts, self.n_actions), axis=1)
            self.loss = tf.compat.v1.reduce_mean(tf.reduce_sum(neg_log_prob * self.td_error))  # reward guided loss

        with tf.compat.v1.variable_scope('h_train'):
            self.train_op = tf.compat.v1.train.AdamOptimizer(self.lr).minimize(
                - self.loss)  # minimize(-exp_v) = maximize(exp_v)

    # def store_transition(self, s, a, r):
    #     # 一次相遇事件 对于两个骑手的总reward,对于两个骑手的---局部0.3权重
    #     self.ep_obs.append(s)
    #     self.ep_as.append(a)
    #     self.ep_rs.append(r)

    def learn(self, s, a, td):
        # s = s[np.newaxis, :]
        # feed_dict = {self.s: s, self.a: a, self.td_error: td}
        # _, exp_v = self.sess.run([self.train_op, self.exp_v], feed_dict)
        # return exp_v
        # discount and normalize episode reward
        # discounted_ep_rs_norm = self._discount_and_norm_rewards()
        # a = a.astype(np.float32)
        # train on episode
        _, exp_v = self.sess.run([self.train_op, self.loss], feed_dict={
            self.s: np.vstack(s[np.newaxis, :]),  # shape=[None, n_obs]
            self.a: np.array(a),  # shape=[None, ]
            self.td_error: td,  # shape=[None, ]
        })
        # print(exp_v)
        # print(self.exp_v )
        self.cost_his.append(exp_v)
        return exp_v

    # def learn(self):
    #     # discount and normalize episode reward
    #     discounted_ep_rs_norm = self._discount_and_norm_rewards()
    #
    #     # train on episode
    #     self.sess.run(self.train_op, feed_dict={
    #         self.s: np.vstack(self.ep_obs),  # shape=[None, n_obs]
    #         self.a: np.array(self.ep_as),  # shape=[None, ]
    #         self.vt: discounted_ep_rs_norm,  # shape=[None, ]
    #     })
    #
    #     self.ep_obs, self.ep_as, self.ep_rs = [], [], []  # empty episode data
    #     # return discounted_ep_rs_norm
    #
    #     # # s = s[np.newaxis, :]
    #     # # feed_dict = {self.s: s, self.a: a, self.td_error: td}
    #     # # _, exp_v = self.sess.run([self.train_op, self.exp_v], feed_dict)
    #     # # return exp_v
    #     # # discount and normalize episode reward
    #     # # discounted_ep_rs_norm = self._discount_and_norm_rewards()
    #     # a = a.astype(np.float32)
    #     # # train on episode
    #     # _, exp_v = self.sess.run([self.train_op, self.exp_v], feed_dict={
    #     #     self.s: np.vstack(s),  # shape=[None, n_obs]
    #     #     self.a: np.array(a),  # shape=[None, ]
    #     #     self.vt: td,  # shape=[None, ]
    #     # })
    #     # # print(exp_v)
    #     # # print(self.exp_v )
    #     # self.cost_his.append(exp_v)
    #     # return exp_v
    #     return discounted_ep_rs_norm
    #
    # def _discount_and_norm_rewards(self):
    #     # discount episode rewards
    #     discounted_ep_rs = np.zeros_like(self.ep_rs)
    #     running_add = 0
    #     for t in reversed(range(0, len(self.ep_rs))):
    #         running_add = running_add * self.gamma + self.ep_rs[t]
    #         discounted_ep_rs[t] = running_add
    #
    #     # normalize episode rewards
    #     discounted_ep_rs -= np.mean(discounted_ep_rs)
    #     discounted_ep_rs /= np.std(discounted_ep_rs)
    #     return discounted_ep_rs

    def choose_action(self, s):
        # s = s[np.newaxis, :]  # np.newaxis 增加一个维度
        # 给一个状态，求

        # s = s * np.ones((self.batch_size, self.n_features))
        # probs = self.sess.run(self.acts_prob, {self.s: s})   # get probabilities for all actions
        # probs = probs[0]
        # probs = probs[np.newaxis, :]
        # return np.random.choice(np.arange(probs.shape[1]), p=probs.ravel())   # return a int
        prob_weights = self.sess.run(self.all_act_prob, feed_dict={self.s: s[np.newaxis, :]})
        # print('high_level_actor,初始pro:',prob_weights)
        # prob_weights = tf.clip_by_value(prob_weights, 1e-10, 1.0)
        # print('high_level_actor,后来pro:', prob_weights)
        action = np.random.choice(range(prob_weights.shape[1]),
                                  p=prob_weights.ravel())  # select action w.r.t the actions prob
        print('high_level_actor,prob:', prob_weights, ',action:', action)
        return action

    def plot_cost(self):
        import matplotlib.pyplot as plt
        plt.plot(np.arange(len(self.cost_his)), self.cost_his)
        plt.ylabel('Cost')
        plt.xlabel('training steps')
        plt.show()


class Actor(object):
    def __init__(self, sess, n_features, n_actions, lr=0.001, batch_size=256):
        self.sess = sess
        self.batch_size = batch_size
        self.n_features = n_features
        self.n_actions = n_actions
        self.lr = lr
        self.gamma = GAMMA

        self.s = tf.compat.v1.placeholder(tf.float32, [None, n_features], "state")
        self.a = tf.compat.v1.placeholder(tf.int32, [None, ], "act")
        self.td_error = tf.compat.v1.placeholder(tf.float32, None, "td_error")  # TD_error

        self.cost_his = []

        with tf.compat.v1.variable_scope('Actor'):
            # bn1 = tf.layers.batch_normalization(self.s, training=True)
            out = tf.compat.v1.layers.dense(
                inputs=self.s,
                units=n_features,  # number of hidden units
                activation=tf.nn.relu,
                kernel_initializer=tf.random_normal_initializer(0., .1),  # weights
                bias_initializer=tf.constant_initializer(0.1),  # biases
                name='o1_ac'
            )
            s_up_dim = tf.reshape(out, [-1, self.n_features, 1])

            u = tf.compat.v1.layers.dense(
                inputs=s_up_dim,
                units=1,  # number of hidden units
                activation=tf.nn.tanh,
                kernel_initializer=tf.random_normal_initializer(0., .1),  # weights
                bias_initializer=tf.constant_initializer(0.1),  # biases
                name='u_act'
            )

            att = tf.compat.v1.layers.dense(
                inputs=u,
                units=1,  # number of hidden units
                # activation=tf.nn.softmax,
                kernel_initializer=tf.random_normal_initializer(0., .1),  # weights
                bias_initializer=tf.constant_initializer(0.1),  # biases
                name='att_act'
            )
            att = tf.reshape(att, [-1, self.n_features])
            att_softmax = tf.nn.softmax(att)
            att_softmax = tf.reshape(att_softmax, [-1, self.n_features, 1])
            self.att = att_softmax
            score_x = s_up_dim * att_softmax

            score_x = tf.reshape(score_x, [-1, self.n_features])

            w1 = tf.constant(1, shape=(1, self.n_features, 32), dtype=tf.float32,
                             name='w1')  # shape=(filter_width,in_channels,out_channels)
            w2 = tf.constant(1, shape=(1, 32, 64), dtype=tf.float32,
                             name='w2')  # shape=(filter_width,in_channels,out_channels)
            w3 = tf.constant(1, shape=(1, 64, 128), dtype=tf.float32,
                             name='w3')  # shape=(filter_width,in_channels,out_channels)

            conv1 = tf.nn.conv1d(score_x[np.newaxis, :], w1, 1, 'VALID')
            bn2 = tf.layers.batch_normalization(conv1, training=True)
            conv1_relu = tf.nn.relu(bn2)
            pool1 = tf.layers.max_pooling1d(conv1_relu, pool_size=1, strides=1)

            conv2 = tf.nn.conv1d(pool1, w2, 1, 'VALID')
            bn3 = tf.layers.batch_normalization(conv2, training=True)
            conv2_relu = tf.nn.relu(bn3)
            pool2 = tf.layers.max_pooling1d(conv2_relu, pool_size=1, strides=1)

            # conv3 = tf.nn.conv1d(pool2, w3, 1, 'VALID')
            # bn4 = tf.layers.batch_normalization(conv3, training=True)
            # conv3_relu = tf.nn.relu(bn4)
            # pool3 = tf.layers.max_pooling1d(conv3_relu, pool_size=1, strides=1)
            #
            # pool3 = pool3[0, :, :]
            pool2 = pool2[0, :, :]
            # l1 = tf.compat.v1.layers.dense(
            #     inputs=pool3,
            #     units=64,  # number of hidden units
            #     activation=tf.nn.relu,
            #     kernel_initializer=tf.random_normal_initializer(0., .1),  # weights
            #     bias_initializer=tf.constant_initializer(0.1),  # biases
            #     name='dense1_act'
            # )
            # l2 = tf.compat.v1.layers.dense(
            #     inputs=l1,
            #     units=32,  # number of hidden units
            #     activation=tf.nn.relu,
            #     kernel_initializer=tf.random_normal_initializer(0., .1),  # weights
            #     bias_initializer=tf.constant_initializer(0.1),  # biases
            #     name='dense2_act'
            # )
            l2 = tf.compat.v1.layers.dense(
                inputs=pool2,
                units=32,  # number of hidden units
                activation=tf.nn.relu,
                kernel_initializer=tf.random_normal_initializer(0., .1),  # weights
                bias_initializer=tf.constant_initializer(0.1),  # biases
                name='dense2_act'
            )

            self.acts_prob = tf.compat.v1.layers.dense(
                inputs=l2,
                units=n_actions,  # output units
                activation=tf.nn.relu,  # get action probabilities
                kernel_initializer=tf.random_normal_initializer(0., .1),  # weights
                bias_initializer=tf.constant_initializer(0.1),  # biases
                name='acts_prob'
            )
            self.all_act_prob = tf.clip_by_value(tf.nn.softmax(self.acts_prob,
                                                               name='act_prob'), 0.0,
                                                 1.0)  # use softmax to convert to probability

        with tf.compat.v1.variable_scope('exp_v'):
            log_prob = - tf.compat.v1.nn.sparse_softmax_cross_entropy_with_logits(logits=self.acts_prob, labels=self.a)
            # log_prob = tf.compat.v1.log(self.acts_prob[0, self.a])
            # softmaxprob = tf.compat.v1.nn.softmax(tf.compat.v1.log(self.acts_prob + 1e-8))
            # logsoftmaxprob = tf.compat.v1.nn.log_softmax(softmaxprob)
            # log_prob = - logsoftmaxprob * self.a
            self.exp_v = tf.reduce_mean(
                tf.reduce_sum(log_prob * self.td_error))  # advantage (TD_error) guided loss
            # self.logits = logits = fc(l3, "logits", self.action_dim,
            #                           act=tf.nn.relu) + 1  # avoid valid_logits are all zeros
            # self.valid_logits = logits * self.neighbor_mask

            # self.softmaxprob = tf.nn.softmax(tf.compat.v1.log(self.valid_logits + 1e-8))
            # self.logsoftmaxprob = tf.nn.log_softmax(self.softmaxprob)
            # self.neglogprob = - self.logsoftmaxprob * self.ACTION
            # self.actor_loss = tf.reduce_mean(tf.reduce_sum(self.neglogprob * self.tfadv, axis=1))

        with tf.compat.v1.variable_scope('train'):
            self.train_op = tf.compat.v1.train.AdamOptimizer(self.lr).minimize(
                -self.exp_v)  # minimize(-exp_v) = maximize(exp_v)

    def learn(self, s, a, td):
        # s = s[np.newaxis, :]
        # feed_dict = {self.s: s, self.a: a, self.td_error: td}
        # _, exp_v = self.sess.run([self.train_op, self.exp_v], feed_dict)
        # return exp_v
        # discount and normalize episode reward
        # discounted_ep_rs_norm = self._discount_and_norm_rewards()
        # a = a.astype(np.float32)
        # train on episode
        _, exp_v = self.sess.run([self.train_op, self.exp_v], feed_dict={
            self.s: np.vstack(s),  # shape=[None, n_obs]
            self.a: np.array(a),  # shape=[None, ]
            self.td_error: td,  # shape=[None, ]
        })
        # print(exp_v)
        # print(self.exp_v )
        self.cost_his.append(exp_v)
        return exp_v

        # self.ep_obs, self.ep_as, self.ep_rs = [], [], []    # empty episode data

    def choose_action(self, s):
        # s = s[np.newaxis, :]  # np.newaxis 增加一个维度
        # 给一个状态，求

        # s = s * np.ones((self.batch_size, self.n_features))
        # probs = self.sess.run(self.acts_prob, {self.s: s})   # get probabilities for all actions
        # probs = probs[0]
        # probs = probs[np.newaxis, :]
        # return np.random.choice(np.arange(probs.shape[1]), p=probs.ravel())   # return a int

        # 将这里的action变为 action_list
        # s_list = []
        # cur_s = []
        # for state_item_count in range(len(s)):
        #     if state_item_count % 13 == 0 and state_item_count != 0:  # 13为一个订单的low_level state
        #         s_list.append(cur_s)
        #         cur_s = []
        #     cur_s.append(s[state_item_count])
        # s_list.append(cur_s)
        #
        # s_list = np.array(s_list)
        #
        # action_list = []
        # for state_item in s_list:
        #     prob_weights = self.sess.run(self.all_act_prob, feed_dict={self.s: state_item[np.newaxis, :]})
        #     action = np.random.choice(range(prob_weights.shape[1]),
        #                               p=prob_weights.ravel())  # select action w.r.t the actions prob
        #     action_list.append(action)

        # prob_weights = self.sess.run(self.all_act_prob, feed_dict={self.s: s[np.newaxis, :]})
        # action_list = []
        prob_weights = self.sess.run(self.all_act_prob, feed_dict={self.s: s[np.newaxis, :]})
        # print('low_level_actor,初始pro:',prob_weights)
        # prob_weights = tf.clip_by_value(prob_weights, 1e-10, 1.0)
        # print('low_level_actor,后来pro:', prob_weights)
        print(prob_weights)
        action_list = []
        # for action_i in range(len(s[np.newaxis, :])):
        action = np.random.choice(range(prob_weights.shape[1]),
                                  p=prob_weights.ravel())  # select action w.r.t the actions prob
            # action_list.append(action)
        # action = np.random.choice(range(prob_weights.shape[1]),
        #                           p=prob_weights.ravel())  # select action w.r.t the actions prob
        # print('low_level_Actor, prob:', prob_weights, ',action:', action_list)
        return action

    def plot_cost(self):
        import matplotlib.pyplot as plt
        plt.plot(np.arange(len(self.cost_his)), self.cost_his)
        plt.ylabel('Cost')
        plt.xlabel('training steps')
        plt.show()


class High_Level_Critic(object):
    def __init__(self, sess, n_features, lr=0.01, memory_size=100000, batch_size=256):
        self.sess = sess
        self.n_features = n_features
        self.batch_size = batch_size
        self.s = tf.compat.v1.placeholder(tf.float32, [None, n_features], "state")
        self.v_ = tf.compat.v1.placeholder(tf.float32, [None, 1], "v_next")
        self.r = tf.compat.v1.placeholder(tf.float32, None, 'r')
        self.memory_size = memory_size
        self.memory = np.zeros((self.memory_size, n_features * 2 + 2))
        self.lr = lr
        self.gamma = GAMMA

        self.cost_his = []

        with tf.compat.v1.variable_scope('HL_Critic'):
            # bn1 = tf.layers.batch_normalization(self.s, training=True)
            out = tf.compat.v1.layers.dense(
                inputs=self.s,
                units=n_features,  # number of hidden units
                activation=tf.nn.relu,
                kernel_initializer=tf.random_normal_initializer(0., .1),  # weights
                bias_initializer=tf.constant_initializer(0.1),  # biases
                name='o1_cr'
            )
            s_up_dim = tf.reshape(out, [-1, self.n_features, 1])

            u = tf.compat.v1.layers.dense(
                inputs=s_up_dim,
                units=1,  # number of hidden units
                activation=tf.nn.tanh,
                kernel_initializer=tf.random_normal_initializer(0., .1),  # weights
                bias_initializer=tf.constant_initializer(0.1),  # biases
                name='u_cr'
            )

            att = tf.compat.v1.layers.dense(
                inputs=u,
                units=1,  # number of hidden units
                # activation=tf.nn.softmax,
                kernel_initializer=tf.random_normal_initializer(0., .1),  # weights
                bias_initializer=tf.constant_initializer(0.1),  # biases
                name='att_cr'
            )
            att = tf.reshape(att, [-1, self.n_features])
            att_softmax = tf.nn.softmax(att)
            att_softmax = tf.reshape(att_softmax, [-1, self.n_features, 1])
            self.att = att_softmax
            score_x = s_up_dim * att_softmax

            score_x = tf.reshape(score_x, [-1, self.n_features])

            w1 = tf.constant(1, shape=(1, self.n_features, 32), dtype=tf.float32,
                             name='hc_w1')  # shape=(filter_width,in_channels,out_channels)
            w2 = tf.constant(1, shape=(1, 32, 64), dtype=tf.float32,
                             name='hc_w2')  # shape=(filter_width,in_channels,out_channels)
            w3 = tf.constant(1, shape=(1, 64, 128), dtype=tf.float32,
                             name='hc_w3')  # shape=(filter_width,in_channels,out_channels)

            conv1 = tf.nn.conv1d(score_x[np.newaxis, :], w1, 1, 'VALID')
            bn2 = tf.layers.batch_normalization(conv1, training=True)
            conv1_relu = tf.nn.relu(bn2)
            pool1 = tf.layers.max_pooling1d(conv1_relu, pool_size=1, strides=1)

            conv2 = tf.nn.conv1d(pool1, w2, 1, 'VALID')
            bn3 = tf.layers.batch_normalization(conv2, training=True)
            conv2_relu = tf.nn.relu(bn3)
            pool2 = tf.layers.max_pooling1d(conv2_relu, pool_size=1, strides=1)

            # conv3 = tf.nn.conv1d(pool2, w3, 1, 'VALID')
            # bn4 = tf.layers.batch_normalization(conv3, training=True)
            # conv3_relu = tf.nn.relu(bn4)
            # pool3 = tf.layers.max_pooling1d(conv3_relu, pool_size=1, strides=1)
            #
            # pool3 = pool3[0, :, :]

            pool2 = pool2[0, :, :]

            # l1 = tf.compat.v1.layers.dense(
            #     inputs=pool3,
            #     units=64,  # number of hidden units
            #     activation=tf.nn.relu,
            #     kernel_initializer=tf.random_normal_initializer(0., .1),  # weights
            #     bias_initializer=tf.constant_initializer(0.1),  # biases
            #     name='dense1_cr'
            # )
            # l2 = tf.compat.v1.layers.dense(
            #     inputs=l1,
            #     units=32,  # number of hidden units
            #     activation=tf.nn.relu,
            #     kernel_initializer=tf.random_normal_initializer(0., .1),  # weights
            #     bias_initializer=tf.constant_initializer(0.1),  # biases
            #     name='dense2_cr'
            # )
            l2 = tf.compat.v1.layers.dense(
                inputs=pool2,
                units=32,  # number of hidden units
                activation=tf.nn.relu,
                kernel_initializer=tf.random_normal_initializer(0., .1),  # weights
                bias_initializer=tf.constant_initializer(0.1),  # biases
                name='dense2_cr'
            )

            self.v = tf.compat.v1.layers.dense(
                inputs=l2,
                units=1,  # output units
                activation=tf.nn.relu,
                kernel_initializer=tf.random_normal_initializer(0., .1),  # weights
                bias_initializer=tf.constant_initializer(0.1),  # biases
                name='V'
            )

        with tf.compat.v1.variable_scope('squared_TD_error1'):
            self.td_error = tf.reduce_mean(self.r + self.gamma * self.v_ - self.v)
            self.loss = 0.5 * tf.reduce_sum(tf.square(self.td_error))  # TD_error = (r+gamma*V_next) - V_eval

        with tf.compat.v1.variable_scope('train1'):
            self.train_op = tf.compat.v1.train.AdamOptimizer(self.lr).minimize(self.loss)

    def store_transition(self, s, a, r, s_):
        if not hasattr(self, 'memory_counter'):
            self.memory_counter = 0

        transition = np.hstack((s, a, r, s_))

        # replace the old memory with new memory
        index = self.memory_counter % self.memory_size
        self.memory[index, :] = transition

        self.memory_counter += 1

    def learn(self, s, r, s_):
        # sample batch memory from all memory
        # s, s_ = s[np.newaxis, :], s_[np.newaxis, :]
        v_ = self.sess.run(self.v, {self.s: s_})
        td_error, _ = self.sess.run([self.td_error, self.train_op],
                                    {self.s: s, self.v_: v_, self.r: r})
        self.cost_his.append(0.5 * np.average(td_error ** 2))

        return td_error

    def plot_cost(self):
        import matplotlib.pyplot as plt
        plt.plot(np.arange(len(self.cost_his)), self.cost_his)
        plt.ylabel('Cost')
        plt.xlabel('training steps')
        plt.show()







class Actor(object):
    def __init__(self, sess,state_dim,  action_dim, learning_rate, replacement): # action_bound,
        self.sess = sess
        self.a_dim = action_dim
        self.n_features = state_dim
        # self.action_bound = action_bound
        self.lr = learning_rate
        self.replacement = replacement
        self.t_replace_counter = 0
        # with tf.name_scope('S'):
        # self.S = tf.placeholder(tf.float32, shape=[None, state_dim], name='s1')
        # # with tf.name_scope('R'):
        # self.R = tf.placeholder(tf.float32, [None, ], name='r')
        # # with tf.name_scope('S_'):
        # self.S_ = tf.placeholder(tf.float32, shape=[None, state_dim], name='s1_')

        with tf.variable_scope('Actor'):
            # input s, output a
            self.a = self._build_net(S, scope='eval_net', trainable=True)

            # input s_, output a, get a_ for critic
            self.a_ = self._build_net(S_, scope='target_net', trainable=False)

        self.e_params = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope='Actor/eval_net')
        self.t_params = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope='Actor/target_net')

        if self.replacement['name'] == 'hard':
            self.t_replace_counter = 0
            self.hard_replace = [tf.assign(t, e) for t, e in zip(self.t_params, self.e_params)]
        else:
            self.soft_replace = [tf.assign(t, (1 - self.replacement['tau']) * t + self.replacement['tau'] * e)
                                 for t, e in zip(self.t_params, self.e_params)]

    def _build_net(self, s, scope, trainable):
        with tf.variable_scope(scope):
            init_w = tf.random_normal_initializer(0., 0.3)
            init_b = tf.constant_initializer(0.1)
            # net = tf.layers.dense(s, 30, activation=tf.nn.relu,
            #                       kernel_initializer=init_w, bias_initializer=init_b, name='l1',
            #                       trainable=trainable)
            out = tf.compat.v1.layers.dense(
                inputs=s,
                units=self.n_features,  # number of hidden units
                activation=tf.nn.relu,
                kernel_initializer=tf.random_normal_initializer(0., .1),  # weights
                bias_initializer=tf.constant_initializer(0.1),  # biases
                name='o1_ac'
            )
            s_up_dim = tf.reshape(out, [-1, self.n_features, 1])

            u = tf.compat.v1.layers.dense(
                inputs=s_up_dim,
                units=1,  # number of hidden units
                activation=tf.nn.tanh,
                kernel_initializer=tf.random_normal_initializer(0., .1),  # weights
                bias_initializer=tf.constant_initializer(0.1),  # biases
                name='u_act'
            )

            att = tf.compat.v1.layers.dense(
                inputs=u,
                units=1,  # number of hidden units
                # activation=tf.nn.softmax,
                kernel_initializer=tf.random_normal_initializer(0., .1),  # weights
                bias_initializer=tf.constant_initializer(0.1),  # biases
                name='att_act'
            )
            att = tf.reshape(att, [-1, self.n_features])
            att_softmax = tf.nn.softmax(att)
            att_softmax = tf.reshape(att_softmax, [-1, self.n_features, 1])
            self.att = att_softmax
            score_x = s_up_dim * att_softmax

            score_x = tf.reshape(score_x, [-1, self.n_features])

            w1 = tf.constant(1, shape=(1, self.n_features, 32), dtype=tf.float32,
                             name='w1')  # shape=(filter_width,in_channels,out_channels)
            w2 = tf.constant(1, shape=(1, 32, 64), dtype=tf.float32,
                             name='w2')  # shape=(filter_width,in_channels,out_channels)
            w3 = tf.constant(1, shape=(1, 64, 128), dtype=tf.float32,
                             name='w3')  # shape=(filter_width,in_channels,out_channels)

            conv1 = tf.nn.conv1d(score_x[np.newaxis, :], w1, 1, 'VALID')
            bn2 = tf.layers.batch_normalization(conv1, training=True)
            conv1_relu = tf.nn.relu(bn2)
            pool1 = tf.layers.max_pooling1d(conv1_relu, pool_size=1, strides=1)

            conv2 = tf.nn.conv1d(pool1, w2, 1, 'VALID')
            bn3 = tf.layers.batch_normalization(conv2, training=True)
            conv2_relu = tf.nn.relu(bn3)
            pool2 = tf.layers.max_pooling1d(conv2_relu, pool_size=1, strides=1)

            # conv3 = tf.nn.conv1d(pool2, w3, 1, 'VALID')
            # bn4 = tf.layers.batch_normalization(conv3, training=True)
            # conv3_relu = tf.nn.relu(bn4)
            # pool3 = tf.layers.max_pooling1d(conv3_relu, pool_size=1, strides=1)
            #
            # pool3 = pool3[0, :, :]
            pool2 = pool2[0, :, :]
            # l1 = tf.compat.v1.layers.dense(
            #     inputs=pool3,
            #     units=64,  # number of hidden units
            #     activation=tf.nn.relu,
            #     kernel_initializer=tf.random_normal_initializer(0., .1),  # weights
            #     bias_initializer=tf.constant_initializer(0.1),  # biases
            #     name='dense1_act'
            # )
            # l2 = tf.compat.v1.layers.dense(
            #     inputs=l1,
            #     units=32,  # number of hidden units
            #     activation=tf.nn.relu,
            #     kernel_initializer=tf.random_normal_initializer(0., .1),  # weights
            #     bias_initializer=tf.constant_initializer(0.1),  # biases
            #     name='dense2_act'
            # )
            l2 = tf.compat.v1.layers.dense(
                inputs=pool2,
                units=32,  # number of hidden units
                activation=tf.nn.relu,
                kernel_initializer=tf.random_normal_initializer(0., .1),  # weights
                bias_initializer=tf.constant_initializer(0.1),  # biases
                name='dense2_act'
            )
            with tf.variable_scope('a'):
                actions = tf.layers.dense(l2, self.a_dim, activation=tf.nn.tanh, kernel_initializer=init_w,
                                          bias_initializer=init_b, name='a', trainable=trainable)
                # scaled_a = tf.multiply(actions, self.action_bound, name='scaled_a')  # Scale output to -action_bound to action_bound
        # return scaled_a
        return actions
    def learn(self, s):   # batch update
        self.sess.run(self.train_op, feed_dict={S: s})

        if self.replacement['name'] == 'soft':
            self.sess.run(self.soft_replace)
        else:
            if self.t_replace_counter % self.replacement['rep_iter_a'] == 0:
                self.sess.run(self.hard_replace)
            self.t_replace_counter += 1

    def choose_action(self, s):
        s = s[np.newaxis, :]    # single state
        actions = self.sess.run(self.a, feed_dict={S: s})[0]  # single action
        var = 3
        # a = np.clip(np.random.normal(actions, var), -2, 2)
        a = np.random.normal(actions, var)


        return a

    def add_grad_to_graph(self, a_grads):
        with tf.variable_scope('policy_grads'):
            # ys = policy;
            # xs = policy's parameters;
            # a_grads = the gradients of the policy to get more Q
            # tf.gradients will calculate dys/dxs with a initial gradients for ys, so this is dq/da * da/dparams
            self.policy_grads = tf.gradients(ys=self.a, xs=self.e_params, grad_ys=a_grads)

        with tf.variable_scope('A_train'):
            opt = tf.train.AdamOptimizer(-self.lr)  # (- learning rate) for ascent policy
            self.train_op = opt.apply_gradients(zip(self.policy_grads, self.e_params))


###############################  Critic  ####################################

class Critic(object):
    def __init__(self, sess, state_dim, action_dim, learning_rate, gamma, replacement, a, a_,memory_size=10000, batch_size=32):
        self.sess = sess
        self.s_dim = state_dim
        self.n_features = state_dim
        self.a_dim = action_dim
        self.lr = learning_rate
        self.gamma = gamma
        self.batch_size = batch_size
        self.replacement = replacement
        self.memory_size = memory_size
        self.memory = np.zeros((self.memory_size, state_dim * 2 + action_dim +1))
        # self.cost_his = []
        # state_dim = 13
        # action_dim = 2
        # all placeholder for tf
        # with tf.name_scope('S'):
        # self.S = tf.placeholder(tf.float32, shape=[None, state_dim], name='state1')
        # # with tf.name_scope('R'):
        # self.R = tf.placeholder(tf.float32, [None, ], name='r')
        # # with tf.name_scope('S_'):
        # self.S_ = tf.placeholder(tf.float32, shape=[None, state_dim], name='state1_')


        with tf.variable_scope('Critic'):
            # Input (s, a), output q
            self.a = tf.stop_gradient(a)    # stop critic update flows to actor
            self.q = self._build_net(S, self.a, 'eval_net', trainable=True)

            # Input (s_, a_), output q_ for q_target
            self.q_ = self._build_net(S_, a_, 'target_net', trainable=False)    # target_q is based on a_ from Actor's target_net

            self.e_params = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope='Critic/eval_net')
            self.t_params = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope='Critic/target_net')

        with tf.variable_scope('target_q'):
            self.target_q = R + self.gamma * self.q_

        with tf.variable_scope('TD_error'):
            self.loss = tf.reduce_mean(tf.squared_difference(self.target_q, self.q))

        with tf.variable_scope('C_train'):
            self.train_op = tf.train.AdamOptimizer(self.lr).minimize(self.loss)

        with tf.variable_scope('a_grad'):
            self.a_grads = tf.gradients(self.q, self.a)[0]   # tensor of gradients of each sample (None, a_dim)

        if self.replacement['name'] == 'hard':
            self.t_replace_counter = 0
            self.hard_replacement = [tf.assign(t, e) for t, e in zip(self.t_params, self.e_params)]
        else:
            self.soft_replacement = [tf.assign(t, (1 - self.replacement['tau']) * t + self.replacement['tau'] * e)
                                     for t, e in zip(self.t_params, self.e_params)]

    def _build_net(self, s, a, scope, trainable):
        with tf.variable_scope(scope):
            init_w = tf.random_normal_initializer(0., 0.1)
            init_b = tf.constant_initializer(0.1)

            with tf.variable_scope('l1'):
                # n_l1 = 30
                # w1_s = tf.get_variable('w1_s', [self.s_dim, n_l1], initializer=init_w, trainable=trainable)
                # w1_a = tf.get_variable('w1_a', [self.a_dim, n_l1], initializer=init_w, trainable=trainable)
                # b1 = tf.get_variable('b1', [1, n_l1], initializer=init_b, trainable=trainable)
                # net = tf.nn.relu(tf.matmul(s, w1_s) + tf.matmul(a, w1_a) + b1)
                out = tf.compat.v1.layers.dense(
                    inputs=s,
                    units=self.n_features,  # number of hidden units
                    activation=tf.nn.relu,
                    kernel_initializer=tf.random_normal_initializer(0., .1),  # weights
                    bias_initializer=tf.constant_initializer(0.1),  # biases
                    name='o1_cr'
                )
                s_up_dim = tf.reshape(out, [-1, self.n_features, 1])

                u = tf.compat.v1.layers.dense(
                    inputs=s_up_dim,
                    units=1,  # number of hidden units
                    activation=tf.nn.tanh,
                    kernel_initializer=tf.random_normal_initializer(0., .1),  # weights
                    bias_initializer=tf.constant_initializer(0.1),  # biases
                    name='u_cr'
                )

                att = tf.compat.v1.layers.dense(
                    inputs=u,
                    units=1,  # number of hidden units
                    # activation=tf.nn.softmax,
                    kernel_initializer=tf.random_normal_initializer(0., .1),  # weights
                    bias_initializer=tf.constant_initializer(0.1),  # biases
                    name='att_cr'
                )
                att = tf.reshape(att, [-1, self.n_features])
                att_softmax = tf.nn.softmax(att)
                att_softmax = tf.reshape(att_softmax, [-1, self.n_features, 1])
                self.att = att_softmax
                score_x = s_up_dim * att_softmax

                score_x = tf.reshape(score_x, [-1, self.n_features])

                w1 = tf.constant(1, shape=(1, self.n_features, 32), dtype=tf.float32,
                                 name='lc_w1')  # shape=(filter_width,in_channels,out_channels)
                w2 = tf.constant(1, shape=(1, 32, 64), dtype=tf.float32,
                                 name='lc_w2')  # shape=(filter_width,in_channels,out_channels)
                w3 = tf.constant(1, shape=(1, 64, 128), dtype=tf.float32,
                                 name='lc_w2')  # shape=(filter_width,in_channels,out_channels)

                conv1 = tf.nn.conv1d(score_x[np.newaxis, :], w1, 1, 'VALID')
                bn2 = tf.layers.batch_normalization(conv1, training=True)
                conv1_relu = tf.nn.relu(bn2)
                pool1 = tf.layers.max_pooling1d(conv1_relu, pool_size=1, strides=1)

                conv2 = tf.nn.conv1d(pool1, w2, 1, 'VALID')
                bn3 = tf.layers.batch_normalization(conv2, training=True)
                conv2_relu = tf.nn.relu(bn3)
                pool2 = tf.layers.max_pooling1d(conv2_relu, pool_size=1, strides=1)

                # conv3 = tf.nn.conv1d(pool2, w3, 1, 'VALID')
                # bn4 = tf.layers.batch_normalization(conv3, training=True)
                # conv3_relu = tf.nn.relu(bn4)
                # pool3 = tf.layers.max_pooling1d(conv3_relu, pool_size=1, strides=1)
                #
                # pool3 = pool3[0, :, :]
                pool2 = pool2[0, :, :]
                #
                # l1 = tf.compat.v1.layers.dense(
                #     inputs=pool3,
                #     units=64,  # number of hidden units
                #     activation=tf.nn.relu,
                #     kernel_initializer=tf.random_normal_initializer(0., .1),  # weights
                #     bias_initializer=tf.constant_initializer(0.1),  # biases
                #     name='l1'
                # )
                # l2 = tf.compat.v1.layers.dense(
                #     inputs=l1,
                #     units=32,  # number of hidden units
                #     activation=tf.nn.relu,
                #     kernel_initializer=tf.random_normal_initializer(0., .1),  # weights
                #     bias_initializer=tf.constant_initializer(0.1),  # biases
                #     name='l2'
                # )
                l2 = tf.compat.v1.layers.dense(
                    inputs=pool2,
                    units=32,  # number of hidden units
                    activation=tf.nn.relu,
                    kernel_initializer=tf.random_normal_initializer(0., .1),  # weights
                    bias_initializer=tf.constant_initializer(0.1),  # biases
                    name='l2'
                )
            with tf.variable_scope('q'):
                q = tf.layers.dense(l2, 1, kernel_initializer=init_w, bias_initializer=init_b, trainable=trainable)   # Q(s,a)
        return q
    def store_transition(self, s, a, r, s_):
        if not hasattr(self, 'memory_counter'):
            self.memory_counter = 0

        transition = np.hstack((s, a, r, s_))

        # replace the old memory with new memory
        index = self.memory_counter % self.memory_size
        self.memory[index, :] = transition

        self.memory_counter += 1
    def learn(self, s, a, r, s_):
        self.sess.run(self.train_op, feed_dict={S: s, self.a: a, R: r, S_: s_})
        if self.replacement['name'] == 'soft':
            self.sess.run(self.soft_replacement)
        else:
            if self.t_replace_counter % self.replacement['rep_iter_c'] == 0:
                self.sess.run(self.hard_replacement)
            self.t_replace_counter += 1
        # self.cost_his.append(self.loss)

