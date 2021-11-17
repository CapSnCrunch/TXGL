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
#graph = {'0' : [('1', B), ('1', B @ B)], '1' : [('0', A)]}
#graph = {'0' : [('1', B), ('2', B @ B)], '1' : [('0', A)], '2' : [('0', A)]}
#graph = {'0' : [('1', B)], '1' : [('0', A), ('2', B)], '2' : [('0', A)]}

#graph = {0 : {1: B}, 1 : {0: A, 2: B}, 2: {0 : A}}
#graph = {0 : {1: B, 2: B @ B}, 1 : {0: A}, 2: {0 : A}}
graph = {0 : {1: B, 1: B @ B}, 1 : {0: A}}

# Triangle Group <a, b, c | a^2 = b^2 = c^2 = 1, (ab)^3 = (cb)^3 = (ac)^4 = 1>
'''A = np.array([[ 0.923879532511287, -0.217284326304659],
               [-0.673986071141597, -0.923879532511287]])
B = np.array([[0.,                1.219308768593441],
               [0.820136806818482, 0.               ]])
C = np.array([[ 0.923879532511287,  0.21728432630466 ],
               [ 0.673986071141597, -0.923879532511286]])

graph = {0: {1: A, 2: B, 3: C},
            1: {4: B, 5: C},
            2: {6: A, 7: C},
            3: {8: A, 9: B},
            4: {10: A, 7: C},
            5: {11: A, 9: B},
            6: {1: B, 5: C},
            7: {8: A, 12: B},
            8: {4: B, 13: C},
            9: {6: A, 12: C},
            10: {14: C},
            11: {4: B, 15: C},
            12: {16: A},
            13: {16: A, 9: B},
            14: {11: A, 12: B},
            15: {17: B},
            16: {10: B, 13: C},
            17: {10: A, 12: C}}'''

graph = {0: {1: A, 2: B, 3: C},
             1: {4: B, 5: C},
             2: {6: A, 7: C},
             3: {8: A, 9: B},
             4: {10: A, 7: C},
             5: {11: A, 9: B},
             6: {10: B, 5: C},
             7: {8: A, 12: B},
             8: {4: B, 13: C},
             9: {6: A, 12: C},
             10: {14: C},
             11: {4: B, 15: C},
             12: {16: A},
             13: {15: A, 9: B},
             14: {11: A, 12: B},
             15: {17: B},
             16: {10: B, 13: C},
             17: {10: A, 12: C}}

words = allwords(graph, 5, 5)
print(len(words))

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
    color = np.array([np.random.uniform(0,1), np.random.uniform(0,1), np.random.uniform(0,1)])
    for j in range(len(words[i])):
        s = np.arctan2(np.linalg.svd(words[i][j])[0][1][0], np.linalg.svd(words[i][j])[0][0][0])
        #intervals.append(Interval(s - eps, s + eps, 0, 0, [], np.array([int(i == 0), int(i == 1)/2, int(i == 2)])))
        intervals.append(Interval(s - eps, s + eps, 0, 0, [], color))
    disconnected_intervals.append(DisconnectedInterval(intervals))

# TODO Build reverse graph
expansion = 1e-3
expand = []
for i in range(1):
    print('I', i)
    # Expand all of the disconnected intervals
    for di in expand:
        for interval in di.components:
            interval.e1 = (interval.e1 + expansion) % np.pi
            interval.e2 = (interval.e2 + expansion) % np.pi
    contained = True
    print('HERE 1')
    expand = [] # Keep track of which intervals don't contain the images they need to
    for l1 in list(graph.keys()):
        for l2 in graph[l1]:
            if not disconnected_intervals[l1].contains_image(disconnected_intervals[l2], graph[l1][l2]):
                contained = False
                expand.append(disconnected_intervals[l1])
    print('HERE')
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
        disconnected_intervals[l2].draw_image(ax, graph[l1][l2])

#for i in range(len(disconnected_intervals)):
#    disconnected_intervals[i].draw(ax)

#for l1 in [0]:
#    for l2 in graph[l1]:
#        disconnected_intervals[l2].draw_image(ax, graph[l1][l2])

#disconnected_intervals[0].draw_image(ax, A) # image of 0 under A
#disconnected_intervals[1].draw_image(ax, B) # image of 1 under B
#disconnected_intervals[2].draw_image(ax, B @ B) # image of 2 under B @ B

# Plot data
ax.set_xlim((-1.2, 1.2))
ax.set_ylim((-1.2, 1.2))
ax.axis("off")
ax.set_aspect("equal")

plt.show()