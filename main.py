import numpy as np

from classes.interval_funcs import *
from classes.group_funcs import *
from classes.intervals import Interval
from classes.pingpong import PingPong

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

    generators = free_group_generators(3, val = 0.5)

    print('Generators:')
    for g in generators:
        print(g)

    p = PingPong(generators)
    p.find_intervals(steps = 30, geo = 0.05, terminate_search = True)
    p.draw_intervals()