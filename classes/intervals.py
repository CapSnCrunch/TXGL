import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Arc
from classes.interval_funcs import *

class Interval():
    def __init__(self, a, b, color = np.array([0,0,1])):
        self.a = a % np.pi
        self.b = b % np.pi

        self.color = color

        self.nearest_interval_a = None
        self.nearest_interval_b = None

    def draw(self, ax):
        '''Draw the interval'''
        theta2, theta1 = get_arc_params(rp1_interval(self.a % np.pi, self.b % np.pi))
        print('drawing between', theta1, theta2)
        ax.add_patch(Arc((0,0), 2., 2., theta1 = theta1, theta2 = theta2, color = self.color, linewidth=10))

    def draw_image(self, ax, mat):
        '''Draw image of the interval under mat'''
        I = rp1_interval(self.a % np.pi, self.b % np.pi)
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
        x, y = mat @ rp1_interval(self.a % np.pi, self.b % np.pi)

        if np.linalg.det(mat) < 0:
            b, a = np.arctan2(y, x)
            a, b = a % np.pi, b % np.pi
        else:
            a, b = np.arctan2(y, x)
            a, b = a % np.pi, b % np.pi
        # return (a, b)
        return Interval(a, b, self.color)

    def contains(self, other):
        '''Check if intervals contains another interval'''
        ta = 360

        # Find the angles vectors occur at in order to compare
        b, a = get_arc_params(rp1_interval(self.a, self.b))
        d, c = get_arc_params(rp1_interval(other.a, other.b))

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
        I = rp1_interval(other.a, other.b)

        # Find the angles vectors occur at in order to compare
        b, a = get_arc_params(rp1_interval(self.a, self.b))
        
        if np.linalg.det(mat) < 0:
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
        a, b = self.a % np.pi, self.b % np.pi
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
        return '(' + str(self.a) + ', ' + str(self.b) + ')'

class DisconnectedInterval():
    def __init__(self, components = [], color = np.array([0,0,1])):
        self.components = components
        self.color = color
        #self.sort()

    def draw(self, ax):
        '''Draw the disconnected interval'''
        for comp in self.components:
            comp.draw(ax)

    def draw_image(self, ax, mat):
        '''Draw the image of disconnected interval under mat'''
        for comp in self.components:
            comp.draw_image(ax, mat)

    def all_rp1(self):
        '''Check if all of RP1 is covered by the components, return None if they do, 
        otherwise, return a point alpha not covered by the components'''
        self.sort()
        for i in range(len(self.components)):
            comp1 = self.components[i]
            comp2 = self.components[(i + 1) % len(self.components)]
            if comp1.intersects(comp2, 0):
                continue
            else:
                return (comp1.b + comp2.a)/2
        return None

    def combine(self, reach = 0, debug = False):
        '''Combine / reduce intervals if they are overlapping
            (assumes that all intervals have the same name, mat, color)
            Will combine intervals if the gap between them is at most 'reach' '''

        self.sort() # Sort components into clockwise order

        # # Shift and renormalize points so that there are no wrap arounds
        # alpha = self.all_rp1()
        # if alpha is not None:
        #     for comp in self.components:
        #         comp.a = (comp.a - alpha) % np.pi
        #         comp.b = (comp.b - alpha) % np.pi

        # self.sort()

        # index = 0 # TODO FIX (infinite loop when A, B not conjugated)
        # while index < len(self.components) and len(self.components) > 1:
        #     if debug:
        #         print('DEBUGGING')
        #         import pdb; pdb.set_trace()
        #     comp1 = self.components[index]
        #     comp2 = self.components[(index + 1) % len(self.components)]
        #     if comp1.intersects(comp2, reach):
        #         comp1.b = max(comp1.b, comp2.b)
        #         #self.components = self.components[:index+1] + self.components[index+2:]
        #         self.components.pop((index+1) % len(self.components))
        #         index -= 1
        #     index += 1

        # # Shift back
        # if alpha is not None:
        #     for comp in self.components:
        #         comp.a = (comp.a + alpha) % np.pi
        #         comp.b = (comp.b + alpha) % np.pi

        # self.sort()

        if self.components == []:
            return

        if debug:
            print()
            print('components (including patches)')
            for i, comp in enumerate(self.components):
                print(i, comp.a, comp.b)

        out = []
        first_comp = self.components.pop(0)
        start, end = first_comp.a, first_comp.b
        if debug:
            print()
            print('first', first_comp.a, first_comp.b)
            print()
        for comp in self.components:
            if debug:
                print('start', start, 'end', end)
            if comp.a > comp.b:
                comp.b += np.pi
            if comp.a <= end:
                if comp.b > end:
                    end = comp.b
            else:
                out.append(Interval(start, end, self.color))
                (start, end) = comp.a, comp.b
                if debug:
                    print('out')
                    for comp in out:
                        print('  ', comp.a, comp.b)

        if end > np.pi:
            while out:
                if debug:
                    print('wrap around case')
                    print('start', start, 'end', end)
                comp = out[0]
                if comp.a + np.pi <= end:
                    out.pop(0)
                    comp_end = comp.b + np.pi
                    if comp_end > end:
                        end = comp_end
                        break
                else:
                    break

        if end >= start + np.pi:
            out = [Interval(0, np.pi, self.color)]
            print('COMPONENT IS ALL OF RP1')
        else:
            out.append(Interval(start, end, self.color))
        
        new_out = []
        for i in range(len(out)):
            if out[i].a != out[i].b:
                new_out.append(out[i])

        self.components = new_out

        if debug:
            print()
            print('components after modding')
            for comp in self.components:
                print(comp.a, comp.b)

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
    i1 = Interval(0, 0.2, np.array([1,0,0]))
    i2 = Interval(0.3, 0.4, np.array([0,1,0]))
    i3 = Interval(0.35, 0.75, np.array([0,0,1]))
    i4 = Interval(0.7, 1, np.array([1,0,0]))
    di = DisconnectedInterval([i1, i2, i3, i4])

    j1 = Interval(0.1, 0.19, np.array([0,0,1]))
    j2 = Interval(0.7, 0.8, np.array([0,0,1]))
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