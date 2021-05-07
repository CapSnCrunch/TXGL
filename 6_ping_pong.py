import numpy as np
import matplotlib.pyplot as plt
import random
import sys

from matplotlib.patches import Circle, Arc

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

def angle_dist(a, b):
    # Return the distance between two angles a and b
    a, b = a % np.pi, b % np.pi
    a, b = min(a, b), max(a, b)
    return min(b - a, np.pi + a - b)

# Example matrix generation 
def rand_matrix(mult):
    # mult determines how large you want the entries to be. Pick mult in (0, 5).
    # random matrix generation
    a = float(np.random.rand(1) * mult)
    c = float(np.random.rand(1) * mult) #* np.random.choice(-1, 1) * 5)
    d = float(np.random.rand(1) * mult)
    b = (a * d - 1) / c

    return np.array([[a, b], [c, d]])

def generators_up_to_conjugacy(eig,mult):
    # Classifies generators of a free group up to conjugacy by specifying eigenvalue

    a = float(np.random.rand(1) * mult)
    c = float(np.random.rand(1) * mult)# * np.random.choice(-1, 1) * 5)
    d = (eig**2 + 1) / eig - a
    b = (a * d - 1) / c

    return np.array([ [a, b], [c, d] ])

# Free Group Stuff
def free_group_graph(n):
    graph = {}
    for i in range(n):
        graph[i+1] = [j+1 for j in range(n)] + [-(j+1) for j in range(n) if j != i]
        graph[-(i+1)] = [j+1 for j in range(n) if j != i] + [-(j+1) for j in range(n)]
    return graph

def free_group_generators(n, mult, conjugate = False):
    # Create a random pair of matrices that are guaranteed to generate a free group in SL(2,R)
    # mult determines how large you want the entries to be. Pick mult in (0, 5)?
    # n is number of generators
    # file:///C:/Users/abhay/Downloads/1028999969.pdf PDF pg 2 / pg 162
    # Title: Pairs of Real 2-by-2 Matrices that Generate Free Products by R.C. Lyndon & J.L. Ullman

    a, c, e, g = float(np.random.rand(1) * mult) , float(np.random.rand(1) * mult) , float(np.random.rand(1) * mult) , float(np.random.rand(1) * mult)
    d, h = float(np.random.rand(1) * mult) + a + 2 , float(np.random.rand(1) * mult) + e + 2
    b, f = (a * d + 1) / c , (e * h + 1) / g

    A = np.array([[-a , b], [-c , d]])
    B = np.array([[ -e , -f], [ g , h]])

    # Conjugate generators by some random SL_2 matrix to space them out (hopefully)
    if conjugate:
        
        C = rand_matrix(mult)

        A = C @ A @ np.linalg.inv(C)
        B = C @ B @ np.linalg.inv(C)

    I = np.array([[1 , 0], [0 , 1]])

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
# n is num of generators, orders is list of finite order of generators you want
'''def free_product_graph(n, orders):
    let_alphabet = [A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P]
    
    for i in range(n):
        let_alphabet[i] = free_product_generators(n, orders, mult)[i]
        num = orders[i]

        for j in range(num):
            let_alphabet[i].append(A**2)'''
    
    
def free_product_generators(n, orders, mult):
    
    fp_generators = []

    for i in range(n):

        angle = np.pi / orders[i]
        X = rand_matrix(mult)
        mat = X @ rotation_matrix(angle) @ np.linalg.inv(X)
        fp_generators.append(mat)

    return fp_generators

