import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Arc
from classes.interval_funcs import *

class Interval():
    def __init__(self, a, b, name, mat, letters, color):
        # TODO We can probably get rid of e1, e2, mat, and letters
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
        '''Draw the interval'''
        theta2, theta1 = get_arc_params(rp1_interval((self.a - self.e1) % np.pi, (self.b + self.e2) % np.pi))
        print('drawing between', theta1, theta2)
        ax.add_patch(Arc((0,0), 2., 2., theta1 = theta1, theta2 = theta2, color = self.color, linewidth=10))

    def draw_image(self, ax, mat):
        '''Draw image of the interval under mat'''
        I = rp1_interval((self.a - self.e1) % np.pi, (self.b + self.e2) % np.pi)
        '''for mat in self.letters:
            if not np.allclose(mat, np.linalg.inv(self.mat)):
                theta2, theta1 = get_arc_params(mat @ I)
                ax.add_patch(Arc((0,0), 2., 2., theta1=theta1, theta2=theta2, color='orange', linewidth=7))'''
        if np.linalg.det(mat) < 0:
            theta1, theta2 = get_arc_params(mat @ I)
        else:
            theta2, theta1 = get_arc_params(mat @ I)
        print('drawing image between',theta1, theta2)
        ax.add_patch(Arc((0,0), 2., 2., theta1 = theta1, theta2 = theta2, color = (self.color + 1)/2, linewidth = 7))

    def get_image(self, mat):
        '''Get image of interval under a given matrix, return the new interval'''
        x, y = mat @ rp1_interval((self.a - self.e1) % np.pi, (self.b + self.e2) % np.pi)

        if np.linalg.det(mat) < 0:
            b, a = np.arctan2(y, x)
            a, b = a % np.pi, b % np.pi
        else:
            a, b = np.arctan2(y, x)
            a, b = a % np.pi, b % np.pi
        # return (a, b)
        return Interval(a, b, 0, 0, [], self.color)

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

    def contains_image(self, other, mat):
        '''Check if mat @ other contained in self'''
        ta = 360

        #print(' ', self.b, self.a, other.b, other.a)

        # Get interval we want to take the image of as a pair of vectors
        I = rp1_interval(other.a - other.e1, other.b + other.e2)

        # Find the angles vectors occur at in order to compare
        b, a = get_arc_params(rp1_interval(self.a - self.e1, self.b + self.e2))
        
        if np.linalg.det(mat) < 1:
            c, d = get_arc_params(mat @ I)
        else:
            d, c = get_arc_params(mat @ I)

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

    def intersects(self, other, reach = 0):
        '''Check if interval intersects another interval with +- reach padding'''
        return (self.a - reach) < other.a < (self.b + reach) or (self.a - reach) < other.b < (self.b + reach)

    def nearest_endpoints(self, intervals):
        '''Find the intervals which are closest to self.a and self.b and assign them to
            nearest_interval_a and nearest_interval_b respectively for later use in expansion'''
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
    
    def __str__(self):
        return str(self.a) + ' ' + str(self.b)

class DisconnectedInterval():
    def __init__(self, components = []):
        self.components = components
        if len(components) > 0:
            self.color = components[0].color
        else:
            self.color = np.array([0, 0, 1])
        #self.sort()

    def draw(self, ax):
        '''Draw the disconnected interval'''
        for comp in self.components:
            comp.draw(ax)

    def draw_image(self, ax, mat):
        '''Draw the image of disconnected interval under mat'''
        for comp in self.components:
            comp.draw_image(ax, mat)

    def combine(self, reach = 0):
        '''Combine / reduce intervals if they are overlapping
            (assumes that all intervals have the same name, mat, color)
            Will combine intervals if the gap between them is at most 'reach' '''

        self.sort() # Sort components into clockwise order

        index = 0 # TODO FIX (infinite loop when A, B not conjugated)
        while index < len(self.components) and len(self.components) > 1:
            comp1 = self.components[index]
            comp2 = self.components[(index + 1) % len(self.components)]
            if comp1.intersects(comp2, reach):
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
    
    def contains_image(self, other, mat):
        '''Check if mat @ other is contained in self'''
        self.combine()
        other.combine()
        for comp2 in other.components:
            contained = False
            for comp1 in self.components:
                if comp1.contains_image(comp2, mat):
                    contained = True
                    break
            if not contained:
                return False
        return True
        
    def sort(self):
        self.components = sorted(self.components, key = lambda comp: comp.a)

if __name__ == '__main__':
    i1 = Interval(0, 0.2, 0, 0, [], np.array([1,0,0]))
    i2 = Interval(0.3, 0.4, 1, 0, [], np.array([0,1,0]))
    i3 = Interval(0.35, 0.75, 2, 0, [], np.array([0,0,1]))
    i4 = Interval(0.7, 1, 2, 0, [], np.array([1,0,0]))
    di = DisconnectedInterval([i1, i2, i3, i4])

    j1 = Interval(0.1, 0.19, 0, 0, [], np.array([0,0,1]))
    j2 = Interval(0.7, 0.8, 2, 0, [], np.array([0,0,1]))
    dj = DisconnectedInterval([j1, j2])

    A = np.array([[0, 1],
                  [1, 0]])
    B = np.array([[ 0.923879532511287, -0.217284326304659],
                  [-0.673986071141597, -0.923879532511287]])

    # print(di.contains(dj))
    # print(len(di.components))
    # print(len(dj.components))

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
    # di.draw(ax)
    # dj.draw(ax)

    #i1.draw(ax)
    # i1Image = i1.get_image(B)
    # print(i1Image)

    # i1.draw_image(ax, B)
    # i1Image.draw(ax)

    # print(i3.get_image(B))

    plt.show()