import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Arc
from interval_funcs import *
from intervals import Interval

orders = [2, 3]

generators = []
for order in orders:
    theta = 2*np.pi / order
    generators += [np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])]

l = 5
C = np.array([[l, 0],
              [0, 1/l]])

generators[1] = C @ generators[1] @ np.linalg.inv(C)
print(generators[0])
print(generators[1])

'''A1 = Interval(np.pi/2, np.pi/1.5, 1, generators[0], generators, 'blue')
B1 = Interval(np.pi/2 - np.pi/6, np.pi/2 + np.pi/6, 1, generators[1], generators, 'red')
B2 = Interval(-np.pi/6, np.pi/6, 1, generators[1]**2, generators, 'green')
intervals = [B1]'''

fig, ax = plt.subplots(figsize = (5, 5))

# Plot data
ax.set_xlim((-1.2, 1.2))
ax.set_ylim((-1.2, 1.2))
ax.axis("off")
ax.set_aspect("equal")

# RP1
rp1 = Circle((0,0), 1.0, fill = False)
ax.add_patch(rp1)

# MANUALLY SET UP INTERVAL
a, b = np.pi/4, np.pi/3

# Draw interval
theta2, theta1 = get_arc_params(rp1_interval((a) % np.pi, (b) % np.pi))
ax.add_patch(Arc((0,0), 2., 2., theta1=theta1, theta2=theta2, color='blue', linewidth=10))

I = rp1_interval((a) % np.pi, (b) % np.pi)
theta2, theta1 = get_arc_params(I @ generators[1])
ax.add_patch(Arc((0,0), 2., 2., theta1=theta1, theta2=theta2, color='orange', linewidth=7))

'''for interval in intervals:
    interval.draw(ax)
for interval in intervals:
    interval.draw_image(ax)'''

plt.show()