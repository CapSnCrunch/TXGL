# This file stores the representations and automatic structures for a number of groups
# we're interested in testing

# Graphs should be saved as {0: {a: A, b: B, ...}, ... , n: {...}} where a needs to map into 0 by A and so on.

import numpy as np

def group(name = 'cyclic', *args):
    '''Returns the automatic structure of the desired group
        name: cyclic, triangle, surface
       *args: orders for cyclic group orders'''
    if name == 'cyclic':
        generators = []
        for order in args:
            theta = np.pi / order
            generators += [np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])]

        l = 1.5 # Interesting: if we increase this, it decreases the number of search steps
        C = np.array([[l, 0], [0, 1/l]])

        A, B = generators

        A = np.linalg.inv(C) @ A @ C
        B = C @ B @ np.linalg.inv(C)

        graph = {0: {1: B}, 1: {0: A, 2: B}, 2: {0 : A}}

        return graph

    elif name == 'triangle':
        # Triangle Group <a, b, c | a^2 = b^2 = c^2 = 1, (ab)^3 = (cb)^3 = (ac)^4 = 1>
        A = np.array([[ 0.923879532511287, -0.217284326304659],
                    [-0.673986071141597, -0.923879532511287]])
        B = np.array([[0.,                1.219308768593441],
                    [0.820136806818482, 0.               ]])
        C = np.array([[ 0.923879532511287,  0.21728432630466 ],
                    [ 0.673986071141597, -0.923879532511286]])

        # graph = {0: {},
        #         1: {4: B, 5: C},
        #         2: {6: A, 7: C},
        #         3: {8: A, 9: B},
        #         4: {10: A, 7: C},
        #         5: {11: A, 9: B},
        #         6: {1: B, 5: C},
        #         7: {8: A, 12: B},
        #         8: {4: B, 13: C},
        #         9: {6: A, 12: C},
        #         10: {14: C},
        #         11: {4: B, 15: C},
        #         12: {16: A},
        #         13: {16: A, 9: B},
        #         14: {11: A, 12: B},
        #         15: {17: B},
        #         16: {10: B, 13: C},
        #         17: {10: A, 12: C}}

        graph = {0: {},
                1: {2: A, 3: B, 4: C},
                2: {5: B, 6: C},
                3: {7: A, 8: C},
                4: {9: A, 10: B},
                5: {11: A, 8: C},
                6: {12: A, 10: B},
                7: {11: B, 6: C},
                8: {9: A, 13: B},
                9: {5: B, 14: C},
                10: {7: A, 13: C},
                11: {15: C},
                12: {5: B, 16: C},
                13: {17: A},
                14: {16: A, 10: B},
                15: {12: A, 13: B},
                16: {18: B},
                17: {11: B, 14: C},
                18: {11: A, 13: C}}

        # graph = {0: {},
        #         1: {2: A, 3: B, 4: C},
        #         2: {3: B, 4: C},
        #         3: {5: A, 4: C},
        #         4: {6: A, 7: B},
        #         5: {4: C},
        #         6: {3: B, 8: C},
        #         7: {9: A},
        #         8: {7: B},
        #         9: {10: C},
        #         10: {11: A, 7: B},
        #         11: {12: B},
        #         12: {5: A, 13: C},
        #         13: {14: A},
        #         14: {5: B, 8: C}}

        
        return graph
    
    elif name == 'surface':
        l = 2 * (2 ** (1/4)) * np.cos(np.pi/8) + (2 ** (1/2)) + 1
        X = np.array([[l, 0], [0, 1/l]])

        R = lambda theta: np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])

        a = X
        b = R(-np.pi/8) @ X @ R(np.pi/8)
        c = R(-np.pi/4) @ X @ R(np.pi/4)
        d = R(-3*np.pi/8) @ X @ R(3*np.pi/8)

        A = np.linalg.inv(a)
        B = np.linalg.inv(b)
        C = np.linalg.inv(c)
        D = np.linalg.inv(d)

        graph = {0: {},
                1: {2: d, 3: D, 4: c, 5: C, 6: b, 7: B, 8: a, 9: A},
                2: {2: d, 4: c, 5: C, 6: b, 7: B, 8: a, 9: A},
                3: {3: D, 4: c, 5: C, 6: b, 7: B, 8: a, 9: A},
                4: {2: d, 10: D, 4: c, 6: b, 11: B, 8: a, 9: A},
                5: {12: d, 3: D, 5: C, 13: b, 7: B, 8: a, 9: A},
                6: {2: d, 3: D, 4: c, 14: C, 6: b, 8: a, 15: A},
                7: {2: d, 3: D, 16: c, 5: C, 7: B, 17: a, 9: A},
                8: {18: d, 3: D, 4: c, 5: C, 6: b, 19: B, 8: a},
                9: {2: d, 20: D, 4: c, 5: C, 21: b, 7: B, 9: A},
                10: {3: D, 4: c, 5: C, 6: b, 7: B, 8: a, 22: A},
                11: {2: d, 3: D, 16: c, 5: C, 7: B, 23: a, 9: A},
                12: {2: d, 4: c, 5: C, 6: b, 7: B, 24: a, 9: A},
                13: {2: d, 3: D, 4: c, 14: C, 6: b, 8: a, 25: A},
                14: {26: d, 3: D, 5: C, 13: b, 7: B, 8: a, 9: A},
                15: {2: d, 27: D, 4: c, 5: C, 21: b, 7: B, 9: A},
                16: {2: d, 28: D, 4: c, 6: b, 11: B, 8: a, 9: A},
                17: {29: d, 3: D, 4: c, 5: C, 6: b, 19: B, 8: a},
                18: {2: d, 4: c, 30: C, 6: b, 7: B, 8: a, 9: A},
                19: {2: d, 3: D, 31: c, 5: C, 7: B, 17: a, 9: A},
                20: {3: D, 32: c, 5: C, 6: b, 7: B, 8: a, 9: A},
                21: {2: d, 3: D, 4: c, 33: C, 6: b, 8: a, 15: A},
                22: {2: d, 20: D, 4: c, 5: C, 34: b, 7: B, 9: A},
                23: {3: D, 4: c, 5: C, 6: b, 19: B, 8: a},
                24: {18: d, 3: D, 4: c, 5: C, 6: b, 35: B, 8: a},
                25: {2: d, 4: c, 5: C, 21: b, 7: B, 9: A},
                26: {2: d, 4: c, 5: C, 6: b, 7: B, 36: a, 9: A},
                27: {3: D, 5: C, 6: b, 7: B, 8: a, 9: A},
                28: {3: D, 4: c, 5: C, 6: b, 7: B, 8: a, 37: A},
                29: {2: d, 4: c, 6: b, 7: B, 8: a, 9: A},
                30: {12: d, 3: D, 5: C, 7: B, 8: a, 9: A},
                31: {2: d, 4: c, 6: b, 11: B, 8: a, 9: A},
                32: {2: d, 10: D, 4: c, 6: b, 8: a, 9: A},
                33: {3: D, 5: C, 13: b, 7: B, 8: a, 9: A},
                34: {2: d, 10: D, 4: c, 6: b, 8: a, 15: A},
                35: {12: d, 3: D, 5: C, 7: B, 17: a, 9: A},
                36: {18: d, 3: D, 4: c, 14: C, 6: b, 8: a},
                37: {2: d, 20: D, 16: c, 5: C, 7: B, 9: A}}
    
        return graph
