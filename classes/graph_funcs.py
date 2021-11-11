import numpy as np

def allwords(graph, n):
    if n == 1:
        return list(graph.keys())
    words = []
    for word in allwords(graph, n-1):
        for letter in graph[word[-1]]:
            words.append(word + letter[0])
    return words

def matrize(words, graph):
    for i in range(len(words)):
        temp = words[i]
        words[i] = np.identity(2)
        for j in range(len(temp)):
            words[i] =  words[i] @ letters[int(temp[j]) - 1]
    return words

if __name__ == '__main__':
    #graph = {'1': ['2', '3'], '2': ['1'], '3': ['1']}
    #for i in range(30):
    #    print('words of length ' + str(i+1) + ':', len(allwords(graph, i+1)))

    ### CREATE REPRESENTATION ###
    orders = [2, 3]

    generators = []
    for order in orders:
        theta = np.pi / order
        generators += [np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])]

    l = 2
    C = np.array([[l, 0],
                [0, 1/l]])

    A, B = generators

    A = np.linalg.inv(C) @ A @ C
    B = C @ B @ np.linalg.inv(C)

    letters = [A, B, B @ B]
    # graph = {'1' : ['2', '3'], '2' : ['1'], '3' : ['1']} # 1 corresponds to A, 2 to B, and 3 to B^-1
    graph = {'1' : [('2', B), ('3', B @ B)], '2' : [('1', A)], '3' : [('1', A)]}

    words = allwords(graph, 5)