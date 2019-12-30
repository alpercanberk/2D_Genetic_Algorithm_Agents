
import numpy as np
from Utils import *

class SquareAgent():

    def __init__(self, type, size, init_coordinates, walls, feed):

        self.size = size
        self.type = type

        self.x = init_coordinates[0]
        self.y = init_coordinates[1]

        self.rect = rectangle(self.size, self.size, self.type)

        self.change_x = -1
        self.change_y = 0

        self.walls = walls
        self.feed = feed

        self.fitness = 0

        self.id = generate_random_id()

        self.brain = None

        log("initializing agent with id: ", self.id)
        log("type", self.type)
        log("coordinates:", (self.x, self.y))
        log("width", self.size)
        log("height", self.size)


    def render(self, display):

        self.y = int(self.y)
        self.x = int(self.x)

        display[self.y:self.y+self.rect.shape[1], self.x:self.x+self.rect.shape[0]] = self.type

    def move(self):

        self.activations = self.brain.make_decision()

        self.change_x = float(self.activations[0] - self.activations[1])
        self.change_y = float(self.activations[2] - self.activations[3])

        log("c_pos agent",self.id, (self.change_x, self.change_y))

    def set_sight_position(self):
        self.brain.sensor.set_sight_position(self.x, self.y)

    def update(self):

        self.set_sight_position()
        self.move()

        self.x += self.change_x

        for wall in self.walls:
            intersection = does_intersect_2d(self.x, self.y, self.size, self.size,
                                 wall.x, wall.y, wall.rect.shape[0], wall.rect.shape[1])
            if intersection:
                log("agent", self.id, "ignore horizontal c_pos")
                if self.change_x < 0:
                    self.x = wall.rect.shape[0]
                else:
                    self.x = wall.x-self.size


        self.y += self.change_y

        for wall in self.walls:
            intersection = does_intersect_2d(self.x, self.y, self.size, self.size,
                                 wall.x, wall.y, wall.rect.shape[0], wall.rect.shape[1])
            if(intersection):
                log("agent", self.id, "ignore vertical c_pos")
                if self.change_y > 0:
                    self.y = wall.y-self.size
                else:
                    self.y = wall.rect.shape[1]



        for food in self.feed:
            if does_intersect_2d(self.x, self.y, self.size, self.size,
                                 food.x, food.y, food.rect.shape[0], food.rect.shape[1]):
                if not food.eaten:
                    self.fitness += 1
                    food.eat()
