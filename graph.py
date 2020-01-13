
import numpy as np

connections = [[1,6], [2,6], [3,7], [7,5], [7,4], [6, 8], [8,4], [2,9], [9, 4], [4,10], [9,5], [4,5]]
weights = np.random.choice(np.arange(-1,1,step=0.01),size=len(connections),replace=True)
print("WEIGHTS", weights)

def clamp(x):
  return int(max(0, min(x, 255)))

def weight_to_color(weight):
    distance = np.tanh(weight)
    low = np.array([255, 0, 0])
    high = np.array([0, 255, 255])
    change = high-low
    color = low + (change * distance)
    return "#{0:02x}{1:02x}{2:02x}".format(clamp(color[0]), clamp(color[1]), clamp(color[2]))

def find_out_neurons(neuron, connections):
    out_neurons = []
    for connection in connections:
        if connection[0] == neuron:
            out_neurons.append(connection[1])
    return out_neurons

def find_in_neurons(neuron, connections):
    in_neurons = []
    for connection in connections:
        if connection[1] == neuron:
            in_neurons.append(connection[0])
    return in_neurons
# 
# def find_all_in_neurons(neuron, connections, all_in_neurons):
#     if len(find_in_neurons(neuron, connections)) == 0:
#         return all_in_neurons
#     for in_neuron in find_in_neurons(neuron, connections):
#         all_in_neurons.append(in_neuron)
#         find_all_in_neurons(in_neuron, connections, all_in_neurons)
#
# all_in_neurons = [6]
# print(find_all_in_neurons(6, connections, all_in_neurons))


def find_depth(neuron, connections, accumulator):
    accumulator += 1
    if len(find_in_neurons(neuron, connections))==0:
        return accumulator

    scores = []
    for in_neuron in find_in_neurons(neuron, connections):
        scores.append(find_depth(in_neuron, connections, accumulator))

    return max(scores)

def find_neurons(connections):
    neurons = []
    for connection in connections:
        for i in connection:
            if i not in neurons:
                neurons.append(i)
    return neurons

neurons = find_neurons(connections)

def find_input_neurons(connections):
    input_neurons = []
    accumulator = 0
    for neuron in neurons:
        if find_depth(neuron, connections, accumulator) == 1:
            input_neurons.append(neuron)
    return input_neurons

input_neurons = find_input_neurons(connections)

def find_output_neurons(connections):
    reverse_connections = [(x,y) for (y,x) in connections]
    return find_input_neurons(reverse_connections)

output_neurons = find_output_neurons(connections)


def find_network_depth(connections, input_neurons, output_neurons):
    accumulator = 0
    return max([find_depth(output_neuron, connections, accumulator) for output_neuron in output_neurons])

def create_layers(neurons, connections, input_neurons, output_neurons):
    layers = [[] for _ in range(find_network_depth(connections, input_neurons, output_neurons))]
    for neuron in neurons:
        accumulator = 0
        if neuron in output_neurons:
            index = len(layers)-1
        elif neuron in input_neurons:
            index = 0
        else:
            index = find_depth(neuron, connections, accumulator)-1
        layers[index].append(neuron)
    return layers

layers = create_layers(neurons, connections, input_neurons, output_neurons)


from tkinter import *
master = Tk()

canvas_width = 500
canvas_height = 500
margin=30
r = 20
w = Canvas(master,
           width=canvas_width,
           height=canvas_height)
w.pack()

node_coordinates = {}

x_interval = (canvas_width-2*margin)/((len(layers))-1)
y_interval_first_layer = (canvas_height-2*margin)/((len(layers[0]))-1)
for node in range(0, len(layers[0])):
    x = margin
    y = margin + y_interval_first_layer * node
    node_coordinates[layers[0][node]] = (x,y)

for layer in range(1, len(layers)):
    x = margin + layer * x_interval
    for node in range(0, len(layers[layer])):
        current_neuron = layers[layer][node]
        input_neurons = find_in_neurons(current_neuron, connections)
        input_neuron_coordinates = [node_coordinates[i_neuron] for i_neuron in input_neurons]
        prev_ys = sum([coordinate[1] for coordinate in input_neuron_coordinates])
        y = prev_ys/len(input_neuron_coordinates)
        node_coordinates[current_neuron] = (x,y)

for layer in range(1, len(layers)-1):
    x = margin + layer * x_interval
    for node in range(0, len(layers[layer])):
        current_neuron = layers[layer][node]
        output_neurons = find_out_neurons(current_neuron, connections)
        output_neuron_coordinates = [node_coordinates[i_neuron] for i_neuron in output_neurons]
        next_ys = sum([coordinate[1] for coordinate in output_neuron_coordinates])
        y = next_ys/len(output_neuron_coordinates)
        previous_y_coordinate = node_coordinates[current_neuron][1]
        new_y_coordinate = (y + previous_y_coordinate)/2
        node_coordinates[current_neuron] = (node_coordinates[current_neuron][0],new_y_coordinate)

for (x,y) in node_coordinates.values():
    w.create_oval(x-r,y-r,x+r,y+r)
    w.create_text(x, y)

for key in node_coordinates.keys():
    w.create_text(node_coordinates[key][0], node_coordinates[key][1], text=key)

for connection in connections:
    node1 = node_coordinates[connection[0]]
    node2 = node_coordinates[connection[1]]
    angle = np.arctan((node1[1]-node2[1])/(node1[0]-node2[0]))
    starting_offset = (r*np.cos(angle), r*np.sin(angle))
    ending_offset = (-1*r*np.cos(angle), -1*r*np.sin(angle))
    color = weight_to_color(weights[connections.index(connection)])
    w.create_line(node1[0]+starting_offset[0], node1[1]+starting_offset[1], node2[0]+ending_offset[0], node2[1]+ending_offset[1], fill=color)

mainloop()
