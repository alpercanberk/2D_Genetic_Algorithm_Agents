
import numpy as np
import random
import string
import math
from scipy.spatial import distance


f= open("log.txt","w+")


def rectangle(width, height, type):
    return np.full((width, height), type)

def line_overlap_2d(l1,r1,l2,r2):

    rightmost_index = 2

    if(r1 > r2):
        rightmost_index = 1

    if(rightmost_index == 2):
        if(r1 > l2):
            return True

    if(rightmost_index == 1):
        if(r2 > l1):
            return True

    return False

def does_intersect_2d(x1, y1, width1, height1, x2, y2, width2, height2):
    intersection_type = []
    if(line_overlap_2d(x1, x1+width1, x2, x2+width2) and line_overlap_2d(y1, y1+height1, y2, y2+height2)):
        return True
    return False

def generate_random_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


def closest_point(observer, targets):
    closest_index = distance.cdist([observer], targets).argmin()
    return targets[closest_index]

def calculate_num_weights(layers):
    num_weights = 0
    n_layers = len(layers)
    for i in range(0, n_layers-1):
        num_weights += layers[i] * layers[i+1]
    return num_weights


# def parse_log(element):
#     if type(element) == tuple:
#         element = [str.strip(str(e)) for e in element]
#         return ','.join(element)
#     else:
#         return str(element)

def log(*args):
    a = [str(element) for element in args]
    string = ' '.join(a)
    f.write(string + "\n")

def clear_log():
    f.truncate(0)
#example simulation

def generate_uniform_coordinates(screen_width, screen_height, wall_thickness, margin, density):

    coordinates = []

    left = wall_thickness + margin
    right = screen_width - wall_thickness - margin
    up = wall_thickness + margin
    down = screen_height - wall_thickness - margin

    x_interval = (right-left)/density
    y_interval = (down-up)/density

    for x in range(int(left), int(right-x_interval), int(x_interval)):
        for y in range(int(up), int(down-y_interval), int(y_interval)):
            randx = random.randrange(x, int(x+x_interval))
            randy = random.randrange(y, int(y+y_interval))
            coordinates.append((randx, randy))

    return coordinates

def dist(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def generate_agent_coordinates(screen_width, screen_height, wall_thickness, margin, n_agents, min_dist):

    left = wall_thickness + margin
    right = screen_width - wall_thickness - margin
    up = wall_thickness + margin
    down = screen_height - wall_thickness - margin

    agent_coordinates = []

    while(len(agent_coordinates) < n_agents):
        randx = random.randrange(left, right)
        randy = random.randrange(up, down)
        new_point = (randx, randy)
        #generates coordinates until every agent is a dist apart from each other, this might get stuck if you set n too big
        #or dist too big, sorry.
        while(True in [dist(new_point, old_point) < min_dist for old_point in agent_coordinates]):
            print('LOOPING')
            randx = random.randrange(left, right)
            randy = random.randrange(up, down)
            new_point = (randx, randy)

        agent_coordinates.append(new_point)
        # agent_coordinates.append([screen_width/2, screen_height/2])

    return agent_coordinates
