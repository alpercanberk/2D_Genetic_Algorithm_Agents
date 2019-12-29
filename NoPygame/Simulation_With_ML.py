
import random
import math

from Sensors import SquareSensor
from Neural_Network import *
from Agent_Brain import *
from Simulation import Simulation

sys.path.insert(1, './Sprites')

from Utils import *
from Wall import Wall
from Food import Food
from Square_Agent import SquareAgent

def default_fitness_metric(self):
    return self.fitness

#example simulation

def generate_uniform_coordinates(screen_width, screen_height, wall_thickness, margin, density):

    coordinates = []

    left = wall_thickness + margin
    right = screen_width - wall_thickness - margin
    up = wall_thickness + margin
    down = screen_height - wall_thickness - margin

    print(left,right,up,down)

    x_interval = (right-left)/density
    y_interval = (down-up)/density

    print(x_interval, y_interval)

    for x in range(int(left), int(right-x_interval), int(x_interval)):
        for y in range(int(up), int(down-y_interval), int(y_interval)):
            randx = random.randrange(x, x+x_interval)
            randy = random.randrange(y, y+y_interval)
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
            randx = random.randrange(left, right)
            randy = random.randrange(up, down)
            new_point = (randx, randy)

        agent_coordinates.append(new_point)

    return agent_coordinates



num_steps = 200

screen_width = 200
screen_height = 500
wall_thickness = 20

type_dict = {
    0:"none",
    1:"agent",
    2:"food",
    3:"wall"
}

agent_size = 5
sight_radius = 5
maxpooling_filter_size = 4

food_size = 2
food_density = 10

agent_dist = 5


class SimulationWithML():

    dummy_simulation = Simulation(screen_height, screen_width, type_dict)
    dummy_sensor = SquareSensor(dummy_simulation.display,
                          agent_size,
                          sight_radius,
                          maxpooling_filter_size,
                          type_dict)

    dummy_brain = AgentBrain(
        display = dummy_simulation.display,
        sensor = dummy_sensor,
        neural_network = forward_propagation,
        layer_sizes = [4,4,4]
    )
    required_num_weights = dummy_brain.num_weights

    def __init__(self, weights):

        inv_type_dict = dict(map(reversed, type_dict.items()))

        self.simulation = Simulation(screen_height, screen_width, type_dict)

        feed = []

        food_coordinates = generate_uniform_coordinates(screen_width, screen_height, wall_thickness, wall_thickness, food_density)
        for coordinate in food_coordinates:
            food = Food(inv_type_dict["food"], food_size, [coordinate[0], coordinate[1]])
            self.simulation.add_sprite(food)
            feed.append(food)

        walls = []
        walls.append(Wall(inv_type_dict["wall"], screen_width, wall_thickness,[0,0]))
        walls.append(Wall(inv_type_dict["wall"], wall_thickness, screen_height,[0,0]))
        walls.append(Wall(inv_type_dict["wall"], screen_height, wall_thickness,[0,screen_height-wall_thickness]))
        walls.append(Wall(inv_type_dict["wall"], wall_thickness, screen_height,[screen_width-wall_thickness,0]))
        for wall in walls:
            self.simulation.add_sprite(wall)

        SquareAgent.fitness_metric = default_fitness_metric

        agent_coordinates = generate_agent_coordinates(screen_width,
                                                       screen_height,
                                                       wall_thickness,
                                                       wall_thickness,
                                                       weights.shape[0],
                                                       agent_dist)

        for i in range(0, len(agent_coordinates)):

            print(agent_coordinates[i])
            sensor = SquareSensor(self.simulation.display,
                                  agent_size,
                                  sight_radius,
                                  maxpooling_filter_size,
                                  type_dict)

            brain = AgentBrain(
                display = self.simulation.display,
                sensor = sensor,
                neural_network = forward_propagation,
                layer_sizes = [4,4,4]
            )

            brain.set_weights(weights[i,:])

            agent = SquareAgent(type=inv_type_dict["agent"],
                                size=5,
                                init_coordinates=agent_coordinates[i],
                                walls=walls,
                                feed=feed
                                )

            agent.brain = brain
            agent.walls = walls
            agent.feed = feed

            self.simulation.add_sprite(agent)

    def get_fitness(self):
        self.simulation.run(num_steps, True)
        return self.simulation.get_fitness(inv_type_dict["agent"])
