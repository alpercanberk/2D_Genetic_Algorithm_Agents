import numpy as np
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
    #Add a randomizer neuron to prevent agents getting stuck
    #still not sure if it work. Could be research paper material though.
    random_neuron_count = 5
    for _ in range(random_neuron_count):
        np.append(X, random.randrange(0, 1))


    #no i'm not storing activations, this is not backprop
    processed_data = X.reshape(1, X.shape[0]).T
    # print(processed_data.shape)
    # print([weight.shape for weight in weights])

    for W in weights:
        print(processed_data.shape)
        print(W.shape)
        Z = np.matmul(W, processed_data)
        A = np.tanh(Z)
        processed_data = A

    return processed_data
