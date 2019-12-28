
import numpy as np
import sys
import time

sys.path.insert(1, './Sprites')

from Wall import Wall
from Food import Food
from Square_Agent import SquareAgent
from Primitives import *

import matplotlib.pyplot as plt
plt.ion()
import numpy as np


class Simulation():

    def __init__(self, screen_width, screen_height, type_dict):

        self.display = np.zeros((screen_width, screen_height))
        self.all_sprites = []

        clear_log()

        log("type dict:")
        for key in type_dict.keys():
            log(type_dict[key], key)

    def add_sprite(self, object):
        self.all_sprites.append(object)


    def render_screen(self, visualize):

        for sprite in self.all_sprites:
            sprite.render(self.display)

        if visualize:
            plt.close()
            plt.matshow(self.display)
            plt.show()
            plt.pause(0.001)

    def update_sprites(self):
        for sprite in self.all_sprites:
            sprite.update()

    def run(self, num_steps, visualize = False):

        for i in range(0, num_steps):
            self.update_sprites()
            if(visualize):
                self.render_screen(visualize)

            self.display = np.zeros((self.display.shape[0], self.display.shape[1]))
            log("Frame", i)


screen_width = 200
screen_height = 500
wall_thickness = 5

type_dict = {
    "none":0,
    "agent":1,
    "food":2,
    "wall":3
}

simulation = Simulation(screen_height, screen_width, type_dict)

feed = []

for i in range(5, 100, 3):
    food = Food(type_dict["food"], 2, [i, i])
    simulation.add_sprite(food)
    feed.append(food)


walls = []

walls.append(Wall(type_dict["wall"], screen_width, wall_thickness,[0,0]))
walls.append(Wall(type_dict["wall"], wall_thickness, screen_height,[0,0]))
walls.append(Wall(type_dict["wall"], screen_height, wall_thickness,[0,screen_height-wall_thickness]))
walls.append(Wall(type_dict["wall"], wall_thickness, screen_height,[screen_width-wall_thickness,0]))

agent = SquareAgent(type=type_dict["agent"], size=5, init_coordinates=[80, 50], walls=walls, feed=feed)
agent.walls = walls
agent.feed = feed

simulation.add_sprite(agent)

for wall in walls:
    simulation.add_sprite(wall)

simulation.run(100)
