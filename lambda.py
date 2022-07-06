import numpy as np
from math import isclose
from classes.intervals import *
from classes.interval_funcs import *

def P(v, v1, v2):
    '''Maps RP1 -> R U {infinity}'''
    a2 = (v[0]**2) * (v2[0]**2 + v2[1]**2) - v2[0]**2
    a1 = (v[0]**2) * (2*v1[0]*v2[0] + 2*v1[1]*v2[1]) - 2*v1[0]*v2[0]
    a0 = (v[0]**2) * (v1[0]**2 + v1[1]**2) - v1[0]**2

    return float((-a1 + np.sqrt(a1**2 - 4*a0*a2)) / (2*a0))

def Pinv(a, v1, v2):
    '''Maps R U {infinity} -> RP1'''
    if a == np.inf:
        return v2
    return (v1 + a * v2) / np.linalg.norm(v1 + a * v2)

def get_lambda(interval, image):
    Ia, Ib = interval.a, interval.b
    Ja, Jb = image.a, image.b

    Ia, Ib = np.transpose(rp1_interval(Ia, Ib))
    Ja, Jb = np.transpose(rp1_interval(Ja, Jb))

    v1 = (Ia+Ib)/2
    v2 = (Ib-Ia)/2

    c, d = P(Ja,v1,v2), P(Jb,v1,v2)
    w, z = Pinv(c,v1,v2), Pinv(d,v1,v2)

    print(f'w = {w}')
    print(f'z = {z}')

    w0, w1 = w[0], w[1]
    z0, z1 = z[0], z[1]

    sigma = (((w0+w1)*(z0+z1)) / ((w1-w0)*(z1-z0))) ** (0.25)
    A = (1/(2*sigma)) * np.array([[sigma**2 + 1, 1 - sigma**2], [1 - sigma**2, 1 + sigma**2]])
    print(f'det(A) = {np.linalg.det(A)}')

    Aw = A @ w
    Az = A @ z

    print(f'P(Aw) = {P(Aw,v1,v2)}, P(Az) = {P(Az,v1,v2)}')

I = Interval(np.pi/6, np.pi/2-np.pi/8)
J = Interval(np.pi/4, np.pi/3)

print(f'Lambda for I, J = {get_lambda(I, J)}')