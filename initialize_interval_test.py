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
# graph = {'1' : ['2', '3'], '2' : ['1'], '3' : ['1']} # 1 corresponds to A, 2 to B, and 3 to B^-1
graph = {'1' : [('2', B), ('3', B @ B)], '2' : [('1', A)], '3' : [('1', A)]}

words = allwords(graph, 5)
separated_words = [[], [], []]
for word in words:
    separated_words[int(word[0])-1].append(word)

for i in range(len(separated_words)):
    separated_words[i] = matrize(separated_words[i], graph)    

disconnected_intervals = []
for l1 in list(graph.keys()):

    intervals = []
    for l2 in graph[l1]:
        sd = []
        for w in separated_words[int(l2)-1]:
            s = np.arctan2(np.linalg.svd(w)[0][1][0], np.linalg.svd(w)[0][0][0])
            sd.append(s)

        eps = 2e-3
        for s in sd:
            intervals.append(Interval(s - eps, s + eps, 0, letters[int(l1) - 1], [letters[int(l1) - 1]], np.array([int(int(l1)-1 == 0), int(int(l1)-1 == 1), int(int(l1)-1 == 2)])))

    disconnected_intervals.append(DisconnectedInterval(intervals))

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
            if not disconnected_intervals[int(l2)-1].contains_image(disconnected_intervals[int(l1)-1]):
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