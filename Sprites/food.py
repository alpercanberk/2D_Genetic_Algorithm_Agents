
import numpy as np
from Utils import *

class Food():

    def __init__(self, type, size ,init_coordinates):

        self.size = size
        self.type = type

        self.x = init_coordinates[0]
        self.y = init_coordinates[1]

        self.rect = rectangle(self.size, self.size, self.type)

        self.eaten = False

        self.id = generate_random_id()

        log("initializing food with id: ", self.id)
        log("type", self.type)
        log("coordinates:", (self.x, self.y))
        log("width", self.size)
        log("height", self.size)

    def render(self, display):
        if not self.eaten:
            display[self.y:self.y+self.rect.shape[1], self.x:self.x+self.rect.shape[0]] = self.type

    def eat(self):
        if not self.eaten:
            log("food", self.id, "eaten")
            self.eaten = True

    def update(self):
        return 0
