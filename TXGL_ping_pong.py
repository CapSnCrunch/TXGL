import numpy as np
import itertools
import matplotlib.pyplot as plt
import random

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
        (x*x - y*y) / (x*x + y*y) # M @
    ])

# Have to solve a quartic equation, but two solutions can be eliminated
def s1_to_rp1(v):
    xs, ys = v[0], v[1]

    y1 = np.sqrt((-ys + np.sqrt(ys**2 + xs**2)) / 2)
    y2 = -np.sqrt((-ys + np.sqrt(ys**2 + xs**2)) / 2)

    x1, x2 = xs / (2*y1), xs / (2*y2)

    return [np.row_stack([x1,y1]).flatten() , np.row_stack([x2,y2]).flatten()]

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

def rand_matrix(n):
    # n determines how large you want the entries to be. Pick n in (0, 5).
    # random matrix generation
    a = float(np.random.rand(1) * n)
    c = float(np.random.rand(1) * n) #* np.random.choice(-1, 1) * 5)
    d = float(np.random.rand(1) * n)
    b = (a * d - 1) / c

    return np.array([[a, b], [c, d]])

def pair_of_free_group_generators(n):
    # Create a random pair of matrices that are guaranteed to generate a free group in SL(2,R)
    # n determines how large you want the entries to be. Pick n in (0, 5).

    # file:///C:/Users/abhay/Downloads/1028999969.pdf PDF pg 2 / pg 162
    # Title: Pairs of Real 2-by-2 Matrices that Generate Free Products by R.C. Lyndon & J.L. Ullman

    a, c, e, g = float(np.random.rand(1) * n) , float(np.random.rand(1) * n) , float(np.random.rand(1) * n) , float(np.random.rand(1) * n)
    d, h = float(np.random.rand(1) * n) + a + 2 , float(np.random.rand(1) * n) + e + 2
    b, f = (a * d + 1) / c , (e * h + 1) / g

    #R = rand_matrix(1)

    return np.array([[-a , b] , [-c , d]]) , np.array([[ -e , -f] , [ g , h]])
    #return R @ np.array([[-a , b] , [-c , d]]) @ np.linalg.inv(R) , R @ np.array([[ -e , -f] , [ g , h]]) @ np.linalg.inv(R)

def generators_up_to_conjugacy(eig,n):
    # Classifies generators of a free group up to conjugacy by specifying eigenvalue

    a = float(np.random.rand(1) * n)
    c = float(np.random.rand(1) * n)# * np.random.choice(-1, 1) * 5)
    d = (eig**2 + 1) / eig - a
    b = (a * d - 1) / c

    return np.array([ [a, b], [c, d] ])

