import numpy as np

I = np.identity(2)
O = I - I

# Checks if two matrices are equal within some tolerance
def mats_equal(mat1, mat2, tol = 1e-5):
    temp = abs(mat2 - mat1)
    return np.all(temp < tol)

# Finds the index of a matrix in a list of matrices
def mat_index(mat, array):
    for i in range(len(array)):
        if mats_equal(mat, array[i]):
            return i
    return None

# Brute force checks the Cayley Graph of n generators
def brute_search(start, depth, *args):
    mats = []
    # Put generators and their inverses in a list
    for mat in args:
        mats.append(mat)
        mats.append(np.linalg.inv(mat))
    # Check if any matrices are inverses of each other
    for i in range(len(mats)):
        if mats_equal(mats[i], np.linalg.inv(mats[i])):
                print('Found one! (1)')
                print(str(i)+str(i))
                return True
        for j in range(i+1, len(mats)):
            if mats_equal(mats[i], mats[j]):
                print('Found one! (2)')
                print(str(i)+str(j))
                return True
    return recurse(start, depth, O, I, '', *mats)

# Recurses through the branches of the Cayley Graph
def recurse(start, depth, current_mat, last_arg, string, *args):
    # Found a nontrivial identity!
    if mats_equal(current_mat, I):
        print('Found one! (3)')
        print(string)
        return True
    # Search terminates after max depth reached
    if depth == start:
        return False
    found = False
    # Branch out one level
    for mat in args:
        # Check to make sure we don't back track
        # TODO keep track of index of matrix instead of matrix itself
        if not mats_equal(mat, np.linalg.inv(last_arg)):
            if mats_equal(current_mat, O):
                found = found or recurse(start, depth - 1, mat, mat, string + str(mat_index(mat, args)), *args)
            else:
                found = found or recurse(start, depth - 1, current_mat * mat, mat, string + str(mat_index(mat, args)), *args)

# Problems from Teddy
A = np.matrix([[1/2*np.sqrt(3*np.sqrt(2) - 4*np.sqrt(np.sqrt(2) + 1) + 4),  -1/2*2**(1/4)],
               [-1/2*(2**(1/4)),  1/2*np.sqrt(3*np.sqrt(2) + 4*np.sqrt(np.sqrt(2) + 1) + 4)]])

B = np.matrix([[1/2*np.sqrt(3*np.sqrt(2) + 4*np.sqrt(np.sqrt(2) + 1) + 4),  -1/2*2**(1/4)],
               [-1/2*2**(1/4),  1/2*np.sqrt(3*np.sqrt(2) - 4*np.sqrt(np.sqrt(2) + 1) + 4)]])

'''A = np.matrix([[ 2.41421356, -1.55377397, -1.55377397],
        [-1.55377397,  1.70710678,  0.70710678],
        [-1.55377397,  0.70710678,  1.70710678]])

B = np.matrix([[ 2.41421356,  1.55377397, -1.55377397],
        [ 1.55377397,  1.70710678, -0.70710678],.
        
        [-1.55377397, -0.70710678,  1.70710678]])'''

print(np.linalg.inv(A)*B*A*np.linalg.inv(B)*np.linalg.inv(A)*B*A*np.linalg.inv(B))

# Other tests
C = np.matrix([[1, 0],
               [2, 1]])

D = np.matrix([[1, 2],
               [2, 1]])

E = np.matrix([[1, 2],
               [2, 3]])

F = np.matrix([[-317811, 196418],
               [196418, -121393]])

# test = np.linalg.inv(F) * np.linalg.inv(E) * F * E
# print(test)
# print(mats_equal(test, I))
#print(np.linalg.det(F))
#print(np.linalg.inv(F)*np.linalg.inv(E)*F*E)

Circ = np.matrix([[1, 0, 0],
                  [0, 0, 1],
                  [0, 1, 0]])

brute_search(0, 16, A, B)
#brute_search(0, 10, E, F)
print('Done.')