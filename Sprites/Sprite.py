
from enum import Enum, IntEnum

class Sprite():

    def render(self, display):
        self.y = int(self.y)
        self.x = int(self.x)
        display[self.y:self.y+self.rect.shape[1], self.x:self.x+self.rect.shape[0]] = self.type

    def update(self):
        return 0

class SpriteType(IntEnum):
    EMPTY = 0
    AGENT = 1
    FOOD = 2
    WALL = 3
