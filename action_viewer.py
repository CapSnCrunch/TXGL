import colorsys
from classes.intervals import *
from classes.interval_funcs import *
from classes.group_funcs import *
from classes.graph_funcs import *

mat = np.array([[0,-1],[1,0]])
mat = np.array([[ 0.923879532511287, -0.217284326304659],
               [-0.673986071141597, -0.923879532511287]])

n = 100
delta = np.pi / n

intervals = []
for i in range(n):
    color = np.array([i for i in colorsys.hsv_to_rgb(i/n,1,1)])
    intervals.append(Interval(i * delta, (i+1) * delta, 0, 0, [], color))

fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (10, 5))

# RP1
rp1 = Circle((0, 0), 1.0, fill = False)
#ax1.add_patch(rp1)

view = 75
for i in range(view, view+1):
    intervals[i].draw(ax1)

for i in range(view, view+1):
    I = rp1_interval(intervals[i].a % np.pi, intervals[i].b % np.pi)
    theta2, theta1 = get_arc_params(mat @ I)
    ax2.add_patch(Arc((0,0), 2., 2., theta1 = theta1, theta2 = theta2, color = intervals[i].color, linewidth = 7))

# Plot data
ax1.set_xlim((-1.2, 1.2))
ax1.set_ylim((-1.2, 1.2))
ax1.axis('off')
ax1.set_aspect('equal')
ax2.set_xlim((-1.2, 1.2))
ax2.set_ylim((-1.2, 1.2))
ax2.axis('off')
ax2.set_aspect('equal')

plt.show()