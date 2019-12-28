
import numpy as np
from Primitives import *

class SquareAgent():

    def __init__(self, type, size, init_coordinates, walls, feed):

        self.size = size
        self.type = type

        self.x = init_coordinates[0]
        self.y = init_coordinates[1]

        self.rect = rectangle(self.size, self.size, self.type)

        self.prev_x = None
        self.prev_y = None

        self.change_x = -1
        self.change_y = 0

        self.walls = walls
        self.feed = feed

        self.score = 0

        self.id = generate_random_id()


        log("initializing agent with id: ", self.id)
        log("type", self.type)
        log("coordinates:", (self.x, self.y))
        log("width", self.size)
        log("height", self.size)


    def render(self, display):
        display[self.y:self.y+self.rect.shape[1], self.x:self.x+self.rect.shape[0]] = self.type

    def move(self):

        self.x += self.change_x
        self.y += self.change_y

        log("agent", self.id, "changed position by:", (self.change_x, self.change_y))

    def update(self):

        self.move()

        for wall in self.walls:
            if does_intersect_2d(self.x, self.y, self.size, self.size,
                                 wall.x, wall.y, wall.rect.shape[0], wall.rect.shape[1]):
                log("agent", self.id, "collided with a wall, ignore change_position")
                if self.change_x < 0:
                    self.x = wall.rect.shape[0]
                if self.change_x > 0:
                    self.x = wall.x-self.size
                if self.change_y > 0:
                    self.y = wall.y-self.size
                if self.change_y < 0:
                    self.y = wall.rect.shape[1]

        for food in self.feed:
            if does_intersect_2d(self.x, self.y, self.size, self.size,
                                 food.x, food.y, food.rect.shape[0], food.rect.shape[1]):
                food.eat()
                self.score += 1
