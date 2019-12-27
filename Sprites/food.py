import pygame

RED = (255, 0, 0)

class Food(pygame.sprite.Sprite):

    def __init__(self, x, y, size):

        super().__init__()

        self.image = pygame.Surface([size, size])
        self.image.fill(RED)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
