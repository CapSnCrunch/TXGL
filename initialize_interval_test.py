from classes.intervals import *
from classes.interval_funcs import *
from classes.group_funcs import *
from classes.graph_funcs import *

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
graph = {'0' : [('1', B), ('2', B @ B)], '1' : [('0', A)], '2' : [('0', A)]}
#graph = {'0' : [('1', B)], '1' : [('0', A), ('2', B)], '2' : [('0', A)]}

words = allwords(graph, 5, 5)

'''eps = 2e-3
disconnected_intervals = []
for l1 in list(graph.keys()):
    intervals = []
    for l2 in graph[l1]:
        for w in words[int(l2[0])]:
            s = np.arctan2(np.linalg.svd(w)[0][1][0], np.linalg.svd(w)[0][0][0])
            intervals.append(Interval(s - eps, s + eps, 0, 0, [], np.array([int(int(l1) == 0), int(int(l1) == 1), int(int(l1) == 2)])))
    disconnected_intervals.append(DisconnectedInterval(intervals))'''

eps = 2e-3
disconnected_intervals = []
for i in range(len(words)):
    intervals = []
    for j in range(len(words[i])):
        s = np.arctan2(np.linalg.svd(words[i][j])[0][1][0], np.linalg.svd(words[i][j])[0][0][0])
        intervals.append(Interval(s - eps, s + eps, 0, 0, [], np.array([int(i == 0), int(i == 1)/2, int(i == 2)])))
    disconnected_intervals.append(DisconnectedInterval(intervals))

# TODO Build reverse graph
expansion = 1e-3
expand = []
for i in range(200):
    # Expand all of the disconnected intervals
    for di in expand:
        for interval in di.components:
            interval.e1 = (interval.e1 + expansion) % np.pi
            interval.e2 = (interval.e2 + expansion) % np.pi
    contained = True
    expand = [] # Keep track of which intervals don't contain the images they need to
    for l1 in list(graph.keys()):
        for l2 in graph[l1]:
            if not disconnected_intervals[int(l1)].contains_image(disconnected_intervals[int(l2[0])], l2[1]):
                contained = False
                expand.append(disconnected_intervals[int(l1)])
    if contained:
        print('Found valid intervals!')
        break

fig, ax = plt.subplots(figsize=(5, 5))

# RP1
rp1 = Circle((0,0), 1.0, fill=False)
ax.add_patch(rp1)

for i in range(len(disconnected_intervals)):
    disconnected_intervals[i].draw(ax)

for l1 in list(graph.keys()):
    for l2 in graph[l1]:
        disconnected_intervals[int(l2[0])].draw_image(ax, l2[1])

#disconnected_intervals[0].draw_image(ax, A) # image of 0 under A
#disconnected_intervals[1].draw_image(ax, B) # image of 1 under B
#disconnected_intervals[2].draw_image(ax, B @ B) # image of 2 under B @ B

# Plot data
ax.set_xlim((-1.2, 1.2))
ax.set_ylim((-1.2, 1.2))
ax.axis("off")
ax.set_aspect("equal")

plt.show()