import numpy as np
import gym
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

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
        self.buffer = np.zeros((self.buffer_size,\
            self.features_cnt + 3 + self.features_cnt)) 
            # state_features(4), state_action, state_reward, done, next_state_features(4)

        # build DNN
        self.model = Sequential()
        self.model.add(Dense(self.units_cnt, input_dim=self.features_cnt, activation='relu'))
        self.model.add(Dense(self.units_cnt, activation='relu'))
        self.model.add(Dense(self.actions_cnt, activation='linear'))
        self.model.compile(loss='mse', optimizer=Adam(lr=self.learn_rate))

        
    # save current data
    def save(self, ob_state, act_state, reward_state, done, ob_next_state):
        self.buffer_save_count += 1
        # locate buffer slot
        buffer_index = self.buffer_save_count % self.buffer_size
        # pack & save
        state_result = [act_state, reward_state, done]
        self.buffer[buffer_index] = np.hstack((ob_state, state_result, ob_next_state))

    def updateBuffer(self):
        pass

    @staticmethod
    def randomSeqGen(total_size, sample_size):
        random_seq = np.zeros(sample_size, dtype=int)
        for idx in xrange(0,sample_size):
            random_seq[idx] = np.random.randint(0, total_size)
        return random_seq

    def train(self):
        # check update
        if self.episodes_completed % self.update_target_ep_cnt == 0:
            # update is needed
            self.updateBuffer()
            print "Buffer updated at :",self.episodes_completed
        
        # sample batch
        if self.buffer_save_count < self.mini_batch_size:
            # current saved data count < required count
            random_seq = DQN.randomSeqGen(self.buffer_save_count, self.mini_batch_size)
        else:
            # current saved data count >= required count
            if self.buffer_save_count < self.buffer_size:
                # buffer is not full
                random_seq = DQN.randomSeqGen(self.buffer_save_count, self.mini_batch_size)
            else:
                # buffer is full
                random_seq = DQN.randomSeqGen(self.buffer_size, self.mini_batch_size)
        # get mini batch
        mini_batch_memory = np.copy(self.buffer[random_seq,:])

        # train the model
        for idx in xrange(0, mini_batch_memory[:,0].size):
            # state_features(4), state_action, state_reward, done, next_state_features(4)
            state_action = mini_batch_memory[idx, self.features_cnt]
            state_reward = mini_batch_memory[idx, self.features_cnt + 1]
            done = mini_batch_memory[idx, self.features_cnt + 2]

            state_features = np.reshape(mini_batch_memory[idx, 0:self.features_cnt], [1, self.features_cnt])
            next_state_features = np.reshape(mini_batch_memory[idx, self.features_cnt + 3:], [1, self.features_cnt])

            if done:
                target = state_reward
            else:
                target = state_reward + self.gamma *\
                         np.amax(self.model.predict(next_state_features)[0])
            target_f = self.model.predict(state_features)
            target_f[0][state_action.astype(int)] = target
            self.model.fit(state_features, target_f, epochs=1, verbose=0)

    def chooseAction(self, ob_state, env):
        rand = np.random.uniform()
        if rand < self.epsilon:
            # choose random action
            return env.action_space.sample()
        else:
            # predict action
            ob_state = np.reshape(ob_state, [1, self.features_cnt])
            action_values = self.model.predict(ob_state)[0]
            return np.argmax(action_values)
