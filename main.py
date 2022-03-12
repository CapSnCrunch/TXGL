from matplotlib.pyplot import disconnect
from classes.intervals import *
from classes.interval_funcs import *
from classes.group_funcs import *
from classes.graph_funcs import *

### CREATE REPRESENTATION ###
orders = [2, 3] # Doesn't work for [3, m]

generators = []
for order in orders:
    theta = np.pi / order
    generators += [np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])]

l = 1.5 # Interesting: if we increase this, it decreases the number of search steps
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

#graph = generate_graph(orders, [A, B])
#print(graph)

# words 5, eps 2e-4, delta 1e-3, combine 1e-4
# Triangle Group <a, b, c | a^2 = b^2 = c^2 = 1, (ab)^3 = (cb)^3 = (ac)^4 = 1>
A = np.array([[ 0.923879532511287, -0.217284326304659],
               [-0.673986071141597, -0.923879532511287]])
B = np.array([[0.,                1.219308768593441],
               [0.820136806818482, 0.               ]])
C = np.array([[ 0.923879532511287,  0.21728432630466 ],
               [ 0.673986071141597, -0.923879532511286]])

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

words = allwords(graph, 6, 6)
#print(len(words))

eps = 2e-4
disconnected_intervals = []
for i in range(len(words)):
    intervals = []
    color = np.array([np.random.uniform(0,0.5), np.random.uniform(0,0.5), np.random.uniform(0,0.5)])
    #color = np.array([0.9*(i==0), 0.9*(i==1), 0.9*(i==2)])
    for j in range(len(words[i])):
        s = np.arctan2(np.linalg.svd(words[i][j])[0][1][0], np.linalg.svd(words[i][j])[0][0][0])
        intervals.append(Interval(s - eps, s + eps, 0, 0, [], color))
    disconnected_intervals.append(DisconnectedInterval(intervals))

### LINEAR EXPANSION SEARCH ###
# Linearly expand intervals which do not fully contain the images they need to by some amount
# expand = [] # List of which intervals need to be expanded (ones which don't fully contain images)
# expansion = 5e-4 # Amount to expand intervals by
# for i in range(75):
#     # Expand all of the disconnected intervals
#     for di in expand:
#         for interval in di.components:
#             interval.e1 = (interval.e1 + expansion) % np.pi
#             interval.e2 = (interval.e2 + expansion) % np.pi
#     failed = 0
#     expand = [] # Keep track of which intervals don't contain the images they need to
#     for l1 in list(graph.keys()):
#         for l2 in graph[l1]:
#             if not disconnected_intervals[l1].contains_image(disconnected_intervals[l2], graph[l1][l2]):
#                 failed += 1
#                 if disconnected_intervals[l1] not in expand:
#                     expand.append(disconnected_intervals[l1])
    
#     print(i, failed)
    # if not failed:
    #     print('Found valid intervals!')
    #     break

#     fig, ax = plt.subplots(figsize = (5, 5), facecolor=((214/255, 245/255, 174/255)))

#     # RP1
#     rp1 = Circle((0, 0), 1.0, fill = False)
#     ax.add_patch(rp1)

#     for j in range(len(disconnected_intervals)):
#         disconnected_intervals[j].combine()
#         disconnected_intervals[j].draw(ax)

#     for l1 in list(graph.keys()):
#         for l2 in graph[l1]:
#             disconnected_intervals[l2].draw_image(ax, graph[l1][l2])

#     # Plot data
#     ax.set_facecolor((1.0, 0.47, 0.42))
#     ax.set_xlim((-1.2, 1.2))
#     ax.set_ylim((-1.2, 1.2))
#     ax.axis('off')
#     ax.set_aspect('equal')

#     plt.savefig(fname = 'txgl/gif2/frame'+str(i)+'.png')
#     plt.clf()
#     plt.close()

### PATCH SEARCH ###
# Extend a disconnected interval exactly the amount required by adding components around the images it must contain and combining
delta = 5e-3 # Extra space just over the image
for i in range(5):
    failed = 0
    for l1 in list(graph.keys()):
        for l2 in graph[l1]:
            # Create a new component around each component which was not contained
            for comp in disconnected_intervals[l2].components:
                if not disconnected_intervals[l1].contains_image(DisconnectedInterval([comp]), graph[l1][l2]):
                    failed += 1
                    color = disconnected_intervals[l1].components[0].color
                    x, y = graph[l1][l2] @ rp1_interval((comp.a - comp.e1) % np.pi, (comp.b + comp.e2) % np.pi)
                    a, b = np.arctan2(y,x) # b, a?
                    disconnected_intervals[l1].components.append(Interval(a - delta, b + delta, 0, 0, [], color))
            disconnected_intervals[l1].combine(3e-2)
    print('Iteration', i, '  Number of failed containments', failed)

    for i in range(len(disconnected_intervals)):
        disconnected_intervals[i].combine()
        print(f"  Components: {len(disconnected_intervals[i].components)}")
        #for comp in disconnected_intervals[i].components:
        #    print(comp.a, comp.b)
        #print()
    
    if not failed:
        print('Found valid intervals!')
        break

    # DRAW FIGURES FOR GIF
    # fig, ax = plt.subplots(figsize = (5, 5))

    # # RP1
    # rp1 = Circle((0, 0), 1.0, fill = False)
    # ax.add_patch(rp1)

    # for j in range(len(disconnected_intervals)):
    #     disconnected_intervals[j].combine()
    #     disconnected_intervals[j].draw(ax)

    # for l1 in list(graph.keys()):
    #     for l2 in graph[l1]:
    #         disconnected_intervals[l2].draw_image(ax, graph[l1][l2])

    # Plot data
    '''ax.set_xlim((-1.2, 1.2))
    ax.set_ylim((-1.2, 1.2))
    ax.axis('off')
    ax.set_aspect('equal')

    plt.savefig(fname = 'git/txgl/gif1/frame'+str(i)+'.png')
    plt.clf()
    plt.close()'''

fig, ax = plt.subplots(figsize = (5, 5), facecolor=((255/255, 255/255, 255/255)))

# RP1
rp1 = Circle((0, 0), 1.0, fill = False)
ax.add_patch(rp1)

for i in range(len(disconnected_intervals)):
    disconnected_intervals[i].combine()
    disconnected_intervals[i].draw(ax)
    print(f"Components:   {len(disconnected_intervals[i].components)}")
    for comp in disconnected_intervals[i].components:
       print(comp.a, comp.b)
    print()

for l1 in list(graph.keys()):
    for l2 in graph[l1]:
        disconnected_intervals[l2].draw_image(ax, graph[l1][l2])

# Plot data
ax.set_xlim((-1.2, 1.2))
ax.set_ylim((-1.2, 1.2))
ax.axis('off')
ax.set_aspect('equal')

plt.show()