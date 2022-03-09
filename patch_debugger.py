import pygame
from matplotlib.pyplot import disconnect
from classes.intervals import *
from classes.interval_funcs import *
from classes.group_funcs import *
from classes.graph_funcs import *
from colors import colors

### CREATE DEBUGGER WINDOW ###
width, height = 600, 400
win = pygame.display.set_mode((width, height))
pygame.display.set_caption('TXGL Patch Search Debugger')

pygame.font.init()
font = pygame.font.SysFont('Roboto', 15)

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
graph = {0: {1: B}, 1: {0: A, 2: B}, 2: {0 : A}}
#graph = {0: {1: B, 2: B @ B}, 1: {0: A}, 2: {0 : A}}
#graph = {0: {1: B, 1: B @ B}, 1: {0: A}}

# For orders [2, 4]
#graph = {0: {1: B}, 1: {0: A, 2: B}, 2: {0: A, 3: B}, 3: {0: A}}

#graph = generate_graph(orders, [A, B])
print(graph)

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

# CREATE INITIAL INTERVALS OF SIZE eps
eps = 2e-4
disconnected_intervals = []
for i in range(len(words)):
    intervals = []
    #color = np.array([np.random.uniform(0,0.5), np.random.uniform(0,0.5), np.random.uniform(0,0.5)])
    #color = np.array([0.9*(i==0), 0.9*(i==1), 0.9*(i==2)])
    color = colors[i]
    for j in range(len(words[i])):
        s = np.arctan2(np.linalg.svd(words[i][j])[0][1][0], np.linalg.svd(words[i][j])[0][0][0])
        intervals.append(Interval(s - eps, s + eps, 0, 0, [], color))
    initial_intervals = DisconnectedInterval(intervals)
    initial_intervals.combine()
    disconnected_intervals.append(initial_intervals)

# Iterate the search on the global variable disconnected_intervals
def iterate():
    ### PATCH SEARCH ###
    # Extend a disconnected interval exactly the amount required by adding components around the images it must contain and combining
    delta = 3e-4 # Extra space just over the image

    failed = {}
    # Look at a particular L1 disconnected interval
    for l1 in list(graph.keys()):
        # Look at each disconnected interval L2 which must be contained in L1
        failed[l1] = 0
        for l2 in graph[l1]:
            # Create a new component around each component which was not contained
            for comp in disconnected_intervals[l2].components:
                if not disconnected_intervals[l1].contains_image(DisconnectedInterval([comp]), graph[l1][l2]):
                    failed[l1] += 1
                    color = disconnected_intervals[l1].components[0].color
                    x, y = graph[l1][l2] @ rp1_interval((comp.a - comp.e1) % np.pi, (comp.b + comp.e2) % np.pi)
                    b, a = np.arctan2(y,x)
                    disconnected_intervals[l1].components.append(Interval(a - delta, b + delta, 0, 0, [], color))
            disconnected_intervals[l1].combine(5e-3)
    
    for i in range(len(disconnected_intervals)):
        disconnected_intervals[i].combine()
        print(f"  Interval {i} Components: {len(disconnected_intervals[i].components)}")
        for comp in disconnected_intervals[i].components:
           print('    ', comp.a, comp.b)
        print()
    
    print('Number of failed containments', sum(failed.values()))
    return failed

# MAIN LOOP
iteration = 0
selected = -1
failed = {}
print()
print('Press any key to run the first iteration')
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            print()
            print('Iteration', iteration)
            print('Running ... ')
            failed = iterate()
            iteration += 1
            print()
            print('Press any key to run iteration', iteration)
        if event.type == pygame.MOUSEBUTTONDOWN:
            cursor = list(pygame.mouse.get_pos())
            if width * 0.04 < cursor[0] < width * 0.11 and height * 0.05 < cursor[1] < height * 0.95:
                dy = int((height * 0.95) / len(disconnected_intervals))
                selected = (cursor[1] - dy / 2) // dy

    # DRAW DEBUG WINDOW
    win.fill((255, 255, 255))

    y = int(height * 0.05)
    for i in range(len(disconnected_intervals)):
        win.blit(font.render(str(i), False, (0, 0, 0)), (width * 0.02, y - 3))
        if i == selected:
            pygame.draw.line(win, (230, 230, 230), (width * 0.04, y), (width * 0.11, y), 20)
        pygame.draw.line(win, disconnected_intervals[i].color * 255, (width * 0.05, y), (width * 0.1, y), 10)
        if failed != {}:
            win.blit(font.render(str(failed[i]), False, (255, 0, 0)), (width * 0.12, y - 3))

        pygame.draw.line(win, (200, 200, 200), (width * 0.15, y), (width * 0.95, y), 2)
        for comp in disconnected_intervals[i].components:
            start = ((width * 0.8) / np.pi) * comp.a + width * 0.15
            end = ((width * 0.8) / np.pi) * comp.b + width * 0.15
            if start < end:
                pass
                pygame.draw.line(win, disconnected_intervals[i].color * 255, (start, y), (np.ceil(end), y), 10)
            else:
                pygame.draw.line(win, disconnected_intervals[i].color * 255, (start, y), (width * 0.95, y), 10)
                pygame.draw.line(win, disconnected_intervals[i].color * 255, (width * 0.15, y), (np.ceil(end), y), 10)

        y += int((height * 0.95) / len(disconnected_intervals))

    pygame.display.update()