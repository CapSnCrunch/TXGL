import numpy as np
import matplotlib.pyplot as plt

from matplotlib.patches import Circle, Arc

# Identity
I = np.array([[1 , 0], [0 , 1]])

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

def angle_dist(a, b):
    # Return the distance between two angles a and b
    a, b = a % np.pi, b % np.pi
    a, b = min(a, b), max(a, b)
    return min(b - a, np.pi + a - b)

# Free Group Stuff
def free_group_graph(n):
    # Create the automatic structure for an n-generators free group
    # Natural numbers are used to represent the generators with negative naturals being inverses
    graph = {}
    for i in range(n):
        graph[i+1] = [j+1 for j in range(n)] + [-(j+1) for j in range(n) if j != i]
        graph[-(i+1)] = [j+1 for j in range(n) if j != i] + [-(j+1) for j in range(n)]
    return graph

def free_group_generators(n, val = 2, conjugate = False):
    # Create a random pair of matrices that are guaranteed to generate a free group
    # Title: Pairs of Real 2-by-2 Matrices that Generate Free Products by R.C. Lyndon & J.L. Ullman (PDF pg 2 / pg 162)
    a, c, e, g = float(np.random.rand(1) * val) , float(np.random.rand(1) * val) , float(np.random.rand(1) * val) , float(np.random.rand(1) * val)
    d, h = float(np.random.rand(1) * val) + a + 2 , float(np.random.rand(1) * val) + e + 2
    b, f = (a * d + 1) / c , (e * h + 1) / g

    A = np.array([[-a , b], [-c , d]])
    B = np.array([[ -e , -f], [ g , h]])

    # Conjugate generators by some random SL2 matrix to space them out (hopefully)
    if conjugate:
        a = float(np.random.rand(1) * 5)
        b = float(np.random.rand(1) * 5)
        c = float(np.random.rand(1) * 5)
        d = (1 + b*c)/a
        C = np.array([[a, b], [c, d]])

        A = C @ A @ np.linalg.inv(C)
        B = C @ B @ np.linalg.inv(C)

    if n == 2:
        return [A, B]
    else:
        generators = []
        temp = I
        for i in range(n):
            temp = A @ temp @ B
            generators.append(temp)

        return generators

# Free Product Stuff
def free_product_graph(orders):
    # Create the automatic structure for a free product group with the given orders
    pass

def free_product_generators(orders):
    # Create a collection generators for a free product group with the given orders
    # TODO This doesnt actually work (maybe try conjugating them but we wont be sure)
    generators = []
    for order in orders:
        theta = 2*np.pi / order
        generators += [np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])]
    return generators

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

        plt.show()

if __name__ == '__main__':

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

    # Preselected generator pairs
    '''A = np.array([[1, 1],
                [2, 3]])
    B = np.array([[1, -1],
                [-2, 3]])'''

    # POTENTIAL ERROR CASE INVESTIGATION
    # CLOSE EIGENVECTORS EXAMPLE (doesnt work for initial_size = 5e-3 but will work for 5e-5)
    '''A = np.array([[-4.57725193, 36.32301585],
                  [-1.27271828, 9.88124901]])
    B = np.array([[-2.95775577e+00, -3.34382580e+03],
                  [8.40590824e-03, 9.16502070e+00]])'''

    # LARGE SEARCH DEPTH EXAMPLE (doesnt work for (10, 0.1) but will work for (15, 0.1))
    '''A = np.array([[-4.42309844, 31.63285742],
                  [-1.03571873, 7.18110696]])
    B = np.array([[-0.11108234, -2.92571545],
                  [0.43322661, 2.40810358]])'''

    generators = free_group_generators(6, val = 0.5)

    print('Generators:')
    for g in generators:
        print(g)

    p = PingPong(generators)
    p.find_intervals(steps = 30, geo = 0.05, terminate_search = True)
    p.draw_intervals()