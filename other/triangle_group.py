import numpy as np

"""
The group we're working with has presentation:

<a, b, c | a^2 = b^2 = c^2 = 1, (ab)^3 = (cb)^3 = (ac)^4 = 1>


"""

# three matrices giving a representation of the group (a -> A, b -> B,
# and c -> C)

A = np.array([[ 0.923879532511287, -0.217284326304659],
               [-0.673986071141597, -0.923879532511287]])

B = np.array([[0.,                1.219308768593441],
               [0.820136806818482, 0.               ]])

C = np.array([[ 0.923879532511287,  0.21728432630466 ],
               [ 0.673986071141597, -0.923879532511286]])

# the finite directed graph representing the geodesic automaton for
# this group. There are 18 vertices (labelled 1 - 18). For each vertex
# v, automaton[v] is a dictionary specifying the outward neighbors of
# v (together with edge labels). For example, vertex 1 has 3 edges
# pointing away from it: one from 1 to 2 labelled 'a', one from 1 to 3
# labelled 'b', and one from 1 to 4 labelled 'c'.

# there's also an alternative automaton on fewer vertices. In theory,
# you should be able to build intervals which work with either of
# these automata.

# you may need to reformat these dictionaries depending on how your
# code expects the automaton to be input.

graph = {'0': [('1', A), ('2', B), ('3', C)],
            '1': [('4', B), ('5', C)],
            '2': [('6', A), ('7', C)],
            '3': [('8', A), ('9', B)],
            '4': [('10', A), ('7', C)],
            '5': [('11', A), ('9', B)],
            '6': [('1', B), ('5', C)],
            '7': [('8', A), ('12', B)],
            '8': [('4', B), ('13', C)],
            '9': [('6', A), ('12', C)],
            '10': [('14', C)],
            '11': [('4', B), ('15', C)],
            '12': [('16', A)],
            '13': [('16', A), ('9', B)],
            '14': [('11', A), ('12', B)],
            '15': [('17', B)],
            '16': [('10', B), ('13', C)],
            '17': [('10', A), ('12', C)]}

'''automaton = {1: {2: ['a'], 3: ['b'], 4: ['c']},
             2: {5: ['b'], 6: ['c']},
             3: {7: ['a'], 8: ['c']},
             4: {9: ['a'], 10: ['b']},
             5: {11: ['a'], 8: ['c']},
             6: {12: ['a'], 10: ['b']},
             7: {11: ['b'], 6: ['c']},
             8: {9: ['a'], 13: ['b']},
             9: {5: ['b'], 14: ['c']},
             10: {7: ['a'], 13: ['c']},
             11: {15: ['c']},
             12: {5: ['b'], 16: ['c']},
             13: {17: ['a']},
             14: {16: ['a'], 10: ['b']},
             15: {12: ['a'], 13: ['b']},
             16: {18: ['b']},
             17: {11: ['b'], 14: ['c']},
             18: {11: ['a'], 13: ['c']}}

alternative_automaton = {1: {2: ['a'], 3: ['b'], 4: ['c']},
                         2: {3: ['b'], 4: ['c']},
                         3: {5: ['a'], 4: ['c']},
                         4: {6: ['a'], 7: ['b']},
                         5: {4: ['c']},
                         6: {3: ['b'], 8: ['c']},
                         7: {9: ['a']},
                         8: {7: ['b']},
                         9: {10: ['c']},
                         10: {11: ['a'], 7: ['b']},
                         11: {12: ['b']},
                         12: {5: ['a'], 13: ['c']},
                         13: {14: ['a']},
                         14: {5: ['b'], 8: ['c']}}'''