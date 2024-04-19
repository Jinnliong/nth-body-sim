import scipy.integrate  # Library for numerical integration (ODE Solvers)
import numpy as np  # Library for numerical calculations
import matplotlib.pyplot as plt  # Library for plotting
from mpl_toolkits.mplot3d import Axes3D  # For 3D plots
from matplotlib import animation  # For creating animations
from matplotlib.animation import PillowWriter  # For saving GIFs
import time

# Input Variables
orbital_factor = 0.5
distance_factor = 1
skip_factor = 100  # Normal speed

# Constants 
G = 6.674e-11  # Gravitational constant
M_sun = 1.989e30  # Mass of the Sun

# Mercury's orbital parameters
a_mercury = distance_factor * 57.91e9  # Semi-major axis (meters)
e_mercury = 0.2056  # Eccentricity
T_mercury = orbital_factor * 88 * 24 * 3600  # Orbital period (seconds)

# Number of frames for Mercury's orbit (proportional to its orbital period)
mercury_frames = int(T_mercury / (24 * 3600))  # Convert orbital period to days and then frames

# Venus Orbital Parameters
a_venus = distance_factor * 108.2e9  # Semi-major axis (meters)
e_venus = 0.0067  # Eccentricity
T_venus = orbital_factor * 225 * 24 * 3600  # Orbital period (seconds)

# Number of frames for Venus's orbit (proportional to its orbital period)
venus_frames = int(T_venus / (24 * 3600))  # Convert orbital period to days and then frames

# Earth Orbital Parameters
a_earth = distance_factor * 149.6e9  # Semi-major axis (meters)
e_earth = 0.0167  # Eccentricity
T_earth = orbital_factor * 365.25 * 24 * 3600  # Orbital period (seconds)

# Number of frames for Earth's orbit (proportional to its orbital period)
earth_frames = int(T_earth / (24 * 3600))  # Convert orbital period to days and then frames

# Mars Orbital Parameters
a_mars = distance_factor * 227.9e9  # Semi-major axis (meters)
e_mars = 0.0934  # Eccentricity
T_mars = orbital_factor * 1.88 * 365.25 * 24 * 3600  # Orbital period (seconds)

# Number of frames for Mars's orbit (proportional to its orbital period)
mars_frames = int(T_mars / (24 * 3600))  # Convert orbital period to days and then frames

# Jupiter Orbital Parameters
a_jupiter = distance_factor * 778.6e9  # Semi-major axis (meters)
e_jupiter = 0.0489  # Eccentricity
T_jupiter = orbital_factor * 11.86 * 365.25 * 24 * 3600  # Orbital period (seconds)

# Number of frames for Jupiter's orbit (proportional to its orbital period)
jupiter_frames = int(T_jupiter / (24 * 3600))  # Convert orbital period to days and then frames

# Saturn Orbital Parameters
a_saturn = distance_factor * 1.433e12  # Semi-major axis (meters)
e_saturn = 0.0565  # Eccentricity
T_saturn = orbital_factor * 29.5 * 365.25 * 24 * 3600  # Orbital period (seconds)

# Number of frames for Saturn's orbit (proportional to its orbital period)
saturn_frames = int(T_saturn / (24 * 3600))  # Convert orbital period to days and then frames

# Uranus Orbital Parameters
a_uranus = distance_factor * 2.88e12  # Semi-major axis (meters)
e_uranus = 0.0444  # Eccentricity
T_uranus = orbital_factor * 84.07 * 365.25 * 24 * 3600  # Orbital period (seconds)

# Number of frames for Uranus's orbit (proportional to its orbital period)
uranus_frames = int(T_uranus / (24 * 3600))  # Convert orbital period to days and then frames

# Neptune Orbital Parameters
a_neptune = distance_factor * 4.495e12  # Semi-major axis (meters)
e_neptune = 0.0113  # Eccentricity
T_neptune = orbital_factor * 164.8 * 365.25 * 24 * 3600  # Orbital period (seconds)

