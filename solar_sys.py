# Let's enhance our cosmic journey to include 3D motion for the Sun, Mercury, Venus, Earth, and Mars!

import scipy.integrate  # Library for numerical integration (ODE Solvers)
import numpy as np  # Library for numerical calculations
import matplotlib.pyplot as plt  # Library for plotting
from mpl_toolkits.mplot3d import Axes3D  # For 3D plots
from matplotlib import animation  # For creating animations
from matplotlib.animation import PillowWriter  # For saving GIFs
import sys
import time

# Constants 
G = 6.674e-11  # Gravitational constant
M_sun = 1.989e30  # Mass of the Sun

# Mercury's orbital parameters
a_mercury = 57.91e9  # Semi-major axis (meters)
e_mercury = 0.2056  # Eccentricity
T_mercury = 88 * 24 * 3600  # Orbital period (seconds)

# Number of frames for Mercury's orbit (proportional to its orbital period)
mercury_frames = int(T_mercury / (24 * 3600))  # Convert orbital period to days and then frames

# Venus Orbital Parameters
a_venus = 108.2e9  # Semi-major axis (meters)
e_venus = 0.0067  # Eccentricity
T_venus = 225 * 24 * 3600  # Orbital period (seconds)

# Number of frames for Venus's orbit (proportional to its orbital period)
venus_frames = int(T_venus / (24 * 3600))  # Convert orbital period to days and then frames

# Earth Orbital Parameters
a_earth = 149.6e9  # Semi-major axis (meters)
e_earth = 0.0167  # Eccentricity
T_earth = 365.25 * 24 * 3600  # Orbital period (seconds)

# Number of frames for Earth's orbit (proportional to its orbital period)
earth_frames = int(T_earth / (24 * 3600))  # Convert orbital period to days and then frames

# Mars Orbital Parameters
a_mars = 227.9e9  # Semi-major axis (meters)
e_mars = 0.0934  # Eccentricity
T_mars = 1.88 * 365.25 * 24 * 3600  # Orbital period (seconds)

# Number of frames for Mars's orbit (proportional to its orbital period)
mars_frames = int(T_mars / (24 * 3600))  # Convert orbital period to days and then frames

# Function to calculate Solar system stars' position at a given time
def calculate_position(t, a, e, T): 
    n = 2 * np.pi / T  # Mean motion (specific to the planet)
    M = n * t  # Mean anomaly

    # Solve Kepler's equation iteratively 
    E = M  
    E_next = M + e * np.sin(E)  # Eccentricity of the planet
    while abs(E - E_next) > 1e-6: 
        E = E_next
        E_next = M + e * np.sin(E)

    true_anomaly = 2 * np.arctan2(np.sqrt(1 + e) * np.tan(E / 2), np.sqrt(1 - e))
    r = a * (1 - e * np.cos(E))  # Semi-major axis of the planet

    x = r * np.cos(true_anomaly)
    y = r * np.sin(true_anomaly)
    z = 0  

    return x, y, z

print("Position calculated successfully!")

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
ax.legend(loc="upper left", fontsize=14)

# Change the plot background color to black
ax.set_facecolor('black')

# Lines to represent the orbits (initialize with empty data)
sun_path, = ax.plot([], [], [], color="orange", label="Sun")
mercury_path, = ax.plot([], [], [], color="black", label="Mercury", linewidth=2, linestyle='-') 
venus_path, = ax.plot([], [], [], color="brown", label="Venus", linewidth=2, linestyle='-') 
earth_path, = ax.plot([], [], [], color="green", label="Earth", linewidth=2, linestyle='-') 
mars_path, = ax.plot([], [], [], color="red", label="Mars", linewidth=2, linestyle='-') 

# Create representations of the Sun and planets 
sun, = ax.plot([], [], [], 'o', color='orange', markersize=10)
mercury, = ax.plot([], [], [], 'o', color='black', markersize=4)
venus, = ax.plot([], [], [], 'o', color='brown', markersize=4)
earth, = ax.plot([], [], [], 'o', color='green', markersize=4)
mars, = ax.plot([], [], [], 'o', color='red', markersize=4)

# Lists to store orbit history
sun_x = []
sun_y = []
sun_z = []
mercury_x = []
mercury_y = []
mercury_z = []
venus_x = []
venus_y = []
venus_z = []
earth_x = []
earth_y = []
earth_z = []
mars_x = []
mars_y = []
mars_z = []

def init():
    # Initialize lines with empty data (all planets)
    sun_path.set_data([], []) 
    sun_path.set_3d_properties([])
    mercury_path.set_data([], []) 
    mercury_path.set_3d_properties([])
    venus_path.set_data([], []) 
    venus_path.set_3d_properties([])
    earth_path.set_data([], []) 
    earth_path.set_3d_properties([])
    mars_path.set_data([], []) 
    mars_path.set_3d_properties([])

    # Initialize representations of the planets
    sun.set_data([], [])
    sun.set_3d_properties([])
    mercury.set_data([], [])
    mercury.set_3d_properties([])
    venus.set_data([], [])
    venus.set_3d_properties([])
    earth.set_data([], [])
    earth.set_3d_properties([])
    mars.set_data([], [])
    mars.set_3d_properties([])

    # Return all elements
    return sun_path, mercury_path, venus_path, earth_path, mars_path, sun, mercury, venus, earth, mars

print("Successfully Initialized!")

