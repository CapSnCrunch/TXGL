import numpy as np
import matplotlib.pyplot as plt
import random

from matplotlib.patches import Circle, Arc

class Interval():
    def __init__(self, a, b, mat, letters, color):
        self.a = a % np.pi
        self.b = b % np.pi
        self.e1 = 0 # epsilon spacing
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

def s1_to_rp1(v):
    """map a vector on S1 to a eigenvector in RP1"""
    xs, ys = v[0], v[1]

    # Have to solve a quartic equation, but two solutions can be eliminated
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

# Return the distance between two angles a and b
# TODO Make this directional, not just the smallest distance
def angle_dist(a, b):
    a, b = min(a, b), max(a, b)
    return min(b - a, np.pi + a - b)


if __name__ == '__main__':

    print()
    print()
    print("How would you like to generate n matrices in SL(2,R) to test if Ping-Pong intervals exist?" )
    print()
    print("1. Keep generating n random matrices in SL(2,R) as potential generators of a Free group until a successful Ping-Pong interval is found.")
    print()
    print("2. Generate a pair of matrices in SL(2,R) that already generate a free group. This function is limited to two generators.")
    print()
    print("3. Specify n eigenvalues to create n corresponding matrices in SL(2,R).")
    print("   Matrices with the specified eigenvalues will continue to be generated until a successful Ping-Pong interval is found.")
    print("   This will classify generators of a free group in conjugacy classes.")
    print()
    print("4. Enter manual inputs for n potential generators in SL(2,R).")
    print()
    
    ''' repeat = True   
        while repeat:

            print()
            Num_of_generators = int(input("Please enter a value for  "))

            if eA == 1 or eB == 1:
                print()
                print("Please do not enter 1 as an eigenvalue. Enter eigenvalues in (0 , ∞) / {1}. Try again!") 
            else:
                print("-"*145)
                repeat = False'''
        

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
            done = True
            pass

    #######################################################################################

    # A eigenvectors mapped onto on S1 (center of blue intervals)
    x1, y1, x2, y2 = np.linalg.eig(A)[1][0][0], np.linalg.eig(A)[1][1][0], np.linalg.eig(A)[1][0][1], np.linalg.eig(A)[1][1][1]
    vA1, vA2 = [x1, y1] , [x2, y2]
    
    # B eigenvectors mapped onto S1 (center of red intervals)
    x3, y3, x4, y4 = np.linalg.eig(B)[1][0][0], np.linalg.eig(B)[1][1][0], np.linalg.eig(B)[1][0][1], np.linalg.eig(B)[1][1][1]
    vB1, vB2 = [x3, y3] , [x4, y4]
    
    print()
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
    #print(s1_to_rp1((get_arc_params(vB1))), ' , ' , s1_to_rp1((get_arc_params(vB2))))
    #print(s1_to_rp1(float(get_arc_params(vB1))), ' , ' , s1_to_rp1(float(get_arc_params(vB2))))
    print()
    print("-"*50)
    print()
    print('A = ', A[0][0], A[0][1], A[1][0], A[1][1])
    print('B = ', B[0][0], B[0][1], B[1][0], B[1][1])


    #if not all_fully_contained:
    #    print('Ping Pong Intervals Not Found.')

    print("-"*145)
    print()
    print('Interval angles and the the epsilon expansions (in rad) on either side of each interval is given below.')
    print()

    p = PingPong((A, B))
    p.find_intervals()
    p.draw_intervals()