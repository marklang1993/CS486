import gym
import numpy as np
import math
import matplotlib.pyplot as plt

import DQN

env = gym.make('CartPole-v0')
# dqn = DQN.DQN()
# dqn = DQN.DQN_Target()
dqn = DQN.DQN_Replay()
# dqn = DQN.DQN_Replay_Target()
discount_rewards = np.zeros(1000)
for i_episode in range(1000):
    observation = env.reset()
    discount_reward = 0.0
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
        discount_reward += reward * math.pow(dqn.gamma, step)

    # record
    discount_rewards[i_episode] = discount_reward
    # notify
    dqn.episode_complete()
    
# plot
plt.plot(np.arange(discount_rewards.size), discount_rewards)
plt.ylabel('Discounted Reward')
plt.xlabel('Episodes')
plt.show()
print discount_rewards