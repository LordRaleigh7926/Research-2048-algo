import os
import pickle
import neat
import gymnasium as gym
import numpy as np
import gameEnvironment

# load the winner
with open('winner_v1', 'rb') as f:
    c = pickle.load(f)


move = {
    0:"Up",
    1:"Down",
    2:"Left",
    3:"Right",
}

# print('Loaded genome:')
# print(c)

# Load the config file, which is assumed to live in
# the same directory as this script.
local_dir = os.path.dirname(__file__)
config_path = os.path.join(local_dir, 'config')
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     config_path)

net = neat.nn.FeedForwardNetwork.create(c, config)


seed = None
env = gym.make("2048", render_mode='human', seed=seed)
observation = env.reset(seed=seed)
observation = observation[0]

done = False
step = 0
while not done:
    step+=1
    print(step)
    action = net.activate(observation)
    # print(move[int(action)])
    observation, reward, done, _, info = env.step(action)