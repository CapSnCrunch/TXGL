import numpy as np

# Identity
I = np.array([[1 , 0], [0 , 1]])

# Free Group Stuff
def free_group_graph(n):
    # Create the automatic structure for an n-generators free group
    # Natural numbers are used to represent the generators with negative naturals being inverses
    graph = {}
    for i in range(n):
        graph[i+1] = [j+1 for j in range(n)] + [-(j+1) for j in range(n) if j != i]
        graph[-(i+1)] = [j+1 for j in range(n) if j != i] + [-(j+1) for j in range(n)]
    return graph

def free_group_generators(n, val = 2, conjugate = False):
    # Create a random pair of matrices that are guaranteed to generate a free group
    # Title: Pairs of Real 2-by-2 Matrices that Generate Free Products by R.C. Lyndon & J.L. Ullman (PDF pg 2 / pg 162)
    a, c, e, g = float(np.random.rand(1) * val) , float(np.random.rand(1) * val) , float(np.random.rand(1) * val) , float(np.random.rand(1) * val)
    d, h = float(np.random.rand(1) * val) + a + 2 , float(np.random.rand(1) * val) + e + 2
    b, f = (a * d + 1) / c , (e * h + 1) / g

    A = np.array([[-a , b], [-c , d]])
    B = np.array([[ -e , -f], [ g , h]])

    # Conjugate generators by some random SL2 matrix to space them out (hopefully)
    if conjugate:
        a = float(np.random.rand(1) * 5)
        b = float(np.random.rand(1) * 5)
        c = float(np.random.rand(1) * 5)
        d = (1 + b*c)/a
        C = np.array([[a, b], [c, d]])

        A = C @ A @ np.linalg.inv(C)
        B = C @ B @ np.linalg.inv(C)

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
def cyclic_free_product_graph(orders):
    # Create the automatic structure for a cyclic free product group with the given orders
    pass

def cyclic_free_product_generators(orders):
    # Create a collection generators for a cyclic free product group with the given orders
    # TODO This doesnt actually work (maybe try conjugating them but we wont be sure)
    generators = []
    for order in orders:
        theta = 2*np.pi / order
        generators += [np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])]
    for i in range(1, len(generators)):
        generators[i] = I @ generators[i] @ I
    return generators

def allwords(graph, n):
    if n == 1:
        return list(graph.keys())
    words = []
    for word in allwords(graph, n-1):
        for letter in graph[word[-1]]:
            words.append(word + letter)
    return words

if __name__ == '__main__':
    graph = {'1': ['2', '3'], '2': ['1'], '3': ['1']}
    for i in range(30):
        print('words of length ' + str(i+1) + ':', len(allwords(graph, i+1)))