# Number of frames for Neptune's orbit (proportional to its orbital period)
neptune_frames = int(T_neptune / (24 * 3600))  # Convert orbital period to days and then frames

# Determine the slowest planet
slowest_planet_name = ""
slowest_planet_frames = max(mercury_frames, venus_frames, earth_frames, mars_frames, jupiter_frames, saturn_frames, uranus_frames, neptune_frames)
if slowest_planet_frames == mercury_frames:
    slowest_planet_name = "Mercury"
elif slowest_planet_frames == venus_frames:
    slowest_planet_name = "Venus"
elif slowest_planet_frames == earth_frames:
    slowest_planet_name = "Earth"
elif slowest_planet_frames == mars_frames:
    slowest_planet_name = "Mars"
elif slowest_planet_frames == jupiter_frames:
    slowest_planet_name = "Jupiter"
elif slowest_planet_frames == saturn_frames:
    slowest_planet_name = "Saturn"
elif slowest_planet_frames == uranus_frames:
    slowest_planet_name = "Uranus"
elif slowest_planet_frames == neptune_frames:
    slowest_planet_name = "Neptune"

print(f"The slowest planet is {slowest_planet_name} with {slowest_planet_frames} frames.")

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
    y = 0
    z = r * np.sin(true_anomaly)

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
ax.set_title("A Cosmic Waltz: Planets Dancing in the Solar System\n", fontsize=14)
ax.title.set_color('white')
ax.xaxis.label.set_color('white')
ax.yaxis.label.set_color('white')
ax.zaxis.label.set_color('white')
ax.tick_params(colors='white')

# Change the plot background color to black
ax.set_facecolor('black')

# Lines to represent the orbits (initialize with empty data)
sun_path, = ax.plot([], [], [], color="orange", label="Sun")
mercury_path, = ax.plot([], [], [], color="darkorange", label="Mercury", linewidth=2, linestyle='-')
venus_path, = ax.plot([], [], [], color="brown", label="Venus", linewidth=2, linestyle='-')
earth_path, = ax.plot([], [], [], color="deepskyblue", label="Earth", linewidth=2, linestyle='-')
mars_path, = ax.plot([], [], [], color="red", label="Mars", linewidth=2, linestyle='-')
jupiter_path, = ax.plot([], [], [], color="cyan", label="Jupiter", linewidth=2, linestyle='-')
saturn_path, = ax.plot([], [], [], color="yellow", label="Saturn", linewidth=2, linestyle='-')
uranus_path, = ax.plot([], [], [], color="lightseagreen", label="Uranus", linewidth=2, linestyle='-')
neptune_path, = ax.plot([], [], [], color="blue", label="Neptune", linewidth=2, linestyle='-')

# Create representations of the Sun and planets 
sun, = ax.plot([], [], [], 'o', color='orange', markersize=10)
mercury, = ax.plot([], [], [], 'o', color='darkorange', markersize=4)
venus, = ax.plot([], [], [], 'o', color='brown', markersize=4)
earth, = ax.plot([], [], [], 'o', color='deepskyblue', markersize=4)
mars, = ax.plot([], [], [], 'o', color='red', markersize=4)
jupiter, = ax.plot([], [], [], 'o', color='cyan', markersize=4)
saturn, = ax.plot([], [], [], 'o', color='yellow', markersize=4)
uranus, = ax.plot([], [], [], 'o', color='lightseagreen', markersize=4)
neptune, = ax.plot([], [], [], 'o', color='blue', markersize=4)

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
jupiter_x = []
jupiter_y = []
jupiter_z = []
saturn_x = []
saturn_y = []
saturn_z = []
uranus_x = []
uranus_y = []
uranus_z = []
neptune_x = []
neptune_y = []
neptune_z = []

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
    saturn_path.set_data([], []) 
    saturn_path.set_3d_properties([])
    uranus_path.set_data([], []) 
    uranus_path.set_3d_properties([])
    neptune_path.set_data([], []) 
    neptune_path.set_3d_properties([])

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
    saturn.set_data([], [])
    saturn.set_3d_properties([])
    uranus.set_data([], [])
    uranus.set_3d_properties([])
    neptune.set_data([], [])
    neptune.set_3d_properties([])

    # Return all elements
    return sun_path, mercury_path, venus_path, earth_path, mars_path, jupiter_path, saturn_path, sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune

