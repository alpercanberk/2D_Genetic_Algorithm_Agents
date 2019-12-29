
import numpy as np
from Utils import *

class Wall():
    def __init__(self, type, width, height, init_coordinates):

        self.type = type

        self.x = init_coordinates[0]
        self.y = init_coordinates[1]

        self.rect = rectangle(width, height, self.type)

        self.id = generate_random_id()

        log("initializing wall with id: ", self.id)
        log("type", self.type)
        log("coordinates:", (self.x, self.y))
        log("width", width)
        log("height", height)


    def render(self, display):
        display[self.y:self.y+self.rect.shape[1], self.x:self.x+self.rect.shape[0]] = self.type

    def update(self):
        return 0
