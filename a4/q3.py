import gym
from gym import spaces
import numpy as np
import math
import matplotlib.pyplot as plt

import DQN

env = gym.make('CartPole-v0')
dqn = DQN.DQN_Replay()
discount_reward = np.zeros(1000)
for i_episode in range(10):
    observation = env.reset()
    for step in range(500):
        #env.render()
        # take an action
        action = dqn.chooseAction(observation)
        # get new observation
        new_observation, reward, done, info = env.step(action)
        # save
        dqn.save(observation, action, reward, done, new_observation)
        # learn
        dqn.train()
        # iterate
        observation = new_observation
        # check
        if done:
            print("Episode finished after {} timesteps".format(step+1))
            break

    # calculate discounted reward
    if i_episode == 0:
        discount_reward[i_episode] = reward * math.pow(dqn.gamma, i_episode)
    else:
        discount_reward[i_episode] = reward * math.pow(dqn.gamma, i_episode) + discount_reward[i_episode - 1]
    # notify
    dqn.episode_complete()
    
# plot
plt.plot(np.arange(discount_reward.size), discount_reward)
plt.ylabel('Discounted Reward')
plt.xlabel('Episodes')
plt.show()