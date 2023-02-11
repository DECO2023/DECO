import numpy as np
import tensorflow as tf

GAMMA = 0.9
np.random.seed(2)
tf.compat.v1.disable_eager_execution()
tf.compat.v1.disable_v2_behavior()
# with tf.device('/device:GPU:0'):
class Actor(object):
    def __init__(self, sess, n_features, n_actions, lr=0.001, batch_size = 32):
        self.sess = sess
        self.batch_size = batch_size
        self.n_features = n_features
        self.n_actions = n_actions
        self.lr = lr

        self.s = tf.compat.v1.placeholder(tf.float32, [None, self.n_features], "state")
        self.a = tf.compat.v1.placeholder(tf.int32, [None, ], "act")
        self.td_error = tf.compat.v1.placeholder(tf.float32, None, "td_error")  # TD_error

        self.cost_his = []

        with tf.compat.v1.variable_scope('Actor'):
            l1 = tf.compat.v1.layers.dense(
                inputs=self.s,
                units=32,    # number of hidden units
                activation=tf.nn.relu,
                kernel_initializer=tf.random_normal_initializer(0., .1),    # weights
                bias_initializer=tf.constant_initializer(0.1),  # biases
                name='l1_a'
            )
            # l2 = tf.compat.v1.layers.dense(
            #     inputs=l1,
            #     units=64,    # number of hidden units
            #     activation=tf.nn.relu,
            #     kernel_initializer=tf.random_normal_initializer(0., .1),    # weights
            #     bias_initializer=tf.constant_initializer(0.1),  # biases
            #     name='l2_a'
            # )
            # l3 = tf.compat.v1.layers.dense(
            #     inputs=l2,
            #     units=32,    # number of hidden units
            #     activation=tf.nn.relu,
            #     kernel_initializer=tf.random_normal_initializer(0., .1),    # weights
            #     bias_initializer=tf.constant_initializer(0.1),  # biases
            #     name='l3_a'
            # )

            self.acts_prob = tf.compat.v1.layers.dense(
                inputs=l1,
                units=n_actions,    # output units
                activation=tf.nn.softmax,   # get action probabilities
                kernel_initializer=tf.random_normal_initializer(0., .1),  # weights
                bias_initializer=tf.constant_initializer(0.1),  # biases
                name='acts_prob'
            )
            self.all_act_prob = tf.nn.softmax(self.acts_prob,
                                                        name='act_prob')  # use softmax to convert to probability

        with tf.compat.v1.variable_scope('exp_v'):
            log_prob = - tf.compat.v1.nn.sparse_softmax_cross_entropy_with_logits(logits=self.acts_prob, labels=self.a)
            # log_prob = tf.compat.v1.log(self.acts_prob[0, self.a])
            # softmaxprob = tf.compat.v1.nn.softmax(tf.compat.v1.log(self.acts_prob + 1e-8))
            # logsoftmaxprob = tf.compat.v1.nn.log_softmax(softmaxprob)
            # log_prob = - logsoftmaxprob * self.a

            self.exp_v = tf.reduce_mean(tf.reduce_sum(log_prob * self.td_error))
            # self.exp_v = tf.reduce_mean(tf.reduce_sum(log_prob * self.td_error, axis=1))
            # advantage (TD_error) guided loss
            # advantage (TD_error) guided loss
            # self.logits = logits = fc(l3, "logits", self.action_dim,
            #                           act=tf.nn.relu) + 1  # avoid valid_logits are all zeros
            # self.valid_logits = logits * self.neighbor_mask

            # self.softmaxprob = tf.nn.softmax(tf.compat.v1.log(self.valid_logits + 1e-8))
            # self.logsoftmaxprob = tf.nn.log_softmax(self.softmaxprob)
            # self.neglogprob = - self.logsoftmaxprob * self.ACTION
            # self.actor_loss = tf.reduce_mean(tf.reduce_sum(self.neglogprob * self.tfadv, axis=1))


        with tf.compat.v1.variable_scope('train'):
            self.train_op = tf.compat.v1.train.AdamOptimizer(self.lr).minimize(-self.exp_v)  # minimize(-exp_v) = maximize(exp_v)

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
             self.s: np.vstack(s[np.newaxis, :]),  # shape=[None, n_obs]
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
        # prob_weights = self.sess.run(self.all_act_prob, feed_dict={self.s: s[np.newaxis, :]})
        prob_weights = self.sess.run(self.all_act_prob, feed_dict={self.s: s[np.newaxis, :]})
        action = np.random.choice(range(prob_weights.shape[1]), p=prob_weights.ravel())  # select action w.r.t the actions prob
        print('prob_weights:',prob_weights,',action:',action)
        # action_list = []
        # for action_i in range(len(s)):
        #     action = np.random.choice(range(prob_weights[action_i].shape[0]),
        #                      p=prob_weights[action_i].ravel())   # select action w.r.t the actions prob
        #     action_list.append(action)

        # return action_list
        return action

    def plot_cost(self):
        import matplotlib.pyplot as plt
        plt.plot(np.arange(len(self.cost_his)), self.cost_his)
        plt.ylabel('Cost')
        plt.xlabel('training steps')
        plt.show()

