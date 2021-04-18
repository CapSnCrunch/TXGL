import numpy as np

# Create a random pair of matrices that are guaranteed to generate a free group
a, c, e, g = float(np.random.rand(1) * 5) , float(np.random.rand(1) * 5) , float(np.random.rand(1) * 5) , float(np.random.rand(1) * 5)
d, h = float(np.random.rand(1) * 5) + a + 2 , float(np.random.rand(1) * 5) + e + 2
b, f = (a * d + 1) / c , (e * h + 1) / g

A = np.array([[-a, b], 
              [-c, d]])
B = np.array([[-e, -f],
              [g, h]])

# Eigenvectors of A and B as columns
Ea = np.linalg.eig(A)[1]
Eb = np.linalg.eig(B)[1]
print(Ea)
print(Eb)

X = np.column_stack((Ea, np.transpose(Eb)[0]))
X = np.row_stack((X, np.array([[0,0,0]])))
print(X)

Y = np.array([[-1, 0, 1],
              [0, 1, 0],
              [0, 0, 0]])

A = Y @ np.linalg.inv(X)

# Find the Pseudo Inverse of the Eigenvector Column Matrix
# https://help.matheass.eu/en/Pseudoinverse.html
# X = np.concatenate((Ea, Eb), axis = 1)
# Xinv = np.transpose(X) @ np.linalg.inv(X @ np.transpose(X))

# Set what values we want to transform eigenvectors to
'''Y = np.array([[-1, 0, 1, 0],
             [0, 1, 0, -1]])'''

# print(X)
# print(Xinv)
# print(X @ Xinv)