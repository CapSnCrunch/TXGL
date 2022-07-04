import numpy as np
from math import isclose
from classes.intervals import *
from classes.interval_funcs import *

def P(v, v1, v2):
    '''Maps RP1 -> R U {infinity}'''
    a2 = (v[0]**2) * (v2[0]**2 + v2[1]**2) - v2[0]**2
    a1 = (v[0]**2) * (2*v1[0]*v2[0] + 2*v1[1]*v2[1]) - 2*v1[0]*v2[0]
    a0 = (v[0]**2) * (v1[0]**2 + v1[1]**2) - v1[0]**2

    return float((-a1 + np.sqrt(a1**2 - 4*a0*a2)) / (2*a0))

def Pinv(a, v1, v2):
    '''Maps R U {infinity} -> RP1'''
    if a == np.inf:
        return v2
    return (v1 + a * v2) / np.linalg.norm(v1 + a * v2)

v1 = np.array([[0],[1]])
v2 = np.array([[1],[0]])

u = (v1 + v2) / 2
v = (v2 - v1) / 2