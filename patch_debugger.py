from tempfile import tempdir
import pygame
from matplotlib.pyplot import disconnect
from classes.intervals import *
from classes.interval_funcs import *
from classes.group_funcs import *
from classes.graph_funcs import *
from colors import colors

### CREATE DEBUGGER WINDOW ###
width, height = 1000, 400
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
# A = np.array([[ 0.923879532511287, -0.217284326304659],
#                [-0.673986071141597, -0.923879532511287]])
# B = np.array([[0.,                1.219308768593441],
#                [0.820136806818482, 0.               ]])
# C = np.array([[ 0.923879532511287,  0.21728432630466 ],
#                [ 0.673986071141597, -0.923879532511286]])

# graph = {0: {},
#             1: {4: B, 5: C},
#             2: {6: A, 7: C},
#             3: {8: A, 9: B},
#             4: {10: A, 7: C},
#             5: {11: A, 9: B},
#             6: {1: B, 5: C},
#             7: {8: A, 12: B},
#             8: {4: B, 13: C},
#             9: {6: A, 12: C},
#             10: {14: C},
#             11: {4: B, 15: C},
#             12: {16: A},
#             13: {16: A, 9: B},
#             14: {11: A, 12: B},
#             15: {17: B},
#             16: {10: B, 13: C},
#             17: {10: A, 12: C}}

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
    delta = 5e-2 # Extra space just over the image (3e-4)

    failed = {}
    # Look at a particular L1 disconnected interval
    for l1 in list(graph.keys()):
        # Look at each disconnected interval L2 which must be contained in L1
        failed[l1] = []
        for l2 in graph[l1]:
            # Create a new component around each component which was not contained
            for comp in disconnected_intervals[l2].components:
                if not disconnected_intervals[l1].contains_image(DisconnectedInterval([comp]), graph[l1][l2]):
                    failed[l1] += [(l2, comp)]
                    color = disconnected_intervals[l1].components[0].color
                    x, y = graph[l1][l2] @ rp1_interval((comp.a - comp.e1) % np.pi, (comp.b + comp.e2) % np.pi)
                    a, b = np.arctan2(y,x)
                    disconnected_intervals[l1].components.append(Interval(a - delta, b + delta, 0, 0, [], color))
            disconnected_intervals[l1].combine(3e-2) # (5e-2)
    
    for i in range(len(disconnected_intervals)):
        disconnected_intervals[i].combine()
        print(f"  Interval {i} Components: {len(disconnected_intervals[i].components)}")
        for comp in disconnected_intervals[i].components:
           print('    ', comp.a, comp.b)
        print()
    
    total = 0
    for i in range(len(failed)):
        total += len(failed[i])
    if total == 0:
        print('FOUND VALID INTERVALS')
    else:
        print('Number of failed containments', total)
    return failed

