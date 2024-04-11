import scipy.integrate
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation
from matplotlib.animation import PillowWriter

# Constants 
G = 6.674e-11  # Gravitational constant
M_sun = 1.989e30  # Mass of the Sun

# Mercury's orbital parameters
a_mercury = 57.91e9  # Semi-major axis (meters)
e_mercury = 0.2056  # Eccentricity
T_mercury = 88 * 24 * 3600  # Orbital period (seconds)

# Venus Orbital Parameters
a_venus = 108.2e9  # Semi-major axis (meters)
e_venus = 0.0067  # Eccentricity
T_venus = 225 * 24 * 3600  # Orbital period (seconds)

# Earth Orbital Parameters
a_earth = 149.6e9  # Semi-major axis (meters)
e_earth = 0.0167  # Eccentricity
T_earth = 365.25 * 24 * 3600  # Orbital period (seconds)

# Mars Orbital Parameters
a_mars = 227.9e9  # Semi-major axis (meters)
e_mars = 0.0934  # Eccentricity
T_mars = 1.88 * 365.25 * 24 * 3600  # Orbital period (seconds)

# Jupiter Orbital Parameters
a_jupiter = 778.5e9  # Semi-major axis (meters)
e_jupiter = 0.0489  # Eccentricity
T_jupiter = 11.86 * 365.25 * 24 * 3600  # Orbital period (seconds)

# Number of frames for each planet's orbit
mercury_frames = int(T_mercury / (24 * 3600))
venus_frames = int(T_venus / (24 * 3600))
earth_frames = int(T_earth / (24 * 3600))
mars_frames = int(T_mars / (24 * 3600))
jupiter_frames = int(T_jupiter / (24 * 3600))

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
jupiter_path, = ax.plot([], [], [], color="cyan", label="Jupiter", linewidth=2, linestyle='-') 

# Create representations of the Sun and planets 
sun, = ax.plot([], [], [], 'o', color='orange', markersize=10)
mercury, = ax.plot([], [], [], 'o', color='black', markersize=4)
venus, = ax.plot([], [], [], 'o', color='brown', markersize=4)
earth, = ax.plot([], [], [], 'o', color='green', markersize=4)
mars, = ax.plot([], [], [], 'o', color='red', markersize=4)
jupiter, = ax.plot([], [], [], 'o', color='cyan', markersize=6)

# Lists to store orbit history
sun_x, sun_y, sun_z = [], [], []
mercury_x, mercury_y, mercury_z = [], [], []
venus_x, venus_y, venus_z = [], [], []
earth_x, earth_y, earth_z = [], [], []
mars_x, mars_y, mars_z = [], [], []
jupiter_x, jupiter_y, jupiter_z = [], [], []

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
    jupiter_path.set_data([], []) 
    jupiter_path.set_3d_properties([])

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
    jupiter.set_data([], [])
    jupiter.set_3d_properties([])

    # Return all elements
    return sun_path, mercury_path, venus_path, earth_path, mars_path, jupiter_path, sun, mercury, venus, earth, mars, jupiter

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

    # Jupiter calculations
    x_jupiter, y_jupiter, z_jupiter = calculate_position(i * T_jupiter / jupiter_frames, a_jupiter, e_jupiter, T_jupiter)
    x_jupiter += x_sun  # Jupiter moves along with the Sun
    y_jupiter += y_sun  # Jupiter moves along with the Sun
    z_jupiter += z_sun  # Jupiter moves along with the Sun

    sun.set_data(x_sun, y_sun)
    sun.set_3d_properties(z_sun)  # Set 3D position

    mercury.set_data(x_mercury, y_mercury)
    mercury.set_3d_properties(z_mercury)

    venus.set_data(x_venus, y_venus)
    venus.set_3d_properties(z_venus)

    earth.set_data(x_earth, y_earth)
    earth.set_3d_properties(z_earth)

    mars.set_data(x_mars, y_mars)
    mars.set_3d_properties(z_mars)

    jupiter.set_data(x_jupiter, y_jupiter)
    jupiter.set_3d_properties(z_jupiter)

    # Store positions for the orbit paths
    sun_x.append(x_sun)
    sun_y.append(y_sun)
    sun_z.append(z_sun)

    mercury_x.append(x_mercury)
    mercury_y.append(y_mercury)
    mercury_z.append(z_mercury)

    venus_x.append(x_venus)
    venus_y.append(y_venus)
    venus_z.append(z_venus)

    earth_x.append(x_earth)
    earth_y.append(y_earth)
    earth_z.append(z_earth)

    mars_x.append(x_mars)
    mars_y.append(y_mars)
    mars_z.append(z_mars)

    jupiter_x.append(x_jupiter)
    jupiter_y.append(y_jupiter)
    jupiter_z.append(z_jupiter)

    # Plot orbit history
    sun_path.set_data(sun_x, sun_y)
    sun_path.set_3d_properties(sun_z)

    mercury_path.set_data(mercury_x, mercury_y)
    mercury_path.set_3d_properties(mercury_z)

    venus_path.set_data(venus_x, venus_y)
    venus_path.set_3d_properties(venus_z)

    earth_path.set_data(earth_x, earth_y)
    earth_path.set_3d_properties(earth_z)

    mars_path.set_data(mars_x, mars_y)
    mars_path.set_3d_properties(mars_z)

    jupiter_path.set_data(jupiter_x, jupiter_y)
    jupiter_path.set_3d_properties(jupiter_z)

    # Set the viewing limits
    ax.set_xlim(-2.5 * a_earth + x_sun, 2.5 * a_earth + x_sun)
    ax.set_ylim(-2.5 * a_earth, 2.5 * a_earth + y_sun)
    ax.set_zlim(-2.5 * a_earth, 2.5 * a_earth + z_sun)

    return sun, mercury, venus, earth, mars, jupiter

# Add the legend
ax.legend()

# Create and run the animation with increased frames
animation = animation.FuncAnimation(fig, animate, frames=3 * max(mercury_frames, venus_frames, earth_frames, mars_frames, jupiter_frames), interval=30, blit=True)

# Save the animation
animation.save("solar_sys_simulation_with_all_planets.gif", writer=PillowWriter(fps=24))
print("GIF Saved Successfully!")

plt.show()
