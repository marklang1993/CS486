import numpy as np
import gridWorld

# action code: 0 - up, 1 - down, 2 - left, 3 - right

def getMax(V_a):
    # init.
    max_a = V_a[0]
    act_taken = 0
    # find max
    for idx in xrange(0, V_a.size):
        if max_a <= V_a[idx]:
            max_a = V_a[idx]
            act_taken = idx
    return act_taken, max_a

def checkValue(V, V_last):
    diff_ths = 0.01 # Threshold difference
    for cur_s in xrange(0, 17):
        a_diff = abs(V[cur_s] - V_last[cur_s])
        if a_diff >= diff_ths:
            return False
    return True

def calculate(T, R, V, d_factor, cur_state):
    V_a = np.zeros(4) # V_a is the array
    if cur_state == 16:
        return 0.0
    # At current state, calcualte Value at each action
    for a_i in xrange(0, 4): # a_i: action taken in the current state
        sum = 0.0
        for s_i in xrange(0, 17): # s_i: next state w.r.t the cur_state
            # calculate the sum
            sum += T[cur_state, s_i, a_i] * V[s_i]
        V_a[a_i] = R[cur_state] + d_factor * sum
    return getMax(V_a)

def iterate(T, R, V, d_factor):
    A = np.zeros(16) # actions taken in each state
    for cur_s in xrange(0, 16):
        (action, V[cur_s]) = calculate(T, R, V, d_factor, cur_s)
        A[cur_s] = action
    return A

def start(a, b):
    # Initialize T, R, V, d_factor
    d_factor = 0.99 # Discount factor
    (T, R) = gridWorld.gridWorld(a, b)
    V = np.copy(R)
    # iterate
    while True:
        V_last = np.copy(V)
        A = iterate(T, R, V, d_factor) 
        if checkValue(V, V_last):
            break

    print "a = ", a, "; b = ", b
    print(V)
    for idx in xrange(0, A.size):
        if A[idx] == 0:
            print "|  UP   |",
        elif A[idx] == 1:
            print "| DOWN  |",
        elif A[idx] == 2:
            print "| LEFT  |",
        elif A[idx] == 3:
            print "| RIGHT |",
        if (idx + 1) % 4 == 0:
            print " " # Change a line

# Transition parameters
a = 0.8  # intended move
b = 0.1  # lateral move
start(a, b)

# Transition parameters
a = 0.9  # intended move
b = 0.05  # lateral move
start(a, b)

# For reference:
# Transition parameters
a = 1  # intended move
b = 0  # lateral move
start(a, b)