def rotation_matrix(theta): 
    return np.array([
        [np.cos(theta), -1 * np.sin(theta)],
        [np.sin(theta), np.cos(theta)]])

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

    # Check if interval contains the image of another interval
    def contains_image(self, other):
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

    # Check if interval intersects another interval
    def intersects(self, other):
        return self.a < other.a < self.b or self.a < other.b < self.b

    # Find the smallest distances between the endpoints of the interval and
    # the endpoints of another interval from a list of intervals
    # (Gives maximum possible expansion of interval in both directions separately)
    '''def nearest_endpoint_dists(self, intervals):
        a, b = (self.a - self.e1) % np.pi, (self.b + self.e2) % np.pi
        
        # Search for nearest interval end to a
        searching = True
        eps = 1e-4
        i = eps
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
            i += eps

        # Search for neearest interval end to b
        searching = True
        i = eps
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
            i += eps

        return a_dist, b_dist'''

    # Find the intervals which are closest to self.a and self.b and assign them to
    # nearest_interval_a and nearest_interval_b respectively for later use in expansion
    def nearest_endpoints(self, intervals):
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

    def create_intervals(self, generators, initial_size = 1e-9, generator_names = ['A', 'B', 'C', 'D', 'E']):
        # Find theta for eigenvectors on S1 via RP1 -> S1
        # Create interval objects with initial values around eigenvectors

        letters = []
        for g in generators:
            letters += [g]
            letters += [np.linalg.inv(g)]
        
        # Blue, Red, Green, Magenta, Cyan, Yellow
        colors = [np.array([0,0,1]), np.array([1,0,0]), np.array([0,1,0]), np.array([1,0,1]), np.array([0,1,1]), np.array([1,1,0])]
        intervals = []
        iter = 0
        for mat in generators:

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
        '''for mat in generators:
            # Eigenvalues
            #print(np.linalg.eig(mat)[0])

            e1 = np.arctan2(np.linalg.eig(mat)[1][1][0], np.linalg.eig(mat)[1][0][0])
            e2 = np.arctan2(np.linalg.eig(mat)[1][1][1], np.linalg.eig(mat)[1][0][1])

            if np.linalg.eig(mat)[0][0] > 1:
                intervals.append(Interval(e1 - initial_size, e1 + initial_size, generator_names[iter], mat, letters, colors[iter]))
                intervals.append(Interval(e2 - initial_size, e2 + initial_size, generator_names[iter].lower(), np.linalg.inv(mat), letters, colors[iter] * 0.5))
            else:
                intervals.append(Interval(e1 - initial_size, e1 + initial_size, generator_names[iter].lower(), np.linalg.inv(mat), letters, colors[iter] * 0.5))
                intervals.append(Interval(e2 - initial_size, e2 + initial_size, generator_names[iter], mat, letters, colors[iter]))

            iter += 1
        return intervals'''

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


    print()
    print()
    print('Hello! How would you like to generate matrices in SL(2,R) to test if Ping-Pong intervals exist?')

    repeat = True
    while repeat:
    
            print()
            val1 = int(input('Press 1 if you want to test for free groups and 2 if you want to test for free products. Then, press Enter. '))

            if val1 != 1 and val1 != 2:
                print("The only options are '1' or '2'. Try again!") 
            else:
                repeat = False

    if val1 == 1:

        done = False
        while not done:

            print("-"*145)
            print()
            print('How do you want to generate n generators?')
            print()
            print("1. Try n random matrices in SL(2,R) as potential generators of a Free group.")
            print()
            print("2. Generate n matrices in SL(2,R) that already generate a free group.")
            print()
            print("3. Specify n eigenvalues to create n corresponding matrices in SL(2,R).")
            print("   This will classify generators of a free group in conjugacy classes.")
            print()
            print("4. Enter manual inputs for n potential generators in SL(2,R).")
            print()

            val2 = int(input("Enter choice 1, 2, 3, or 4 and press Enter: "))
            print("-"*145)

            repeat = True   
            while repeat:

                print()
                num_of_gen = int(input("Please enter an integer value for the number of generators you'd like. "))

                if type(num_of_gen) is not int:
                    print()
                    print("That is not an integer. Try again!") 
                else:
                    #num_of_gen = int(num_of_gen)
                    print("-"*145)
                    repeat = False

            mult = 0.25
            if val2 == 1:
                # random matrix generation

                generators = []
                for n in range(num_of_gen):
                    matrix = rand_matrix(5)
                    generators.append(matrix)

                eig_list = []
                for mat in generators:
                        e = np.linalg.eig(mat)[0][0]
                        eig_list.append(e)

            elif val2 == 2:
                # Create a random pair of matrices that are guaranteed to generate a free group in SL(2,R)

                repeat = True
                while repeat:
                    print()
                    conj = int(input("Would you like to conjugate our generators by a matrix in SL(2,R)? Enter 1 for yes and 2 for no. "))

                    if conj == 1 or conj == 2:
                        print("-"*145)
                        repeat = False 
                    else:
                        print()
                        print("Please enter '1' or '2'. Try again!")

                if conj == 1:
                    generators = free_group_generators(num_of_gen, mult, True)
                elif conj == 2:    
                    generators = free_group_generators(num_of_gen, mult, False)

                eig_list = []
                for mat in generators:
                        e = np.linalg.eig(mat)[0][0]
                        eig_list.append(e)

            if val2 == 3: 

                print()
                print("Please enter eigenvalues in (0 , ∞) / {1}.") 
                eig_list = []

                repeat = True   
                while repeat:
                    print()

                    for n in range(num_of_gen):
                        e = float(input("Enter an eigenvalue to genenerate matrix #" + str(n+1) + " in SL(2,R) and press Enter: "))
                        eig_list.append(e)

                    if any([e == 1 for e in eig_list]):
                        print("-"*145)
                        repeat = False 
                    else:
                        print()
                        print("Please do not enter 1 as an eigenvalue. Enter eigenvalues in (0 , ∞) / {1}. Try again!")

                generators = []
                for e in eig_list:
                    g = generators_up_to_conjugacy(e, mult)
                    generators.append(g)

            if val2 == 4:

                print()
                print( np.array( [["a", "b"],
                                ["c", "d"]] )  )
                print()
                print("Please fill in the letters for the entries of your generating matrices:")
                print()

                generators = []
                eig_list = []
                for n in range(num_of_gen):

                    a, b, c, d = input("Enter the values of a, b, c, d for matrix #" + str(n+1) + ". Seperate the values by a space and then press Enter: ").split()
                    a, b, c, d = float(a), float(b), float(c), float(d)
                    mat = np.array([[a, b], 
                                [c, d]])

                    generators.append(mat)
                    eig_list.append(np.linalg.eig(mat)[0][0])
                print("-"*145)

            print()
                
            if any([np.iscomplex(e) == True for e in eig_list]):
                print('Eigenvalues for one or more of your generator are complex. Sorry, but try again!')
                continue
            elif any([np.abs(e - float(1)) < 0.0001 for e in eig_list]):
                print('Eigenvalues for one or more of your generators are 1. Sorry, but try again!')
                continue
            else:
                done = True
                pass
        
    if val1 == 2:
        print()
        print('Still in progress, sorry!')
        print()
        sys.exit()

    #######################################################################################
    i = 0
    alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    maincolors = ['blue', 'red', 'green', 'magenta', 'cyan', 'yellow']
    inversecolors = ['navy blue', 'maroon', 'neon green', 'purple', 'teel', 'olive']

    print('|' + "-"*119 + '|')
    print('| (x,y) = (1,0) corresponds to θ = 0°. (x,y) = (-1,0) corresponds to 180° and -180°. (x,y) = (0,±1) corresponds to ±90°.|')
    print('|' + "-"*119 + '|')
    print()
    print("-"*119)
    print()

    for g in generators:
        print('  Generator ' + alphabet[i] + ' corresponds to the ' + maincolors[i] + ' interval. '), print( alphabet[i] + '^(-1) corresponds to the ' + inversecolors[i] + ' interval.')
        i += 1
    print()
    print('Since we have ' + str(len(generators)) + ' generators, we should expect each interval to contain ' + str(2 * len(generators) - 1) + ' images.')
    print()
    print("-"*119)

    i = 0
    for mat in generators:

        # v1, v2 are eigenvectors mapped onto on S1
        x1, y1, x2, y2 = np.linalg.eig(mat)[1][0][0], np.linalg.eig(mat)[1][1][0], np.linalg.eig(mat)[1][0][1], np.linalg.eig(mat)[1][1][1]
        v1, v2 = [x1, y1] , [x2, y2]

        print()
        print(alphabet[i] + ' = ')
        print(mat)
        print('Determinant = ', np.linalg.det(mat))
        print()
        print('Eigenvalues = ', np.linalg.eig(mat)[0][0],' , ', np.linalg.eig(mat)[0][1], ";")
        print('Eigenvectors = [', np.linalg.eig(mat)[1][0][0] , ',' , np.linalg.eig(mat)[1][1][0], '] ,', '[', np.linalg.eig(mat)[1][0][1] , ',', np.linalg.eig(mat)[1][1][1], '].')
        print()
        print('Coordinates of the center of ' + maincolors[i] + ' intervals (eigenvectors of ' + alphabet[i] + ' mapped onto S1) are: ')
        print(rp1_to_s1(v1).flatten(), ' , ', rp1_to_s1(v2).flatten())
        print()
        print('Angles associated with the center of the ' + maincolors[i] + ' intervals (in degrees) are: ')
        print(float(get_arc_params(v1)), ' , ', float(get_arc_params(v2)))
        print()
        print("-"*145)

        i += 1

        #print(s1_to_rp1((get_arc_params(vB1))), ' , ' , s1_to_rp1((get_arc_params(vB2))))
        #print(s1_to_rp1(float(get_arc_params(vB1))), ' , ' , s1_to_rp1(float(get_arc_params(vB2))))
    print()
    i = 0
    for mat in generators:
        print(alphabet[i] + ' = ', mat[0][0], mat[0][1], mat[1][0], mat[1][1])
        i += 1
    print()
    #print(free_group_generators(3,[2,3,4]))
    #print(X) #Y, Z)
    #print(X@X)#, Y@Y@Y, Z@Z@Z@Z)

    p = PingPong(generators)
    p.find_intervals(steps = 20, geo = 0.05, terminate_search = True)
    p.draw_intervals()