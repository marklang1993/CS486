import numpy as np
import tensorflow as tf

class DQN(object):
    def __init__(self):
        # variables initialization (given)
        self.actions_cnt = 2 # Left & Right
        self.features_cnt = 4 # x, x', theta, theta'
        self.learn_rate = 0.1 # AdamOptimizer using 0.1
        self.gamma = 0.99
        self.epsilon = 0.05 # epsilon greedy
        self.buffer_size = 1000
        self.buffer_save_count = 0 # how many times save() is called
        self.update_target_ep_cnt = 2 # update the the target network after every 2 episodes
        self.mini_batch_size = 50
        self.units_cnt = 10 # rectified linear units

        # variables initialization (run-time)
        self.episodes_completed = 0
        self.buffer = np.zeros((\
            self.buffer_size,\
            self.features_cnt + 2 + self.features_cnt)) 
            # state_features(4), state_action, state_reward, next_state_features(4)

        # building DQN
        # 1. Input layer of 4 nodes
        self.state_features = tf.placeholder(\
            tf.float32,\
            shape=[None, self.features_cnt],\
            name='state_features') # current state features
        self.state_action = tf.placeholder(\
            tf.int32,\
            shape=[None, ],\
            name='state_action') # action in current state
        self.state_reward = tf.placeholder(\
            tf.float32,\
            shape= [None, ],\
            name='state_reward') # reward in current state
        self.next_state_features = tf.placeholder(\
            tf.float32,\
            shape=[None, self.features_cnt],\
            name='next_state_features') # next state features

        # 2. Two hidden layers of 10 rectified linear units (fully connected)
        def buildDNN(c, inputs, units_cnt):
            val_init = tf.random_normal_initializer(-1.0, 1.0)
            # Layer 1
            with tf.variable_scope('layer1'):
                layer1_weight = tf.get_variable(\
                    'layer1_weight',\
                    [self.features_cnt, units_cnt],\
                    None,\
                    val_init,\
                    collections=c) # weight matrix(4*10) in layer 1
                layer1_bias = tf.get_variable(\
                    'layer1_bias',\
                    [1, units_cnt],\
                    None,\
                    val_init,\
                    collections=c) # bias row matrix(1*10) in layer 1
                # rectified linear units & construct by "layer1(1*10) = inputs * W + b"
                layer1 = tf.nn.relu(\
                    tf.matmul(inputs, layer1_weight)\
                    + layer1_bias)

            # Layer 2
            with tf.variable_scope('layer2'):
                layer2_weight = tf.get_variable(\
                    'layer2_weight',\
                    [units_cnt, self.actions_cnt],\
                    None,\
                    val_init,\
                    collections=c) # weight matrix(10*2) in layer 2
                layer2_bias = tf.get_variable(\
                    'layer2_bias',\
                    [1, self.actions_cnt],\
                    None,\
                    val_init,\
                    collections=c) # bias row matrix(1*2) in layer 2
                # construct by "layer2(1*2) = layer1 * W + b"
                layer2 = tf.matmul(layer1, layer2_weight) + layer2_bias
            return layer2

        # 3. Build estimate network (for current state)
        with tf.variable_scope('estimate_network'):
            self.DQN_estimate = buildDNN(
                ['DQN_estimate', tf.GraphKeys.GLOBAL_VARIABLES],
                self.state_features,
                self.units_cnt
            ) # matrix (4*2)

        # 4. Build target network (for next state - NOTE: W is fixed)
        with tf.variable_scope('target_network'):
            self.DQN_target = buildDNN(
                ['DQN_target', tf.GraphKeys.GLOBAL_VARIABLES],
                self.next_state_features,
                self.units_cnt
            ) # matrix (4*2)

        # 5. Calculate Q target value (slides 20, p7)
        self.Q_target = tf.stop_gradient(\
            self.state_reward +\
            self.gamma * tf.reduce_max(\
                self.DQN_target, axis=1, name='max_next_state'),
            name='Q_target')

        # 6. Calcuate Q value for current state w.r.t. action
        self.Q_estimate = tf.reduce_sum(\
            self.DQN_estimate * tf.one_hot(\
                self.state_action,\
                depth=self.actions_cnt,\
                dtype=tf.float32,\
                name='take_action'),\
            axis=1,\
            name='Q_estimate')
        
        # 7. Calculate Squared error
        self.squared_error = 0.5 * tf.squared_difference(\
            self.Q_target, self.Q_estimate, name='squared_error')

        # 8. Train
        self.train_operation = tf.train.AdamOptimizer(\
            self.learn_rate).minimize(self.squared_error)
        
        # Get tensorflow running session
        self.session = tf.Session()
        # Turn on the tensorboard
        tf.summary.FileWriter("tensorboard/", self.session.graph)
        # Run
        self.session.run(tf.global_variables_initializer())
        self.costs = []
        
    # save current data
    def save(self, ob_state, act_state, reward_state, ob_next_state):
        self.buffer_save_count += 1
        # locate buffer slot
        buffer_index = self.buffer_save_count % self.buffer_size
        # pack & save
        state_result = [act_state, reward_state]
        self.buffer[buffer_index] = np.hstack((ob_state, state_result, ob_next_state))

    def updateBuffer(self):
        # get all parameters of 2 network
        DQN_estimate_params = tf.get_collection('DQN_estimate')
        DQN_target_params = tf.get_collection('DQN_target')
        # get assign tensors
        zipped_pairs = zip(DQN_estimate_params, DQN_target_params)
        assign_tensors = list()
        for estimate_param, target_param in : zipped_pairs
             assign_tensors.append(tf.assign(target_param, estimate_param))
        # update
        self.session.run(assign_tensors)

    def train(self):
        # check update
        if self.episodes_completed % self.update_target_ep_cnt == 0:
            # update is needed
            self.updateBuffer()
            print "Buffer updated at :",self.episodes_completed
        
        # sample mini-batch
        if 


    def chooseAction(self, ob_state, env):
        rand = np.random.uniform()
        if rand < self.epsilon:
            # choose random action
            return env.action_space.sample()
        else:
            # choose action by using DQN
            ob_state = ob_state[np.newaxis] # add 1 dummy dimension
            return self.session.run(self.Q_estimate,\
                feed_dict={self.state_features: ob_state})


dqn = DQN()
