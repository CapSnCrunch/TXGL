from matplotlib.pyplot import get
import numpy as np
from math import isclose
from classes.intervals import *
from classes.interval_funcs import *

def P(v):
    '''Maps RP1 -> R U {infinity}'''
    if v[0] == 0:
        return np.inf
    return float(v[1] / v[0])

def Pinv(a, v1, v2):
    '''Maps R U {infinity} -> RP1'''
    if a == np.inf:
        return v2
    return (v1 + a * v2) / np.linalg.norm(v1 + a * v2)