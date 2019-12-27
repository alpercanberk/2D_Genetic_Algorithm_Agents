import pygame
import random
import numpy as np
import math

import sys
sys.path.insert(1, './Sprites')
from wall import Wall
from food import Food
from agent import Agent

from neural_network import *

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 50, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

DEFAULT_FOOD_SIZE = 3
DEFAULT_AGENT_SIZE = 5

def default_fitness_metric(self):
    return self.fitness

def calculate_num_weights(layers):
    num_weights = 0
    n_layers = len(layers)
    for i in range(0, n_layers-1):
        num_weights += layers[i] * layers[i+1]
    return num_weights

def sensor(self, display):
        display_copy = display.copy()
        # sight = display_copy.subsurface(self.rect.x - sight_radius,
        #                           self.rect.y - sight_radius,
        #                           2*sight_radius + self.agent_size,
        #                           2*sight_radius + self.agent_size)
        sight = display_copy.subsurface(0,0,50,50)
        sight_array = np.array(pygame.surfarray.pixels3d(sight))
        # sight1 = sight[:self.rect.x][:self.rect.y].flat
        # sight[self.rect.x+self.agent_size:][self.rect.y+self.agent_size:].flat

        color_slices = []
        for array_slice in np.rollaxis(sight_array, 2):
            color_slices.append(array_slice)

        #I could have implemented maxpooling myself, but who has time for that
        sight_array = np.array([skimage.measure.block_reduce(slice, (maxpooling_filter_size, maxpooling_filter_size), np.max) for slice in color_slices])

        #flatten for the regular dnn, no fancy CNNs here
        sight_array = np.array(sight_array.flat)

        #Normalize the data
        sight_array = sight_array / np.linalg.norm(sight_array)

        pygame.image.save(sight, "sight.jpg")
        return sight_array

class AgentBrain():

    def __init__(self,
                 display,
                 clock,
                 sensor,
                 neural_network,
                 layer_sizes,
                 ):

        self.display = display
        self.input_size = sensor(self, display).shape[0]
        self.layer_sizes = list(layer_sizes).insert(0, self.input_size)
        self.num_weights = calculate_num_weights(self.layer_sizes)
        self.weights = []

    def set_weights(weights):

        if(weights.shape[0] == self.num_weights):

            layer_shapes = []
            for i in range(0, len(self.layer_sizes)-1):
                layer_shapes.append((self.layer_sizes[i], self.layer_sizes[i+1]))

            previous_weight_length = 0
            for width, height in layer_shapes:
                weight_length = width*height
                self.weights.append(weights[previous_weight_length: weight_length])
                previous_weight_length = weight_length

        else:
            print("You have input the incorrect number of weights,\
                  please input", self.num_weights, "weights")

    def make_decision():
        decision = neural_network(self.weights,
                                  self.sensor(display))
        return decision




class Simulation():

    def __init__(self,
                 display,
                 food_size=DEFAULT_FOOD_SIZE,
                 agent_size=DEFAULT_AGENT_SIZE,
                 ):

        self.screen_width, self.screen_height = pygame.display.get_surface().get_size()

        self.wall_list = pygame.sprite.Group()
        self.feed_list = pygame.sprite.Group()
        self.agent_list = []
        self.all_sprites_list = pygame.sprite.Group()

        #this class can only create food and agents in one size
        self.food_size = food_size
        self.agent_size = agent_size

    def create_wall(self, x, y, wall_width, wall_height, color):

        new_wall = Wall(x, y, wall_width, wall_height, color)
        self.wall_list.add(new_wall)
        self.all_sprites_list.add(new_wall)

    def generate_food(self, coordinates):

        for coordinate in coordinates:
            new_food = Food(coordinate[0], coordinate[1], self.food_size)
            self.feed_list.add(new_food)
            self.all_sprites_list.add(new_food)

    def generate_agents(coordinates,
                     display,
                     brains,
                     fitness_metric=default_fitness_metric):

        for coordinate in coordinates:
            new_agent = Agent(brain,
                              coordinate[0],
                              coordinate[1],
                              self.agent_size)
            new_agent.fitness_metric = fitness_metric
            agent_list.append(new_agent)
            all_sprites_list.add(new_agent)

    def run_game(self, max_steps):

        all_sprite_list = self.all_sprites_list

        step_count = 0
        done = False
        while done is not True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

            if(step_count > max_steps):
                done = True

            display.fill(BLACK)

            all_sprite_list.draw(display)

            all_sprite_list.update()
            pygame.display.update()

            clock.tick(60)

            step_count += 1

    def get_fitness(self):
        return [agent.fitness_metric() for agent in self.agent_list]


pygame.init()
display=pygame.display.set_mode((300,300))
clock=pygame.time.Clock()

simulation = Simulation(display)

screen_width = simulation.screen_width
screen_height = simulation.screen_height

simulation.create_wall(0,0, screen_width, 30, BLUE)

food_coordinates = [[30,30], [50,50], [70,70]]

simulation.generate_food(food_coordinates)

simulation.run_game(500)
