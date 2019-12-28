import pygame
import random
import numpy as np
import math

import sys
sys.path.insert(1, './Sprites')
from wall import Wall
from food import Food
from agent import Agent

from Neural_Network import *
from Agent_Brain import *
from Sensors import *

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 50, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

DEFAULT_FOOD_SIZE = 3
DEFAULT_AGENT_SIZE = 5

def default_fitness_metric(self):
    return self.fitness

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
        self.display = display

    def create_wall(self, x, y, wall_width, wall_height, color):

        new_wall = Wall(x, y, wall_width, wall_height, color)
        self.wall_list.add(new_wall)
        self.all_sprites_list.add(new_wall)

    def generate_food(self, coordinate):

        new_food = Food(coordinate[0], coordinate[1], self.food_size)
        self.feed_list.add(new_food)
        self.all_sprites_list.add(new_food)

    def generate_agent(self,
                     coordinate,
                     brain,
                     fitness_metric=default_fitness_metric):

        new_agent = Agent(brain,
                          coordinate[0],
                          coordinate[1],
                          self.agent_size)
        new_agent.fitness_metric = fitness_metric
        new_agent.wall_list = self.wall_list
        new_agent.feed_list = self.feed_list
        self.agent_list.append(new_agent)
        self.all_sprites_list.add(new_agent)

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

            self.display.fill(BLACK)

            all_sprite_list.draw(self.display)

            all_sprite_list.update()
            pygame.display.update()

            # clock.tick(60)

            step_count += 1

    def get_fitness(self):
        return [agent.fitness_metric() for agent in self.agent_list]
