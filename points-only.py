from multiprocessing.dummy import Array
import pygame
import numpy as np
from sympy import Point
from groups import group
from classes.group_funcs import *
from classes.graph_funcs import *

class Application():
    def __init__(self, width = 600, height = 400):
        # self.win = pygame.display.set_mode((width, height))
        # pygame.display.set_caption('TXGL Point Permeation')

        self.graph = group('triangle')
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
    
    def permeate(self):
        for i, pc in enumerate(self.point_collections):
            collections_to_permeate_to = []
            matrices_to_permeate_by = []
            for j, edges in enumerate(self.graph.values()):
                if i in edges.keys():
                    # print(f'{i} in {j}')
                    collections_to_permeate_to.append(self.point_collections[j])
                    matrices_to_permeate_by.append(edges[i])
            pc.permeate_to_collections(collections_to_permeate_to, matrices_to_permeate_by)

    def print_collections(self):
        for i, pc in enumerate(self.point_collections):
            print('Collection', i)
            print(' New Points', pc.new_points)
            print(' Old Points', pc.old_points)

    def print_point_counts(self):
        total_new_points = 0
        total_old_points = 0
        for pc in self.point_collections:
            total_new_points += int(pc.new_points.size / 2)
            total_old_points += int(pc.old_points.size / 2)
        print(f'New Points: {total_new_points}   Old Points: {total_old_points}')

class PointCollection():
    def __init__(self):
        # Vectors in RP1 which have yet to be permeated
        self.new_points = np.array([])

        # Vectors in RP1 which have already been permeated
        self.old_points = np.array([])

        # # Values between 0 and pi
        # self.angles = []

    # def add_point_from_angle(self, angle):
    #     self.angles.append(angle)

    #     point = np.array([
    #         [np.cos(angle)],
    #         [np.sin(angle)]
    #     ])

    #     if self.new_points.size == 0:
    #         self.new_points = point
    #     else:
    #         self.new_points = np.append(self.new_points, point, axis = 0)

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
            point_images = mat @ self.new_points
            collection.add_points(point_images)
        self.stash_points()

app = Application()
app.setup()

app.print_point_counts()
for i in range(15):
    app.permeate()
    app.print_point_counts()