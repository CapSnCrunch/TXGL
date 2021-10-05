import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Arc

from interval_funcs import *

class Interval():
    def __init__(self, a, b, name, mat, letters, color):
        self.a = a % np.pi
        self.b = b % np.pi
        self.e1 = 0
        self.e2 = 0

        self.name = name
        self.mat = mat
        self.color = color
        self.letters = letters

        self.nearest_interval_a = None
        self.nearest_interval_b = None

    def draw(self, ax):
        # Draw the interval
        theta2, theta1 = get_arc_params(rp1_interval((self.a - self.e1) % np.pi, (self.b + self.e2) % np.pi))
        ax.add_patch(Arc((0,0), 2., 2., theta1=theta1, theta2=theta2, color=self.color, linewidth=10))

    def draw_image(self, ax):
        # Draw image of the interval under all letters except inv(self.mat)
        I = rp1_interval((self.a - self.e1) % np.pi, (self.b + self.e2) % np.pi)
        for mat in self.letters:
            if not np.allclose(mat, np.linalg.inv(self.mat)):
                theta2, theta1 = get_arc_params(mat @ I)
                ax.add_patch(Arc((0,0), 2., 2., theta1=theta1, theta2=theta2, color='orange', linewidth=7))

    def contains_image(self, other):
        # Check if interval contains the image of another interval
        ta = 360

        # Get interval we want to take the image of as a pair of vectors
        I = rp1_interval(other.a - other.e1, other.b + other.e2)

        # Find the angles vectors occur at in order to compare
        b, a = get_arc_params(rp1_interval(self.a - self.e1, self.b + self.e2))
        d, c = get_arc_params(self.mat @ I)

        '''a, b = (self.a - self.e1) % ta, (self.b + self.e2) % ta
        c, d = (other.a - other.e1) % ta, (other.b + other.e2) % ta'''
        if a > b:
            if c > d:
                return d < b and a < c
            else:
                if c < b:
                    return d < b and a < (c + ta)
                else:
                    return (d - ta) < b and a < c
        else:
            if c > d:
                return False
            else:    
                return a < c and d < b

    def intersects(self, other):
        # Check if interval intersects another interval
        return self.a < other.a < self.b or self.a < other.b < self.b

    def nearest_endpoints(self, intervals):
        # Find the intervals which are closest to self.a and self.b and assign them to
        # nearest_interval_a and nearest_interval_b respectively for later use in expansion
        a, b = (self.a - self.e1) % np.pi, (self.b + self.e2) % np.pi
        searching = True
        eps = 1e-5
        i = eps
        while searching:
            for interval in intervals:
                if self != interval:
                    other_b = (interval.b + interval.e2) % np.pi
                    if angle_dist(a - i, other_b) <= eps:
                        self.nearest_interval_a = interval
                        interval.nearest_interval_b = self
                        searching = False
                        break
            if i >= np.pi:
                break
            i += eps