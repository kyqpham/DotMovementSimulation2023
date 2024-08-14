import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# parameters for the dots
num_initial_dots = 10
max_dots = 1000
dot_radius = 5
dot_speed = 6
spawn_interval = 5
lifespan = 200

# axes dimensions
screen_width = 800
screen_height = 600

# define hex colors
hex_colors = ['#FF3EA5', '#FF7ED4', '#FFB5DA']

# initialization of the dots with random positions and velocities
# uses broadcasting to scale to the dimension of the axes
# positions and velocities are kept as 2D arrays as they have
# both an x-value and a y-value

# subtracts 0.5 from velocities to ensure that the velocities are closer
# to zero and kept as a decimal, so that it can be scaled up with the 
# dot speed, while staying in a moderate velocity

# ages are kept as a 1D aray as well, as there is only one vallue that can 
# be stored
# fills it with zeroes as the age that all dots start with is zero
dot_positions = np.random.rand(num_initial_dots, 2) * [screen_width, screen_height]
dot_velocities = (np.random.rand(num_initial_dots, 2) - 0.5) * dot_speed
dot_ages = np.zeros(num_initial_dots)

# creating a 1D array of colors that each dot spawned will have
dot_colors = np.random.choice(hex_colors, num_initial_dots)

# creating the plot
fig, ax = plt.subplots()
ax.set_xlim(0, screen_width)
ax.set_ylim(0, screen_height)

# initializing the actual plot with the x-value and y-value coordinates
# also uses the dot_colors array for the colors
scatter = ax.scatter(dot_positions[:, 0], dot_positions[:, 1], s=dot_radius**2, c=dot_colors)

# frame count for easier age tracking
frame_count = 0

# update every frame
def update(frame):
    global dot_positions, dot_velocities, dot_ages, dot_colors, frame_count

    # dot spawner, using the modulus operation to ensure that the dots are spawned every
    # couple frames. also checks to ensure that the amount of dots does not surpass
    # the maximum amount of  dots
    if len(dot_positions) < max_dots and frame % spawn_interval == 0:
        new_positions = np.random.rand(1, 2) * [screen_width, screen_height]
       
        new_velocities = (np.random.rand(1, 2) - 0.5) * dot_speed
        new_colors = np.random.choice(hex_colors, 1)
        dot_positions = np.vstack((dot_positions, new_positions))
        dot_velocities = np.vstack((dot_velocities, new_velocities))
        
        dot_ages = np.append(dot_ages, 0)
        dot_colors = np.append(dot_colors, new_colors)

    # updating the positions
    dot_positions += dot_velocities

    # checks for wall collisions + reverses trajectory as needed
    mask_x = (dot_positions[:, 0] < 0) | (dot_positions[:, 0] > screen_width)
    dot_velocities[mask_x, 0] *= -1
    dot_positions[:, 0] = np.clip(dot_positions[:, 0], 0, screen_width)

    mask_y = (dot_positions[:, 1] < 0) | (dot_positions[:, 1] > screen_height)
    dot_velocities[mask_y, 1] *= -1
    dot_positions[:, 1] = np.clip(dot_positions[:, 1], 0, screen_height)

    # dot aging 
    dot_ages += 1

    # dot death and removal using masks
    # the mask checks if the condition was met, filling the array
    # of either true or false
    # then sets the original arrays to the next true value
    # this cuts out any false values, thus any dead dots from the array
    alive_mask = dot_ages <= lifespan
    dot_positions = dot_positions[alive_mask]
    dot_velocities = dot_velocities[alive_mask]
    dot_ages = dot_ages[alive_mask]
    dot_colors = dot_colors[alive_mask]

    # updating the scatter plot
    scatter.set_offsets(dot_positions)
    scatter.set_color(dot_colors)

    frame_count += 1
    return scatter,

# showing the graph
ani = FuncAnimation(fig, update, frames=range(200), interval=20, blit=True)
plt.show()