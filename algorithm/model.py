import numpy as np
import tensorflow as tf
from d2l import tensorflow as d2l

# from stable_baselines.common.tf_layers import conv, linear, conv_to_fc
# from baselines.a2c.utils import ortho_init

# 2个critic

GAMMA = 0.9
np.random.seed(2)
tf.compat.v1.disable_eager_execution()
tf.compat.v1.disable_v2_behavior()

batch_size, num_steps = 256, 35
train_iter, vocab = d2l.load_data_time_machine(batch_size, num_steps)
#@save

def get_params(vocab_size, num_hiddens):
    num_inputs = num_outputs = vocab_size

    def normal(shape):
        return tf.random.normal(shape=shape,stddev=0.01,mean=0,dtype=tf.float32)

    def three():
        return (tf.Variable(normal((num_inputs, num_hiddens)), dtype=tf.float32),
                tf.Variable(normal((num_hiddens, num_hiddens)), dtype=tf.float32),
                tf.Variable(tf.zeros(num_hiddens), dtype=tf.float32))

    W_xz, W_hz, b_z = three()  # 更新门参数
    W_xr, W_hr, b_r = three()  # 重置门参数
    W_xh, W_hh, b_h = three()  # 候选隐状态参数
    # 输出层参数
    W_hq = tf.Variable(normal((num_hiddens, num_outputs)), dtype=tf.float32)
    b_q = tf.Variable(tf.zeros(num_outputs), dtype=tf.float32)
    params = [W_xz, W_hz, b_z, W_xr, W_hr, b_r, W_xh, W_hh, b_h, W_hq, b_q]
    return params
def init_gru_state(batch_size, num_hiddens):
    return (tf.zeros((batch_size, num_hiddens)), )
def gru(inputs, state, params):
    W_xz, W_hz, b_z, W_xr, W_hr, b_r, W_xh, W_hh, b_h, W_hq, b_q = params
    H, = state
    outputs = []
    for X in inputs:
        X = tf.reshape(X,[-1,W_xh.shape[0]])
        Z = tf.sigmoid(tf.matmul(X, W_xz) + tf.matmul(H, W_hz) + b_z)
        R = tf.sigmoid(tf.matmul(X, W_xr) + tf.matmul(H, W_hr) + b_r)
        H_tilda = tf.tanh(tf.matmul(X, W_xh) + tf.matmul(R * H, W_hh) + b_h)
        H = Z * H + (1 - Z) * H_tilda
        Y = tf.matmul(H, W_hq) + b_q
        outputs.append(Y)
    return tf.concat(outputs, axis=0), (H,)



# 通道注意力
class MultiHeadAttention(tf.keras.layers.Layer):
    """多头注意力"""
    def __init__(self, key_size, query_size, value_size, num_hiddens,
                 num_heads, dropout, bias=False, **kwargs):
        super().__init__(**kwargs)
        self.num_heads = num_heads
        self.attention = d2l.DotProductAttention(dropout)
        self.W_q = tf.keras.layers.Dense(num_hiddens, use_bias=bias)
        self.W_k = tf.keras.layers.Dense(num_hiddens, use_bias=bias)
        self.W_v = tf.keras.layers.Dense(num_hiddens, use_bias=bias)
        self.W_o = tf.keras.layers.Dense(num_hiddens, use_bias=bias)

    def call(self, queries, keys, values, valid_lens, **kwargs):
        # queries，keys，values的形状:
        # (batch_size，查询或者“键－值”对的个数，num_hiddens)
        # valid_lens　的形状:
        # (batch_size，)或(batch_size，查询的个数)
        # 经过变换后，输出的queries，keys，values　的形状:
        # (batch_size*num_heads，查询或者“键－值”对的个数，
        # num_hiddens/num_heads)
        queries = transpose_qkv(self.W_q(queries), self.num_heads)
        keys = transpose_qkv(self.W_k(keys), self.num_heads)
        values = transpose_qkv(self.W_v(values), self.num_heads)

        if valid_lens is not None:
            # 在轴0，将第一项（标量或者矢量）复制num_heads次，
            # 然后如此复制第二项，然后诸如此类。
            # valid_lens = tf.repeat(valid_lens, repeats=self.num_heads, axis=0)
            valid_lens = tf.tile(valid_lens, [self.num_heads])

        # output的形状:(batch_size*num_heads，查询的个数，
        # num_hiddens/num_heads)
        output = self.attention(queries, keys, values, valid_lens, **kwargs)

        # output_concat的形状:(batch_size，查询的个数，num_hiddens)
        output_concat = transpose_output(output, self.num_heads)
        return self.W_o(output_concat)

