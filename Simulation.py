
import numpy as np
import sys
import time

sys.path.insert(1, './Sprites')
from Utils import *

import matplotlib.pyplot as plt
from pylab import rcParams
rcParams['figure.figsize'] = 10,10

plt.ion()

class Simulation():

    def __init__(self, screen_width, screen_height):

        self.display = np.zeros((screen_width, screen_height))
        self.all_sprites = []

        clear_log()

        log("screen_size")
        log("width", screen_width)
        log("height", screen_height)

        self.visualize = False
        self.walls = []

    def add_sprite(self, object):
        self.all_sprites.append(object)

    def add_wall(self, object):
        self.walls.append(object)
        self.all_sprites.append(object)

    def render_screen(self):

        for sprite in self.all_sprites:
            sprite.render(self.display)

        if self.visualize:
            plt.close()
            plt.matshow(self.display)
            plt.show()
            plt.pause(0.001)

    def update_sprites(self):
        for sprite in self.all_sprites:
            sprite.update()

    def collect_sprites(self, type, condition=(lambda x: True)):
        return [sprite for sprite in self.all_sprites if sprite.type == type and condition(sprite)]

    def collect_coordinates(self, type, condition=(lambda x: True)):
        return [(sprite.x, sprite.y) for sprite in self.all_sprites if sprite.type == type and condition(sprite)]

    def run(self, num_steps, visualize = False):

        if visualize:
            self.visualize = True

        for i in range(0, num_steps):
            log("Frame", i)
            self.render_screen()
            self.update_sprites()
            if not (i == num_steps):
                self.display = np.zeros((self.display.shape[0], self.display.shape[1]))

    def get_fitness(self, type):
        return [agent.fitness_metric() for agent in self.all_sprites if agent.type == type]
