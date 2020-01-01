import numpy as np
import sys
import math

sys.path.insert(1, './Sprites')
from Utils import *


class AgentBrain():

    def __init__(self,
                 simulation,
                 neural_network,
                 layer_sizes,
                 type_dict
                 ):

        self.simulation = simulation
        self.type_dict = type_dict

        self.x = 0
        self.y = 0
        self.food_coordinates = [[0,0]]

        self.input_size = self.get_output_shape()
        self.layer_sizes = list(layer_sizes)
        self.layer_sizes.insert(0, self.input_size)
        self.num_weights = calculate_num_weights(self.layer_sizes)
        self.bias_sizes = self.layer_sizes[1:]
        self.num_biases = sum(self.bias_sizes)

        self.weights = []
        self.biases = []

        self.neural_network = neural_network


    def set_weights(self, weights):

        if(weights.shape[0] == self.num_weights + self.num_biases):

            flat_weights = []

            layer_shapes = []
            for i in range(0, len(self.layer_sizes)-1):
                layer_shapes.append((self.layer_sizes[i], self.layer_sizes[i+1]))

            previous_weight_length = 0

            for width, height in layer_shapes:
                weight_length = width*height

                flat_weights.append(weights[previous_weight_length: previous_weight_length + weight_length])
                previous_weight_length = weight_length+previous_weight_length

            for i in range(0, len(flat_weights)):
                self.weights.append(flat_weights[i].reshape(layer_shapes[i][1], layer_shapes[i][0]))

            prev_index = self.num_weights
            for bias_size in self.bias_sizes:
                self.biases.append(weights[prev_index:prev_index+bias_size])
                prev_index += bias_size

            self.biases = np.array([np.array(bias_layer) for bias_layer in self.biases])
        else:
            print("You have input the incorrect number of weights,\
                  please input", self.num_weights, "weights")

    def get_sight(self):
        nearest_food = closest_point((self.x, self.y), self.food_coordinates)
        dist_from_nearest_food = math.sqrt((self.x-nearest_food[0])**2 + (self.y-nearest_food[1])**2)

        try:
            angle_to_the_nearest_food = math.atan((self.y-nearest_food[1])/(self.x-nearest_food[0]))
        except:
            angle_to_the_nearest_food = math.pi/2

        return np.array((dist_from_nearest_food, angle_to_the_nearest_food))

    def get_output_shape(self):
        return self.get_sight().shape[0]

    def set_brain_position(self, x, y):
        self.x = x
        self.y = y

    def set_food_coordinates(self, food_coordinates):
        self.food_coordinates = food_coordinates

    def make_decision(self):
        self.set_food_coordinates(self.simulation.collect_coordinates(self.type_dict["food"], lambda food: food.eaten == False))
        decision = self.neural_network(self.weights, self.biases, self.get_sight())
        return decision
