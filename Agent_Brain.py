import numpy as np
import pygame

def calculate_num_weights(layers):
    num_weights = 0
    n_layers = len(layers)
    for i in range(0, n_layers-1):
        num_weights += layers[i] * layers[i+1]
    return num_weights

class AgentBrain():

    def __init__(self,
                 display,
                 sensor,
                 neural_network,
                 layer_sizes,
                 ):

        self.display = display
        self.input_size = sensor.get_output_shape()
        self.layer_sizes = list(layer_sizes)
        self.layer_sizes.insert(0, self.input_size)
        self.num_weights = calculate_num_weights(self.layer_sizes)
        self.weights = []

        self.neural_network = neural_network
        self.sensor = sensor

    def set_weights(self, weights):

        if(weights.shape[0] == self.num_weights):

            flat_weights = []

            layer_shapes = []
            for i in range(0, len(self.layer_sizes)-1):
                layer_shapes.append((self.layer_sizes[i], self.layer_sizes[i+1]))

            previous_weight_length = 0

            print(layer_shapes, "layer_shapes\n")

            for width, height in layer_shapes:
                weight_length = width*height

                flat_weights.append(weights[previous_weight_length: previous_weight_length + weight_length])
                previous_weight_length = weight_length+previous_weight_length

            for i in range(0, len(flat_weights)):
                print(layer_shapes[i][0], layer_shapes[0][1], "shapes")
                self.weights.append(flat_weights[i].reshape(layer_shapes[i][1], layer_shapes[i][0]))

        else:
            print("You have input the incorrect number of weights,\
                  please input", self.num_weights, "weights")

    def make_decision(self):
        decision = self.neural_network(self.weights, self.sensor.get_sight())
        return decision
