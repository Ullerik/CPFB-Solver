import numpy as np
from numba import njit
import time
import matplotlib.pyplot as plt
import random
import json

from backend.solver_logic import *

mode = "FB"
search_depth = 4
table_depth = 4
search_algs_CPFB, table_CPFB = CP_solver_setup(mode, search_depth, table_depth, move_transition=move_transition, start_grips=np.array([1]), skip_U=True, prnt=False)

print(len(search_algs_CPFB),len(table_CPFB))

def sort_solves(solves):
    # sort solves by length of solution, meaning sol.split(" ") is the length of the solution, such that the shortest ones are first
    solves.sort(key=lambda x: len(x.split(" ")))
    # sort by number of S moves
    solves.sort(key=lambda x: x.count("S")+x.count("M")+x.count("E"))
    # next, sort them by number of f/F moves, such that the ones with the least f/F moves are first
    solves.sort(key=lambda x: x.count("f") + x.count("F"))
    return solves

def process_scramble(scramble, rotation):
    # TODO: find the first instance of x, y, or z
    # We wanna rotate the scramble such that we can solve with corner in DBL in DBL every time

    scramble = (scramble + " " + rotation).strip()
    print("Solving ", scramble)

    solves = CP_solver(scramble, mode, search_algs_CPFB, table_CPFB)

    solves = sort_solves(solves)

    return solves