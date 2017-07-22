import numpy as np
import random
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adagrad


class DQN(object):
    def __init__(self):
        # variables initialization (given)
        self.actions_cnt = 2  # Left & Right
        self.features_cnt = 4  # x, x', theta, theta'
        self.learn_rate = 0.1
        self.gamma = 0.99
        self.epsilon = 0.05  # epsilon greedy
        self.units_cnt = 10  # rectified linear units
        self.buffer = np.hstack([0.0, 0.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

        # build DNN
        self.model = Sequential()
        self.model.add(Dense(self.units_cnt, input_dim=self.features_cnt, activation='relu'))
        self.model.add(Dense(self.units_cnt, activation='relu'))
        self.model.add(Dense(self.actions_cnt, activation='linear'))
        self.model.compile(loss='mse', optimizer=Adagrad(lr=self.learn_rate))

    # save current data
    def save(self, ob_state, act_state, reward_state, done, ob_next_state):
        state_result = [act_state, reward_state, done]
        self.buffer = np.copy(np.hstack((ob_state, state_result, ob_next_state)))

    def episode_complete(self):
        pass

    def train(self):
        # train the model
        # state_features(4), state_action, state_reward, done, next_state_features(4)
        state_action = self.buffer[self.features_cnt].astype(int)
        state_reward = self.buffer[self.features_cnt + 1]
        done = self.buffer[self.features_cnt + 2]

        state_features = np.reshape(self.buffer[0:self.features_cnt], [1, self.features_cnt])
        next_state_features = np.reshape(self.buffer[self.features_cnt + 3:], [1, self.features_cnt])

        current_state_Q_val = self.model.predict(state_features)
        next_state_Q_val = self.model.predict(next_state_features)
        if done:
            Q_val = state_reward
        else:
            Q_val = state_reward + self.gamma * \
                                   np.amax(next_state_Q_val[0])
        current_state_Q_val[0][state_action] = Q_val
        self.model.fit(state_features, current_state_Q_val, epochs=1, verbose=0)

    def chooseAction(self, ob_state):
        rand = np.random.rand()
        if rand < self.epsilon:
            # choose random action
            return np.random.randint(self.actions_cnt)
        else:
            # predict action
            ob_state = np.reshape(ob_state, [1, self.features_cnt])
            action_values = self.model.predict(ob_state)[0]
            return np.argmax(action_values)


class DQN_Replay(object):
    def __init__(self):
        # variables initialization (given)
        self.actions_cnt = 2 # Left & Right
        self.features_cnt = 4 # x, x', theta, theta'
        self.learn_rate = 0.1
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
        self.model.compile(loss='mse', optimizer=Adagrad(lr=self.learn_rate))

        
    # save current data
    def save(self, ob_state, act_state, reward_state, done, ob_next_state):
        self.buffer_save_count += 1
        # locate buffer slot
        buffer_index = self.buffer_save_count % self.buffer_size
        # pack & save
        state_result = [act_state, reward_state, done]
        self.buffer[buffer_index] = np.copy(np.hstack((ob_state, state_result, ob_next_state)))


    def episode_complete(self):
        pass


    def train(self):
        if self.buffer_save_count < self.mini_batch_size:
            # current saved data count < required count
            random_seq = np.arange(0, self.buffer_save_count)
        else:
            # current saved data count >= required count
            if self.buffer_save_count < self.buffer_size:
                # buffer is not full
                random_seq = random.sample(np.arange(0, self.buffer_save_count), self.mini_batch_size)
            else:
                # buffer is full
                random_seq = random.sample(np.arange(0, self.buffer_size), self.mini_batch_size)
        # get mini batch
        mini_batch_memory = np.copy(self.buffer[random_seq,:])

        # train the model
        for idx in xrange(0, mini_batch_memory[:,0].size):
            # state_features(4), state_action, state_reward, done, next_state_features(4)
            state_action = mini_batch_memory[idx, self.features_cnt].astype(int)
            state_reward = mini_batch_memory[idx, self.features_cnt + 1]
            done = mini_batch_memory[idx, self.features_cnt + 2]

            state_features = np.reshape(mini_batch_memory[idx, 0:self.features_cnt], [1, self.features_cnt])
            next_state_features = np.reshape(mini_batch_memory[idx, self.features_cnt + 3:], [1, self.features_cnt])

            current_state_Q_val = self.model.predict(state_features)
            next_state_Q_val = self.model.predict(next_state_features)
            if done:
                Q_val = state_reward
            else:
                Q_val = state_reward + self.gamma *\
                         np.amax(next_state_Q_val[0])
            current_state_Q_val[0][state_action] = Q_val
            self.model.fit(state_features, current_state_Q_val, epochs=1, verbose=0)


    def chooseAction(self, ob_state):
        rand = np.random.rand()
        if rand < self.epsilon:
            # choose random action
            return np.random.randint(self.actions_cnt)
        else:
            # predict action
            ob_state = np.reshape(ob_state, [1, self.features_cnt])
            action_values = self.model.predict(ob_state)[0]
            return np.argmax(action_values)


class DQN_Target(object):
    def __init__(self):
        # variables initialization (given)
        self.actions_cnt = 2 # Left & Right
        self.features_cnt = 4 # x, x', theta, theta'
        self.learn_rate = 0.1
        self.gamma = 0.99
        self.epsilon = 0.05 # epsilon greedy
        self.update_target_ep_cnt = 2 # update the the target network after every 2 episodes
        self.units_cnt = 10 # rectified linear units
        self.buffer = np.hstack([0.0, 0.0, 0.0, 0.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

        # variables initialization (run-time)
        self.episodes_completed = 0

        # build DNN
        self.model = Sequential()
        self.model.add(Dense(self.units_cnt, input_dim=self.features_cnt, activation='relu'))
        self.model.add(Dense(self.units_cnt, activation='relu'))
        self.model.add(Dense(self.actions_cnt, activation='linear'))
        self.model.compile(loss='mse', optimizer=Adagrad(lr=self.learn_rate))

        # build target DNN
        self.model_target = Sequential()
        self.model_target.add(Dense(self.units_cnt, input_dim=self.features_cnt, activation='relu'))
        self.model_target.add(Dense(self.units_cnt, activation='relu'))
        self.model_target.add(Dense(self.actions_cnt, activation='linear'))
        self.model_target.compile(loss='mse', optimizer=Adagrad(lr=self.learn_rate))


    # save current data
    def save(self, ob_state, act_state, reward_state, done, ob_next_state):
        state_result = [act_state, reward_state, done]
        self.buffer = np.copy(np.hstack((ob_state, state_result, ob_next_state)))


    # update target
    def updateTarget(self):
        self.model_target.set_weights(self.model.get_weights())


    def episode_complete(self):
        self.episodes_completed = self.episodes_completed + 1
        # check update
        if self.episodes_completed % self.update_target_ep_cnt == 0:
            # update is needed
            self.updateTarget()
            print "Target updated at :",self.episodes_completed


    def train(self):
        # train the model
        # state_features(4), state_action, state_reward, done, next_state_features(4)
        state_action = self.buffer[self.features_cnt].astype(int)
        state_reward = self.buffer[self.features_cnt + 1]
        done = self.buffer[self.features_cnt + 2]

        state_features = np.reshape(self.buffer[0:self.features_cnt], [1, self.features_cnt])
        next_state_features = np.reshape(self.buffer[self.features_cnt + 3:], [1, self.features_cnt])

        current_state_Q_val = self.model.predict(state_features)
        next_state_Q_val = self.model_target.predict(next_state_features)
        if done:
            Q_val = state_reward
        else:
            Q_val = state_reward + self.gamma *\
                     np.amax(next_state_Q_val[0])
        current_state_Q_val[0][state_action] = Q_val
        self.model.fit(state_features, current_state_Q_val, epochs=1, verbose=0)


    def chooseAction(self, ob_state):
        rand = np.random.rand()
        if rand < self.epsilon:
            # choose random action
            return np.random.randint(self.actions_cnt)
        else:
            # predict action
            ob_state = np.reshape(ob_state, [1, self.features_cnt])
            action_values = self.model.predict(ob_state)[0]
            return np.argmax(action_values)


class DQN_Replay_Target(object):
    def __init__(self):
        # variables initialization (given)
        self.actions_cnt = 2 # Left & Right
        self.features_cnt = 4 # x, x', theta, theta'
        self.learn_rate = 0.1
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
        self.model.compile(loss='mse', optimizer=Adagrad(lr=self.learn_rate))

        # build target DNN
        self.model_target = Sequential()
        self.model_target.add(Dense(self.units_cnt, input_dim=self.features_cnt, activation='relu'))
        self.model_target.add(Dense(self.units_cnt, activation='relu'))
        self.model_target.add(Dense(self.actions_cnt, activation='linear'))
        self.model_target.compile(loss='mse', optimizer=Adagrad(lr=self.learn_rate))


    # save current data
    def save(self, ob_state, act_state, reward_state, done, ob_next_state):
        self.buffer_save_count += 1
        # locate buffer slot
        buffer_index = self.buffer_save_count % self.buffer_size
        # pack & save
        state_result = [act_state, reward_state, done]
        self.buffer[buffer_index] = np.copy(np.hstack((ob_state, state_result, ob_next_state)))


    # update target
    def updateTarget(self):
        self.model_target.set_weights(self.model.get_weights())


    def episode_complete(self):
        self.episodes_completed = self.episodes_completed + 1
        # check update
        if self.episodes_completed % self.update_target_ep_cnt == 0:
            # update is needed
            self.updateTarget()
            print "Target updated at :",self.episodes_completed


    def train(self):
        if self.buffer_save_count < self.mini_batch_size:
            # current saved data count < required count
            random_seq = np.arange(0, self.buffer_save_count)
        else:
            # current saved data count >= required count
            if self.buffer_save_count < self.buffer_size:
                # buffer is not full
                random_seq = random.sample(np.arange(0, self.buffer_save_count), self.mini_batch_size)
            else:
                # buffer is full
                random_seq = random.sample(np.arange(0, self.buffer_size), self.mini_batch_size)
        # get mini batch
        mini_batch_memory = np.copy(self.buffer[random_seq,:])

        # train the model
        for idx in xrange(0, mini_batch_memory[:,0].size):
            # state_features(4), state_action, state_reward, done, next_state_features(4)
            state_action = mini_batch_memory[idx, self.features_cnt].astype(int)
            state_reward = mini_batch_memory[idx, self.features_cnt + 1]
            done = mini_batch_memory[idx, self.features_cnt + 2]

            state_features = np.reshape(mini_batch_memory[idx, 0:self.features_cnt], [1, self.features_cnt])
            next_state_features = np.reshape(mini_batch_memory[idx, self.features_cnt + 3:], [1, self.features_cnt])

            current_state_Q_val = self.model.predict(state_features)
            next_state_Q_val = self.model_target.predict(next_state_features)
            if done:
                Q_val = state_reward
            else:
                Q_val = state_reward + self.gamma *\
                         np.amax(next_state_Q_val[0])
            current_state_Q_val[0][state_action] = Q_val
            self.model.fit(state_features, current_state_Q_val, epochs=1, verbose=0)


    def chooseAction(self, ob_state):
        rand = np.random.rand()
        if rand < self.epsilon:
            # choose random action
            return np.random.randint(self.actions_cnt)
        else:
            # predict action
            ob_state = np.reshape(ob_state, [1, self.features_cnt])
            action_values = self.model.predict(ob_state)[0]
            return np.argmax(action_values)
