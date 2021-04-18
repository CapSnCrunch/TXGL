import pygame
import numpy as np
import matplotlib.pyplot as plt

class Interval():
    def __init__(self, a, b, mat, letters, color):
        self.a = a
        self.b = b
        self.mat = mat
        self.color = color
        self.letters = letters

    def get_image(self):
        # get image of the interval under all letters but inv(self.mat)
        I = rp1_interval(self.a, self.b)
    
    def draw(self, win):
        theta1, theta2 = get_arc_params(rp1_interval(self.a, self.b))
        pygame.draw.arc(win, self.color, (30, 30, 440, 440), np.radians(theta2), np.radians(theta1), 20)

def rp1_to_s1(v):
    """map a point in R^2 - {0} to S1 via the homeo RP1 -> S1"""
    x, y = v[0], v[1]

    return np.row_stack([
        2*x*y / (x*x + y*y),
        (x*x - y*y) / (x*x + y*y)
    ])

def get_arc_params(interval):
    """map a pair of points in R^2 - {0} to a pair of circle angles"""
    x, y = rp1_to_s1(interval)
    return np.arctan2(y,x) * 180 / np.pi

def rp1_interval(theta1, theta2):
    """get a pair of points in RP1 representing the pair of angles theta1, theta2

    note: theta1, theta2 paramaterize the double cover of RP^1"""
    return np.array([
        [np.cos(theta1), np.cos(theta2)],
        [np.sin(theta1), np.sin(theta2)]
    ])

def update_window(win, intervals):
    win.fill((255, 255, 255))
    pygame.draw.circle(win, (200,200,200), (250,250), 210, 3)
    for interval in intervals:
        interval.draw(win)
    #pygame.draw.rect(win, (255, 0, 0), (30, 30, 440, 440))
    pygame.display.update()

if __name__ == '__main__':

    window_size = 500
    win = pygame.display.set_mode((window_size, window_size))
    pygame.display.set_caption('Ping Pong')

    ########################################################################
    # a pair of matrices in SL(2, Z), which (maybe?) generate a free group
    A = np.array([[1, 1],
                [2, 3]])

    B = np.array([[1, -1],
                [-2, 3]])

    generators = [A, B]
    letters = []
    for g in generators:
        letters += [g]
        letters += [np.linalg.inv(g)]

    # Theta for Eigenvectors on S1 via RP1 -> S1
    colors = [(0, 0, 255), (255, 0, 0)]
    intervals = []
    iter = 0
    for mat in generators:

        e1 = np.arctan2(np.linalg.eig(mat)[1][1][0], np.linalg.eig(mat)[1][0][0])
        e2 = np.arctan2(np.linalg.eig(mat)[1][1][1], np.linalg.eig(mat)[1][0][1])

        intervals.append(Interval(e1 - 0.05, e1 + 0.05, mat, letters, colors[iter]))
        intervals.append(Interval(e2 - 0.05, e2 + 0.05, np.linalg.inv(mat), letters, colors[iter]))

        iter += 1
    ########################################################################

    clock = pygame.time.Clock()
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        update_window(win, intervals)