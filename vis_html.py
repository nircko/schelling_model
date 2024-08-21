import numpy as np
import matplotlib.pyplot as plt
import random
import matplotlib.animation as animation


class SchellingModel:
    def __init__(self, grid_size, num_agents, empty_ratio=0.1, similar_wanted=0.3):
        self.grid_size = grid_size
        self.num_agents = num_agents
        self.similar_wanted = similar_wanted
        self.empty_ratio = empty_ratio

        self.empty_cells = int(self.grid_size ** 2 * self.empty_ratio)
        self.num_red = (self.grid_size ** 2 - self.empty_cells) // 2
        self.num_blue = self.num_red

        self.grid = np.zeros((self.grid_size, self.grid_size), dtype=int)
        self.populate_grid()

    def populate_grid(self):
        positions = [(x, y) for x in range(self.grid_size) for y in range(self.grid_size)]
        random.shuffle(positions)

        for i in range(self.num_red):
            x, y = positions.pop()
            self.grid[x, y] = 1  # Red agent

        for i in range(self.num_blue):
            x, y = positions.pop()
            self.grid[x, y] = 2  # Blue agent

    def is_happy(self, x, y):
        agent = self.grid[x, y]
        if agent == 0:
            return True  # Empty cell

        neighbors = [
            (x2, y2)
            for x2 in range(x - 1, x + 2)
            for y2 in range(y - 1, y + 2)
            if (0 <= x2 < self.grid_size and 0 <= y2 < self.grid_size) and (x2 != x or y2 != y)
        ]

        similar = sum(1 for x2, y2 in neighbors if self.grid[x2, y2] == agent)
        total_neighbors = sum(1 for x2, y2 in neighbors if self.grid[x2, y2] != 0)

        if total_neighbors == 0:
            return True  # No neighbors, no reason to move

        return (similar / total_neighbors) >= self.similar_wanted

    def move_agent(self, x, y):
        empty_positions = [(i, j) for i in range(self.grid_size) for j in range(self.grid_size) if self.grid[i, j] == 0]
        if empty_positions:
            new_x, new_y = random.choice(empty_positions)
            self.grid[new_x, new_y] = self.grid[x, y]
            self.grid[x, y] = 0

    def step(self):
        moved = False
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if self.grid[x, y] != 0 and not self.is_happy(x, y):
                    self.move_agent(x, y)
                    moved = True
        return moved

    def run(self, steps=100):
        for _ in range(steps):
            if not self.step():
                break

    def plot(self):
        plt.imshow(self.grid, cmap="RdBu", vmin=0, vmax=2)
        plt.axis('off')

    def animate(self, steps=100, interval=200, save_as="schelling_model.gif"):
        fig, ax = plt.subplots()
        ims = []

        for _ in range(steps):
            im = ax.imshow(self.grid, animated=True, cmap="RdBu", vmin=0, vmax=2)
            ims.append([im])
            if not self.step():
                break

        ani = animation.ArtistAnimation(fig, ims, interval=interval, blit=True, repeat_delay=1000)

        # Use the Pillow writer for saving the animation as a GIF
        ani.save(save_as, writer='pillow')


# Simulation parameters
grid_size = 100
num_agents = 1000
empty_ratio = 0.2
similar_wanted = 0.44
steps = 1000000

# Initialize and run the model
model = SchellingModel(grid_size, num_agents, empty_ratio, similar_wanted)
model.animate(steps=steps, interval=100, save_as="schelling_model.html")

# Show the final state
plt.figure()
model.plot()
plt.show()
