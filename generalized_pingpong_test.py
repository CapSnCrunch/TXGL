import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Arc
from classes.interval_funcs import *
from classes.intervals import Interval

### CREATE REPRESENTATION ###
orders = [2, 3]

generators = []
for order in orders:
    theta = np.pi / order
    generators += [np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])]

l = 2
C = np.array([[l, 0],
              [0, 1/l]])

A, B = generators

A = np.linalg.inv(C) @ A @ C
B = C @ B @ np.linalg.inv(C)

letters = [A, B, B @ B]
graph = {1 : [2, 3], 2 : [1], 3 : [1]} # 1 corresponds to A, 2 to B, and 3 to B^-1

### INITIALIZE INTERVALS ###
eps = 1e-2
intervals = []

# np.linalg.svd will always sort in descending order
# Initialize interval for A
sa = np.arctan2(np.linalg.svd(A)[0][1][1], np.linalg.svd(A)[0][0][1])
intervals.append(Interval(sa - eps, sa + eps, 1, A, letters, np.array([0, 0, 1])))

# Initialize interval for B
sb = np.arctan2(np.linalg.svd(B)[0][1][1], np.linalg.svd(B)[0][0][1])
intervals.append(Interval(sb - eps, sb + eps, 2, B, letters, np.array([1, 0, 0])))

# Initialize intervals for B^-1
sbb = np.arctan2(np.linalg.svd(B @ B)[0][1][1], np.linalg.svd(B @ B)[0][0][1])
intervals.append(Interval(sbb - eps, sbb + eps, 3, B @ B, letters, np.array([0, 1, 0])))

### FIND INTERVALS ###
expansion = 1e-3
steps = 200
iter = 0
while iter < steps:
    for interval in intervals:
        interval.e1 = (interval.e1 + expansion) % np.pi
        interval.e2 = (interval.e2 + expansion) % np.pi

    # Check containment
    Ia, Ib, Ibb = intervals

    if Ib.contains_image(Ia):
        print('Ib contains image of Ia')
    if Ibb.contains_image(Ia):
        print('Ibb contains image of Ia')
    if Ia.contains_image(Ib):
        print('Ia contains image of Ib')
    if Ia.contains_image(Ibb):
        print('Ia contains image of Ibb')

    if Ib.contains_image(Ia) and Ibb.contains_image(Ia) and Ia.contains_image(Ib) and Ia.contains_image(Ibb):
        print('Found valid intervals in', iter, 'iterations!')
        break
    iter += 1

### DRAW INTERVALS ###
fig, ax = plt.subplots(figsize = (5, 5))

# Plot data
ax.set_xlim((-1.2, 1.2))
ax.set_ylim((-1.2, 1.2))
ax.axis('off')
ax.set_aspect('equal')

# RP1
rp1 = Circle((0,0), 1.0, fill = False)
ax.add_patch(rp1)

for interval in intervals:
    interval.draw(ax)

'''for i in graph:
    # Change from an int to the actual interval object
    for temp in intervals:
        if temp.name == i:
            interval = temp
    I = rp1_interval((interval.a - interval.e1) % np.pi, (interval.b + interval.e2) % np.pi)
    for j in graph[i]:
        # Change from an int to the actual interval object
        for temp in intervals:
            if temp.name == j:
                other = temp
        theta2, theta1 = get_arc_params(other.mat @ I)
        ax.add_patch(Arc((0,0), 2., 2., theta1=theta1, theta2=theta2, color='orange', linewidth=7))'''

for i in graph:
    # Change from an int to the actual interval object
    for temp in intervals:
        if temp.name == i:
            interval = temp
    I = rp1_interval((interval.a - interval.e1) % np.pi, (interval.b + interval.e2) % np.pi)
    theta2, theta1 = get_arc_params(interval.mat @ I)
    ax.add_patch(Arc((0,0), 2., 2., theta1 = theta1, theta2 = theta2, color = np.array([0.5, 0.5, 0.5]) + interval.color / 2, linewidth = 7))

plt.show()