# MAIN LOOP
iteration = 0
selected = -1
selected_error = None
failed = {}
print()
print('Press SPACE to run the first iteration')
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print()
                print('Iteration', iteration)
                print('Running ... ')
                failed = iterate()
                iteration += 1
                print()
                print('Press SPACE to run iteration', iteration)
            elif selected_error != None:
                for i, comp in failed[selected]:
                    if selected_error == None or selected_error == comp:
                        # Draw the failed image of that component in the selected interval
                        x, y = graph[selected][i] @ rp1_interval((comp.a - comp.e1) % np.pi, (comp.b + comp.e2) % np.pi)
                        a, b = np.arctan2(y, x) # b, a?
                        a, b = a % np.pi, b % np.pi

                        print('  IMAGE OF FAILED COMPONENT', a, b)
                    
                        print('  SHOULD BE CONTAINED IN')
                        for comp2 in disconnected_intervals[selected].components:
                            print('    ', comp2.a, comp2.b)
                
        if event.type == pygame.MOUSEBUTTONDOWN:
            cursor = list(pygame.mouse.get_pos())
            print(selected, selected_error)
            h = int(height * 0.05)
            dh = int((height * 0.95) / len(disconnected_intervals))
            if width * 0.04 < cursor[0] < width * 0.11 and height * 0.05 < cursor[1] < height * 0.95:
                selected = (cursor[1] - 8) // dh
                selected_error = None
                #if failed != {}:
                #    print(failed[selected])
            elif selected != -1 and failed != {}:
                # Check if we are selecting a particular image
                deselect = True
                for i, comp in failed[selected]:
                    start = ((width * 0.75) / np.pi) * comp.a + width * 0.15
                    end = ((width * 0.75) / np.pi) * comp.b + width * 0.15
                    if start < end and (start - 2) < cursor[0] < (end + 2) and (h + dh*i - 10) < cursor[1] < (h + dh*i + 10):
                        selected_error = comp
                        deselect = False
                    elif end < start and (width * 0.15 < cursor[0] < (end + 2) or (start + 2) < cursor[0] < (width * 0.75)) and (h + dh*i - 10) < cursor[1] < (h + dh*i + 10):
                        selected_error = comp
                        deselect = False
                if deselect == True and selected_error != None:
                    selected_error = None
                elif deselect == True and selected_error == None:
                    selected = -1

    # DRAW DEBUG WINDOW
    win.fill((255, 255, 255))

    h = int(height * 0.05)
    dh = int((height * 0.95) / len(disconnected_intervals))
    for i in range(len(disconnected_intervals)):
        # Interval Indicators
        win.blit(font.render(str(i), False, (0, 0, 0)), (width * 0.02, h + dh*i - 3))
        if i == selected:
            pygame.draw.line(win, (230, 230, 230), (width * 0.04, h + dh*i), (width * 0.11, h + dh*i), 20)
        pygame.draw.line(win, disconnected_intervals[i].color * 255, (width * 0.05, h + dh*i), (width * 0.1, h + dh*i), 10)
        if failed != {}:
            win.blit(font.render(str(len(failed[i])), False, (255, 0, 0)), (width * 0.12, h + dh*i - 3))

        # Interval Components
        pygame.draw.line(win, (200, 200, 200), (width * 0.15, h + dh*i), (width * 0.9, h + dh*i), 1 + (selected == i) * 2)
        for comp in disconnected_intervals[i].components:
            start = ((width * 0.75) / np.pi) * comp.a + width * 0.15
            end = ((width * 0.75) / np.pi) * comp.b + width * 0.15
            if start < end:
                pygame.draw.line(win, disconnected_intervals[i].color * 255, (np.floor(start), h + dh*i), (np.ceil(end), h + dh*i), 10)
            else:
                pygame.draw.line(win, disconnected_intervals[i].color * 255, (np.floor(start), h + dh*i), (width * 0.9, h + dh*i), 10)
                pygame.draw.line(win, disconnected_intervals[i].color * 255, (width * 0.15, h + dh*i), (np.ceil(end), h + dh*i), 10)
        
        # Number of Components
        win.blit(font.render(str(len(disconnected_intervals[i].components)), False, (0, 0, 0)), (width * 0.95, h + dh*i - 3))
        
    if selected != -1 and failed != {}:
        for i, comp in failed[selected]:
            alpha = 0.5
            if selected_error == None or selected_error == comp:
                alpha = 1
                
            # Draw the original component whose image failed to be in the selected interval
            start = ((width * 0.75) / np.pi) * comp.a + width * 0.15
            end = ((width * 0.75) / np.pi) * comp.b + width * 0.15
            if start < end:
                pygame.draw.line(win, (255, 0, 0, alpha), (np.floor(start), h + dh*i), (np.ceil(end), h + dh*i), 15)
            else:
                pygame.draw.line(win, (255, 0, 0, alpha), (np.floor(start), h + dh*i), (width * 0.9, h + dh*i), 15)
                pygame.draw.line(win, (255, 0, 0, alpha), (width * 0.15, h + dh*i), (np.ceil(end), h + dh*i), 15)
            
            if selected_error == None or selected_error == comp:
                # Draw the failed image of that component in the selected interval
                x, y = graph[selected][i] @ rp1_interval((comp.a - comp.e1) % np.pi, (comp.b + comp.e2) % np.pi)
                a, b = np.arctan2(y, x) # b, a?
                a, b = a % np.pi, b % np.pi

                start = ((width * 0.75) / np.pi) * a + width * 0.15
                end = ((width * 0.75) / np.pi) * b + width * 0.15

                if start < end:
                    pygame.draw.line(win, (150, 0, 0), (np.floor(start), h + dh*selected), (np.ceil(end), h + dh*selected), 5)
                else:
                    pygame.draw.line(win, (150, 0, 0), (np.floor(start), h + dh*selected), (width * 0.9, h + dh*selected), 5)
                    pygame.draw.line(win, (150, 0, 0), (width * 0.15, h + dh*selected), (np.ceil(end), h + dh*selected), 5)

    pygame.display.update()