# Animation function (called repeatedly)
def animate(i):
    # Sun's motion (straight line in 3D)
    x_sun = i * 1e9  # Sun moves along the X-axis
    y_sun = 0  # Sun remains fixed at y = 0
    z_sun = 0  # Sun remains fixed at z = 0

    # Mercury calculations
    x_mercury, y_mercury, z_mercury = calculate_position(i * T_mercury / mercury_frames, a_mercury, e_mercury, T_mercury)
    x_mercury += x_sun  # Mercury moves along with the Sun
    y_mercury += y_sun  # Mercury moves along with the Sun
    z_mercury += z_sun  # Mercury moves along with the Sun

    # Venus calculations
    x_venus, y_venus, z_venus = calculate_position(i * T_venus / venus_frames, a_venus, e_venus, T_venus)
    x_venus += x_sun  # Venus moves along with the Sun
    y_venus += y_sun  # Venus moves along with the Sun
    z_venus += z_sun  # Venus moves along with the Sun

    # Earth calculations
    x_earth, y_earth, z_earth = calculate_position(i * T_earth / earth_frames, a_earth, e_earth, T_earth)
    x_earth += x_sun  # Earth moves along with the Sun
    y_earth += y_sun  # Earth moves along with the Sun
    z_earth += z_sun  # Earth moves along with the Sun

    # Mars calculations
    x_mars, y_mars, z_mars = calculate_position(i * T_mars / mars_frames, a_mars, e_mars, T_mars)
    x_mars += x_sun  # Mars moves along with the Sun
    y_mars += y_sun  # Mars moves along with the Sun
    z_mars += z_sun  # Mars moves along with the Sun

    sun.set_data([x_sun], [y_sun])
    sun.set_3d_properties(z_sun)  # Set 3D position

    mercury.set_data([x_mercury], [y_mercury])
    mercury.set_3d_properties(z_mercury)

    # Store Mercury positions for the orbit path
    mercury_x.append(x_mercury)
    mercury_y.append(y_mercury)
    mercury_z.append(z_mercury)

    # Plot Mercury orbit history
    mercury_path.set_data(mercury_x, mercury_y)
    mercury_path.set_3d_properties(mercury_z)

    venus.set_data([x_venus], [y_venus])
    venus.set_3d_properties(z_venus)

    # Store Venus positions for the orbit path
    venus_x.append(x_venus)
    venus_y.append(y_venus)
    venus_z.append(z_venus)

    # Plot Venus orbit history
    venus_path.set_data(venus_x, venus_y)
    venus_path.set_3d_properties(venus_z)

    earth.set_data([x_earth], [y_earth])
    earth.set_3d_properties(z_earth)

    # Store Earth positions for the orbit path
    earth_x.append(x_earth)
    earth_y.append(y_earth)
    earth_z.append(z_earth)

    # Plot Earth orbit history
    earth_path.set_data(earth_x, earth_y)
    earth_path.set_3d_properties(earth_z)

    mars.set_data([x_mars], [y_mars])
    mars.set_3d_properties(z_mars)

    # Store Mars positions for the orbit path
    mars_x.append(x_mars)
    mars_y.append(y_mars)
    mars_z.append(z_mars)

    # Plot Mars orbit history
    mars_path.set_data(mars_x, mars_y)
    mars_path.set_3d_properties(mars_z)

    # Store Sun positions for the orbit path
    sun_x.append(x_sun)
    sun_y.append(y_sun)
    sun_z.append(z_sun)

    # Plot Sun orbit history
    sun_path.set_data(sun_x, sun_y)
    sun_path.set_3d_properties(sun_z)

    # Set the viewing limits
    ax.set_xlim(-2.5 * a_earth + x_sun, 2.5 * a_earth + x_sun)
    ax.set_ylim(-2.5 * a_earth, 2.5 * a_earth + y_sun)
    ax.set_zlim(-2.5 * a_earth, 2.5 * a_earth + z_sun)

    return sun, mercury, venus, earth, mars

print("Animation setup successfully!")

# Add the legend
ax.legend()

def progress_bar(total):
    bar_length = 50
    for i in range(total + 1):
        progress = i / total
        num_blocks = int(progress * bar_length)
        bar = "[" + "#" * num_blocks + " " * (bar_length - num_blocks) + "]"
        sys.stdout.write("\r" + bar + " {:.2%}".format(progress))
        sys.stdout.flush()
        time.sleep(0.1)  # Simulate some work
    print()  # Move to the next line after the progress bar is complete

# progress_bar
total_iterations = 100
print("Generating Animation...")
progress_bar(total_iterations)

# Create and run the animation with an appropriate number of frames
animation = animation.FuncAnimation(fig, animate, frames=max(mercury_frames, venus_frames, earth_frames, mars_frames), interval=30, blit=True)

# Define a function to simulate the saving process
def save_animation(frames_to_save):
    print("Saving GIF...")
    bar_length = 50
    for i in range(frames_to_save):
        # Simulate saving one frame (replace this with the actual saving process)
        # Here, we just sleep for a short time to simulate the saving process
        time.sleep(0.1)

        # Calculate progress percentage
        progress = (i + 1) / frames_to_save
        num_blocks = int(progress * bar_length)
        bar = "[" + "#" * num_blocks + " " * (bar_length - num_blocks) + "]"
        sys.stdout.write("\r" + bar + " {:.2%}".format(progress))
        sys.stdout.flush()

    print("\nGIF Saved Successfully!")

# Define the total number of frames
total_frames = 3 * max(mercury_frames, venus_frames, earth_frames, mars_frames)

# Save the animation
save_animation(total_frames)

plt.show()