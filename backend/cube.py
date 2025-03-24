import numpy as np
from numba import njit
import time
import matplotlib.pyplot as plt
import random
import json

from backend.support import *

@njit
def applyIntMoves(state,moves):
    new_state = np.copy(state)
    for move in moves:
        if move == -1: # no move
            break
        new_state = _change_state(new_state, move_array[move])
    return new_state

# jitted functions

@njit
def _change_state(state,changes):
    new_state = np.copy(state)
    for i,j in enumerate(changes):
        new_state[i] = state[j]
    return new_state

@njit
def _apply_int_moves(state,moves):
    new_state = np.copy(state)
    for move in moves:
        if move == -1: # no move
            break
        new_state = _change_state(new_state, move_array[move])
    return new_state

@njit
def _f2l_solved(state):
    return state[50]==6 and state[46]==6 and state[46]==6 and state[52]==6 and state[45]==6 and state[47]==6 and state[51]==6 and state[53]==6 and state[3]==1 and state[4]==1 and state[5]==1 and state[6]==1 and state[7]==1 and state[8]==1 and state[12]==2 and state[13]==2 and state[14]==2 and state[15]==2 and state[16]==2 and state[17]==2 and state[21]==3 and state[22]==3 and state[23]==3 and state[24]==3 and state[25]==3 and state[26]==3 and state[30]==4 and state[31]==4 and state[32]==4 and state[33]==4 and state[34]==4 and state[35]==4

# cube definition

class Cube:
    def __init__(self,mode = ""):
        '''
        mode: 0 - normal, 1 - debug, 2 - normal but top layer all 0s, 3 - normal but side of top layer all 0s
        '''
        self.mode = mode
        if mode == "": # normal
            self.mode = "normal"
            self.state = np.array([1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,5,5,5,5,5,5,5,5,5,6,6,6,6,6,6,6,6,6])
        elif mode == "id": #show index of each sticker
            self.state = np.array(range(54))
        elif mode == "cp": #CP
            self.state = np.array([7,0,8,0,0,0,1,0,3,8,0,6,0,0,0,3,0,4,6,0,5,0,0,0,4,0,2,5,0,7,0,0,0,2,0,1,5,0,6,0,0,0,7,0,8,1,0,3,0,0,0,2,0,4])
        elif mode == "223": #2x2x3 - centers
            self.state = np.array([0,0,0,1,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,3,0,3,3,0,0,0,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,6,6,0,6,6,0,6,6,0])
        elif mode == "FB+222RBD": # First block + 222 in BRD
            self.state = np.array([0,0,0,1,1,0,1,0,0,0,0,0,0,2,2,0,2,2,0,0,0,3,3,3,3,3,3,0,0,0,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,6,0,0,6,6,6,6,6,6])
        elif mode == "FB": # First block (for cpfb)
            self.state = np.array([0,0,0,1,0,0,1,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,3,0,0,3,0,0,0,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,6,0,0,6,0,0,6,0,0])
<<<<<<< HEAD
        elif mode == "FB_D": # First block (for cpfb)
            self.state = np.array([0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,3,0,0,0,0,0,0,4,4,4,0,0,0,0,0,0,0,0,0,6,6,0,6,6,0,6,6,0])
