import multiprocessing
import os
import pickle

import neat
import numpy as np

import gameEnvironment
import gymnasium as gym



runs_per_net = 20

move = {
    0:"Up",
    1:"Down",
    2:"Left",
    3:"Right",
}


# Use the NN network phenotype and the discrete actuator force function.
def eval_genome(genome, config):
    net = neat.nn.FeedForwardNetwork.create(genome, config)

    fitnesses = []

    for runs in range(runs_per_net):
        env = gym.make("2048")

        observation = env.reset()

        observation = observation[0]

        fitness = 0.0
        done = False

        while not done:

            action_array = net.activate(observation.tolist())
            observation, reward, done, _, _ = env.step(action=action_array)
            fitness += reward

        # if done==True:
        #     print(f'Genome fininished with fitness : {fitness}')

        fitnesses.append(fitness)

    return np.mean(fitnesses)


def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        genome.fitness = eval_genome(genome, config)


def run():
    # Load the config file, which is assumed to live in
    # the same directory as this script.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    pop = neat.Population(config)
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    pop.add_reporter(neat.StdOutReporter(True))

    pe = neat.ParallelEvaluator(multiprocessing.cpu_count(), eval_genome)
    winner = pop.run(pe.evaluate)

    # Save the winner.
    with open('winner_v1', 'wb') as f:
        pickle.dump(winner, f)

    print(winner)



if __name__ == '__main__':
    run()