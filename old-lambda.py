from matplotlib.pyplot import get
import numpy as np
from math import isclose
from classes.intervals import *
from classes.interval_funcs import *

def P(v):
    '''Maps RP1 -> R U {infinity}'''
    if v[0] == 0:
        return np.inf
    return float(v[1] / v[0])

def Pinv(a):
    '''Maps R U {infinity} -> RP1'''
    if a == np.inf:
        return np.array([[1],[0]])
    return (1 / np.sqrt(1 + a**2)) * np.array([[1],[a]])

def get_lambda(interval, image):
    Ia, Ib = interval.a, interval.b
    Ja, Jb = image.a, image.b

    Ia, Ib = np.transpose(rp1_interval(Ia, Ib))
    a, b = P(Ia), P(Ib)
    u, v = Pinv(a), Pinv(b)

    Ja, Jb = np.transpose(rp1_interval(Ja, Jb))
    c, d = P(Ja), P(Jb)
    w, z = Pinv(c), Pinv(d)

    print(f'Ia = {Ia}, Ib = {Ib}, Ja = {Ja}, Jb = {Jb}')
    print(f'a = {a}, b = {b}, c = {c}, d = {d}')
    print(f'u = {u}, v = {v}, w = {w}, z = {z}')
    print()

    # Transforms outside interval to (-1, 1)
    # alpha = 1 / (np.sqrt(2*(1+a**2)*(1+b**2)) * (b-a))
    alpha = np.sqrt(1 / (2*(b-a)))
    A = alpha * np.array([[b-a, 0], [-b-a, 2]])

    # A should be in SL(2,R)
    print(f'A = {A}')
    print(f'Det(A) = {np.linalg.det(A)}')

    Au = A @ u 
    Av = A @ v
    Aw = A @ w
    Az = A @ z

    # print(f'Au = {Au}')
    # print(f'Av = {Av}')
    
    # These should be -1 and 1
    print(f'P(Au) = {P(Au)}, P(Av) = {P(Av)}')
    print()

    w0, w1 = Aw[0][0], Aw[1][0]
    z0, z1 = Az[0][0], Az[1][0]


    sigma = (((w0+w1)*(z0+z1)) / ((w1-w0)*(z1-z0))) ** (0.25)
    print(f'sigma = {sigma}')

    B = (1/(2*sigma)) * np.array([[sigma**2 + 1, 1 - sigma**2], [1 - sigma**2, 1 + sigma**2]])
    print(f'B = {B}')
    print(f'Det(B) = {np.linalg.det(B)}')

    BAu = B @ Au
    BAv = B @ Av
    BAw = B @ Aw
    BAz = B @ Az

    # These should remain the same as before
    print(f'P(BAu) = {P(BAu)}, P(BAv) = {P(BAv)}')

    # These should negate one another
    print(f'P(BAw) = {P(BAw)}, P(BAz) = {P(BAz)}')
    print()

    return 1/abs(P(BAw))

I = Interval(np.pi/6, np.pi/2-np.pi/8)
J = Interval(np.pi/4, np.pi/3)

print(f'Lambda for I, J = {get_lambda(I, J)}')

# Garbage but holding on to just in case
# p2 = (w1-w0)*(z0-z1) + (w0-w1)*(z1-z0)
# p1 = (w1-w0)*(z0+z1) + (w0+w1)*(z0-z1) + (w0-w1)*(z0+z1) + (w0+w1)*(z1-z0)
# p0 = (w0+w1)*(z0+z1) + (w0+w1)*(z0+z1)
# p2 = (c-b)*(b-d) + (d-b)*(b-c)
# p1 = -(c-b)*(a+d) - (b-c)*(b-d) - (b-c)*(b-d) - (a+c)*(d-b)
# p0 = (b-c)*(a+d) + (a+c)*(b-d)
# sigma = ((-p1 + (p1**2 - 4*p0*p2)**(1/2)) / (2*p0)) ** (1/2)