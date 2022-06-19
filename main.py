from select import select
from tempfile import tempdir
import pygame
from matplotlib.pyplot import disconnect
from classes.intervals import *
from classes.interval_funcs import *
from classes.group_funcs import *
from classes.graph_funcs import *
from groups import group
from colors import colors

### CREATE DEBUGGER WINDOW ###
width, height = 1000, 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption('TXGL Patch Search Debugger')

pygame.font.init()
font = pygame.font.SysFont('Roboto', 18)
titleFont = pygame.font.SysFont('Roboto', 25)

### GET REPRESENTATION ###
graph = group('surface')

print('Finding interval starting points...')
# words = allwords(graph, 3, 3)
words = oneword(graph, 100)
print('Initializing intervals...')

# CREATE INITIAL INTERVALS OF SIZE eps
eps = 5e-4
disconnected_intervals = []
print('words', words)
for i in range(len(words)):
    intervals = []
    color = colors[i]
    for j in range(len(words[i])):
        s = np.arctan2(np.linalg.svd(words[i][j])[0][1][0], np.linalg.svd(words[i][j])[0][0][0])
        intervals.append(Interval(s - eps, s + eps, color))
    initial_intervals = DisconnectedInterval(intervals, color)
    initial_intervals.combine()
    disconnected_intervals.append(initial_intervals)

print('Intervals created.')

# Get the current failing images
def get_failures():
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
    return failed

def expand_interval(n, delta = 5e-3, debug = False):
    '''Expand the n-th inteverval by exactly enough to contain all of its necessary images'''
    '''
        n: Index of interval in disconnected_intervals to expand
        delta: Padding on patches over images
    '''
    print('num components before', len(disconnected_intervals[n].components))
    print('MAKING PATCHES')
    new_components = []
    for l2 in graph[n]:
        # Create a new component around each component which was not contained
        for comp in disconnected_intervals[l2].components:
            if not disconnected_intervals[n].contains_image(DisconnectedInterval([comp]), graph[n][l2]):
                image = comp.get_image(graph[n][l2])
                image.a -= delta
                image.b += delta    
                new_components.append(image)
                print('  ('+str(image.a), str(image.b)+')')
    disconnected_intervals[n].components += new_components
    print('num components after', len(disconnected_intervals[n].components))
    disconnected_intervals[n].combine(3e-2, debug) # (5e-2)
    print()

# Iterate the search on the global variable disconnected_intervals
def iterate():
    ### PATCH SEARCH ###
    ''' Extend a disconnected interval exactly the amount required by adding components around the images it must contain and combining'''
    '''
        n: Index of interval in disconnected_intervals to expand
        delta: Padding on patches over images
    '''
    delta = 1e-2 # Extra space just over the image (3e-4)

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
                    image = comp.get_image(graph[l1][l2])
                    image.a -= delta
                    image.b += delta
                    disconnected_intervals[l1].components.append(image)
            disconnected_intervals[l1].combine(3e-2) # (5e-2)
    
    total = 0
    for i in range(len(failed)):
        total += len(failed[i])
    if total == 0:
        print('FOUND VALID INTERVALS')
    else:
        print('Number of failed containments', total)