# @save
def transpose_qkv(X, num_heads):
    """为了多注意力头的并行计算而变换形状"""
    # 输入X的形状:(batch_size，查询或者“键－值”对的个数=53，num_hiddens=32)
    # 输出X的形状:(batch_size，查询或者“键－值”对的个数，num_heads，
    # num_hiddens/num_heads)
    X = tf.reshape(X, shape=(batch_size, X.shape[1], num_heads, X.shape[2] // num_heads))
    # X = tf.reshape(X, shape=(batch_size, X.shape[1], num_heads, -1))

    # 输出X的形状:(batch_size，num_heads，查询或者“键－值”对的个数,
    # num_hiddens/num_heads)
    X = tf.transpose(X, perm=(0, 2, 1, 3))

    # 最终输出的形状:(batch_size*num_heads,查询或者“键－值”对的个数,
    # num_hiddens/num_heads)
    return tf.reshape(X, shape=(-1, X.shape[2], X.shape[3]))
    # return tf.reshape(X, shape=(-1, X.shape[2], X.shape[3]))

# @save
def transpose_output(X, num_heads):
    """逆转transpose_qkv函数的操作"""
    X = tf.reshape(X, shape=(-1, num_heads, X.shape[1], X.shape[2]))
    X = tf.transpose(X, perm=(0, 2, 1, 3))
    return tf.reshape(X, shape=(X.shape[0], X.shape[1], -1))

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
            num_hiddens, num_heads = 32, 4

            gru_cell = tf.keras.layers.GRUCell(num_hiddens,
                                               kernel_initializer='glorot_uniform')
            gru_layer = tf.keras.layers.RNN(gru_cell, time_major=True,
                                            return_sequences=True, return_state=True)

            # gru_output = d2l.RNNModel(gru_layer, vocab_size=len(score_x))
            rnn_input = self.s[:, -4:]
            outputs, h_ = gru_layer(rnn_input[np.newaxis,:])
            input_embedding = tf.concat([self.s[:,:n_features-4],h_],axis=1)


            attention = MultiHeadAttention(num_hiddens, num_hiddens, num_hiddens,
                                           num_hiddens, num_heads, 0.5)

            # batch_size, num_queries = 256, 4
            # num_kvpairs = 6
            # valid_lens = tf.constant([7, 3])
            valid_lens = tf.constant([1] * batch_size)  # [3,2]
            # X = tf.ones((batch_size, num_queries, num_hiddens))
            # Y = tf.ones((batch_size, num_kvpairs, num_hiddens))
            # X = np.dstack([self.s]* num_hiddens)
            # Y = np.dstack([self.s]* num_hiddens)
            opti_s = tf.expand_dims(input_embedding, 2)
            result = tf.concat([opti_s, opti_s], 2)
            for times in range(num_hiddens - 2):
                result = tf.concat([result, opti_s], 2)
            X = result
            Y = result

            # self.s[:, :, np.newaxis], self.s[:, :, np.newaxis], self.s[:, :, np.newaxis]
            score_x = attention(X, Y, Y, valid_lens, training=True)

            score_x = tf.reshape(score_x, [batch_size,num_hiddens * (num_hiddens + n_features-4)])

            s_l = tf.compat.v1.layers.dense(
                inputs=score_x,
                units=512,  # number of hidden units
                activation=tf.nn.relu,
                kernel_initializer=tf.random_normal_initializer(0., .1),  # weights
                bias_initializer=tf.constant_initializer(0.1),  # biases
                name='h_att_dense1'
            )

            w1 = tf.constant(1, shape = (1,512, 256), dtype=tf.float32,
                             name='h_w1')  # shape=(filter_width,in_channels,out_channels)
            w2 = tf.constant(1, shape=(1, 256, 128), dtype=tf.float32,
                             name='h_w2')  # shape=(filter_width,in_channels,out_channels)
            w3 = tf.constant(1, shape=(1, 128, 64), dtype=tf.float32,
                             name='h_w3')  # shape=(filter_width,in_channels,out_channels)

            conv1 = tf.nn.conv1d(s_l[np.newaxis, :], w1, 1, 'VALID')
            bn2 = tf.layers.batch_normalization(conv1, training=True)
            conv1_relu = tf.nn.relu(bn2)
            pool1 = tf.layers.max_pooling1d(conv1_relu, pool_size=1, strides=1)

            conv2 = tf.nn.conv1d(pool1, w2, 1, 'VALID')
            bn3 = tf.layers.batch_normalization(conv2, training=True)
            conv2_relu = tf.nn.relu(bn3)
            pool2 = tf.layers.max_pooling1d(conv2_relu, pool_size=1, strides=1)

            conv3 = tf.nn.conv1d(pool2, w3, 1, 'VALID')
            bn4 = tf.layers.batch_normalization(conv3, training=True)
            conv4_relu = tf.nn.relu(bn4)
            pool3 = tf.layers.max_pooling1d(conv4_relu, pool_size=1, strides=1)
            pool3 = pool3[0, :, :]

            # pool2 = pool2[0, :, :]

            fusion1 = tf.compat.v1.layers.dense(
                inputs=pool3,
                units=64,  # number of hidden units
                activation=tf.nn.relu,
                kernel_initializer=tf.random_normal_initializer(0., .1),  # weights
                bias_initializer=tf.constant_initializer(0.1),  # biases
                name='dense1'
            )
            fusion2 = tf.compat.v1.layers.dense(
                inputs=fusion1,
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
        input = []
        for repeat_id in range(self.batch_size):
            input.append(s)

        prob_weights = self.sess.run(self.all_act_prob, feed_dict={self.s: np.array(input)})
        # prob_weights = self.sess.run(self.all_act_prob, feed_dict={self.s: s[np.newaxis, :]})

        # print('high_level_actor,初始pro:',prob_weights)
        # prob_weights = tf.clip_by_value(prob_weights, 1e-10, 1.0)
        # print('high_level_actor,后来pro:', prob_weights)
        action = np.random.choice(range(prob_weights.shape[1]),
                                  p=prob_weights[0].ravel())  # select action w.r.t the actions prob
        # action = np.random.choice(range(prob_weights.shape[1]),
        #                           p=prob_weights.ravel())  # select action w.r.t the actions prob
        print('high_level_actor,prob:', prob_weights[0], ',action:', action)
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

        self.s = tf.compat.v1.placeholder(tf.float32, [batch_size, n_features], "state")
        self.a = tf.compat.v1.placeholder(tf.int32, [batch_size, ], "act")
        self.td_error = tf.compat.v1.placeholder(tf.float32, None, "td_error")  # TD_error

        self.cost_his = []

        with tf.compat.v1.variable_scope('Actor'):
            # bn1 = tf.layers.batch_normalization(self.s, training=True)

            num_hiddens, num_heads = 32, 4
            attention = MultiHeadAttention(num_hiddens, num_hiddens, num_hiddens,
                                           num_hiddens, num_heads, 0.5)

            # batch_size, num_queries = 256, 4
            # num_kvpairs = 6
            # valid_lens = tf.constant([7, 3])
            valid_lens = tf.constant([1] * batch_size)  # [3,2]
            # X = tf.ones((batch_size, num_queries, num_hiddens))
            # Y = tf.ones((batch_size, num_kvpairs, num_hiddens))
            # X = np.dstack([self.s]* num_hiddens)
            # Y = np.dstack([self.s]* num_hiddens)
            opti_s = tf.expand_dims(self.s, 2)
            result = tf.concat([opti_s, opti_s], 2)
            for times in range(num_hiddens - 2):
                result = tf.concat([result, opti_s], 2)
            X = result
            Y = result

            # self.s[:, :, np.newaxis], self.s[:, :, np.newaxis], self.s[:, :, np.newaxis]
            score_x = attention(X, Y, Y, valid_lens, training=True)

            score_x = tf.reshape(score_x, [batch_size, num_hiddens * n_features])

            s_l = tf.compat.v1.layers.dense(
                inputs=score_x,
                units=512,  # number of hidden units
                activation=tf.nn.relu,
                kernel_initializer=tf.random_normal_initializer(0., .1),  # weights
                bias_initializer=tf.constant_initializer(0.1),  # biases
                name='a_dense1'
            )

            w1 = tf.constant(1, shape=(1, 512, 256), dtype=tf.float32,
                             name='a_w1')  # shape=(filter_width,in_channels,out_channels)
            w2 = tf.constant(1, shape=(1, 256, 128), dtype=tf.float32,
                             name='a_w2')  # shape=(filter_width,in_channels,out_channels)
            w3 = tf.constant(1, shape=(1, 128, 64), dtype=tf.float32,
                             name='a_w3')  # shape=(filter_width,in_channels,out_channels)

            conv1 = tf.nn.conv1d(s_l[np.newaxis, :], w1, 1, 'VALID')
            bn2 = tf.layers.batch_normalization(conv1, training=True)
            conv1_relu = tf.nn.relu(bn2)
            pool1 = tf.layers.max_pooling1d(conv1_relu, pool_size=1, strides=1)

            conv2 = tf.nn.conv1d(pool1, w2, 1, 'VALID')
            bn3 = tf.layers.batch_normalization(conv2, training=True)
            conv2_relu = tf.nn.relu(bn3)
            pool2 = tf.layers.max_pooling1d(conv2_relu, pool_size=1, strides=1)

            conv3 = tf.nn.conv1d(pool2, w3, 1, 'VALID')
            bn4 = tf.layers.batch_normalization(conv3, training=True)
            conv4_relu = tf.nn.relu(bn4)
            pool3 = tf.layers.max_pooling1d(conv4_relu, pool_size=1, strides=1)
            pool3 = pool3[0, :, :]

            # pool2 = pool2[0, :, :]
            l1 = tf.compat.v1.layers.dense(
                inputs=pool3,
                units=64,  # number of hidden units
                activation=tf.nn.relu,
                kernel_initializer=tf.random_normal_initializer(0., .1),  # weights
                bias_initializer=tf.constant_initializer(0.1),  # biases
                name='dense1_act'
            )
            l2 = tf.compat.v1.layers.dense(
                inputs=l1,
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
        input = []
        for repeat_id in range(self.batch_size):
            input.append(s)

        # prob_weights = self.sess.run(self.all_act_prob, feed_dict={self.s: s[np.newaxis, :]})
        prob_weights = self.sess.run(self.all_act_prob, feed_dict={self.s: np.array(input)})

        # print('low_level_actor,初始pro:',prob_weights)
        # prob_weights = tf.clip_by_value(prob_weights, 1e-10, 1.0)
        # print('low_level_actor,后来pro:', prob_weights)
        print(prob_weights)
        action_list = []
        # for action_i in range(len(s[np.newaxis, :])):

        action = np.random.choice(range(prob_weights.shape[1]),
                                  p=prob_weights[0].ravel())  # select action w.r.t the actions prob
        # action = np.random.choice(range(prob_weights.shape[1]),
        #                           p=prob_weights.ravel())  # select action w.r.t the actions prob

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
        self.s = tf.compat.v1.placeholder(tf.float32, [batch_size, n_features], "state")
        self.v_ = tf.compat.v1.placeholder(tf.float32, [batch_size, 1], "v_next")
        self.r = tf.compat.v1.placeholder(tf.float32, None, 'r')
        self.memory_size = memory_size
        self.memory = np.zeros((self.memory_size, n_features * 2 + 2))
        self.lr = lr
        self.gamma = GAMMA

        self.cost_his = []

        with tf.compat.v1.variable_scope('HL_Critic'):
            num_hiddens, num_heads = 32, 4

            gru_cell = tf.keras.layers.GRUCell(num_hiddens,
                                               kernel_initializer='glorot_uniform')
            gru_layer = tf.keras.layers.RNN(gru_cell, time_major=True,
                                            return_sequences=True, return_state=True)

            # gru_output = d2l.RNNModel(gru_layer, vocab_size=len(score_x))
            rnn_input = self.s[:, -4:]
            outputs, h_ = gru_layer(rnn_input[np.newaxis, :])
            input_embedding = tf.concat([self.s[:, :n_features - 4], h_], axis=1)

            attention = MultiHeadAttention(num_hiddens, num_hiddens, num_hiddens,
                                           num_hiddens, num_heads, 0.5)

            # batch_size, num_queries = 256, 4
            # num_kvpairs = 6
            # valid_lens = tf.constant([7, 3])
            valid_lens = tf.constant([1] * batch_size)  # [3,2]
            # X = tf.ones((batch_size, num_queries, num_hiddens))
            # Y = tf.ones((batch_size, num_kvpairs, num_hiddens))
            # X = np.dstack([self.s]* num_hiddens)
            # Y = np.dstack([self.s]* num_hiddens)
            opti_s = tf.expand_dims(input_embedding, 2)
            result = tf.concat([opti_s, opti_s], 2)
            for times in range(num_hiddens - 2):
                result = tf.concat([result, opti_s], 2)
            X = result
            Y = result

            # self.s[:, :, np.newaxis], self.s[:, :, np.newaxis], self.s[:, :, np.newaxis]
            score_x = attention(X, Y, Y, valid_lens, training=True)

            score_x = tf.reshape(score_x, [batch_size, num_hiddens * (num_hiddens + n_features - 4)])

            s_l = tf.compat.v1.layers.dense(
                inputs=score_x,
                units=512,  # number of hidden units
                activation=tf.nn.relu,
                kernel_initializer=tf.random_normal_initializer(0., .1),  # weights
                bias_initializer=tf.constant_initializer(0.1),  # biases
                name='hc_dense1'
            )

            w1 = tf.constant(1, shape=(1, 512, 256), dtype=tf.float32,
                             name='hc_w1')  # shape=(filter_width,in_channels,out_channels)
            w2 = tf.constant(1, shape=(1, 256, 128), dtype=tf.float32,
                             name='hc_w2')  # shape=(filter_width,in_channels,out_channels)
            w3 = tf.constant(1, shape=(1, 128, 64), dtype=tf.float32,
                             name='hc_w3')  # shape=(filter_width,in_channels,out_channels)

            conv1 = tf.nn.conv1d(s_l[np.newaxis, :], w1, 1, 'VALID')
            bn2 = tf.layers.batch_normalization(conv1, training=True)
            conv1_relu = tf.nn.relu(bn2)
            pool1 = tf.layers.max_pooling1d(conv1_relu, pool_size=1, strides=1)

            conv2 = tf.nn.conv1d(pool1, w2, 1, 'VALID')
            bn3 = tf.layers.batch_normalization(conv2, training=True)
            conv2_relu = tf.nn.relu(bn3)
            pool2 = tf.layers.max_pooling1d(conv2_relu, pool_size=1, strides=1)

            conv3 = tf.nn.conv1d(pool2, w3, 1, 'VALID')
            bn4 = tf.layers.batch_normalization(conv3, training=True)
            conv4_relu = tf.nn.relu(bn4)
            pool3 = tf.layers.max_pooling1d(conv4_relu, pool_size=1, strides=1)
            pool3 = pool3[0, :, :]

            # pool2 = pool2[0, :, :]

            l1= tf.compat.v1.layers.dense(
                inputs=pool3,
                units=64,  # number of hidden units
                activation=tf.nn.relu,
                kernel_initializer=tf.random_normal_initializer(0., .1),  # weights
                bias_initializer=tf.constant_initializer(0.1),  # biases
                name='dense1_cr'
            )
            l2 = tf.compat.v1.layers.dense(
                inputs=l1,
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


class Critic(object):
    def __init__(self, sess, n_features, lr=0.01, memory_size=100000, batch_size=256):
        self.sess = sess
        self.n_features = n_features
        self.batch_size = batch_size
        self.lr = lr
        self.s = tf.compat.v1.placeholder(tf.float32, [batch_size, n_features], "state")
        self.v_ = tf.compat.v1.placeholder(tf.float32, [batch_size, 1], "v_next")
        self.r = tf.compat.v1.placeholder(tf.float32, None, 'r')
        self.memory_size = memory_size
        self.memory = np.zeros((self.memory_size, n_features * 2 + 2))
        self.gamma = GAMMA
        self.cost_his = []

        with tf.compat.v1.variable_scope('Critic'):
            # bn1 = tf.layers.batch_normalization(self.s, training=True)
            # num_hiddens, num_heads = 32, 5
            # attention = MultiHeadAttention(num_hiddens, num_hiddens, num_hiddens,
            #                                num_hiddens, num_heads, 0.5)
            #
            # batch_size, num_queries = 256, 4
            # num_kvpairs, valid_lens = 6, tf.constant([3, 2])
            # X = tf.ones((batch_size, num_queries, num_hiddens))
            # Y = tf.ones((batch_size, num_kvpairs, num_hiddens))


            num_hiddens, num_heads = 32, 4
            attention = MultiHeadAttention(num_hiddens, num_hiddens, num_hiddens,
                                           num_hiddens, num_heads, 0.5)

            # batch_size, num_queries = 256, 4
            # num_kvpairs = 6
            # valid_lens = tf.constant([7, 3])
            valid_lens = tf.constant([1] * batch_size)  # [3,2]
            # X = tf.ones((batch_size, num_queries, num_hiddens))
            # Y = tf.ones((batch_size, num_kvpairs, num_hiddens))
            # X = np.dstack([self.s]* num_hiddens)
            # Y = np.dstack([self.s]* num_hiddens)
            opti_s = tf.expand_dims(self.s, 2)
            result = tf.concat([opti_s, opti_s], 2)
            for times in range(num_hiddens - 2):
                result = tf.concat([result, opti_s], 2)
            X = result
            Y = result

            # self.s[:, :, np.newaxis], self.s[:, :, np.newaxis], self.s[:, :, np.newaxis]
            score_x = attention(X, Y, Y, valid_lens, training=True)

            score_x = tf.reshape(score_x, [batch_size, num_hiddens * n_features])
            s_l = tf.compat.v1.layers.dense(
                inputs=score_x,
                units=512,  # number of hidden units
                activation=tf.nn.relu,
                kernel_initializer=tf.random_normal_initializer(0., .1),  # weights
                bias_initializer=tf.constant_initializer(0.1),  # biases
                name='c_dense1'
            )

            w1 = tf.constant(1, shape=(1, 512, 256), dtype=tf.float32,
                             name='c_w1')  # shape=(filter_width,in_channels,out_channels)
            w2 = tf.constant(1, shape=(1, 256, 128), dtype=tf.float32,
                             name='c_w2')  # shape=(filter_width,in_channels,out_channels)
            w3 = tf.constant(1, shape=(1, 128, 64), dtype=tf.float32,
                             name='c_w3')  # shape=(filter_width,in_channels,out_channels)

            conv1 = tf.nn.conv1d(s_l[np.newaxis, :], w1, 1, 'VALID')
            bn2 = tf.layers.batch_normalization(conv1, training=True)
            conv1_relu = tf.nn.relu(bn2)
            pool1 = tf.layers.max_pooling1d(conv1_relu, pool_size=1, strides=1)

            conv2 = tf.nn.conv1d(pool1, w2, 1, 'VALID')
            bn3 = tf.layers.batch_normalization(conv2, training=True)
            conv2_relu = tf.nn.relu(bn3)
            pool2 = tf.layers.max_pooling1d(conv2_relu, pool_size=1, strides=1)

            conv3 = tf.nn.conv1d(pool2, w3, 1, 'VALID')
            bn4 = tf.layers.batch_normalization(conv3, training=True)
            conv4_relu = tf.nn.relu(bn4)
            pool3 = tf.layers.max_pooling1d(conv4_relu, pool_size=1, strides=1)
            pool3 = pool3[0, :, :]

            # pool2 = pool2[0, :, :]
            l1 = tf.compat.v1.layers.dense(
                inputs=pool3,
                units=64,  # number of hidden units
                activation=tf.nn.relu,
                kernel_initializer=tf.random_normal_initializer(0., .1),  # weights
                bias_initializer=tf.constant_initializer(0.1),  # biases
                name='l1'
            )
            l2 = tf.compat.v1.layers.dense(
                inputs=l1,
                units=32,  # number of hidden units
                activation=tf.nn.relu,
                kernel_initializer=tf.random_normal_initializer(0., .1),  # weights
                bias_initializer=tf.constant_initializer(0.1),  # biases
                name='l2'
            )

            self.v = tf.compat.v1.layers.dense(
                inputs=l2,
                units=1,  # output units
                activation=tf.nn.relu,
                kernel_initializer=tf.random_normal_initializer(0., .1),  # weights
                bias_initializer=tf.constant_initializer(0.1),  # biases
                name='V'
            )

        with tf.compat.v1.variable_scope('squared_TD_error'):
            self.td_error = tf.reduce_mean(self.r + self.gamma * self.v_ - self.v)
            self.loss = 0.5 * tf.reduce_sum(tf.square(self.td_error))  # TD_error = (r+gamma*V_next) - V_eval

        with tf.compat.v1.variable_scope('train'):
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
