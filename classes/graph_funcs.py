import numpy as np

def allwords(graph, current_length, max_length):
    '''Return a list of matrices representing words of length max_length sorted by starting letter'''
    if current_length == 1:
        states = list(graph.keys())
        return zip(states, [np.identity(2) for i in range(len(states))])
    words = []
    for word in allwords(graph, current_length-1, max_length):
        for letter in graph[word[0][-1]]:
            words.append((word[0] + letter[0], word[1] @ letter[1]))
    if current_length < max_length:
        return words
    else:
        print([[word[0] for word in words if word[0][0] == letter] for letter in list(graph.keys())])
        return [[word[1] for word in words if word[0][0] == letter] for letter in list(graph.keys())]

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
    graph = {'0' : [('1', B), ('2', B @ B)], '1' : [('0', A)], '2' : [('0', A)]}

    words = allwords(graph, 5, 5)
    print(words)