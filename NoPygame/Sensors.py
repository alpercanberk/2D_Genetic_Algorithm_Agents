import numpy as np
import pygame
import skimage.measure

class SquareSensor():
        def __init__(self, display, agent_size, sight_radius, maxpooling_filter_size):

            self.maxpooling_filter_size = maxpooling_filter_size
            self.sight_radius = sight_radius

            x,y = pygame.display.get_surface().get_size()

            self.x = x/2
            self.y = y/2

            self.display = display

            self.agent_size = agent_size

        def get_sight(self):
            display_copy = self.display.copy()
            sight = display_copy.subsurface(self.x - self.sight_radius,
                                      self.y - self.sight_radius,
                                      2*self.sight_radius + self.agent_size,
                                      2*self.sight_radius + self.agent_size)
            # sight = display_copy.subsurface(0,0,50,50)
            sight3d = np.array(pygame.surfarray.pixels3d(sight))

            color_slices = []
            for array_slice in np.rollaxis(sight3d, 2):
                color_slices.append(array_slice)

            #I could have implemented maxpooling myself, but who has time for that
            sight_array = np.array([skimage.measure.block_reduce(slice, (self.maxpooling_filter_size, self.maxpooling_filter_size), np.max) for slice in color_slices])

            #flatten for the regular dnn, no fancy CNNs here
            sight_array = np.array(sight_array.flat)

            #Normalize the data
            sight_array = sight_array / np.linalg.norm(sight_array)

            #for debug purposes
            pygame.image.save(sight, "sight.jpg")
            return sight_array

        def get_output_shape(self):
            return self.get_sight().shape[0]

        def set_sight_position(self, x, y):
            self.x = x
            self.y = y
