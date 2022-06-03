import colorsys
from classes.intervals import *
from classes.interval_funcs import *
from classes.group_funcs import *
from classes.graph_funcs import *

# A, B in <a, b, c | a^2 = b^2 = c^2 = 1, (ab)^3 = (cb)^3 = (ac)^4 = 1>
mat = np.array([[ 0.923879532511287, -0.217284326304659],
               [-0.673986071141597, -0.923879532511287]])

# OLD SURFACE GROUP REPRESENTATION
# l = 2 * (2 ** (1/4)) * np.cos(np.pi/8) + (2 ** (1/2)) + 1
# X = np.array([[l, 0], [0, 1/l]])

# R = lambda theta: np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])

# a = X
# b = R(-np.pi/8) @ X @ R(np.pi/8)
# c = R(-np.pi/4) @ X @ R(np.pi/4)
# d = R(-3*np.pi/8) @ X @ R(3*np.pi/8)

# A = np.linalg.inv(a)
# B = np.linalg.inv(b)
# C = np.linalg.inv(c)
# D = np.linalg.inv(d)

# NEW SURFACE GROUP REPRESENTATION
s = 12
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

mat = d

#mat = np.array([[0.70710678, -1.59099026],
#                [0.31426968, 0.70710678]])

# A, B in <a,b | a^2 = b^3 = 1>
#mat = np.array([[0, -1], [1, 0]])
#mat = np.array([[6.123234e-17, -2.500000e-01],
#                [4.000000e+00, 6.123234e-17]])
#mat = np.array([[0.5, -3.46410162],
#                [0.21650635, 0.5]])

n = 200
delta = np.pi / n

intervals = []
for i in range(n):
    color = np.array([i for i in colorsys.hsv_to_rgb(i/n,1,1)])
    intervals.append(Interval(i * delta - delta / 10, (i+1) * delta + delta / 10, color))

fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (10, 5))

# RP1
rp1 = Circle((0, 0), 1.0, fill = False)
#ax1.add_patch(rp1)

view = 0
# 13, 14 acts weird
for i in range(n):
    intervals[i].draw(ax1)

for i in range(n):
    I = rp1_interval(intervals[i].a % np.pi, intervals[i].b % np.pi)

    # Check if the transformation flips orientation (if it does we need to flip angles)
    if np.linalg.det(mat) < 0:
        theta2, theta1 = sorted(get_arc_params(mat @ I), reverse = True)
        #if theta1 < theta2 and np.sign(theta1) != np.sign(theta2):
        #    theta1 -= 180
        #    print(i, theta1, theta2)

        # Check if the image will contain infinity (if it does we need to flip angles)
        test_interval = Interval(3*np.pi/4 - 1e-3, 3*np.pi/4 + 1e-3, 0, 0, [], np.array([0,0,0]))
        if intervals[i].contains_image(test_interval, np.linalg.inv(mat)):
            theta1, theta2 = theta2, theta1
            print("image contains infinity")
            test_interval.draw(ax2)
            test_interval.draw_image(ax1, np.linalg.inv(mat))

    else:
        theta2, theta1 = get_arc_params(mat @ I)

    #a, b = get_arc_params(mat @ I)
    #if a > b:
    #    print(i)
    #    print(rp1_to_s1(I))
    #    print(rp1_to_s1(mat @ I))
    #    print(get_arc_params(mat @ I))
        
    ax2.add_patch(Arc((0,0), 2., 2., theta1 = theta1, theta2 = theta2, color = intervals[i].color, linewidth = 10))

#test_interval = rp1_interval(3*np.pi/4 - 1e-3, 3*np.pi/4 + 1e-3)
#temp2, temp1 = get_arc_params(test_interval)
#ax2.add_patch(Arc((0,0), 2., 2., theta1 = temp1, theta2 = temp2, color = "black", linewidth = 10))
#temp2, temp1 = get_arc_params(np.linalg.inv(mat) @ test_interval)
#ax1.add_patch(Arc((0,0), 2., 2., theta1 = temp2, theta2 = temp1, color = "black", linewidth = 10))

# Plot data
ax1.set_xlim((-1.1, 1.1))
ax1.set_ylim((-1.1, 1.1))
ax1.axis('off')
ax1.set_aspect('equal')
ax2.set_xlim((-1.1, 1.1))
ax2.set_ylim((-1.1, 1.1))
ax2.axis('off')
ax2.set_aspect('equal')

plt.show()