=======
>>>>>>> 26616da5966baeda8ff865bf6cfa65a4f3c367b9
        elif mode == "Line": # 1x1x3 (for cpline)
            self.state = np.array([0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,4,4,4,0,0,0,0,0,0,0,0,0,6,0,0,6,0,0,6,0,0])
        elif mode == "DLcorners": # DL-corners (for cp)
            self.state = np.array([0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,4,0,4,0,0,0,0,0,0,0,0,0,6,0,0,0,0,0,6,0,0])
        elif mode == "223+EO": #2x2x3 + EO
            self.state = np.array([0,0,0,1,1,5,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,5,3,3,0,3,3,0,0,0,4,4,4,4,4,4,0,5,0,5,0,5,0,5,0,6,6,0,6,6,5,6,6,0])    
        else:
            print("NOTE! Mode not found. Using normal mode.")
            self.mode = "normal"
            self.state = np.array([1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,5,5,5,5,5,5,5,5,5,6,6,6,6,6,6,6,6,6])


    def __repr__(self):
        s = self.state
        space = "  "*(self.mode == 1)
        rpr =                    f"{space}       {s[36]} {s[37]} {s[38]}"
        rpr +=                 f"\n{space}       {s[39]} {s[40]} {s[41]}"
        rpr +=                 f"\n{space}       {s[42]} {s[43]} {s[44]}"
        
        rpr += f"\n{s[27]} {s[28]} {s[29]}  {s[0]} {s[1]} {s[2]}  {s[9]} {s[10]} {s[11]}  {s[18]} {s[19]} {s[20]}"
        rpr += f"\n{s[30]} {s[31]} {s[32]}  {s[3]} {s[4]} {s[5]}  {s[12]} {s[13]} {s[14]}  {s[21]} {s[22]} {s[23]}"
        rpr += f"\n{s[33]} {s[34]} {s[35]}  {s[6]} {s[7]} {s[8]}  {s[15]} {s[16]} {s[17]}  {s[24]} {s[25]} {s[26]}"
        
        
        rpr +=                 f"\n{space}       {s[45]} {s[46]} {s[47]}"
        rpr +=                 f"\n{space}       {s[48]} {s[49]} {s[50]}"
        rpr +=                 f"\n{space}       {s[51]} {s[52]} {s[53]}"
        return rpr+"\n"
        
    def change_state(self,changes):
        '''
        changes: np.array of size 6*9, descibing where each id goes.
        Doing nothing would be [0,1,2,3,...,53]
        '''
        self.state = _change_state(self.state,changes)
        
    def is_solved(self):
        if self.mode == 1:
            if np.array_equal(self.state,np.array(range(54))):
                return True
        else:
            if np.array_equal(self.state,np.array([1]*9+[2]*9+[3]*9+[4]*9+[5]*9+[6]*9)):
                return True
        return False
    
    def f2l_solved(self):
        # only works in nondebug mode
        if _f2l_solved(cube.state):
            return True
        return False
        
    def apply_move(self,move):
        self.change_state(moves[move])
    
    def apply_moves(self,alg):
        # alg in string
        if alg:
            alg = alg.split(" ")
            for move in alg:
                self.change_state(move_dict[move])

    def apply_int_moves(self,alg):
        # alg is a numpy array of ints
        self.state = _apply_int_moves(self.state,alg)

    def apply_alg(self,alg):
        # alg: string identifier
        self.change_state(alg_dict[alg])
            
    def apply_algs(self,alg_list):
        # moves in string
        if alg_list:
            algs = alg_list.split(" ")
            for alg in algs:
                self.change_state(alg_dict[alg])
                
    def plot(self,colors=["grey","green","r","b","darkorange","w","y","black"]):
        plot_2d_cube(self.state, colors=colors)
        
    def get_short_state(self):
        state = cube.state.tolist()
        short_state = state[0:4]
        short_state += state[5:13]
        short_state += state[14:22]
        short_state += state[23:31]
        short_state += state[32:40]
        short_state += state[41:49]
        short_state += state[50:54]
        return np.array(short_state,dtype=float)
    
    def copy(self):
        cCube = Cube(self.mode)
        cCube.state = self.state.copy()
        return cCube
    
@njit
def id_from_state(state, ids = np.array(range(54))):
    '''
    assumes no rotation
    make sure the cube is in the correct orientation! (mode 2 for F2L only)
    '''
    ID = str(state[ids[0]])
    for i in ids[1:]:
        ID += str(state[i])
    return ID #you might want to int() this afterwards

def plot_alg(alg):
    cube = Cube()
    cube.apply_moves(alg)
    cube.plot()













