import csv
import os
import gymnasium as gym
from gymnasium import spaces
from gymnasium.envs.registration import register
from gymnasium.utils.env_checker import check_env
import numpy as np
import environment as ev
import math


register(
    id = '2048',
    entry_point="gameEnvironment:_2048_Game_Env"
)

class _2048_Game_Env(gym.Env):

    metadata = {"render_modes": ["human"], "render_fps": 1, "seed": 42}

    def __init__(self, render_mode=None, seed=None):
        self.grid_rows = 4
        self.grid_cols = 4
        self.largest_tile = 4
        self.render_mode = render_mode
        if render_mode == "human":
            self.game = ev.Game2048Env(True)
        else:
            self.game = ev.Game2048Env()
        self.seed = 42

        self.action_space = spaces.Discrete(4)
        self.same_state_repeat = 0
        self.observation_space = spaces.Box(
            low=0,
            high=65536,
            shape=(16,),
            dtype=int,
        )

        # Logging setup
        self.log_file = "game_logs.csv"
        self.step_count = 0
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        if seed is not None:
            self.game.reset(seed)
        else:
            self.game.reset()

        self.step_count = 0
        self.largest_tile = 4
        obs = self.game.grid.flatten()
        return obs, {}

    def step(self, action):
        old_state = self.game.get_state()
        self.game.move(action)

        terminated = False
        info = {}
        reward = 0

        # Calculate reward
        num_new_blocks = len(self.game.multiplier)
        merged_tiles = self.game.multiplier

        for tile in merged_tiles:
            reward += math.log2(tile)

        new_largest_tile = np.max(self.game.grid)
        if new_largest_tile > self.largest_tile:
            reward += new_largest_tile
            self.largest_tile = new_largest_tile

        empty_tiles = np.sum(self.game.grid == 0)
        reward += 2 * empty_tiles

        if num_new_blocks == 0:
            reward -= 10

        new_state = self.game.get_state()
        if np.array_equal(new_state, old_state):
            self.same_state_repeat += 1
            reward -= 20 * self.same_state_repeat
        else:
            self.same_state_repeat = 0

        if self.game.wasted_steps > 5:
            reward -= 5 * (self.game.wasted_steps - 5)

        terminated = self.game.check_game_over()
        if terminated:
            final_score = np.sum(self.game.grid)
            reward += 0.1 * final_score
            info["final_score"] = final_score

        if self.game.wasted_steps>10 or self.same_state_repeat>10:
            reward-=100
        self.step_count += 1

        reward += self.step_count * 0.1

        obs = self.game.get_state()
        return obs, reward, terminated, False, info

    def render(self):
        pass
