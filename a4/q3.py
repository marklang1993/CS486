import gym
from gym import spaces
import DQN

env = gym.make('CartPole-v0')
dqn = DQN.DQN_Replay()
for i_episode in range(1000):
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

        if done:
            print("Episode finished after {} timesteps".format(step+1))
            break

    dqn.episode_complete()