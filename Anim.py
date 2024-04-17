import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Settings
num_viruses = 5  # Number of virus particles
num_cells = 3    # Number of cells
arena_size = 10  # Size of the simulation area

# Initialize the positions of viruses and cells randomly
viruses = np.random.rand(num_viruses, 2) * arena_size
cells = np.random.rand(num_cells, 2) * arena_size

fig, ax = plt.subplots()
virus_dots, = plt.plot(viruses[:, 0], viruses[:, 1], 'ro', label='Monkeypox Virus')
cell_dots, = plt.plot(cells[:, 0], cells[:, 1], 'bo', label='Cells')

def init():
    ax.set_xlim(0, arena_size)
    ax.set_ylim(0, arena_size)
    return virus_dots, cell_dots

def update(frame):
    # Move viruses towards the nearest cell
    for i, virus in enumerate(viruses):
        distances = np.sqrt(np.sum((cells - virus) ** 2, axis=1))
        nearest_cell_index = np.argmin(distances)
        direction = cells[nearest_cell_index] - virus
        direction /= np.linalg.norm(direction)
        viruses[i] += direction * 0.1  # Move the virus

    virus_dots.set_data(viruses[:, 0], viruses[:, 1])
    return virus_dots, cell_dots

ani = animation.FuncAnimation(fig, update, frames=range(50), init_func=init, blit=True)

plt.legend()
plt.show()
