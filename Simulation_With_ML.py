
import random
import math

from Neural_Network import *
from Agent_Brain import *
from Simulation import Simulation

from Simulation_Settings import *

sys.path.insert(1, './Sprites')

from Utils import *
from Wall import Wall
from Food import Food
from Square_Agent import SquareAgent


class SimulationWithML():

    #only required so that the shapes of the weights can be initialized properly
    dummy_brain = AgentBrain(
        simulation = None,
        neural_network = forward_propagation,
        layer_sizes = LAYER_SIZES,
        type_dict = None
    )
    required_num_weights = dummy_brain.num_weights
    required_num_biases = dummy_brain.num_biases

    def __init__(self, weights):

        self.visualize = False

        self.simulation = Simulation(SCREEN_HEIGHT, SCREEN_WIDTH, TYPE_DICT)

        feed = []
        food_coordinates = generate_uniform_coordinates(SCREEN_WIDTH, SCREEN_HEIGHT, WALL_THICKNESS, WALL_THICKNESS*(1/2), FOOD_DENSITY)
        for coordinate in food_coordinates:
            food = Food(TYPE_DICT["food"], FOOD_SIZE, [coordinate[0], coordinate[1]])
            self.simulation.add_sprite(food)
            feed.append(food)

        walls = []
        walls.append(Wall(TYPE_DICT["wall"], SCREEN_WIDTH, WALL_THICKNESS,[0,0]))
        walls.append(Wall(TYPE_DICT["wall"], WALL_THICKNESS, SCREEN_HEIGHT,[0,0]))
        walls.append(Wall(TYPE_DICT["wall"], SCREEN_HEIGHT, WALL_THICKNESS,[0,SCREEN_HEIGHT-WALL_THICKNESS]))
        walls.append(Wall(TYPE_DICT["wall"], WALL_THICKNESS, SCREEN_HEIGHT,[SCREEN_WIDTH-WALL_THICKNESS,0]))
        for wall in walls:
            self.simulation.add_sprite(wall)

        agent_coordinates = generate_agent_coordinates(SCREEN_WIDTH,
                                                       SCREEN_HEIGHT,
                                                       WALL_THICKNESS,
                                                       WALL_THICKNESS,
                                                       weights.shape[0],
                                                       MIN_AGENT_DIST)

        for i in range(0, len(agent_coordinates)):

            brain = AgentBrain(
                simulation = self.simulation,
                neural_network = forward_propagation,
                layer_sizes = LAYER_SIZES,
                type_dict = TYPE_DICT
            )

            brain.set_weights(weights[i,:])

            agent = SquareAgent(type=TYPE_DICT["agent"],
                                size=AGENT_SIZE,
                                init_coordinates=agent_coordinates[i],
                                walls=walls,
                                feed=feed
                                )

            agent.brain = brain
            agent.walls = walls
            agent.feed = feed

            self.simulation.add_sprite(agent)

    def get_fitness(self):
        self.simulation.run(NUM_STEPS_PER_GAME, self.visualize)
        return self.simulation.get_fitness(TYPE_DICT["agent"])
