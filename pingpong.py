import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Arc

from interval_funcs import *
from group_funcs import *
from intervals import Interval

class PingPong():
    def __init__(self, generators, graph = None):
        self.generators = generators
        self.graph = graph
        if graph == None:
            self.graph = free_group_graph(len(generators))
        self.intervals = []
        # self.epsilons = [0 for i in range(2 * len(generators))]

    def create_intervals(self, generators, initial_size = 1e-9):
        # Find theta for eigenvectors on S1 via RP1 -> S1
        # Create interval objects with initial values around eigenvectors

        letters = []
        for g in generators:
            letters += [g]
            letters += [np.linalg.inv(g)]
        
        # Blue, Red, Green, Yellow, Cyan, Magenta
        colors = [np.array([0,0,1]), np.array([1,0,0]), np.array([0,1,0]), np.array([1,0,1]), np.array([0,1,1]), np.array([1,1,0])]
        intervals = []
        iter = 0
        for mat in generators:
            # Eigenvalues
            #print(np.linalg.eig(mat)[0])

            e1 = np.arctan2(np.linalg.eig(mat)[1][1][0], np.linalg.eig(mat)[1][0][0])
            e2 = np.arctan2(np.linalg.eig(mat)[1][1][1], np.linalg.eig(mat)[1][0][1])

            if np.linalg.eig(mat)[0][0] > 1:
                intervals.append(Interval(e1 - initial_size, e1 + initial_size, -(iter + 1), mat, letters, colors[iter]))
                intervals.append(Interval(e2 - initial_size, e2 + initial_size, (iter + 1), np.linalg.inv(mat), letters, colors[iter] * 0.5))
            else:
                intervals.append(Interval(e1 - initial_size, e1 + initial_size, (iter + 1), np.linalg.inv(mat), letters, colors[iter] * 0.5))
                intervals.append(Interval(e2 - initial_size, e2 + initial_size, -(iter + 1), mat, letters, colors[iter]))

            iter += 1
        return intervals

    def check_containment(self):
        containment = True
        for interval in self.intervals:
            for other in self.intervals:
                if other.name in self.graph[interval.name]:
                    containment = containment and interval.contains_image(other)
        return containment

    def find_intervals(self, steps = 10, geo = 0.1, terminate_search = False):
        # Initialize intervals with initial_size diameter
        self.intervals = self.create_intervals(self.generators)

        # Find which intervals lie on the left and right of each interval
        for interval in self.intervals:
            interval.nearest_endpoints(self.intervals)

        # Display nearest intervals for debug
        '''for interval in self.intervals:
            print(interval.a, interval.b)
            print('NEAREST TO A', interval.nearest_interval_a.a, interval.nearest_interval_a.b)
            print('NEAREST TO B', interval.nearest_interval_b.a, interval.nearest_interval_b.b)
            print()'''

        # Geometric expansion factor (must be <0.5)
        # (expand epsilon by the max distance it could expand times geo)
        iter = 0
        while iter < steps:
            for interval in self.intervals:
                # a_dist, b_dist = interval.nearest_endpoint_dists(self.intervals)
                a_dist = angle_dist(interval.a - interval.e1, interval.nearest_interval_a.b + interval.nearest_interval_a.e2)
                b_dist = angle_dist(interval.b + interval.e2, interval.nearest_interval_b.a - interval.nearest_interval_b.e1)
                interval.e1 += a_dist * geo
                interval.e2 += b_dist * geo
            if self.check_containment() and terminate_search:
                break
            iter += 1

        # Check orders of 'ladders' based on eigenvalues

    def draw_intervals(self):
        fig, ax = plt.subplots(figsize = (5, 5))

        # Plot data
        ax.set_xlim((-1.2, 1.2))
        ax.set_ylim((-1.2, 1.2))
        ax.axis("off")
        ax.set_aspect("equal")

        # RP1
        rp1 = Circle((0,0), 1.0, fill = False)
        ax.add_patch(rp1)

        for interval in self.intervals:
            interval.draw(ax)
            '''print((interval.a - interval.e1) % np.pi, (interval.b + interval.e2) % np.pi)
            print(interval.nearest_endpoint_dists(self.intervals))
            print()'''
        for interval in self.intervals:
            interval.draw_image(ax)

        if self.check_containment():
            print('Intervals are valid for Ping Pong!')
        else:
            print('Ping Pong intervals not found.')
            with open(os.path.dirname(__file__) + '\error_log.txt', 'a') as error_log:
                error_log.write('\n')
                error_log.write(str(self.generators))
                error_log.write('\n')

        plt.show()