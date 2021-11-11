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

words = allwords(graph, 5, 5)

disconnected_intervals = []
for l1 in list(graph.keys()):
    intervals = []
    for l2 in graph[l1]:
        sd = []
        for w in words[int(l2[0])]:
            s = np.arctan2(np.linalg.svd(w)[0][1][0], np.linalg.svd(w)[0][0][0])
            sd.append(s)
        eps = 2e-3
        for s in sd:
            intervals.append(Interval(s - eps, s + eps, 0, letters[int(l1)], [letters[int(l1)]], np.array([int(int(l1) == 0), int(int(l1) == 1), int(int(l1) == 2)])))
    disconnected_intervals.append(DisconnectedInterval(intervals))

# TODO Build reverse graph
expansion = 1e-2
for i in range(1):
    # Expand all of the disconnected intervals
    for di in disconnected_intervals:
        for interval in di.components:
            interval.e1 = (interval.e1 + expansion) % np.pi
            interval.e2 = (interval.e2 + expansion) % np.pi
    contained = True
    for l1 in list(graph.keys()):
        for l2 in graph[l1]:
            if not disconnected_intervals[int(l2[0])].contains_image(disconnected_intervals[int(l1)]):
                contained = False
            print(l1, 'contains', l2, contained)
    if contained:
        print('Found valid intervals!')
        break

fig, ax = plt.subplots(figsize=(5, 5))

# RP1
rp1 = Circle((0,0), 1.0, fill=False)
ax.add_patch(rp1)

for di in disconnected_intervals:
    di.draw(ax)

for di in disconnected_intervals:
    di.draw_image(ax)

#plot data
ax.set_xlim((-1.2, 1.2))
ax.set_ylim((-1.2, 1.2))
ax.axis("off")
ax.set_aspect("equal")

plt.show()