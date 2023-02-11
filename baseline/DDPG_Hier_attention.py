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
    def __init__(self, sess, state_dim, action_dim, learning_rate, replacement): # action_bound,
        self.sess = sess
        self.a_dim = action_dim
        # self.action_bound = action_bound
        self.lr = learning_rate
        self.replacement = replacement
        self.t_replace_counter = 0
        self.n_features = state_dim
        # with tf.name_scope('high_S'):
    #     self.S = tf.placeholder(tf.float32, shape=[None, state_dim], name='s')
    # # with tf.name_scope('high_R'):
    #     self.R = tf.placeholder(tf.float32, [None, ], name='r')
    # # with tf.name_scope('high_S_'):
    #     self.S_ = tf.placeholder(tf.float32, shape=[None, state_dim], name='s_')

        with tf.variable_scope('high_Actor'):
            # input s, output a
            self.a = self._build_net(high_S, scope='high_eval_net', trainable=True)

            # input s_, output a, get a_ for critic
            self.a_ = self._build_net(high_S_, scope='high_target_net', trainable=False)

        self.e_params = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope='high_Actor/high_eval_net')
        self.t_params = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope='high_Actor/high_target_net')

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

            pool2 = pool2[0, :, :]

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

            with tf.variable_scope('high_a'):
                actions = tf.layers.dense(fusion2, self.a_dim, activation=tf.nn.tanh, kernel_initializer=init_w,
                                          bias_initializer=init_b, name='a', trainable=trainable)
                # scaled_a = tf.multiply(actions, self.action_bound, name='scaled_a')  # Scale output to -action_bound to action_bound
        # return scaled_a
        return actions
    def learn(self, s):   # batch update
        self.sess.run(self.train_op, feed_dict={high_S: s})

        if self.replacement['name'] == 'soft':
            self.sess.run(self.soft_replace)
        else:
            if self.t_replace_counter % self.replacement['rep_iter_a'] == 0:
                self.sess.run(self.hard_replace)
            self.t_replace_counter += 1

    def choose_action(self, s):
        s = s[np.newaxis, :]    # single state
        actions = self.sess.run(self.a, feed_dict={high_S: s})[0]  # single action
        var = 3
        # a = np.clip(np.random.normal(actions, var), -2, 2)
        a = np.random.normal(actions, var)


        return a

    def add_grad_to_graph(self, a_grads):
        with tf.variable_scope('high_policy_grads'):
            # ys = policy;
            # xs = policy's parameters;
            # a_grads = the gradients of the policy to get more Q
            # tf.gradients will calculate dys/dxs with a initial gradients for ys, so this is dq/da * da/dparams
            self.policy_grads = tf.gradients(ys=self.a, xs=self.e_params, grad_ys=a_grads)

        with tf.variable_scope('high_A_train'):
            opt = tf.train.AdamOptimizer(-self.lr)  # (- learning rate) for ascent policy
            self.train_op = opt.apply_gradients(zip(self.policy_grads, self.e_params))


###############################  Critic  ####################################

class High_Level_Critic(object):
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
        # with tf.name_scope('high_S'):
        # self.S = tf.placeholder(tf.float32, shape=[None, state_dim], name='state')
        # # with tf.name_scope('high_R'):
        # self.R = tf.placeholder(tf.float32, [None, ], name='r')
        # # with tf.name_scope('high_S_'):
        # self.S_ = tf.placeholder(tf.float32, shape=[None, state_dim], name='state_')


        with tf.variable_scope('high_Critic'):
            # Input (s, a), output q
            self.a = tf.stop_gradient(a)    # stop critic update flows to actor
            self.q = self._build_net(high_S, self.a, 'high_eval_net', trainable=True)

            # Input (s_, a_), output q_ for q_target
            self.q_ = self._build_net(high_S_, a_, 'high_target_net', trainable=False)    # target_q is based on a_ from Actor's target_net

            self.e_params = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope='high_Critic/high_eval_net')
            self.t_params = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope='high_Critic/high_target_net')

        with tf.variable_scope('high_target_q'):
            self.target_q = high_R + self.gamma * self.q_

        with tf.variable_scope('high_TD_error'):
            self.loss = tf.reduce_mean(tf.squared_difference(self.target_q, self.q))

        with tf.variable_scope('high_C_train'):
            self.train_op = tf.train.AdamOptimizer(self.lr).minimize(self.loss)

        with tf.variable_scope('high_a_grad'):
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
                # w1_s = tf.get_variable('high_w1_s', [self.s_dim, n_l1], initializer=init_w, trainable=trainable)
                # w1_a = tf.get_variable('high_w1_a', [self.a_dim, n_l1], initializer=init_w, trainable=trainable)
                # b1 = tf.get_variable('high_b1', [1, n_l1], initializer=init_b, trainable=trainable)
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

            with tf.variable_scope('high_q'):
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
        self.sess.run(self.train_op, feed_dict={high_S: s, self.a: a, high_R: r, high_S_: s_})
        if self.replacement['name'] == 'soft':
            self.sess.run(self.soft_replacement)
        else:
            if self.t_replace_counter % self.replacement['rep_iter_c'] == 0:
                self.sess.run(self.hard_replacement)
            self.t_replace_counter += 1
        # self.cost_his.append(self.loss)




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

