
import numpy as np
from Utils import *

from Sprite import Sprite, SpriteType

class SquareAgent(Sprite):

    def __init__(self, simulation, size, init_coordinates):

        self.simulation = simulation

        self.size = size
        self.type = SpriteType.AGENT

        self.x = init_coordinates[0]
        self.y = init_coordinates[1]

        self.rect = rectangle(self.size, self.size, self.type)

        self.brain = None

        self.change_x = 0
        self.change_y = 0

        self.fitness = 0

        self.id = generate_random_id()

        self.v = 2
        self.steer_v = 2
        self.direction = np.random.uniform(0,2*np.pi)

        self.distance_traveled = 0

        log("initializing agent with id: ", self.id)
        log("type", self.type)
        log("coordinates:", (self.x, self.y))
        log("width", self.size)
        log("height", self.size)

    def move(self):

        activations = self.brain.make_decision()

        velocity = (activations[0]-activations[1])*self.v
        self.direction += (activations[2] - activations[3])*self.steer_v

        self.change_x = velocity * np.cos(self.direction)
        self.change_y = velocity * np.sin(self.direction)

        # try:
        #     normalizing_constant = math.sqrt(self.change_x ** 2 + self.change_y ** 2) * (1/self.v)
        #     self.change_x /= normalizing_constant
        #     self.change_y /= normalizing_constant
        # except:
        #     pass

        log("c_pos agent",self.id, (self.change_x, self.change_y))

    def fitness_metric(self):
        return self.fitness

    def update(self):

        self.move()

        self.x += self.change_x

        walls = self.simulation.walls
        feed = self.simulation.collect_sprites(SpriteType.FOOD, (lambda food: food.eaten == False))

        for wall in walls:
            intersection = does_intersect_2d(self.x, self.y, self.size, self.size,
                                 wall.x, wall.y, wall.rect.shape[0], wall.rect.shape[1])
            if intersection:
                log("agent", self.id, "ignore horizontal c_pos")
                if self.change_x < 0:
                    self.x = wall.rect.shape[0]
                else:
                    self.x = wall.x-self.size


        self.y += self.change_y

        for wall in walls:
            intersection = does_intersect_2d(self.x, self.y, self.size, self.size,
                                 wall.x, wall.y, wall.rect.shape[0], wall.rect.shape[1])
            if(intersection):
                log("agent", self.id, "ignore vertical c_pos")
                if self.change_y > 0:
                    self.y = wall.y-self.size
                else:
                    self.y = wall.rect.shape[1]

        self.distance_traveled += np.sqrt(self.change_x**2 + self.change_y**2)

        for food in feed:
            if does_intersect_2d(self.x, self.y, self.size, self.size,
                                 food.x, food.y, food.rect.shape[0], food.rect.shape[1]):
                if not food.eaten:
                    self.fitness += 1
                    food.eat()
