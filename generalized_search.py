import numpy as np
import matplotlib.pyplot as plt

from matplotlib.patches import Circle, Arc

class Interval():
    def __init__(self, a, b, mat, letters, color):
        self.a = a % np.pi
        self.b = b % np.pi
        self.e1 = 0
        self.e2 = 0
        self.mat = mat
        self.color = color
        self.letters = letters

    # Draw the interval
    def draw(self, ax):
        theta2, theta1 = get_arc_params(rp1_interval((self.a - self.e1) % np.pi, (self.b + self.e2) % np.pi))
        ax.add_patch(Arc((0,0), 2., 2., theta1=theta1, theta2=theta2, color=self.color, linewidth=10))

    # Draw image of the interval under all letters except inv(self.mat)
    def draw_image(self, ax):
        I = rp1_interval((self.a - self.e1) % np.pi, (self.b + self.e2) % np.pi)
        for mat in self.letters:
            if not np.allclose(mat, np.linalg.inv(self.mat)):
                theta2, theta1 = get_arc_params(mat @ I)
                ax.add_patch(Arc((0,0), 2., 2., theta1=theta1, theta2=theta2, color='orange', linewidth=7))

    # Check if interval contains another interval
    def contains(self, other):
        a, b = (self.a - self.e1) % np.pi, (self.b + self.e2) % np.pi
        c, d = (other.a - other.e1) % np.pi, (other.b + other.e2) % np.pi
        if a > b:
            if c > d:
                return d < b and a < c
            else:
                if c < b:
                    return d < b and a < (c + np.pi)
                else:
                    return (d - np.pi) < b and a < c
        else:
            if c > d:
                return False
            else:    
                return a < c and d < b

    # Check if interval intersects another interval
    def intersects(self, other):
        return self.a < other.a < self.b or self.a < other.b < self.b

    # Find the smallest distances between the endpoints of the interval and
    # the endpoints of another interval from a list of intervals
    # (Gives maximum possible expansion of interval in both directions separately)
    def nearest_endpoint_dists(self, intervals):
        a, b = (self.a - self.e1) % np.pi, (self.b + self.e2) % np.pi
        '''a_dist, b_dist = np.pi, np.pi
        for interval in intervals:
            if self != interval:
                c, d = (interval.a - interval.e1) % np.pi, (interval.b + interval.e2) + np.pi

                # Set a_dist to the minimum of a_dist and the distance between a and c
                # then set a_dist to the minimum of a_dist and the distance between a and d
                if angle_dist(a, c) < angle_dist(b, c):
                    a_dist = min([a_dist, angle_dist(a, c)])
                if angle_dist(a, d) < angle_dist(b, d):
                    a_dist = min([a_dist, angle_dist(a, d)])

                # Set b_dist to the minimum of b_dist and the distance between b and c
                # then set b_dist to the minimum of b_dist and the distance between b and d
                if angle_dist(b, c) < angle_dist(a, c):
                    b_dist = min([b_dist, angle_dist(b, c)])
                if angle_dist(b, d) < angle_dist(a, d):
                    b_dist = min([b_dist, angle_dist(b, d)])'''
        
        # Search for nearest interval end to a
        searching = True
        i = 0.01
        while searching:
            for interval in intervals:
                if self != interval:
                    c, d = (interval.a - interval.e1) % np.pi, (interval.b + interval.e2) % np.pi
                    if angle_dist((a - i) % np.pi, d) <= 0.01:
                        a_dist = angle_dist(a, d)
                        searching = False
                        break
                    # I think we may always run into d first so we might not need this one
                    if angle_dist((a - i) % np.pi, c) <= 0.01:
                        a_dist = angle_dist(a, c)
                        searching = False
                        break
            i += 0.01

        # Search for neearest interval end to b
        searching = True
        i = 0.01
        while searching:
            for interval in intervals:
                if self != interval:
                    c, d = (interval.a - interval.e1) % np.pi, (interval.b + interval.e2) % np.pi
                    if angle_dist((b + i) % np.pi, c) <= 0.01:
                        b_dist = angle_dist(b, c)
                        searching = False
                        break
                    # I think we may always run into c first so we might not need this one
                    if angle_dist((b + i) % np.pi, d) <= 0.01:
                        b_dist = angle_dist(b, d)
                        searching = False
                        break
            i += 0.01

        return a_dist, b_dist

