from classes.intervals import *
from classes.interval_funcs import *
from classes.group_funcs import *
from classes.graph_funcs import *

### CREATE REPRESENTATION ###
orders = [2, 4]

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

# For order [2, 3]
#graph = {0: {1: B}, 1: {0: A, 2: B}, 2: {0 : A}}
#graph = {0: {1: B, 2: B @ B}, 1: {0: A}, 2: {0 : A}}
#graph = {0: {1: B, 1: B @ B}, 1: {0: A}}

# For orders [2, 4]
#graph = {0: {1: B}, 1: {0: A, 2: B}, 2: {0: A, 3: B}, 3: {0: A}}

graph = generate_graph(orders, [A, B])

# Triangle Group <a, b, c | a^2 = b^2 = c^2 = 1, (ab)^3 = (cb)^3 = (ac)^4 = 1>
A = np.array([[ 0.923879532511287, -0.217284326304659],
               [-0.673986071141597, -0.923879532511287]])
B = np.array([[0.,                1.219308768593441],
               [0.820136806818482, 0.               ]])
C = np.array([[ 0.923879532511287,  0.21728432630466 ],
               [ 0.673986071141597, -0.923879532511286]])

print(A@A)
print(B@B)
print(C@C)
print(A@B@A@B@A@B)
print(C@B@C@B@C@B)
print(A@C@A@C@A@C@A@C)

graph = {0: {},
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
            17: {10: A, 12: C}}

'''graph = {0: {1: A, 2: B, 3: C},
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
             17: {10: A, 12: C}}'''

words = allwords(graph, 5, 5)
print(len(words))

eps = 2e-4
disconnected_intervals = []
for i in range(len(words)):
    intervals = []
    color = np.array([np.random.uniform(0,0.5), np.random.uniform(0,0.5), np.random.uniform(0,0.5)])
    for j in range(len(words[i])):
        s = np.arctan2(np.linalg.svd(words[i][j])[0][1][0], np.linalg.svd(words[i][j])[0][0][0])
        #intervals.append(Interval(s - eps, s + eps, 0, 0, [], np.array([int(i == 0), int(i == 1)/2, int(i == 2)])))
        intervals.append(Interval(s - eps, s + eps, 0, 0, [], color))
    disconnected_intervals.append(DisconnectedInterval(intervals))

# TODO Build reverse graph
expansion = 1e-3
expand = []
for i in range(100):
    print(i)
    # Expand all of the disconnected intervals
    for di in expand:
        for interval in di.components:
            interval.e1 = (interval.e1 + expansion) % np.pi
            interval.e2 = (interval.e2 + expansion) % np.pi
    contained = True
    expand = [] # Keep track of which intervals don't contain the images they need to
    for l1 in list(graph.keys()):
        for l2 in graph[l1]:
            if not disconnected_intervals[l1].contains_image(disconnected_intervals[l2], graph[l1][l2]):
                contained = False
                expand.append(disconnected_intervals[l1])
    if contained:
        print('Found valid intervals!')
        break

fig, ax = plt.subplots(figsize = (5, 5))

# RP1
rp1 = Circle((0, 0), 1.0, fill = False)
ax.add_patch(rp1)

for i in range(len(disconnected_intervals)):
    disconnected_intervals[i].draw(ax)

for l1 in list(graph.keys()):
    for l2 in graph[l1]:
        disconnected_intervals[l2].draw_image(ax, graph[l1][l2])

#for i in [10]:
#    disconnected_intervals[i].draw(ax)

#for l1 in [0]:
#    for l2 in graph[l1]:
#        print(l1, l2)
#        disconnected_intervals[l2].draw_image(ax, graph[l1][l2])

#disconnected_intervals[10].draw_image(ax, graph[0][1])
#disconnected_intervals[2].draw_image(ax, graph[0][2])
#disconnected_intervals[3].draw_image(ax, graph[0][3])

# Plot data
ax.set_xlim((-1.2, 1.2))
ax.set_ylim((-1.2, 1.2))
ax.axis('off')
ax.set_aspect('equal')

plt.show()