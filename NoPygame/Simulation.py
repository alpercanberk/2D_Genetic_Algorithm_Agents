
import numpy as np
import sys
import time

from Sensors import SquareSensor
from Neural_Network import *
from Agent_Brain import *

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

        log("screen_size")
        log("width", screen_width)
        log("height", screen_height)

        log("type dict:")
        for key in type_dict.keys():
            log(type_dict[key], key)

        self.visualize=False

    def add_sprite(self, object):
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

    def run(self, num_steps, visualize = False):

        if visualize:
            self.visualize = True

        for i in range(0, num_steps):
            self.update_sprites()
            self.render_screen()
            if not (i == num_steps):
                self.display = np.zeros((self.display.shape[0], self.display.shape[1]))
            log("Frame", i)



#example simulation

screen_width = 200
screen_height = 500
wall_thickness = 5

type_dict = {
    0:"none",
    1:"agent",
    2:"food",
    3:"wall"
}

agent_size = 5
sight_radius = 20
maxpooling_filter_size = 2

inv_type_dict = dict(map(reversed, type_dict.items()))
simulation = Simulation(screen_height, screen_width, type_dict)

feed = []

for i in range(5, 100, 3):
    food = Food(inv_type_dict["food"], 2, [i, i])
    simulation.add_sprite(food)
    feed.append(food)

walls = []

walls.append(Wall(inv_type_dict["wall"], screen_width, wall_thickness,[0,0]))
walls.append(Wall(inv_type_dict["wall"], wall_thickness, screen_height,[0,0]))
walls.append(Wall(inv_type_dict["wall"], screen_height, wall_thickness,[0,screen_height-wall_thickness]))
walls.append(Wall(inv_type_dict["wall"], wall_thickness, screen_height,[screen_width-wall_thickness,0]))

sensor = SquareSensor(simulation.display,
                      agent_size,
                      sight_radius,
                      maxpooling_filter_size,
                      type_dict)

brain = AgentBrain(
    display = simulation.display,
    sensor = sensor,
    neural_network = forward_propagation,
    layer_sizes = [4,4,4]
)

weights = np.random.choice(np.arange(-1,1,step=0.01),size=brain.num_weights,replace=True)
brain.set_weights(weights)

agent = SquareAgent(type=inv_type_dict["agent"],
                    size=5,
                    init_coordinates=[80, 50],
                    walls=walls,
                    feed=feed
                    )

agent.brain = brain
agent.walls = walls
agent.feed = feed

simulation.add_sprite(agent)

for wall in walls:
    simulation.add_sprite(wall)

simulation.run(100)
