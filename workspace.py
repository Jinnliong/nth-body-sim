import scipy.integrate
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation
from matplotlib.animation import PillowWriter
import sys
import time

# Constants 
G = 6.674e-11 # Gravitational constant
M_sun = 1.989e30 # Mass of the Sun

# Planetary orbital parameters
planet_params = {
    "Mercury": {"a": 57.91e9, "e": 0.2056, "T": 88 * 24 * 3600},
    "Venus": {"a": 108.2e9, "e": 0.0067, "T": 225 * 24 * 3600},
    "Earth": {"a": 149.6e9, "e": 0.0167, "T": 365.25 * 24 * 3600},
    "Mars": {"a": 227.9e9, "e": 0.0934, "T": 1.88 * 365.25 * 24 * 3600},
    "Jupiter": {"a": 778.5e9, "e": 0.0489, "T": 11.86 * 365.25 * 24 * 3600}
}

# Number of frames for each planet's orbit
planet_frames = {name: int(params["T"] / (24 * 3600)) for name, params in planet_params.items()}

# Function to calculate Solar system stars' position at a given time
def calculate_position(t, a, e, T): 
    n = 2 * np.pi / T # Mean motion (specific to the planet)
    M = n * t # Mean anomaly

# Solve Kepler's equation iteratively 
    E = M
    E_next = M + e * np.sin(E) # Eccentricity of the planet
    while abs(E - E_next) > 1e-6: 
        E = E_next
        E_next = M + e * np.sin(E)

    true_anomaly = 2 * np.arctan2(np.sqrt(1 + e) * np.tan(E / 2), np.sqrt(1 - e))
    r = a * (1 - e * np.cos(E)) # Semi-major axis of the planet

    x = r * np.cos(true_anomaly)
    y = 0 # Fix planets to the x-z plane
    z = r * np.sin(true_anomaly)

    return x, y, z

print("Position Calculated Successfully!")

# Set up the plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Add labels and title
fig.patch.set_facecolor('black')
ax.set_xlabel("x-coordinate", fontsize=14)
ax.set_ylabel("y-coordinate", fontsize=14)
ax.set_zlabel("z-coordinate", fontsize=14)
ax.set_title("A Cosmic Waltz: Planets in the Solar System\n", fontsize=14)
ax.title.set_color('white')
ax.xaxis.label.set_color('white')
ax.yaxis.label.set_color('white')
ax.zaxis.label.set_color('white')
ax.tick_params(colors='white')

# Change the plot background color to black
ax.set_facecolor('black')

# Colors for planets 
colors = {
    "Mercury": "darkorange", 
    "Venus": "yellow",
    "Earth": "deepskyblue", 
    "Mars": "crimson", 
    "Jupiter": "peachpuff" 
}

# Color for the Sun
sun_color = 'yellow'  

# Lines to represent the orbits (initialize with empty data)
orbit_paths = {}
planets = {}

for name, params in planet_params.items():
    orbit_paths[name], = ax.plot([], [], [], label=name, linewidth=2, linestyle='-', color=colors[name]) 
    planets[name], = ax.plot([], [], [], 'o', markersize=4, color=colors[name]) 

# Lists to store orbit history
planet_positions = {name: ([], [], []) for name in planet_params}

def init():
    for name in planet_params:
        orbit_paths[name].set_data([], [])
        orbit_paths[name].set_3d_properties([])
        planets[name].set_data([], [])
        planets[name].set_3d_properties([])

    return [orbit_paths[name] for name in planet_params] + [planets[name] for name in planet_params]

print("Initialization Executed Successfully!")

# Animation function (called repeatedly)
def animate(i):
    sun_x, sun_y, sun_z = i * 1e9, 0, 0  # Sun's motion (straight line in 3D)
    sun, = ax.plot([sun_x], [sun_y], [sun_z], 'o', color=sun_color, markersize=10)  # Draw the Sun

    for name, params in planet_params.items():
        x, y, z = calculate_position(i * params["T"] / planet_frames[name], params["a"], params["e"], params["T"])
        x += sun_x # Planets move along with the Sun
        y += sun_y
        z += sun_z

        orbit_paths[name].set_data(planet_positions[name][0] + [x], planet_positions[name][1] + [y])
        orbit_paths[name].set_3d_properties(planet_positions[name][2] + [z])
        planet_positions[name] = (planet_positions[name][0] + [x], planet_positions[name][1] + [y], planet_positions[name][2] + [z])
 
        planets[name].set_data([x], [y])
        planets[name].set_3d_properties([z])

    # Calculate the maximum distance reached by any planet
    max_distance = max(planet_params[name]["a"] * (1 + planet_params[name]["e"]) for name in planet_params)

    # Set the buffer value (you can adjust this as needed)
    buffer = 0.05 * max_distance # 20% buffer around the furthest planet

    # Set the viewing limits with the buffer
    ax.set_xlim(-max_distance - buffer, max_distance + buffer)
    ax.set_ylim(-max_distance - buffer, max_distance + buffer)
    ax.set_zlim(-max_distance - buffer, max_distance + buffer)

    return [orbit_paths[name] for name in planet_params] + [planets[name] for name in planet_params] + [sun] 

print("Animation Set Successfully!")

# Display the legend
ax.legend(loc="upper left", fontsize=14)

# Create and run the animation with an appropriate number of frames
ani = animation.FuncAnimation(fig, animate, frames=max(planet_frames.values()), interval=30, blit=True)

# Define the total number of frames
total_frames = 3 * max(planet_frames.values())

# Save the animation
ani.save("solar_sys.gif", writer=PillowWriter(fps=24))
print("GIF Save Attempted")

# Display the animation
plt.show()
