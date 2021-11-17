import numpy as np

"""def allwords(graph, current_length, max_length):
    '''Return a list of matrices representing words of length max_length sorted by starting letter'''
    if current_length == 1:
        states = list(graph.keys())
        return zip([states], [np.identity(2) for i in range(len(states))])
    words = []
    for word in allwords(graph, current_length-1, max_length):
        for letter in graph[word[0][-1]]:
            words.append((word[0] + [letter[0]], word[1] @ letter[1]))
    if current_length < max_length:
        return words
    else:
        print(words)
        print([[word[0] for word in words if word[0][0] == letter] for letter in list(graph.keys())])
        return [[word[1] for word in words if word[0][0] == letter] for letter in list(graph.keys())]"""

def allwords(graph, current_length, max_length):
    '''Return a list of matrices representing words of length max_length sorted by starting letter'''
    if current_length == 1:
        states = [[s] for s in list(graph.keys())]
        return zip(states, [np.identity(2) for i in range(len(states))])
    words = []
    for word in allwords(graph, current_length-1, max_length):
        for letter in list(graph[word[0][-1]].keys()):
            words.append((word[0] + [letter], word[1] @ graph[word[0][-1]][letter]))
    if current_length < max_length:
        return words
    else:
        print([[word[0] for word in words if word[0][0] == letter] for letter in list(graph.keys())])
        return [[word[1] for word in words if word[0][0] == letter] for letter in list(graph.keys())]

def generate_graph(orders, mats):
    n, m = orders
    A, B = mats
    graph = {0 : {1 : B}, 1 : {0 : A}}
    for i in range(m - 2):
        graph[len(list(graph.keys())) - 1][len(list(graph.keys()))] = B
        graph[len(list(graph.keys()))] = {0: A}
    for i in range(n - 2):
        if i == 0:
            graph[0][len(list(graph.keys()))] = A
        else:
            graph[len(list(graph.keys())) - 1][len(list(graph.keys()))] = A
        graph[len(list(graph.keys()))-1][1] = B
    return graph

if __name__ == '__main__':

    ### CREATE REPRESENTATION ###
    orders = [2, 3]

    generators = []
    for order in orders:
        theta = np.pi / order
        generators += [np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])]
    C = np.array([[2, 0],
                [0, 1/2]])
    A, B = generators
    A = np.linalg.inv(C) @ A @ C
    B = C @ B @ np.linalg.inv(C)

    letters = [A, B, B @ B]
    graph = {0 : {1: B, 2: B @ B}, 1 : {0: A}, 2: {0 : A}}

    words = allwords(graph, 5, 5)
    print(words)

    print(generate_graph([2, 4], ['A', 'B']))