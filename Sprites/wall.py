
import numpy as np
from Utils import *

from Sprite import Sprite, SpriteType

class Wall(Sprite):
    def __init__(self, width, height, init_coordinates):

        self.type = SpriteType.WALL

        self.x = init_coordinates[0]
        self.y = init_coordinates[1]

        self.rect = rectangle(width, height, self.type)

        self.id = generate_random_id()

        log("initializing wall with id: ", self.id)
        log("type", self.type)
        log("coordinates:", (self.x, self.y))
        log("width", width)
        log("height", height)