class PingPong():
    def __init__(self, generators, graph = None):
        self.generators = generators
        self.graph = graph
        self.intervals = []
        self.epsilons = [0 for i in range(2 * len(generators))]
    
    def create_intervals(self, generators, initial_size = 5e-3):
        # Find theta for eigenvectors on S1 via RP1 -> S1
        # Create interval objects with initial values around eigenvectors
        letters = []
        for g in generators:
            letters += [g]
            letters += [np.linalg.inv(g)]
        
        colors = [np.array([0,0,1]), np.array([1,0,0]), np.array([0,1,0])]
        intervals = []
        iter = 0
        for mat in generators:
            # Eigenvalues
            #print(np.linalg.eig(mat)[0])

            e1 = np.arctan2(np.linalg.eig(mat)[1][1][0], np.linalg.eig(mat)[1][0][0])
            e2 = np.arctan2(np.linalg.eig(mat)[1][1][1], np.linalg.eig(mat)[1][0][1])

            if np.linalg.eig(mat)[0][0] > 1:
                intervals.append(Interval(e1 - initial_size, e1 + initial_size, mat, letters, colors[iter]))
                intervals.append(Interval(e2 - initial_size, e2 + initial_size, np.linalg.inv(mat), letters, colors[iter] * 0.5))
            else:
                intervals.append(Interval(e1 - initial_size, e1 + initial_size, np.linalg.inv(mat), letters, colors[iter] * 0.5))
                intervals.append(Interval(e2 - initial_size, e2 + initial_size, mat, letters, colors[iter]))

            iter += 1
        return intervals

    def find_intervals(self):
        self.intervals = self.create_intervals(self.generators)

        # Geometric expansion factor (must be <0.5)
        # (expand epsilon by the max distance it could expand times geo)
        geo = 0.05
        iter = 0
        while iter < 30:
            for interval in self.intervals:
                a_dist, b_dist = interval.nearest_endpoint_dists(self.intervals)
                interval.e1 += a_dist * geo
                interval.e2 += b_dist * geo

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
            print((interval.a - interval.e1) % np.pi, (interval.b + interval.e2) % np.pi)
            print(interval.nearest_endpoint_dists(self.intervals))
            print()
        for interval in self.intervals:
            interval.draw_image(ax)
        plt.show()

def rp1_to_s1(v):
    """map a point in R^2 - {0} to S1 via the homeo RP1 -> S1"""
    x, y = v[0], v[1]

    return np.row_stack([
        2*x*y / (x*x + y*y),
        (x*x - y*y) / (x*x + y*y)
    ])

def get_arc_params(interval):
    """map a pair of points in R^2 - {0} to a pair of circle angles"""
    x, y = rp1_to_s1(interval)
    return np.arctan2(y,x) * 180 / np.pi

def rp1_interval(theta1, theta2):
    """get a pair of points in RP1 representing the pair of angles theta1, theta2
    note: theta1, theta2 parameterize the double cover of RP^1"""
    return np.array([
        [np.cos(theta1), np.cos(theta2)],
        [np.sin(theta1), np.sin(theta2)]
    ])

# Return the distance between two angles a and b
# TODO Make this directional, not just the smallest distance
def angle_dist(a, b):
    a, b = min(a, b), max(a, b)
    return min(b - a, np.pi + a - b)

if __name__ == '__main__':

    # Create a random pair of matrices that are guaranteed to generate a free group
    a, c, e, g = float(np.random.rand(1) * 5) , float(np.random.rand(1) * 5) , float(np.random.rand(1) * 5) , float(np.random.rand(1) * 5)
    d, h = float(np.random.rand(1) * 5) + a + 2 , float(np.random.rand(1) * 5) + e + 2
    b, f = (a * d + 1) / c , (e * h + 1) / g

    A = np.array([[-a , b], [-c , d]])
    B = np.array([[ -e , -f], [ g , h]])

    # Create a random pair of matrices in SL2
    '''a = float(np.random.rand(1) * 5)
    b = float(np.random.rand(1) * 5)
    c = float(np.random.rand(1) * 5)
    d = (1 + b*c)/a

    A = np.array([[a, b], [c, d]])

    a = float(np.random.rand(1) * 5)
    b = float(np.random.rand(1) * 5)
    c = float(np.random.rand(1) * 5)
    d = (1 + b*c)/a

    B = np.array([[a, b], [c, d]])'''

    print(A)
    print(B)
    print()

    p = PingPong((A, B))
    p.find_intervals()
    p.draw_intervals()