import numpy as np
import random



class Game2048Env:
    def __init__(self, render=False):
        self.grid_size = 4
        self.multiplier = []
        self.grid = np.zeros((self.grid_size, self.grid_size), dtype=int)
        self.reset()
        self.render = render
        self.wasted_steps=0

    def reset(self, seed=None):
        if seed!=None:
            random.seed(seed)
        self.multiplier = []
        self.grid = np.zeros((self.grid_size, self.grid_size), dtype=int)
        self.add_random_tile()
        self.add_random_tile()
        return self.get_state()

    def add_random_tile(self):
        empty_cells = list(zip(*np.where(self.grid == 0)))
        if empty_cells:
            r, c = random.choice(empty_cells)
            self.grid[r][c] = 2 if random.random() < 0.9 else 4

    def get_state(self):
        return self.grid.flatten().reshape(16)  # Normalized flattened grid

    def move(self, direction):
        self.multiplier = []
        if direction == 0: # Up
            self.grid = self.grid.T
            self.grid = np.array([self.merge(row) for row in self.grid])
            self.grid = self.grid.T
        elif direction == 1: # Down
            self.grid = self.grid.T
            self.grid = np.array([self.merge(row[::-1])[::-1] for row in self.grid])
            self.grid = self.grid.T
        elif direction == 2: # Left
            self.grid = np.array([self.merge(row) for row in self.grid])
        elif direction == 3: # Right
            self.grid = np.array([self.merge(row[::-1])[::-1] for row in self.grid])

        add_tile = False
        for i in self.get_state():
            if i == 0:
                add_tile = True
                break

        if add_tile:
            self.add_random_tile()

        if len(self.multiplier) == 0:
            self.wasted_steps+=1
        else:
            self.wasted_steps=0

        if self.render:
            print(f"Wasted Steps: {self.wasted_steps}")
            print(f"New Blocks: {self.multiplier}")
            print(self.grid)

    def merge(self, row):

        new_row = [i for i in row if i != 0]

        for i in range(len(new_row) - 1):
            if new_row[i] == new_row[i + 1]:
                new_row[i] *= 2
                New_Multiplied_Block = new_row[i]
                self.multiplier.append(New_Multiplied_Block)
                new_row[i + 1] = 0

        new_row = [i for i in new_row if i != 0]

        return new_row + [0] * (self.grid_size - len(new_row))

    def check_game_over(self):
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                if self.grid[r][c] == 0:
                    return False
                if c < self.grid_size - 1 and self.grid[r][c] == self.grid[r][c + 1]:
                    return False
                if r < self.grid_size - 1 and self.grid[r][c] == self.grid[r + 1][c]:
                    return False
                
        return True


