import numpy as np
import skimage.measure
import sys
import random

def softmax(z):
    s = np.exp(z.T) / np.sum(np.exp(z.T), axis=1).reshape(-1, 1)
    return s


def sigmoid(z):
    s = 1 / (1 + np.exp(-z))
    return s


def forward_propagation(weights, X):

    #my cheesy maxpooling doesn't work without this
    color_slices = []
    for array_slice in np.rollaxis(X, 2):
        color_slices.append(array_slice)

    #I could have implemented maxpooling myself, but who has time for that
    X = np.array([skimage.measure.block_reduce(slice, (maxpooling_filter_size, maxpooling_filter_size), np.max) for slice in color_slices])

    #flatten for the regular dnn, no fancy CNNs here
    X = np.array(X.flat)

    #Normalize the data
    X = X / np.linalg.norm(X)

    #Add a randomizer neuron to prevent agents getting stuck
    #still not sure if it work. Could be research paper material though.
    random_neuron_count = 5
    for _ in range(random_neuron_count):
        np.append(X, random.randrange(0, 1))


    #no i'm not storing activations, this is not backprop
    processed_data = X.T
    for W in weights:
        Z = np.matmul(W, input)
        A = np.tanh(Z)
        processed_data = A

    return processed_data
