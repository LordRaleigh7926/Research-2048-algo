import gymnasium as gym
from gymnasium import spaces
from gymnasium.envs.registration import register
from gymnasium.utils.env_checker import check_env
import numpy as np
import environment as ev
import math


register(
    id = '_2048_',
    entry_point="gameEnvironment:_2048_Game_Env"
)

class _2048_Game_Env(gym.Env):

    metadata = {"render_modes": ["human"], "render_fps":1, 'seed':42}

    def __init__(self, render_mode = None, seed=42):

        self.grid_rows = 4
        self.grid_cols = 4
        self.render_mode = render_mode
        self.game = ev.Game2048Env()
        self.seed = 42

        self.action_space = spaces.Discrete(4)

        self.observation_space = spaces.Box(
            low=0,
            high=100000000,
            shape=(16,),
            dtype=int
        )

    def reset(self, seed=None, options = None):

        super().reset(seed=seed)

        if seed  != None:
            self.game.reset(seed)
        else:
            self.game.reset()

        info = {} #for debugging

        obs = self.game.grid.flatten()

        if self.render_mode == 'human':
            pass

        return (obs, info)
    
    def step(self, action):

        old_state = self.game.get_state()

        self.game.move(action)

        reward = 0
        terminated = False

        info = {}

        for i in self.game.multiplier:
            reward+=math.log2(i)**2

        # for r in self.game.grid:
        #     for c in r:
        #         if c == 0:
        #             reward += 50
        new_state = self.game.get_state()

        same_state = True
        for i in range(16):
            if new_state[i] != old_state[i]:
                same_state = False

        if same_state:
            reward-=200

        obs = self.game.get_state()

        print(self.game.grid)

        return obs, reward, terminated, False, info
    
    def render(self):
        pass


if __name__ == '__main__':

    env = gym.make('_2048_', render_mode='human', seed = 42)

    # check_env(env.unwrapped)

    obs = env.reset()[0]

    for i in range(10):
        rand_action = env.action_space.sample()
        print(rand_action)
        obs, reward, terminated, _, _ = env.step(rand_action) 
        print(reward)