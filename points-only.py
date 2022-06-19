import pygame
import numpy as np
from groups import group
from colors import colors
from classes.graph_funcs import *

class Application():
    def __init__(self):
        # self.graph = group('cyclic', 2, 3)
        # self.graph = group('triangle')
        self.graph = group('surface')

        self.point_collections = []
    
    def setup(self):
        self.point_collections = []

        print('Finding starting points...')
        # words = allwords(graph, 5, 5)
        words = oneword(self.graph, 100)

        print('Setting starting points...')
        # print('words', words)
        for i in range(len(words)):
            pc = PointCollection()
            for j in range(len(words[i])):
                s = np.array([
                    [np.linalg.svd(words[i][j])[0][1][0]], 
                    [np.linalg.svd(words[i][j])[0][0][0]]
                ])
                pc.add_points(s)
            self.point_collections.append(pc)
         
        print('Setup complete')
    
    def permeate(self, steps = 1, print_counts = False, safe_terminate = True):
        ''' Get the images of all points under all actions they should be mapped by steps-many times'''
        for step in range(steps):
            for i, pc in enumerate(self.point_collections):
                collections_to_permeate_to = []
                matrices_to_permeate_by = []
                for j, edges in enumerate(self.graph.values()):
                    if i in edges.keys():
                        # print(f'{i} in {j}')
                        collections_to_permeate_to.append(self.point_collections[j])
                        matrices_to_permeate_by.append(edges[i])
                pc.permeate_to_collections(collections_to_permeate_to, matrices_to_permeate_by)
            app.get_angles()

            if print_counts:
                app.print_collections()
                app.print_point_counts()

            if safe_terminate:
                _, total_old_points = app.get_point_counts()
                if total_old_points > 5e5:
                    print('QUIT WITH SAFE TERMINATE')
                    pygame.quit()

    def get_angles(self):
        for pc in self.point_collections:
            pc.get_angles()

    def get_point_counts(self):
        total_new_points = 0
        total_old_points = 0
        for pc in self.point_collections:
            total_new_points += int(pc.new_points.size / 2)
            total_old_points += int(pc.old_points.size / 2)
        return (total_new_points, total_old_points)

    def print_collections(self):
        print()
        for i, pc in enumerate(self.point_collections):
            print('Collection', i)
            print(' New Points', int(pc.new_points.size / 2))
            print(' Old Points', int(pc.old_points.size / 2))
            print(' Angles', len(pc.angles))
        print()

    def print_point_counts(self):
        total_new_points, total_old_points = self.get_point_counts()
        print(f'New Points: {total_new_points}   Old Points: {total_old_points}')

    def draw(self, win):
        total = 0
        for i, pc in enumerate(self.point_collections):
            radius = (width * 0.9) * i / len(self.point_collections) + width * 0.1
            pygame.draw.ellipse(win, (230, 230, 230), (width/2 - radius / 2, height/2 - radius / 2, radius, radius), 1)
            for angle in pc.angles:
                pygame.draw.arc(win, colors[i] * 255, (width/2 - radius / 2, height/2 - radius / 2, radius, radius), angle * 2 - 0.03, angle * 2 + 0.03, 3)
            total += len(pc.angles)

class PointCollection():
    def __init__(self):
        # Vectors in RP1 which have yet to be permeated
        self.new_points = np.array([])

        # Vectors in RP1 which have already been permeated
        self.old_points = np.array([])

        # Values between 0 and pi
        self.angles = []

    def add_points(self, points):
        if self.new_points.size == 0:
            self.new_points = points
        else:
            self.new_points = np.append(self.new_points, points, axis = 1)

    def stash_points(self):
        if self.old_points.size == 0:
            self.old_points = self.new_points
        else:
            self.old_points = np.append(self.old_points, self.new_points, axis = 1)
        self.new_points = np.array([])

    def permeate_to_collections(self, collections, matrices):
        if self.new_points.size == 0:
            return 'No points to permeate'
        for collection, mat in zip(collections, matrices):
            randomly_permuted_new_points = np.transpose(np.random.permutation(np.transpose(self.new_points)))
            point_images = mat @ randomly_permuted_new_points[:,:10]
            collection.add_points(point_images)
        self.stash_points()

    def get_angles(self):
        if self.old_points.size == 0:
            return Exception('No points to get angles for, try using app.permeate()')
        self.angles = np.arctan2(self.old_points[0], self.old_points[1])
        # self.condense_angles()
    
    def condense_angles(self):
        if len(self.angles) == 0:
            return 'No angles to condense'
        self.angles.sort()
        
        new_angles = []
        index = 0
        while index < len(self.angles) - 1:
            if self.angles[index] + 0.3 > self.angles[index+1]:
                new_angles.append(self.angles[index])
                index += 2
            else:
                index += 1
        self.angles = new_angles

app = Application()
app.setup()

app.get_angles()
# app.print_collections()
# app.print_point_counts()

width, height = 600, 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption('TXGL Point Permeation')

count = 1
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                app.permeate(steps = 1, print_counts = False)
            
    win.fill((255, 255, 255))
    app.draw(win)
    count += 1
    # print(count)
    pygame.display.update()