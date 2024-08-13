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

# Define hex colors
hex_colors = ['#FF3EA5', '#FF7ED4', '#FFB5DA']

# initialization of the dots with random positions and velocities
# uses broadcoasting to scale to the dimensions of the axes.abs
# positions and velocities are kept as 2D arrays as they have 
# both an x-value and a y-value

# subtracts 0.5 from the velocities to ensure that the velocities are closer to 0
# as a decimal, so that it can be scaled up with the dot speed

# ages are kept as a 1D array as well (as there is only one value that can be stored)
# fills it with zeroes as the age that all dots start with is zero (age is measured by frames)
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
# also uses the dot_colors array
scatter = ax.scatter(dot_positions[:, 0], dot_positions[:, 1], s=dot_radius**2, c=dot_colors)

#starting the frame count to keep track of age
frame_count = 0

# update every frame
def update(frame):
    global dot_positions, dot_velocities, dot_ages, dot_colors, frame_count
    
    # dot spawner, using the modulus operation to ensure that the dots are spawned every
    # couple frames. also checks to ensure that the amount of dots does not surpass
    # the maximum amount of  dots

    # each dot velocity or position is added to the original respective array with vstack
    # as colors and ages are 1D arrays, they are appended as normal
    if len(dot_positions) < max_dots and frame_count % spawn_interval == 0:
        new_positions = np.random.rand(1, 2) * [screen_width, screen_height]
        
        new_velocities = (np.random.rand(1, 2) - 0.5) * dot_speed
        dot_positions = np.vstack((dot_positions, new_positions))
        dot_velocities = np.vstack((dot_velocities, new_velocities))

        dot_ages = np.append(dot_ages, 0)
        new_color = np.random.choice(hex_colors)
        dot_colors = np.append(dot_colors, new_color)
    
    # updating the positions
    dot_positions += dot_velocities
    
    # checks for wall collisions + reverses trajectory as needed
    mask_x = (dot_positions[:, 0] < 0) | (dot_positions[:, 0] > screen_width)
    dot_velocities[mask_x, 0] *= -1
    dot_positions[:, 0] = np.clip(dot_positions[:, 0], 0, screen_width)
    
    mask_y = (dot_positions[:, 1] < 0) | (dot_positions[:, 1] > screen_height)
    dot_velocities[mask_y, 1] *= -1
    dot_positions[:, 1] = np.clip(dot_positions[:, 1], 0, screen_height)
    
    # dot aging and death
    dot_ages += 1
    dot_colors[dot_ages > lifespan] = '#FFFFFF' 

    # updating the plot
    scatter.set_color(dot_colors)
    scatter.set_offsets(dot_positions)
    
    frame_count += 1
    return scatter,

#showing the graph
ani = FuncAnimation(fig, update, frames=range(200), interval=20, blit=True)
plt.show()
