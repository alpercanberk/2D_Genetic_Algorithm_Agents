from Simulation import *
from Game_Utils import *

pygame.init()
display=pygame.display.set_mode((500,500))
clock=pygame.time.Clock()

simulation = Simulation(display)

screen_width = simulation.screen_width
screen_height = simulation.screen_height

wall_thickness = 50

simulation.create_wall(0,0, screen_width, wall_thickness, BLUE)
simulation.create_wall(0,0, wall_thickness, screen_height, BLUE)
simulation.create_wall(0,screen_height-wall_thickness, screen_width, wall_thickness, BLUE)
simulation.create_wall(screen_width-wall_thickness,0, wall_thickness, screen_height, BLUE)

food_coordinates = generate_food_coordinates_with_margin(screen_width, screen_height, wall_thickness, 20)

for coordinate in food_coordinates:
    simulation.generate_food(coordinate)

agent_coordinates = [[100, 100]]

maxpooling_filter_size = 5
sight_radius = 20

sensor = SquareSensor(display, simulation.agent_size, sight_radius, maxpooling_filter_size)

for agent_coordinate in agent_coordinates:
    brain = AgentBrain(display, sensor, forward_propagation, [4,4,4])
    weights = np.random.choice(np.arange(-1,1,step=0.01),size=brain.num_weights,replace=True)
    brain.set_weights(weights)
    simulation.generate_agent(agent_coordinate, brain)

simulation.run_game(500)
