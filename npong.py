import numpy as np
import itertools
import matplotlib.pyplot as plt

from matplotlib.patches import Circle, Arc
from matplotlib.animation import FuncAnimation

class Interval():
    def __init__(self, a, b, mat, letters, color):
        self.a = a
        self.b = b
        self.mat = mat
        self.color = color
        self.letters = letters

    # Draw image of the interval
    def draw(self, ax):
        theta2, theta1 = get_arc_params(rp1_interval(self.a, self.b))
        ax.add_patch(Arc((0,0), 2., 2., theta1=theta1, theta2=theta2, color=self.color, linewidth=10))

    # Draw image of the interval under all letters except inv(self.mat)
    # Check containment of the images within the interval
    def draw_image(self, ax):
        I = rp1_interval(self.a, self.b)
        for mat in letters:
            if not np.allclose(mat, np.linalg.inv(self.mat)):
                theta2, theta1 = get_arc_params(mat @ I)
                ax.add_patch(Arc((0,0), 2., 2., theta1=theta1, theta2=theta2, color='orange', linewidth=7))

def rp1_to_s1(v):
    """map a point in R^2 - {0} to S1 via the homeo RP1 -> S1"""
    x, y = v[0], v[1]

    return np.row_stack([
        2*x*y / (x*x + y*y),
        (x*x - y*y) / (x*x + y*y)
    ])

def s1_to_rp1(v):
    pass

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

def contains(a, b, c, d):
    # Check if (a,b) is contained in (c,d)
    return a < c and b > d

def non_triv_intersect(a, b, c, d):
    # Check if (a,b) intersects (c,d) nontrivially
    return a < c < b or a < d < b

def create_intervals(generators, epsilon):
    # Find theta for eigenvectors on S1 via RP1 -> S1
    # Create interval objects with initial values around eigenvectors
    colors = ['blue', 'red']
    intervals = []
    iter = 0
    for mat in generators:
        # Eigenvalues
        #print(np.linalg.eig(mat)[0])

        e1 = np.arctan2(np.linalg.eig(mat)[1][1][0], np.linalg.eig(mat)[1][0][0])
        e2 = np.arctan2(np.linalg.eig(mat)[1][1][1], np.linalg.eig(mat)[1][0][1])

        if np.linalg.eig(mat)[0][0] > 1:
            intervals.append(Interval(e1 - epsilon, e1 + epsilon, mat, letters, colors[iter]))
            intervals.append(Interval(e2 - epsilon, e2 + epsilon, np.linalg.inv(mat), letters, colors[iter]))
        else:
            intervals.append(Interval(e1 - epsilon, e1 + epsilon, np.linalg.inv(mat), letters, colors[iter]))
            intervals.append(Interval(e2 - epsilon, e2 + epsilon, mat, letters, colors[iter]))

        iter += 1
    return intervals

if __name__ == '__main__':

    # Check out 0.2 or 0.25!
    epsilon = 0.25

    # A pair of matrices in SL(2, Z), which (maybe?) generate a free group
    A = np.array([[1, 1],
                [2, 3]])
    B = np.array([[1, -1],
                [-2, 3]])
    '''A = np.array([[3, 0],
              [0, 1/3]])
    B = np.array([[5/3, 4/3],
              [4/3, 5/3]])'''
    '''A = np.array([[2, 3],
                [0, 2]])
    B = np.array([[2, 0],
                [3, 2]])'''
    '''A = np.array([[2, 3],
                [1, 2]])
    B = A @ A'''
    '''A = np.array([[4.41637304, 0.25017704], 
                  [3.38921208, 0.41842096]])
    B = np.array([[3.0185778, 0.09649246],
                [3.55607133, 0.44495592]])'''

    # Get all letters (this includes generators and their inverses)
    generators = [A, B]
    letters = []
    for g in generators:
        letters += [g]
        letters += [np.linalg.inv(g)]

    ##########################################################################################################
    for epsilon in np.arange(0.01, 0.4, 0.01):
        intervals = create_intervals(generators, epsilon)
        for pair in itertools.combinations(intervals, 2):
            if non_triv_intersect(pair[0].a, pair[0].b, pair[1].a, pair[1].b):
                print('Intervals are intersecting!')
        all_fully_contained = True
        for interval in intervals:
            fully_contained = True
            for other_interval in intervals:
                I = rp1_interval(other_interval.a, other_interval.b)
                if not np.allclose(other_interval.mat, np.linalg.inv(interval.mat)):
                    theta2, theta1 = get_arc_params(interval.mat @ I)
                    b, a = get_arc_params(rp1_interval(interval.a, interval.b))
                    # print(a, b, theta1, theta2)
                    if a > b:
                        # Interval crosses the break point
                        if theta1 > theta2:
                            # Inner interval crosses the break point
                            fully_contained = fully_contained and contains(theta2, theta1, b, a)
                        else:
                            if theta1 > 0:
                                # Inner interval completely above break point
                                fully_contained = fully_contained and contains(theta2-360, theta1, b, a)
                            else:
                                # Inner interval completely below break point
                                fully_contained = fully_contained and contains(theta2, theta1+360, b, a)
                    else:
                        fully_contained = fully_contained and contains(a, b, theta1, theta2)
            all_fully_contained = all_fully_contained and fully_contained

        if all_fully_contained:
            intervals = create_intervals(generators, epsilon + 0.05)
            break
    ##########################################################################################################

    if not all_fully_contained:
        print('Ping Pong Intervals Not Found.')

    fig, ax = plt.subplots(figsize=(5, 5))

    # Plot data
    ax.set_xlim((-1.2, 1.2))
    ax.set_ylim((-1.2, 1.2))
    ax.axis("off")
    ax.set_aspect("equal")

    # RP1
    rp1 = Circle((0,0), 1.0, fill=False)
    ax.add_patch(rp1)

    # Draw intervals
    # Draw images of intervals under the respective transforms
    '''for i in range(1):
        intervals[i].draw(ax)
    for i in range(1):
        print(intervals[i].draw_image(ax))
    '''

    for interval in intervals:
        interval.draw(ax)
    for interval in intervals:
        interval.draw_image(ax)
    plt.show()

    '''plt.ion()
    for i in range(1000):

        plt.draw()
        plt.pause(0.0001)
        plt.clf()'''