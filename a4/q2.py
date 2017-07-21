import numpy as np
import random
import gridWorld

# action code: 0 - up, 1 - down, 2 - left, 3 - right

def conclude(Q):
    opVal = np.zeros(17)
    opAct = np.zeros(17)
    for state in xrange(0, 17):
        curAct = 0
        curVal = Q[state, curAct]
        for action in xrange(0, 4):
            if curVal < Q[state, action]:
                # Update
                curAct = action
                curVal = Q[state, action]
        # Record the optimal value
        opVal[state] = curVal
        opAct[state] = curAct
    return opVal, opAct

# Choose an action
# Q: Q value table
# s: current state
# RETURN: action
def chooseAction(Q, s):
    # current setting
    max_Q_action = 0
    max_Q_val = Q[s, max_Q_action]
    for action in xrange(0,4):
        if max_Q_val < Q[s, action]:
            # Find the maxium Q value
            max_Q_val = Q[s, action]
            max_Q_action = action
    return max_Q_action

# Execute an action
# T_op: transition table used for optimal execution
# T_ra: transition table used for random execution
# E: execution count at (state, action)
# RETURN: next state
def executeAction(T_op, T_ra, epsilon, E, state, action):
    E[state, action] = E[state, action] + 1
    # find next state - roll a 3-face die
    rand = random.random()
    if rand < epsilon:
        # execute random action
        t_space = np.copy(T_ra[state,:,action])
        # set init. value to be invalid value
        next_state_1 = 20
        next_state_2 = 20
        # find next_state 1
        for next_state in xrange(0, t_space.size):
            if t_space[next_state] != 0:
                t_space[next_state] -= 0.5
                next_state_1 = next_state
                break
        # find next_state 2
        for next_state in xrange(0, t_space.size):
            if t_space[next_state] != 0:
                t_space[next_state] -= 0.5
                next_state_2 = next_state
                break
        # execute
        if rand < (epsilon / 2):
            return next_state_1
        else:
            return next_state_2
        
    else:
        # execute optimal action
        t_space = T_op[state,:,action]
        for next_state in xrange(0, t_space.size):
            if t_space[next_state] != 0:
                return next_state

# get learning rate
def getLRate(s, a, E):
    return 1.0/E[s, a]

def getMaxEval_Q(Q, next_state):
    max_action = chooseAction(Q, next_state)
    return Q[next_state, max_action]

def calculate(R, Q, E, d_factor, s, a, next_state):
    diff = R[s] + d_factor * getMaxEval_Q(Q, next_state) - Q[s, a]
    Q[s, a] = Q[s, a] + getLRate(s, a, E) * diff

def iterate(T_op, T_ra, epsilon, R, Q, E, d_factor, start_state):
    for episode_idx in xrange(0, 10000):
        s = start_state # get the initial state
        while s != 16:
            action = chooseAction(Q, s)
            next_state = executeAction(T_op, T_ra, epsilon, E, s, action)
            print next_state,
            reward = R[next_state] # receive an immediate reward
            calculate(R, Q, E, d_factor, s, action, next_state)
            s = next_state
        print ""

def start(a, b):
    # Initialize
    epsilon = 0.05 # EPSILON (0.05 or 0.2)
    d_factor = 0.99 # Discount factor
    (T_op, R) = gridWorld.gridWorld(1.0, 0.0) # Only used to simulate the environment
    (T_ra, R) = gridWorld.gridWorld(0.0, 0.5) # Only used to simulate the environment
    Q = np.zeros((17, 4)) # Q value - init. to 0
    E = np.zeros((17, 4)) # Exection count at (s, a)
    # iterate
    iterate(T_op, T_ra, epsilon, R, Q, E, d_factor, 4) # 4 is the start state
    # conclude
    opVal, opAct = conclude(Q)
    # display
    print "UP:"
    print Q[:,0]
    print "DOWN:"
    print Q[:,1]
    print "LEFT:"
    print Q[:,2]
    print "RIGHT:"
    print Q[:,3]
    for state in xrange(0, 16):
        print opVal[state],
        if (state + 1)%4 == 0:
            print " "

    for state in xrange(0, 16):
        if opAct[state] == 0:
            print "|  UP   |",
        elif opAct[state] == 1:
            print "| DOWN  |",
        elif opAct[state] == 2:
            print "| LEFT  |",
        elif opAct[state] == 3:
            print "| RIGHT |",
        if (state + 1) % 4 == 0:
            print " "

start(0.8, 0.1)