# MAIN LOOP
iteration = 0
selected_interval = -1
selected_failure = -1
selected_error = None
failed = get_failures()
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

                iterate()
                failed = get_failures()
                iteration += 1

                print()
                print('Press SPACE to run iteration', iteration)
                
            elif event.key == pygame.K_e and selected_failure != -1:
                expand_interval(selected_failure)
                failed = get_failures()

            elif event.key == pygame.K_d and selected_failure != -1:
                expand_interval(selected_failure, debug = True)
                failed = get_failures()

            elif event.key == pygame.K_UP and selected_failure != -1:
                print('COMPONENTS OF INTERVAL', selected_failure)
                for i, comp in enumerate(disconnected_intervals[selected_failure].components):
                    print(' ', i, ' (' + str(comp.a) + ',', str(comp.b) + ')')
                print('FAILED TO CONTAIN')
                for i, comp in enumerate(failed[selected_failure]):
                    print(' ', i, ' (' + str(comp[1].a) + ',', str(comp[1].b) + ')')
                print()

            elif event.key == pygame.K_DOWN and selected_error != None:
                for i, comp in failed[selected_failure]:
                    if selected_error == None or selected_error == comp:
                        # Draw the failed image of that component in the selected interval
                        # x, y = graph[selected][i] @ rp1_interval((comp.a - comp.e1) % np.pi, (comp.b + comp.e2) % np.pi)
                        # b, a = np.arctan2(y, x) # b, a?
                        # a, b = a % np.pi, b % np.pi

                        image = comp.get_image(graph[selected_failure][i])

                        print('  IMAGE OF FAILED COMPONENT', image.a, image.b)
                    
                        print('  SHOULD BE CONTAINED IN')
                        for comp2 in disconnected_intervals[selected_failure].components:
                            print('    ', comp2.a, comp2.b)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            cursor = list(pygame.mouse.get_pos())
            h = int(height * 0.1)
            dh = int((height * 0.80) / len(disconnected_intervals))
            if width * 0.04 < cursor[0] < width * 0.11 and height * 0.1 - dh/2 < cursor[1] < height * 0.9:
                selected_interval = int((cursor[1] - height * 0.1 + dh/2) // dh)
                selected_failure = -1
                selected_error = None
            if width * 0.11 < cursor[0] < width * 0.14 and height * 0.1 - dh/2 < cursor[1] < height * 0.9:
                selected_interval = -1
                selected_failure = int((cursor[1] - height * 0.1 + dh/2) // dh)
                selected_error = None
            elif selected_failure != -1 and failed != {}:
                # Check if we are selecting a particular image
                deselect = True
                for i, comp in failed[selected_failure]:
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
                    selected_failure = -1

    # DRAW DEBUG WINDOW
    win.fill((255, 255, 255))

    # TITLE
    title = titleFont.render('Texas Experimental Geometry Lab', False, (0, 0, 0))
    title_rect = title.get_rect(center=(width * 0.50, height * 0.03))
    win.blit(title, title_rect)

    sub_title = font.render('Ping Pong with Automatic Structures', False, (0, 0, 0))
    sub_title_rect = sub_title.get_rect(center=(width * 0.50, height * 0.07))
    win.blit(sub_title, sub_title_rect)

    # INTERVALS
    h = int(height * 0.1)
    dh = int((height * 0.80) / len(disconnected_intervals))
    for i in range(len(disconnected_intervals)):
        # Interval Indicators
        win.blit(font.render(str(i), False, (0, 0, 0)), (width * 0.02, h + dh*i - 3))
        if i == selected_interval:
            pygame.draw.line(win, (230, 230, 230), (width * 0.04, h + dh*i), (width * 0.11, h + dh*i), 20)
        if i == selected_failure:
            pygame.draw.circle(win, (250, 200, 200), (width * 0.122, h + dh*(selected_failure) + 2), 10)
        pygame.draw.line(win, disconnected_intervals[i].color * 255, (width * 0.05, h + dh*i), (width * 0.1, h + dh*i), 10)

        # Number of Failures
        if failed != {}:
            win.blit(font.render(str(len(failed[i])), False, (255, 0, 0)), (width * 0.12, h + dh*i - 3))

        # Interval Components
        pygame.draw.line(win, (200, 200, 200), (width * 0.15, h + dh*i), (width * 0.9, h + dh*i), 1 + (selected_failure == i) * 2)
        for comp in disconnected_intervals[i].components:
            start = ((width * 0.75) / np.pi) * comp.a + width * 0.15
            end = ((width * 0.75) / np.pi) * comp.b + width * 0.15
            if start < end:
                pygame.draw.line(win, disconnected_intervals[i].color * 255, (np.floor(start), h + dh*i), (np.ceil(end), h + dh*i), 10)
            else:
                pygame.draw.line(win, disconnected_intervals[i].color * 255, (np.floor(start), h + dh*i), (width * 0.9, h + dh*i), 10)
                pygame.draw.line(win, disconnected_intervals[i].color * 255, (width * 0.15, h + dh*i), (np.ceil(end), h + dh*i), 10)
            pygame.draw.line(win, disconnected_intervals[i].color * 255, (np.floor(start), h + dh*i), (np.floor(start)+1, h + dh*i), 14)
            pygame.draw.line(win, disconnected_intervals[i].color * 255, (np.ceil(end) + 1, h + dh*i), (np.ceil(end), h + dh*i), 14)
        
        # Number of Components
        win.blit(font.render(str(len(disconnected_intervals[i].components)), False, (0, 0, 0)), (width * 0.95, h + dh*i - 3))
    
    # SELECTED INTERVAL (DRAW THE IMAGES OF THE CURRENT INTERVAL)
    if selected_interval != -1:
        # Get which intervals the selected interval maps into
        map_locations = []
        for vertex, edges in graph.items():
            if selected_interval in list(edges.keys()):
                map_locations.append(vertex)
        
        color = disconnected_intervals[selected_interval].color * 255
        for i in map_locations:
            for comp in disconnected_intervals[selected_interval].components:
                image = comp.get_image(graph[i][selected_interval])

                start = ((width * 0.75) / np.pi) * image.a + width * 0.15
                end = ((width * 0.75) / np.pi) * image.b + width * 0.15

                if start < end:
                    pygame.draw.line(win, color * 0.5, (np.floor(start), h + dh*i), (np.ceil(end), h + dh*i), 5)
                else:
                    pygame.draw.line(win, color * 0.5, (np.floor(start), h + dh*i), (width * 0.9, h + dh*i), 5)
                    pygame.draw.line(win, color * 0.5, (width * 0.15, h + dh*i), (np.ceil(end), h + dh*i), 5)
                pygame.draw.line(win, color * 0.5, (np.floor(start), h + dh*i), (np.floor(start)+1, h + dh*i), 7)
                pygame.draw.line(win, color * 0.5, (np.ceil(end) + 1, h + dh*i), (np.ceil(end), h + dh*i), 7)

    # SELECTED FAILURE (DRAW WHICH IMAGES SHOULD HAVE BEEN CONTAINED)
    if selected_failure != -1 and failed != {}:
        for i, comp in failed[selected_failure]:
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
            pygame.draw.line(win, (255, 0, 0), (np.floor(start), h + dh*i), (np.floor(start)+1, h + dh*i), 17)
            pygame.draw.line(win, (255, 0, 0), (np.ceil(end) + 1, h + dh*i), (np.ceil(end), h + dh*i), 17)
            
            if selected_error == None or selected_error == comp:
                # Draw the failed image of that component in the selected interval
                # x, y = graph[selected][i] @ rp1_interval((comp.a - comp.e1) % np.pi, (comp.b + comp.e2) % np.pi)
                # b, a = np.arctan2(y, x) # b, a?
                # a, b = a % np.pi, b % np.pi

                image = comp.get_image(graph[selected_failure][i])

                start = ((width * 0.75) / np.pi) * image.a + width * 0.15
                end = ((width * 0.75) / np.pi) * image.b + width * 0.15

                if start < end:
                    pygame.draw.line(win, (150, 0, 0), (np.floor(start), h + dh*selected_failure), (np.ceil(end), h + dh*selected_failure), 5)
                else:
                    pygame.draw.line(win, (150, 0, 0), (np.floor(start), h + dh*selected_failure), (width * 0.9, h + dh*selected_failure), 5)
                    pygame.draw.line(win, (150, 0, 0), (width * 0.15, h + dh*selected_failure), (np.ceil(end), h + dh*selected_failure), 5)
                pygame.draw.line(win, (150, 0, 0), (np.floor(start), h + dh*selected_failure), (np.floor(start)+1, h + dh*selected_failure), 7)
                pygame.draw.line(win, (150, 0, 0), (np.ceil(end) + 1, h + dh*selected_failure), (np.ceil(end), h + dh*selected_failure), 7)

    # INTERVAL COMPONENT VALUES
    if selected_interval != -1 or selected_failure != -1:
        # Display which interval is selected and what it maps into
        map_locations = []
        for vertex, edges in graph.items():
            if max(selected_interval, selected_failure) in list(edges.keys()):
                map_locations.append(vertex)
        map_string = ''
        for i, n in enumerate(map_locations):
            if i < len(map_locations) - 2:
                map_string += f'{n}, '
            elif i == len(map_locations) - 2:
                map_string += f'{n}, and '
            else:
                map_string += f'{n}'
        if map_string == '':
            map_string = 'nothing'
        win.blit(titleFont.render(f'Interval {max(selected_interval, selected_failure)}', False, (0, 0, 0)), (width * 0.02, height * 0.9))
        win.blit(font.render(f'maps into {map_string}', False, (0, 0, 0)), (width * 0.12, height * 0.905))
    
        # Display the interval components

    else:
        win.blit(titleFont.render('No Interval Selected', False, (0, 0, 0)), (width * 0.02, height * 0.9))

    pygame.display.update()