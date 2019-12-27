import pygame
import math
import numpy as np
import random

WHITE = (255, 255, 255)
BLUE = (100, 100, 255)

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
MAX_AGENTS = 10

AGENT_SIZE = 10
FOOD_SIZE = 3
WALL_THICKNESS = 60

def edge_proximity_punishment(left, right, point):
    return (right-point)^2 + (point-left)^2

class Agent(pygame.sprite.Sprite):

    def __init__(self, brain, x, y, agent_size, display):

        super().__init__()

        #Initialize a font that's as big as the agent
        pygame.font.init()
        self.font = pygame.font.SysFont('times', int(agent_size), True, False)
        self.agent_size = agent_size

        # Set height, width
        self.image = pygame.Surface([agent_size, agent_size])
        self.image.fill(WHITE)

        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

        self.change_x = 0
        self.change_y = 0

        #these will be assigned later
        self.walls = None
        self.feed = None

        self.food_score = 0

        self.sight_radius = 30

        self.brain = brain
        self.display = display

        self.max_v = 4
        self.rotation_speed = 0.5
        self.theta = 0

        self.activations = []

        self.diversity_of_direction=[0,0,0,0]

        self.total_change_x = 0
        self.total_change_y = 0

    def get_sight_radius():
        return self.sight_radius

    def move(self):

        self.activations = self.brain(self.sight)

        self.change_x = self.activations[0] - self.activations[1]
        self.change_y = self.activations[2] - self.activations[3]

        normalizing_constant = math.sqrt(self.change_x ** 2 + self.change_y**2)

        self.change_x *= self.activations[4] * self.max_v
        self.change_y *= self.activations[4] * self.max_v

        self.change_x /= normalizing_constant
        self.change_y /= normalizing_constant

        self.total_change_x += abs(self.change_x)
        self.total_change_y += abs(self.change_y)

        if self.change_x > 0:
            self.diversity_of_direction[0] = 1
        else:
            self.diversity_of_direction[1] = 1

        if self.change_y > 0:
            self.diversity_of_direction[2] = 1
        else:
            self.diversity_of_direction[3] = 1

    def get_score(self):

        # epp = edge_proximity_punishment(0, SCREEN_WIDTH, self.rect.x) + edge_proximity_punishment(0, SCREEN_HEIGHT, self.rect.y)
        score = self.food_score
        return score

    def respawn(self):
        self.rect.x = random.randrange(WALL_THICKNESS + AGENT_SIZE, SCREEN_WIDTH - WALL_THICKNESS - AGENT_SIZE)
        # self.rect.y = random.randrange(WALL_THICKNESS + AGENT_SIZE, SCREEN_HEIGHT - WALL_THICKNESS - AGENT_SIZE)


    def update(self):

        #render score on agent
        text = self.font.render(str(self.food_score), True, BLUE)
        self.image.fill(WHITE)
        self.image.blit(text, [self.agent_size/4,0])


        self.get_sight(self.display)
        self.move()

        self.rect.x += self.change_x

        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            # If we are moving right, set our right side to the left side of
            # the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            else:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:

            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom

        food_found = pygame.sprite.spritecollide(self, self.feed, True)

        for food in food_found:
            self.food_score += 1

    def get_sight(self, display):
        sight_radius = self.sight_radius
        display_copy = display.copy()
        sight = display_copy.subsurface(self.rect.x - sight_radius,
                                  self.rect.y - sight_radius,
                                  2*sight_radius + self.agent_size,
                                  2*sight_radius + self.agent_size)
        sight = np.array(pygame.surfarray.pixels3d(sight))
        print(sight.shape)
        # sight1 = sight[:self.rect.x][:self.rect.y].flat
        # sight[self.rect.x+self.agent_size:][self.rect.y+self.agent_size:].flat
        # pygame.image.save(sight, "screenshot.jpg")
        self.sight = sight

    def get_activations():
        return self.activations
