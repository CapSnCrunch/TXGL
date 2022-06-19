import numpy as np

# we expect to get a discrete faithful rep as long as this parameter
# is sufficiently large (in fact, larger than 2sqrt(2) + 3). 7 should
# be good enough.
s = 7.0

a = np.array([
    [  s,   0],
    [  0, 1/s]
])

b = np.array([
    [1/2*s + 1/2/s, 1/2*s - 1/2/s],
    [1/2*s - 1/2/s, 1/2*s + 1/2/s]
])

c = np.array([
    [ -1/2*(s**6 - s**4 + 11*s**2 - 3)/(s**5 - 6*s**3 + s),  1/2*(3*s**6 - s**4 - 3*s**2 + 1)/(s**5 - 6*s**3 + s)],
    [  -1/2*(s**6 - 3*s**4 - s**2 + 3)/(s**5 - 6*s**3 + s), 1/2*(3*s**6 - 11*s**4 + s**2 - 1)/(s**5 - 6*s**3 + s)]
])

d = np.array([
    [ (s**5 - 2*s**3 - 3*s)/(s**4 - 6*s**2 + 1), -2*(s**5 - 2*s**3 + s)/(s**4 - 6*s**2 + 1)],
    [ 2*(s**4 - 2*s**2 + 1)/(s**5 - 6*s**3 + s), -(3*s**4 + 2*s**2 - 1)/(s**5 - 6*s**3 + s)]
])

# technically, you can compute these inverses numerically or by hand,
# but here are the simplified forms:

A = np.array([
    [1/s,   0],
    [  0,   s]
])

B = np.array([
    [ 1/2*s + 1/2/s, -1/2*s + 1/2/s],
    [-1/2*s + 1/2/s,  1/2*s + 1/2/s]
])

C = np.array([
    [1/2*(3*s**6 - 11*s**4 + s**2 - 1)/(s**5 - 6*s**3 + s), -1/2*(3*s**6 - s**4 - 3*s**2 + 1)/(s**5 - 6*s**3 + s)],
    [   1/2*(s**6 - 3*s**4 - s**2 + 3)/(s**5 - 6*s**3 + s),  -1/2*(s**6 - s**4 + 11*s**2 - 3)/(s**5 - 6*s**3 + s)]
])

D = np.array([
    [-(3*s**4 + 2*s**2 - 1)/(s**5 - 6*s**3 + s),  2*(s**5 - 2*s**3 + s)/(s**4 - 6*s**2 + 1)],
    [-2*(s**4 - 2*s**2 + 1)/(s**5 - 6*s**3 + s),  (s**5 - 2*s**3 - 3*s)/(s**4 - 6*s**2 + 1)]
])

# should be close to the identity (numerically)
print(a @ b @ A @ B @ c @ d @ C @ D)