# Animation function (called repeatedly)
def animate(i):

    # Calculate the frame index considering the skip factor
    frame_index = i * skip_factor

    # You will use 'frame_index' instead of 'i' to fetch or calculate the positions:
    x_mercury, y_mercury, z_mercury = calculate_position(frame_index * T_mercury / mercury_frames, a_mercury, e_mercury, T_mercury)
    x_venus, y_venus, z_venus = calculate_position(frame_index * T_venus / venus_frames, a_venus, e_venus, T_venus)
    x_earth, y_earth, z_earth = calculate_position(frame_index * T_earth / earth_frames, a_earth, e_earth, T_earth)
    x_mars, y_mars, z_mars = calculate_position(frame_index * T_mars / mars_frames, a_mars, e_mars, T_mars)
    x_jupiter, y_jupiter, z_jupiter = calculate_position(frame_index * T_jupiter / jupiter_frames, a_jupiter, e_jupiter, T_jupiter)
    x_saturn, y_saturn, z_saturn = calculate_position(frame_index * T_saturn / saturn_frames, a_saturn, e_saturn, T_saturn)
    x_uranus, y_uranus, z_uranus = calculate_position(frame_index * T_uranus / uranus_frames, a_uranus, e_uranus, T_uranus)
    x_neptune, y_neptune, z_neptune = calculate_position(frame_index * T_neptune / neptune_frames, a_neptune, e_neptune, T_neptune)

    # Sun's motion (straight line in 3D)
    x_sun = frame_index* 1e9  # Sun moves along the X-axis
    y_sun = 0  # Sun remains fixed at y = 0
    z_sun = 0  # Sun remains fixed at z = 0

    # Mercury calculations
    #x_mercury, y_mercury, z_mercury = calculate_position(i * T_mercury / mercury_frames, a_mercury, e_mercury, T_mercury)
    x_mercury += x_sun  # Mercury moves along with the Sun
    y_mercury += y_sun  # Mercury moves along with the Sun
    z_mercury += z_sun  # Mercury moves along with the Sun

    # Venus calculations
    #x_venus, y_venus, z_venus = calculate_position(i * T_venus / venus_frames, a_venus, e_venus, T_venus)
    x_venus += x_sun  # Venus moves along with the Sun
    y_venus += y_sun  # Venus moves along with the Sun
    z_venus += z_sun  # Venus moves along with the Sun

    # Earth calculations
    #x_earth, y_earth, z_earth = calculate_position(i * T_earth / earth_frames, a_earth, e_earth, T_earth)
    x_earth += x_sun  # Earth moves along with the Sun
    y_earth += y_sun  # Earth moves along with the Sun
    z_earth += z_sun  # Earth moves along with the Sun

    # Mars calculations
    #x_mars, y_mars, z_mars = calculate_position(i * T_mars / mars_frames, a_mars, e_mars, T_mars)
    x_mars += x_sun  # Mars moves along with the Sun
    y_mars += y_sun  # Mars moves along with the Sun
    z_mars += z_sun  # Mars moves along with the Sun

    # Jupiter calculations
    x_jupiter += x_sun  # Jupiter moves along with the Sun
    y_jupiter += y_sun  # Jupiter moves along with the Sun
    z_jupiter += z_sun  # Jupiter moves along with the Sun

    # Saturn calculations
    x_saturn += x_sun  # Saturn moves along with the Sun
    y_saturn += y_sun  # Saturn moves along with the Sun
    z_saturn += z_sun  # Saturn moves along with the Sun

    # Uranus calculations
    x_uranus += x_sun  # Uranus moves along with the Sun
    y_uranus += y_sun  # Uranus moves along with the Sun
    z_uranus += z_sun  # Uranus moves along with the Sun

    # Neptune calculations
    x_neptune += x_sun
    y_neptune += y_sun
    z_neptune += z_sun

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

    jupiter.set_data([x_jupiter], [y_jupiter])
    jupiter.set_3d_properties(z_jupiter)

    # Store Jupiter positions for the orbit path
    jupiter_x.append(x_jupiter)
    jupiter_y.append(y_jupiter)
    jupiter_z.append(z_jupiter)

    # Plot Jupiter orbit history
    jupiter_path.set_data(jupiter_x, jupiter_y)
    jupiter_path.set_3d_properties(jupiter_z)

    saturn.set_data([x_saturn], [y_saturn])
    saturn.set_3d_properties(z_saturn)

    # Store Saturn positions for the orbit path
    saturn_x.append(x_saturn)
    saturn_y.append(y_saturn)
    saturn_z.append(z_saturn)

    # Plot Saturn orbit history
    saturn_path.set_data(saturn_x, saturn_y)
    saturn_path.set_3d_properties(saturn_z)

    uranus.set_data([x_uranus], [y_uranus])
    uranus.set_3d_properties(z_uranus)

    # Store Uranus positions for the orbit path
    uranus_x.append(x_uranus)
    uranus_y.append(y_uranus)
    uranus_z.append(z_uranus)

    # Plot Uranus orbit history
    uranus_path.set_data(uranus_x, uranus_y)
    uranus_path.set_3d_properties(uranus_z)

    neptune.set_data([x_neptune], [y_neptune])
    neptune.set_3d_properties(z_neptune)

    # Store Uranus positions for the orbit path
    neptune_x.append(x_neptune)
    neptune_y.append(y_neptune)
    neptune_z.append(z_neptune)

    # Plot Uranus orbit history
    neptune_path.set_data(neptune_x, neptune_y)
    neptune_path.set_3d_properties(neptune_z)

    # Store Sun positions for the orbit path
    sun_x.append(x_sun)
    sun_y.append(y_sun)
    sun_z.append(z_sun)

    # Plot Sun orbit history
    sun_path.set_data(sun_x, sun_y)
    sun_path.set_3d_properties(sun_z)

    # Set the viewing limits
    #ax.set_xlim(-2.5 * a_earth + x_sun, 2.5 * a_earth + x_sun)
    #ax.set_ylim(-2.5 * a_earth, 2.5 * a_earth + y_sun)
    #ax.set_zlim(-2.5 * a_earth, 2.5 * a_earth + z_sun)
    ax.set_xlim(-0.5 * a_neptune + x_sun, 0.5 * a_neptune + x_sun)
    ax.set_ylim(-0.5 * a_neptune, 0.5 * a_neptune + y_sun)
    ax.set_zlim(-0.5 * a_neptune, 0.5 * a_neptune + z_sun)

    return sun, mercury, venus, earth, mars,jupiter, saturn, uranus, neptune

# Add the legend
ax.legend(loc="upper left", fontsize=14, bbox_to_anchor=(-0.2, 1))

# Create and run the animation with increased frames
ani = animation.FuncAnimation(fig, animate, frames=2 * max(mercury_frames, venus_frames, earth_frames, mars_frames, uranus_frames, neptune_frames), interval=30, blit=True)

# Calculate total frames considering the speed factor
total_frames = int(1 * max(mercury_frames, venus_frames, earth_frames, mars_frames, jupiter_frames, saturn_frames, uranus_frames, neptune_frames))

start_time = time.time()

# Save the animation with progress indicator
writer = PillowWriter(fps=24, metadata=dict(artist='Me'), bitrate=1800)
with writer.saving(fig, "solar_sys.gif", dpi=100):
    for i in range(total_frames):  # Loop adjusted for the new total_frames calculation
        animate(i)
        writer.grab_frame()
        completion = (i+1) / total_frames * 100
        elapsed_time = time.time() - start_time
        print(f"Saving frame {i+1}/{total_frames} - Completion: {completion:.2f}% - Elapsed Time: {elapsed_time:.2f} seconds", end="\r")

print(f"\nGIF Saved Successfully in {elapsed_time:.2f} seconds!")

plt.show()