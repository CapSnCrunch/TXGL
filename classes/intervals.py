import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Arc
from classes.interval_funcs import *

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

    def contains(self, other):
        '''Check if intervals contains another interval'''
        ta = 360

        # Find the angles vectors occur at in order to compare
        b, a = get_arc_params(rp1_interval(self.a - self.e1, self.b + self.e2))
        d, c = get_arc_params(rp1_interval(other.a - other.e1, other.b + other.e2))

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

    def contains_image(self, other):
        # Check if interval contains the image of another interval
        ta = 360

        # Get interval we want to take the image of as a pair of vectors
        I = rp1_interval(other.a - other.e1, other.b + other.e2)

        # Find the angles vectors occur at in order to compare
        b, a = get_arc_params(rp1_interval(self.a - self.e1, self.b + self.e2))
        #d, c = get_arc_params(self.mat @ I)
        d, c = get_arc_params(other.mat @ I)

        print(' ', b, a, d, c)

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

class DisconnectedInterval():
    def __init__(self, components = []):
        self.components = components

    def draw(self, ax):
        for comp in self.components:
            comp.draw(ax)

    def draw_image(self, ax):
        for comp in self.components:
            comp.draw_image(ax)

    def combine(self):
        '''Combine / reduce intervals if they are overlapping
            (assumes that all intervals have the same name, mat, color) '''
        '''for i in range(len(self.components)):
            comp1 = self.components[i]
            comp2 = self.components[(i+1) % len(self.components)]
            if comp1.intersects(comp2):
                comp1.a = min(comp1.a, comp2.a)
                comp1.b = max(comp1.b, comp2.b)'''
        
        index = 0
        while index < len(self.components):
            comp1 = self.components[index]
            comp2 = self.components[(index + 1) % len(self.components)]
            if comp1.intersects(comp2):
                comp1.a = min(comp1.a, comp2.a)
                comp1.b = max(comp1.b, comp2.b)
                self.components = self.components[:index+1] + self.components[index+2:]
                index -= 1
            index += 1

    def contains(self, other):
        '''Check if interval contains another disconnected interval'''
        self.combine()
        other.combine()
        for comp2 in other.components:
            contained = False
            for comp1 in self.components:
                if comp1.contains(comp2):
                    contained = True
                    break
            if not contained:
                return False
        return True
    
    def contains_image(self, other):
        self.combine()
        other.combine()
        for comp2 in other.components:
            contained = False
            for comp1 in self.components:
                if comp1.contains_image(comp2):
                    print(' component contained')
                    contained = True
                    break
            if not contained:
                return False
        return True
        
    def sort(self):
        #TODO sort the intervals in order from 'left to right'
        pass

if __name__ == '__main__':
    i1 = Interval(0, 0.2, 0, 0, [], np.array([1,0,0]))
    i2 = Interval(0.3, 0.4, 1, 0, [], np.array([1,0,0]))
    i3 = Interval(0.35, 0.75, 2, 0, [], np.array([1,0,0]))
    i4 = Interval(0.7, 1, 2, 0, [], np.array([1,0,0]))
    di = DisconnectedInterval([i1, i2, i3, i4])

    j1 = Interval(0.1, 0.19, 0, 0, [], np.array([0,0,1]))
    j2 = Interval(0.7, 0.8, 2, 0, [], np.array([0,0,1]))
    dj = DisconnectedInterval([j1, j2])

    print(di.contains(dj))
    print(len(di.components))
    print(len(dj.components))

    ### DRAW INTERVALS ###
    fig, ax = plt.subplots(figsize = (5, 5))

    # Plot data
    ax.set_xlim((-1.2, 1.2))
    ax.set_ylim((-1.2, 1.2))
    ax.axis('off')
    ax.set_aspect('equal')

    # RP1
    rp1 = Circle((0,0), 1.0, fill = False)
    ax.add_patch(rp1)

    # Disconnected Interval
    di.draw(ax)
    dj.draw(ax)

    plt.show()