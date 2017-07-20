import numpy as np
import gridWorld

# action code: 0 - up, 1 - down, 2 - left, 3 - right

# Choose an action
# Q: Q value table
# s: current state
# RETURN: action
def chooseAction(Q, s):
    # current setting
    max_Q_action = 0
    max_Q_val = Q[s, max_Q_action]
    for action in xrange(0,4):
        if Q[s, action] > max_Q_val:
            # Find the maxium Q value
            max_Q_val = Q[s, action]
            max_Q_action = action
    return max_Q_action

# Execute an action
# T: transition table
# E: execution count at (s, a)
# RETURN: next state
def executeAction(T, E, s, a):
    E[s, a] = E[s, a] + 1
    # find next state
    t_space = T[s,:,a]
    for next_state in xrange(0, t_space.size):
        if t_space[next_state] != 0:
            return next_state

def getLRate(s, a, E):
    return 1.0/E[s, a]

def getMaxEval_Q(Q, next_state):
    max_action = chooseAction(Q, next_state)
    return Q[next_state, max_action]

def calculate(T, R, Q, E, d_factor, s, a, next_state):
    diff = R[s] + d_factor * getMaxEval_Q(Q, next_state) - Q[s, a]
    Q[s, a] = Q[s, a] + getLRate(s, a, E) * diff

def iterate(T, R, Q, E, d_factor, start_state):
    s = start_state # get the initial state
    for episode_idx in xrange(0, 10000):
        action = chooseAction(Q, s)
        next_state = executeAction(T, E, s, action)
        reward = R[next_state] # receive an immediate reward
        calculate(T, R, Q, E, d_factor, s, action, next_state)
        s = next_state

def start(a, b):
    # Initialize T, R, Q, E, d_factor
    d_factor = 0.99 # Discount factor
    (T, R) = gridWorld.gridWorld(1.0, 0.0) # Only used to simulate the environment
    Q = np.zeros((17, 4)) # Q value - init. to 0
    E = np.zeros((17, 4)) # Exection count at (s, a)
    # iterate
    iterate(T, R, Q, E, d_factor, 4)
    print Q

start(0.8, 0.1)