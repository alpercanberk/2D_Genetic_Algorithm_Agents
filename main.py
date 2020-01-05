from Genetic_Algorithm import *
from Simulation_With_ML import *

import matplotlib
import matplotlib.pyplot as plt

from Simulation_Settings import *

sys.path.insert(1, './Sprites')
from Utils import log

figure = plt.figure()

plt.xlabel('Generation #')
plt.ylabel('Average Fitness')
plt.ion()

num_weights = SimulationWithML.required_num_weights
num_biases = SimulationWithML.required_num_biases

print(num_weights, "weights for each agent")

weights_pop_size = (num_individuals_per_pop, num_weights)
biases_pop_size = (num_individuals_per_pop, num_biases)

print(weights_pop_size)
print(biases_pop_size)

new_weight_pop = np.random.choice(np.arange(-1,1,step=0.01),size=weights_pop_size,replace=True)
new_bias_pop = np.zeros(biases_pop_size)

new_population = np.concatenate((new_weight_pop, new_bias_pop),axis=1)
pop_size = new_population.shape
print(new_population.shape, "new_population.shape")


avg_fitness_array = []
max_fitness_array = []

plt.show()

do_visualize = False

log("Simulation with", num_generations, "generations")

for generation in range(num_generations):

    if generation == num_generations-1:
        do_visualize = True

    generation_average_fitness=0

    print('############## GENERATION ' + str(generation)+ ' ###############' )
    # Measuring the fitness of each chromosome in the population.

    fitness, avg_fitness = cal_pop_fitness(new_population, do_visualize)
    avg_fitness_array.append(avg_fitness)
    max_fitness_array.append(np.max(fitness))


    print('#######  fittest chromosome in generation ' + str(generation) +' has the fitness value:  ', np.max(fitness)
          , '\n And the average fitness value is:', avg_fitness)

    if (generation == num_generations - 1):
        # save_fittest(new_population, fitness)
        print("")
    else:
        plt.close()

    plt.plot(avg_fitness_array, label="Average Fitness")
    plt.plot(max_fitness_array, label="Max Fitness Individual")
    plt.legend()
    plt.show()
    plt.pause(0.001)

    # Selecting the best parents in the population for mating.
    parents = select_mating_pool(new_population, fitness, num_parents_mating)
    # Generating next generation using crossover.
    offspring_crossover = crossover(parents, offspring_size=(pop_size[0] - parents.shape[0], pop_size[1]))

    # Adding some variations to the offsrping using mutation.
    offspring_mutation = mutation(offspring_crossover)

    # Creating the new population based on the parents and offspring.
    new_population[0:parents.shape[0], :] = parents
    new_population[parents.shape[0]:, :] = offspring_mutation
