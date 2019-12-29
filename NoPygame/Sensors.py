import numpy as np
import skimage.measure

import matplotlib.pyplot as plt

class SquareSensor():
        def __init__(self, display, agent_size, sight_radius, maxpooling_filter_size, type_dict):

            self.maxpooling_filter_size = maxpooling_filter_size
            self.sight_radius = sight_radius

            x,y = display.shape

            self.x = x/2
            self.y = y/2

            self.display = display

            self.agent_size = agent_size

            self.type_dict = type_dict

        def get_sight(self):

            left = int(self.x - self.sight_radius)
            right = int(left + 2*self.sight_radius + self.agent_size)

            up = int(self.y - self.sight_radius)
            down = int(up + self.agent_size + 2*self.sight_radius)

            print(up,down,left,right, "udlr")
            print(self.display.shape)
            print(down-up, "down-up")
            print(self.display[left:right, 10:25].shape, "dummy shape")

            sight = self.display[left:right, up:down]

            print(sight.shape, "sight shape")

            sight3d = np.zeros((sight.shape[0], sight.shape[1], len(self.type_dict.keys())))

            for x in range(sight.shape[0]):
                for y in range(sight.shape[1]):
                    sight3d[x, y, int(sight[x, y])] = 1

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
            return sight_array

        def get_output_shape(self):
            return self.get_sight().shape[0]

        def set_sight_position(self, x, y):
            self.x = x
            self.y = y