def create_intervals(generators, epsilon):
    # Find theta for eigenvectors on S1 via RP1 -> S1
    # Create interval objects with initial values around eigenvectors
    colors = [np.array([0,0,1]), np.array([1,0,0])]
    intervals = []
    iter = 0

    for mat in generators:

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

    print()
    print()
    print("How would you like to generate 2 matrices in SL(2,R) to test if Ping-Pong intervals exist?" )
    print()
    print("1. Keep generating 2 random matrices in SL(2,R) as potential generators of a Free group until a successful Ping-Pong interval is found.")
    print()
    print("2. Generate a pair of matrices in SL(2,R) that already generate a free group.")
    print()
    print("3. Specify two eigenvalues to create two corresponding matrices in SL(2,R).")
    print("   Matrices with the specified eigenvalues will continue to be generated until a successful Ping-Pong interval is found.")
    print("   This will classify generators of a free group in conjugacy classes.")
    print()
    print("4. Enter manual inputs for 2 potential generators in SL(2,R).")
    print()

    val = int(input("Enter choice 1, 2, 3, or 4 and press Enter: "))
    print("-"*145)

    if val == 3: 

        print()
        print("Please enter eigenvalues in (0 , ∞) / {1}.") 

        repeat = True   
        while repeat:

            print()
            eA = float(input("Enter an eigenvalue to genenerate the first matrix in SL(2,R) and press Enter: "))
            eB = float(input("Enter an eigenvalue to genenerate the second matrix in SL(2,R) and press Enter: "))

            if eA == 1 or eB == 1:
                print()
                print("Please do not enter 1 as an eigenvalue. Enter eigenvalues in (0 , ∞) / {1}. Try again!") 
            else:
                print("-"*145)
                repeat = False
    
    if val == 4:

        print()
        print( np.array( [["a", "b"],
                          ["c", "d"]] )  )
        print()
        print( np.array( [["e", "f"],
                          ["g", "h"]] )  )
        print()
        print("Please fill in the letters above for the two matrices:")
        a, b, c, d = input("Enter the values of a, b, c, d. Seperate the values by a space and then press Enter: ").split()
        e, f, g, h = input("Enter the values of e, f, g, h. Seperate the values by a space and then press Enter: ").split()
        a, b, c, d, e, f, g, h = float(a), float(b), float(c), float(d), float(e), float(f), float(g), float(h)
        print("-"*145)

    print()

    

    done = False
    while not done:

        i = 1

        if val == 1:
            # random matrix generation
            print('checking')

            A, B = rand_matrix(7), rand_matrix(7)
            eA, eB = np.linalg.eig(A)[0][0], np.linalg.eig(B)[0][0]

        elif val == 2:
            # Create a random pair of matrices that are
            # guaranteed to generate a free group in SL(2,R)

            A, B = pair_of_free_group_generators(5)
            eA, eB = np.linalg.eig(A)[0][0], np.linalg.eig(B)[0][0]

        elif val == 3:
            # generate a pair of matrices by their eigenvalues (classifying them in conjugacy classes)
            print('checking')

            A = generators_up_to_conjugacy(eA,3)
            B = generators_up_to_conjugacy(eB,3)

        elif val == 4:

            A = np.array([[a, b], 
                          [c, d]])
            B = np.array([[e, f],
                          [g, h]])
            eA, eB = np.linalg.eig(A)[0][0], np.linalg.eig(B)[0][0]
            

        if np.iscomplex(eA) == True or np.iscomplex(eB) == True:
            continue
        elif np.abs(eA - float(1)) < 0.0001 or np.abs(eB - float(1)) < 0.0001:
            continue
        else:
            pass

        # Get all letters (this includes generators and their inverses)
        generators = [A, B]
        letters = []
        for g in generators:
            letters += [g]
            letters += [np.linalg.inv(g)]

        '''#X = generators[0]
        Y = np.array([
        [np.linalg.eig(A)[1][0][0], np.linalg.eig(A)[1][1][0]],
        [np.linalg.eig(A)[1][0][1], np.linalg.eig(A)[1][1][1]]])
        M = np.linalg.inv(Y)'''

        ##########################################################################################################
        # TODO Make sure intervals don't overlap
        for epsilon in np.arange(0.01, 0.4, 0.01):
            intervals = create_intervals(generators, epsilon)
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

            for pair in itertools.combinations(intervals, 2):
                if non_triv_intersect(pair[0].a, pair[0].b, pair[1].a, pair[1].b):
                    if i == 1:
                        print('Intervals are intersecting!')
                        print()
                        i += 1
                    intervals = create_intervals(generators, epsilon - 0.01)
                    done = False

            if all_fully_contained and not done:
                intervals = create_intervals(generators, epsilon + 0.01)
                done = True

            if done:
                break
    ##########################################################################################################

    # A eigenvectors mapped onto on S1 (center of blue intervals)
    x1, y1, x2, y2 = np.linalg.eig(A)[1][0][0], np.linalg.eig(A)[1][1][0], np.linalg.eig(A)[1][0][1], np.linalg.eig(A)[1][1][1]
    vA1, vA2 = [x1, y1] , [x2, y2]
    
    # B eigenvectors mapped onto S1 (center of red intervals)
    x3, y3, x4, y4 = np.linalg.eig(B)[1][0][0], np.linalg.eig(B)[1][1][0], np.linalg.eig(B)[1][0][1], np.linalg.eig(B)[1][1][1]
    vB1, vB2 = [x3, y3] , [x4, y4]
    

    print('A = ')
    print(A)
    print('Determinant = ', np.linalg.det(A))
    print()
    print('Eigenvalues = ', np.linalg.eig(A)[0][0],' , ', np.linalg.eig(A)[0][1], ";")
    print('Eigenvectors = [', np.linalg.eig(A)[1][0][0] , ',' , np.linalg.eig(A)[1][1][0], '] ,', '[', np.linalg.eig(A)[1][0][1] , ',', np.linalg.eig(A)[1][1][1], '].')
    print()
    print("-"*50)
    print()
    print('B = ')
    print(B)
    print('Determinant = ', np.linalg.det(B))
    print()
    print('Eigenvalues = ', np.linalg.eig(B)[0][0],' , ', np.linalg.eig(B)[0][1], ";")
    print('Eigenvectors = [', np.linalg.eig(B)[1][0][0] , ',' , np.linalg.eig(B)[1][1][0], '] ,', '[', np.linalg.eig(B)[1][0][1] , ',', np.linalg.eig(B)[1][1][1], '].')
    print()
    print('|' + "-"*119 + '|')
    print('| (x,y) = (1,0) corresponds to θ = 0°. (x,y) = (-1,0) corresponds to 180° and -180°. (x,y) = (0,±1) corresponds to ±90°.|')
    print('|' + "-"*119 + '|')
    print()
    print('Coordinates of the center of blue intervals (eigenvectors of A mapped onto S1) are: ')
    print(rp1_to_s1(vA1).flatten(), ' , ', rp1_to_s1(vA2).flatten())
    print()
    print('Angles associated with the center of the red intervals (in degrees) are: ')
    print(float(get_arc_params(vA1)), ' , ', float(get_arc_params(vA2)))
    print()
    print("-"*50)
    print()
    print('Coordinates of the center of red intervals (eigenvectors of B mapped onto S1) are: ')
    print(rp1_to_s1(vB1).flatten(), ' , ', rp1_to_s1(vB2).flatten())
    print()
    print('Angles associated with the center of the red intervals (in degrees) are: ')
    print(float(get_arc_params(vB1)), ' , ', float(get_arc_params(vB2)))
    print()
    print("-"*50)
    print()
    print('A = ', A[0][0], A[0][1], A[1][0], A[1][1])
    print('B = ', B[0][0], B[0][1], B[1][0], B[1][1])
    print()
    print('epsilon = ', epsilon)


    if not all_fully_contained:
        print('Ping Pong Intervals Not Found.')

    print("-"*145)
    print()


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

    for interval in intervals:
        interval.draw(ax)
    for interval in intervals:
        interval.draw_image(ax)
    plt.show()
