import numpy as np

# The function gridWorld returns the transition function T and reward function M
def gridWorld(a, b):

    # Grid world layout:
    #
    #  ---------------------
    #  |  0 |  1 |  2 |  3 |
    #  ---------------------
    #  |  4 |  5 |  6 |  7 |
    #  ---------------------
    #  |  8 |  9 | 10 | 11 |
    #  ---------------------
    #  | 12 | 13 | 14 | 15 |
    #  ---------------------
    #
    #  Goal state: 15 
    #  Bad state: 9
    #  End state: 16
    #
    #  The end state is an absorbing state that the agent transitions 
    #  to after visiting the goal state.
    #
    #  There are 17 states in total (including the end state) 
    #  and 4 actions (up, down, right, left).
    #

    #%%%%%%%%%%%%%%%%%%% rewards %%%%%%%%%%%%%%%%%%%%%%

    # Rewards are stored in a one dimensional array R[s]
    #
    # All states have a reward of -1 except:
    # Goal state: 100
    # Bad state: -70
    # End state: 0 

    # initialize rewards to -1
    R = -np.ones((17))

    # set rewards
    R[15] = 100;  # goal state
    R[9] = -70;   # bad state
    R[16] = 0;    # end state

    #%%%%%%%%%%%%%%%%%% transitions %%%%%%%%%%%%%%%%%%%

    # Transitions are stored in a 3 dimensional array T[s,s',a] such that
    # T[s,s',a] = Pr(s'|s,a)

    # initialize all transition probabilities to 0
    T = np.zeros((17,17,4))

    # For a given action, the agent has probability a of moving 
    # by one square in the intended direction and probability b
    # of moving sideways.  When the agent bumps into a wall, 
    # it stays in its current location.

    # up (a = 0)

    T[0,0,0] = a+b
    T[0,1,0] = b

    T[1,0,0] = b
    T[1,1,0] = a
    T[1,2,0] = b
    
    T[2,1,0] = b
    T[2,2,0] = a
    T[2,3,0] = b
    
    T[3,2,0] = b
    T[3,3,0] = a+b

    T[4,4,0] = b
    T[4,0,0] = a
    T[4,5,0] = b
    
    T[5,4,0] = b
    T[5,1,0] = a
    T[5,6,0] = b
    
    T[6,5,0] = b
    T[6,2,0] = a
    T[6,7,0] = b
    
    T[7,6,0] = b
    T[7,3,0] = a
    T[7,7,0] = b
    
    T[8,8,0] = b
    T[8,4,0] = a
    T[8,9,0] = b
    
    T[9,8,0] = b
    T[9,5,0] = a
    T[9,10,0] = b
    
    T[10,9,0] = b
    T[10,6,0] = a
    T[10,11,0] = b
    
    T[11,10,0] = b
    T[11,7,0] = a
    T[11,11,0] = b
    
    T[12,12,0] = b
    T[12,8,0] = a
    T[12,13,0] = b
    
    T[13,12,0] = b
    T[13,9,0] = a
    T[13,14,0] = b
    
    T[14,13,0] = b
    T[14,10,0] = a
    T[14,15,0] = b
    
    T[15,16,0] = 1
    T[16,16,0] = 1
    
    # down (a = 1)

    T[0,0,1] = b
    T[0,4,1] = a
    T[0,1,1] = b
    
    T[1,0,1] = b
    T[1,5,1] = a
    T[1,2,1] = b
    
    T[2,1,1] = b
    T[2,6,1] = a
    T[2,3,1] = b
    
    T[3,2,1] = b
    T[3,7,1] = a
    T[3,3,1] = b
    
    T[4,4,1] = b
    T[4,8,1] = a
    T[4,5,1] = b
    
    T[5,4,1] = b
    T[5,9,1] = a
    T[5,6,1] = b
    
    T[6,5,1] = b
    T[6,10,1] = a
    T[6,7,1] = b
    
    T[7,6,1] = b
    T[7,11,1] = a
    T[7,7,1] = b
    
    T[8,8,1] = b
    T[8,12,1] = a
    T[8,9,1] = b
    
    T[9,8,1] = b
    T[9,13,1] = a
    T[9,10,1] = b
    
    T[10,9,1] = b
    T[10,14,1] = a
    T[10,11,1] = b
    
    T[11,10,1] = b
    T[11,15,1] = a
    T[11,11,1] = b
    
    T[12,12,1] = a+b
    T[12,13,1] = b
    
    T[13,12,1] = b
    T[13,13,1] = a
    T[13,14,1] = b
    
    T[14,13,1] = b
    T[14,14,1] = a
    T[14,15,1] = b
    
    T[15,16,1] = 1
    T[16,16,1] = 1
    
    # left (a = 2)

    T[0,0,2] = a+b
    T[0,4,2] = b
    
    T[1,1,2] = b
    T[1,0,2] = a
    T[1,5,2] = b
    
    T[2,2,2] = b
    T[2,1,2] = a
    T[2,6,2] = b
    
    T[3,3,2] = b
    T[3,2,2] = a
    T[3,7,2] = b
    
    T[4,0,2] = b
    T[4,4,2] = a
    T[4,8,2] = b
    
    T[5,1,2] = b
    T[5,4,2] = a
    T[5,9,2] = b
    
    T[6,2,2] = b
    T[6,5,2] = a
    T[6,10,2] = b
    
    T[7,3,2] = b
    T[7,6,2] = a
    T[7,11,2] = b
    
    T[8,4,2] = b
    T[8,8,2] = a
    T[8,12,2] = b
    
    T[9,5,2] = b
    T[9,8,2] = a
    T[9,13,2] = b
    
    T[10,6,2] = b
    T[10,9,2] = a
    T[10,14,2] = b
    
    T[11,7,2] = b
    T[11,10,2] = a
    T[11,15,2] = b
    
    T[12,8,2] = b
    T[12,12,2] = a+b
    
    T[13,9,2] = b
    T[13,12,2] = a
    T[13,13,2] = b
    
    T[14,10,2] = b
    T[14,13,2] = a
    T[14,14,2] = b
    
    T[15,16,2] = 1
    T[16,16,2] = 1
    
    # right (a = 3)

    T[0,0,3] = b
    T[0,1,3] = a
    T[0,4,3] = b
    
    T[1,1,3] = b
    T[1,2,3] = a
    T[1,5,3] = b
    
    T[2,2,3] = b
    T[2,3,3] = a
    T[2,6,3] = b
    
    T[3,3,3] = a+b
    T[3,7,3] = b
    
    T[4,0,3] = b
    T[4,5,3] = a
    T[4,8,3] = b
    
    T[5,1,3] = b
    T[5,6,3] = a
    T[5,9,3] = b
    
    T[6,2,3] = b
    T[6,7,3] = a
    T[6,10,3] = b
    
    T[7,3,3] = b
    T[7,7,3] = a
    T[7,11,3] = b
    
    T[8,4,3] = b
    T[8,9,3] = a
    T[8,12,3] = b
    
    T[9,5,3] = b
    T[9,10,3] = a
    T[9,13,3] = b
    
    T[10,6,3] = b
    T[10,11,3] = a
    T[10,14,3] = b
    
    T[11,7,3] = b
    T[11,11,3] = a
    T[11,15,3] = b
    
    T[12,8,3] = b
    T[12,13,3] = a
    T[12,12,3] = b
    
    T[13,9,3] = b
    T[13,14,3] = a
    T[13,13,3] = b
    
    T[14,10,3] = b
    T[14,15,3] = a
    T[14,14,3] = b
    
    T[15,16,3] = 1
    T[16,16,3] = 1
    
    return T,R