class Critic(object):
    def __init__(self, sess, n_features, lr=0.01, memory_size=100000, batch_size=32):
        self.sess = sess
        self.n_features = n_features
        self.s = tf.compat.v1.placeholder(tf.float32, [None, n_features], "state")
        self.v_ = tf.compat.v1.placeholder(tf.float32, [None, 1], "v_next")
        self.r = tf.compat.v1.placeholder(tf.float32, None, 'r')
        self.batch_size = batch_size
        self.memory_size = memory_size
        self.memory = np.zeros((self.memory_size, n_features * 2 + 2))

        self.cost_his = []

        with tf.compat.v1.variable_scope('Critic'):
            l1 = tf.compat.v1.layers.dense(
                inputs=self.s,
            #     units=128,  # number of hidden units
            #     activation=tf.nn.relu,  # None
            #     # have to be linear to make sure the convergence of actor.
            #     # But linear approximator seems hardly learns the correct Q.
            #     kernel_initializer=tf.random_normal_initializer(0., .1),  # weights
            #     bias_initializer=tf.constant_initializer(0.1),  # biases
            #     name='l1'
            # )
            # l2 = tf.compat.v1.layers.dense(
            #     inputs=l1,
            #     units=64,    # number of hidden units
            #     activation=tf.nn.relu,
            #     kernel_initializer=tf.random_normal_initializer(0., .1),    # weights
            #     bias_initializer=tf.constant_initializer(0.1),  # biases
            #     name='l2'
            # )
            # l3 = tf.compat.v1.layers.dense(
            #     inputs=l2,
                units=32,    # number of hidden units
                activation=tf.nn.relu,
                kernel_initializer=tf.random_normal_initializer(0., .1),    # weights
                bias_initializer=tf.constant_initializer(0.1),  # biases
                name='l3'
            )

            self.v = tf.compat.v1.layers.dense(
                inputs=l1,
                units=1,  # output units
                activation=None,
                kernel_initializer=tf.random_normal_initializer(0., .1),  # weights
                bias_initializer=tf.constant_initializer(0.1),  # biases
                name='V'
            )

        with tf.compat.v1.variable_scope('squared_TD_error'):
            self.td_error = tf.reduce_mean(self.r + GAMMA * self.v_ - self.v)
            self.loss = 0.5 * tf.reduce_sum(tf.square(self.td_error))  # TD_error = (r+gamma*V_next) - V_eval

        with tf.compat.v1.variable_scope('train'):
            self.train_op = tf.compat.v1.train.AdamOptimizer(lr).minimize(self.loss)

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
        # r = r[:,np.newaxis]
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