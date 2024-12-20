import tkinter as tk
import random
import numpy as np

class Game2048:
    def __init__(self, master):
        self.master = master
        self.master.title("2048")
        self.grid_size = 4
        self.cell_size = 100
        self.grid = np.zeros((self.grid_size, self.grid_size), dtype=int)

        self.colors = {
            0: "#cdc1b4", 2: "#eee4da", 4: "#ede0c8", 8: "#f2b179",
            16: "#f59563", 32: "#f67c5f", 64: "#f65e3b", 128: "#edcf72",
            256: "#edcc61", 512: "#edc850", 1024: "#edc53f", 2048: "#edc22e"
        }

        self.canvas = tk.Canvas(self.master, width=self.grid_size * self.cell_size,
                                height=self.grid_size * self.cell_size, bg="#bbada0")
        self.canvas.pack()

        self.add_random_tile()
        self.add_random_tile()
        self.draw_grid()
        
        self.master.bind("<Key>", self.handle_keypress)

        
        

    def add_random_tile(self):
        
        empty_cells = list(zip(*np.where(self.grid == 0)))

        if empty_cells:
            r, c = random.choice(empty_cells)
            self.grid[r][c] = 2 if random.random() < 0.9 else 4

    def draw_grid(self):
        self.canvas.delete("all")
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                value = self.grid[r][c]
                color = self.colors.get(value, "#3c3a32")
                x0 = c * self.cell_size
                y0 = r * self.cell_size
                x1 = x0 + self.cell_size
                y1 = y0 + self.cell_size
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="#bbada0")
                if value:
                    font = ("Helvetica", 24, "bold")
                    self.canvas.create_text(x0 + self.cell_size / 2, y0 + self.cell_size / 2,
                                            text=str(value), fill="black", font=font)

    def handle_keypress(self, event):
        key = event.keysym
        if key in ("Up", "Down", "Left", "Right"):
            self.move(key)
            self.add_random_tile()
            self.draw_grid()
            if self.check_game_over():
                self.canvas.create_text(self.grid_size * self.cell_size / 2,
                                        self.grid_size * self.cell_size / 2,
                                        text="Game Over", fill="red",
                                        font=("Helvetica", 36, "bold"))

    def move(self, direction):
        if direction == "Up":
            self.grid = self.grid.T
            self.grid = np.array([self.merge(row) for row in self.grid])
            self.grid = self.grid.T
        elif direction == "Down":
            self.grid = self.grid.T
            self.grid = np.array([self.merge(row[::-1])[::-1] for row in self.grid])
            self.grid = self.grid.T
        elif direction == "Left":
            self.grid = np.array([self.merge(row) for row in self.grid])
        elif direction == "Right":
            self.grid = np.array([self.merge(row[::-1])[::-1] for row in self.grid])

    def merge(self, row):
        
            # Remove zeros from the row
            new_row = [i for i in row if i != 0]
            
            # Merge the row by checking adjacent elements
            for i in range(len(new_row) - 1):
                if new_row[i] == new_row[i + 1]:
                    new_row[i] *= 2
                    new_row[i + 1] = 0
            
            # Remove any zeros after merging
            new_row = [i for i in new_row if i != 0]
            
            # Pad the row with zeros to maintain grid_size length
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

if __name__ == "__main__":
    root = tk.Tk()
    game = Game2048(root)
    root.mainloop()
