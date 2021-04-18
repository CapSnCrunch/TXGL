#!/usr/bin/env python
# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt

from matplotlib.patches import Circle, Arc
from matplotlib.widgets import Slider

def rp1_to_s1(v):
    """map a point in R^2 - {0} to S1 via the homeo RP1 -> S1"""
    x, y = v[0], v[1]

    return np.row_stack([
        2*x*y / (x*x + y*y),
        (x*x - y*y) / (x*x + y*y)
    ])

# print(rp1_to_s1((1.5, 0)))
# print(rp1_to_s1((1, 1)))

def get_arc_params(interval):
    """map a pair of points in R^2 - {0} to a pair of circle angles"""
    x, y = rp1_to_s1(interval)
    return np.arctan2(y,x) * 180 / np.pi

# print(get_arc_params((1.413, 0.588, 1, 1)))

def get_arc(interval, **kwargs):
    """get a matplotlib arc object for a pair of points in R^2 - {0}"""
    print('kwargs', kwargs)
    theta1, theta2 = get_arc_params(interval)
    print('theta1 theta2', theta1, theta2)
    return Arc((0,0), 2., 2., theta1=theta1, theta2=theta2, **kwargs)

def get_arc_intervals(word, **kwargs):
    """get data to build some matplotlib arcs out of some words in F2"""
    if word[-1] == 'A':
        intervals = ["I1", "I2", "J2"]
    elif word[-1] == 'B':
        intervals = ["I1", "J1", "I2"]
    elif word[-1] == 'a':
        intervals = ["J1", "I2", "J2"]
    elif word[-1] == 'b':
        intervals = ["I1", "J1", "J2"]

    return [
        {"transform":word, "base":interval, "params":kwargs}
        for interval in intervals
    ]

def get_arcs(arc_info, intervals, matrix_map):
    """get some matplotlib arcs out of arc info"""
    print('arc_info', arc_info)
    print('intervals', intervals)
    print('matrix_map', matrix_map)

    arcs = []
    for arc in arc_info:
        print('arc[transform]', arc["transform"], 'end')
        transform = matrix_word(matrix_map, arc["transform"])
        print(transform)
        print('arc[base]', arc["base"], 'end')
        interval = transform @ intervals[arc["base"]]
        print('interval', interval)
        arcs.append(get_arc(interval, **arc["params"]))
    return arcs

def rp1_interval(theta1, theta2):
    """get a pair of points in RP1 representing the pair of angles theta1, theta2

    note: theta1, theta2 paramaterize the double cover of RP^1"""
    return np.array([
        [np.cos(theta1), np.cos(theta2)],
        [np.sin(theta1), np.sin(theta2)]
    ])

def matrix_word(matrix_map, word):
    """given a dict from generators to matrices, get the matrix representing a word in the generators"""
    matrix = np.identity(2)
    for gen in word:
        matrix = matrix @ matrix_map[gen]

    return matrix

#a pair of matrices in SL(2, Z), which (maybe?) generate a free group
A = np.array([[1, 1],
              [2, 3]])

B = np.array([[1, -1],
              [-2, 3]])

'''A = np.array([[3, 0],
              [0, 1/3]])

B = np.array([[5/3, 4/3],
              [4/3, 5/3]])'''

a = np.linalg.inv(A)
b = np.linalg.inv(B)

generators = [A,B]

# Theta for Eigenvectors on S1 via RP1 -> S1
eigenvec_thetas = []
for mat in generators:

    e1 = np.arctan2(np.linalg.eig(mat)[1][1][0] , np.linalg.eig(mat)[1][0][0])
    e2 = np.arctan2(np.linalg.eig(mat)[1][1][1] , np.linalg.eig(mat)[1][0][1])
    eigenvec_thetas.append(e1)
    eigenvec_thetas.append(e2)

    '''e1 = np.arccos(np.linalg.eig(mat)[1])[0][0]
    e2 = np.arccos(np.linalg.eig(mat)[1])[0][1]

    if e1 not in eigenvec_thetas:
        eigenvec_thetas.append(e1 % 3.14159)
    else:
        eigenvec_thetas.append(-e1 % 3.14159)
    if e2 not in eigenvec_thetas:
        eigenvec_thetas.append(e2 % 3.14159)
    else:
        eigenvec_thetas.append(-e2 % 3.14159)

print(np.arccos(np.linalg.eig(A)[1])[0][0] , np.arccos(np.linalg.eig(A)[1])[0][1])
print(np.arccos(np.linalg.eig(B)[1])[0][0] , np.arccos(np.linalg.eig(B)[1])[0][1])
print(np.arctan2(np.linalg.eig(A)[1][1][0] , np.linalg.eig(B)[1][0][0]) , np.arctan2(np.linalg.eig(A)[1][1][1] , np.linalg.eig(B)[1][0][1]))
print(np.arctan2(np.linalg.eig(B)[1][1][0] , np.linalg.eig(B)[1][0][0]) , np.arctan2(np.linalg.eig(B)[1][1][1] , np.linalg.eig(B)[1][0][1]))'''

initial_intervals = []

for t in eigenvec_thetas:
    # print(t + 0.05, t - 0.05)
    initial_intervals.append(rp1_interval(t + 0.05, t - 0.05))

#initial values for the ping-pong intervals
'''I1 = rp1_interval(1.5, 0.9)
J1 = rp1_interval(2.8, 2.3)
I2 = rp1_interval(2.1, 1.7)
J2 = rp1_interval(0.8, 0.4)'''

I1 = initial_intervals[1]
J1 = initial_intervals[0]
I2 = initial_intervals[3]
J2 = initial_intervals[2]

#the set of arcs we'll be drawing (the original arcs, plus arcs transformed by generators of the group)
arcs_to_draw = ([
    {"transform":"", "base":"I1", "params":{"color":"blue", "linewidth":10}},
    {"transform":"", "base":"J1", "params":{"color":"blue", "linewidth":10}},
    {"transform":"", "base":"I2", "params":{"color":"red", "linewidth":10}},
    {"transform":"", "base":"J2", "params":{"color":"red", "linewidth":10}}
    ] + get_arc_intervals("A", color="orange", linewidth=7)
    + get_arc_intervals("B", color="pink", linewidth=7)
    + get_arc_intervals("a", color="orange", linewidth=7)
    + get_arc_intervals("b", color="pink", linewidth=7))

fig, ax = plt.subplots(figsize=(5, 5))

#rp1
rp1 = Circle((0,0), 1.0, fill=False)
ax.add_patch(rp1)

#get some arcs and add them to the drawing
arcs = get_arcs(arcs_to_draw,
                {"I1":I1, "I2":I2, "J1":J1, "J2":J2},
                {"A":A, "B":B, "a":a, "b":b})

for arc in arcs:
    ax.add_patch(arc)

#plot data
ax.set_xlim((-1.2, 1.2))
ax.set_ylim((-1.2, 1.2))
ax.axis("off")
ax.set_aspect("equal")

plt.show()