import colorsys
from classes.intervals import *
from classes.interval_funcs import *
from classes.group_funcs import *
from classes.graph_funcs import *

# A in <a, b, c | a^2 = b^2 = c^2 = 1, (ab)^3 = (cb)^3 = (ac)^4 = 1>
mat = np.array([[ 0.923879532511287, -0.217284326304659],
               [-0.673986071141597, -0.923879532511287]])

# A, B in <a,b | a^2 = b^3 = 1>
'''mat = np.array([[0, -1], [1, 0]])
mat = np.array([[6.123234e-17, -2.500000e-01],
                [4.000000e+00, 6.123234e-17]])
mat = np.array([[0.5, -3.46410162],
                [0.21650635, 0.5]])'''

n = 200
delta = np.pi / n

intervals = []
for i in range(n):
    color = np.array([i for i in colorsys.hsv_to_rgb(i/n,1,1)])
    intervals.append(Interval(i * delta - delta / 10, (i+1) * delta + delta / 10, 0, 0, [], color))

fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (10, 5))

# RP1
rp1 = Circle((0, 0), 1.0, fill = False)
#ax1.add_patch(rp1)

view = 0
for i in range(n):
    intervals[i].draw(ax1)

for i in range(n):
    I = rp1_interval(intervals[i].a % np.pi, intervals[i].b % np.pi)
    if np.linalg.det(mat) < 0:
        theta2, theta1 = sorted(get_arc_params(mat @ I), reverse = True)
    else:
        theta2, theta1 = get_arc_params(mat @ I)
    ax2.add_patch(Arc((0,0), 2., 2., theta1 = theta1, theta2 = theta2, color = intervals[i].color, linewidth = 10))

# Plot data
ax1.set_xlim((-1.1, 1.1))
ax1.set_ylim((-1.1, 1.1))
ax1.axis('off')
ax1.set_aspect('equal')
ax2.set_xlim((-1.1, 1.1))
ax2.set_ylim((-1.1, 1.1))
ax2.axis('off')
ax2.set_aspect('equal')

plt.show()