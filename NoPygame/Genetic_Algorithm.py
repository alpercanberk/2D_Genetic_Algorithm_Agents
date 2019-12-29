from Simulation_With_ML import *
from random import choice, randint


# I copied some of this code from https://github.com/TheAILearner/Training-Snake-Game-With-Genetic-Algorithm/blob/master/Genetic_Algorithm.py
# please don't sue me :)


def cal_pop_fitness(pop):
    # calculating the fitness value by playing a game with the given weights in chromosome
    sim = SimulationWithML(pop)
    fit = sim.get_fitness()
    print('fitness values of chromosomes from this generation:', str(fit))
    fitness_array = np.array(fit)
    return fitness_array, (sum(fitness_array)/pop.shape[0])



def select_mating_pool(pop, fitness, num_parents):
    # Selecting the best individuals in the current generation as parents for producing the offspring of the next generation.
    parents = np.empty((num_parents, pop.shape[1]))
    for parent_num in range(num_parents):
        max_fitness_idx = np.where(fitness == np.max(fitness))
        max_fitness_idx = max_fitness_idx[0][0]
        parents[parent_num, :] = pop[max_fitness_idx, :]
        fitness[max_fitness_idx] = -99999999
    return parents

def save_fittest(pop, fitness):
    max_fitness_idx = np.where(fitness == np.max(fitness))
    np.save('fittest_agent.npy', pop[max_fitness_idx, :])
    # return pop[max_fitness_idx, :]


def crossover(parents, offspring_size):
    # creating children for next generation
    offspring = np.empty(offspring_size)

    for k in range(offspring_size[0]):

        while True:
            parent1_idx = random.randint(0, parents.shape[0] - 1)
            parent2_idx = random.randint(0, parents.shape[0] - 1)
            # produce offspring from two parents if they are different
            if parent1_idx != parent2_idx:
                for j in range(offspring_size[1]):
                    if random.uniform(0, 1) < 0.5:
                        offspring[k, j] = parents[parent1_idx, j]
                    else:
                        offspring[k, j] = parents[parent2_idx, j]
                break
    return offspring


def mutation(offspring_crossover):
    # mutating the offsprings generated from crossover to maintain variation in the population

    for idx in range(offspring_crossover.shape[0]):
        for _ in range(25):
            i = randint(0,offspring_crossover.shape[1]-1)

        random_value = np.random.choice(np.arange(-1,1,step=0.001),size=(1),replace=False)
        offspring_crossover[idx, i] = offspring_crossover[idx, i] + random_value

    return offspring_crossover
