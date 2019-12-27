import pygame
import math
import numpy as np
import random

WHITE = (255, 255, 255)
BLUE = (100, 100, 255)


class Agent(pygame.sprite.Sprite):

    def __init__(self, brain, x, y, agent_size):

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
        self.wall_list = None
        self.feed_list = None

        self.fitness = 0
        self.brain = brain

    def move(self):

        self.activations = self.brain.make_decision()

        self.change_x = self.activations[0] - self.activations[1]
        self.change_y = self.activations[2] - self.activations[3]

    def update(self):

        self.brain.sensor.set_sight_position(self.rect.x, self.rect.y)
        #render score on agent
        text = self.font.render(str(self.fitness), True, BLUE)
        self.image.fill(WHITE)
        self.image.blit(text, [self.agent_size/4,0])

        self.move()

        self.rect.x += self.change_x

        block_hit_list = pygame.sprite.spritecollide(self, self.wall_list, False)
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
        block_hit_list = pygame.sprite.spritecollide(self, self.wall_list, False)
        for block in block_hit_list:

            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom

        food_found = pygame.sprite.spritecollide(self, self.feed_list, True)

        for food in food_found:
            self.fitness += 1
