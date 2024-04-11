# Let's enhance our cosmic journey to include 3D motion for the Sun, Mercury, and Venus!

import scipy.integrate  # Library for numerical integration (ODE Solvers)
import numpy as np  # Library for numerical calculations
import matplotlib.pyplot as plt  # Library for plotting
from mpl_toolkits.mplot3d import Axes3D  # For 3D plots
from matplotlib import animation  # For creating animations
from matplotlib.animation import PillowWriter  # For saving GIFs

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
ax.set_title("A Cosmic Waltz: Mercury and Venus in the Solar System\n", fontsize=14)
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

# Create representations of the Sun and planets 
sun, = ax.plot([], [], [], 'o', color='orange', markersize=10)
mercury, = ax.plot([], [], [], 'o', color='black', markersize=4)
venus, = ax.plot([], [], [], 'o', color='brown', markersize=4)

# Lists to store orbit history
mercury_x = []
mercury_y = []
mercury_z = []
venus_x = []
venus_y = []
venus_z = []

def init():
    # Initialize lines with empty data (all planets)
    sun_path.set_data([], []) 
    sun_path.set_3d_properties([])
    mercury_path.set_data([], []) 
    mercury_path.set_3d_properties([])
    venus_path.set_data([], []) 
    venus_path.set_3d_properties([])

    # Initialize representations of the planets
    sun.set_data([], [])
    sun.set_3d_properties([])
    mercury.set_data([], [])
    mercury.set_3d_properties([])
    venus.set_data([], [])
    venus.set_3d_properties([])

    # Return all elements
    return sun_path, mercury_path, venus_path, sun, mercury, venus 

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

    sun.set_data(x_sun, y_sun)
    sun.set_3d_properties(z_sun)  # Set 3D position

    mercury.set_data(x_mercury, y_mercury)
    mercury.set_3d_properties(z_mercury)

    # Store Mercury positions for the orbit path
    mercury_x.append(x_mercury)
    mercury_y.append(y_mercury)
    mercury_z.append(z_mercury)

    # Plot Mercury orbit history
    mercury_path.set_data(mercury_x, mercury_y)
    mercury_path.set_3d_properties(mercury_z)

    venus.set_data(x_venus, y_venus)
    venus.set_3d_properties(z_venus)

    # Store Venus positions for the orbit path
    venus_x.append(x_venus)
    venus_y.append(y_venus)
    venus_z.append(z_venus)

    # Plot Venus orbit history
    venus_path.set_data(venus_x, venus_y)
    venus_path.set_3d_properties(venus_z)

    # Set the viewing limits
    ax.set_xlim(-2.5 * a_venus + x_sun, 2.5 * a_venus + x_sun)
    ax.set_ylim(-2.5 * a_venus, 2.5 * a_venus)
    ax.set_zlim(-2.5 * a_venus, 2.5 * a_venus)

    return sun, mercury, venus

# Add the legend
ax.legend()

# Create and run the animation
animation = animation.FuncAnimation(fig, animate, frames=max(mercury_frames, venus_frames), interval=30, blit=True)

# Save the animation
animation.save("solar_sys_simulation.gif", writer=PillowWriter(fps=24))
print("GIF Saved Successfully!")

plt.show()