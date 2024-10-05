import numpy as np
import matplotlib.pyplot as plt
import random
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap, BoundaryNorm

class SchellingModel:
    def __init__(self, grid_size, empty_ratio=0.1, similar_wanted=0.3):
        self.grid_size = grid_size
        self.empty_ratio = empty_ratio
        self.similar_wanted = similar_wanted

        self.empty_cells = int(self.grid_size ** 2 * self.empty_ratio)
        self.num_agents = self.grid_size ** 2 - self.empty_cells
        self.num_red = self.num_agents // 2
        self.num_blue = self.num_agents - self.num_red

        self.grid = np.zeros((self.grid_size, self.grid_size), dtype=int)
        self.populate_grid()

    def populate_grid(self):
        positions = [(x, y) for x in range(self.grid_size) for y in range(self.grid_size)]
        random.shuffle(positions)

        # Place red agents with spin +1
        for _ in range(self.num_red):
            x, y = positions.pop()
            self.grid[x, y] = 1  # Red agent (spin +1)

        # Place blue agents with spin -1
        for _ in range(self.num_blue):
            x, y = positions.pop()
            self.grid[x, y] = -1  # Blue agent (spin -1)

        # Remaining positions are empty (0)

    def is_happy(self, x, y):
        agent = self.grid[x, y]
        if agent == 0:
            return True  # Empty cell is always "happy"

        # Get neighbors
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue  # Skip the agent itself
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size:
                    neighbor = self.grid[nx, ny]
                    if neighbor != 0:
                        neighbors.append(neighbor)

        if not neighbors:
            return True  # No neighbors

        similar = sum(1 for neighbor in neighbors if neighbor == agent)
        total_neighbors = len(neighbors)

        return (similar / total_neighbors) >= self.similar_wanted

    def move_agent(self, x, y):
        empty_positions = list(zip(*np.where(self.grid == 0)))
        if empty_positions:
            new_x, new_y = random.choice(empty_positions)
            self.grid[new_x, new_y] = self.grid[x, y]
            self.grid[x, y] = 0

    def step(self):
        unhappy_agents = []
        # Collect all agents
        agents = list(zip(*np.where(self.grid != 0)))
        random.shuffle(agents)

        for x, y in agents:
            if not self.is_happy(x, y):
                unhappy_agents.append((x, y))

        # Move unhappy agents
        for x, y in unhappy_agents:
            self.move_agent(x, y)

        # Count the number of red and blue agents
        num_red = np.sum(self.grid == 1)
        num_blue = np.sum(self.grid == -1)
        print(f"Number of Red Agents: {num_red}, Number of Blue Agents: {num_blue}")

        return len(unhappy_agents) > 0  # Return True if any agents moved

    def run(self, max_steps=100):
        for _ in range(max_steps):
            if not self.step():
                break

    def plot(self):
        # Define custom colors
        colors = ['#4C65A1', '#D3D3D3', '#A83D3D']  # [Blue, Empty, Red]
        cmap = ListedColormap(colors)
        bounds = [-1.5, -0.5, 0.5, 1.5]
        norm = BoundaryNorm(bounds, cmap.N)

        img = plt.imshow(self.grid, cmap=cmap, norm=norm)
        plt.axis('off')

        # Create colorbar with custom labels
        cbar = plt.colorbar(img, ticks=[-1, 0, 1], orientation='vertical')
        cbar.ax.set_yticklabels(['Blue Agent', 'Empty', 'Red Agent'])
        cbar.ax.tick_params(length=0)

    def animate(self, steps=100, interval=200, save_as="schelling_model_animation.gif"):
        fig, ax = plt.subplots()
        # Define custom colors
        colors = ['#0000FF', '#D3D3D3', '#FF0000']  # [Blue, Empty, Red]
        cmap = ListedColormap(colors)
        bounds = [-1.5, -0.5, 0.5, 1.5]
        norm = BoundaryNorm(bounds, cmap.N)

        ims = []

        for _ in range(steps):
            im = ax.imshow(self.grid.copy(), animated=True, cmap=cmap, norm=norm)
            ims.append([im])
            if not self.step():
                print("No more unhappy agents. Simulation stabilized.")
                break

        # Add colorbar with custom labels
        cbar = fig.colorbar(im, ticks=[-1, 0, 1], orientation='vertical')
        cbar.ax.set_yticklabels(['Blue Agent', 'Empty', 'Red Agent'])
        cbar.ax.tick_params(length=0)

        ax.axis('off')

        ani = animation.ArtistAnimation(fig, ims, interval=interval, blit=True, repeat_delay=1500)

        # Save the animation
        ani.save(save_as, writer='pillow')
        plt.close(fig)
        print(f"Animation saved as {save_as}")

# Simulation parameters
grid_size = 50
empty_ratio = 0.2
similar_wanted = 0.44
steps = 100

# Initialize and run the model
model = SchellingModel(grid_size, empty_ratio, similar_wanted)
model.animate(steps=steps, interval=200, save_as="schelling_model_animation.gif")

# Show the final state
plt.figure()
model.plot()
plt.show()
