import scipy.integrate # Library for numerical integration (ODE Solvers)
import numpy as np  # Library for numerical calculations
import matplotlib.pyplot as plt  # Library for plotting
from mpl_toolkits.mplot3d import Axes3D  # For 3D plots
from matplotlib import animation  # For creating animations
from matplotlib.animation import PillowWriter

# Constants 
G = 6.674e-11  # Gravitational constant
M_sun = 1.989e30  # Mass of the Sun

# Mercury's orbital parameters
a = 57.91e9  # Semi-major axis (meters)
e = 0.2056  # Eccentricity
T = 88 * 24 * 3600  # Orbital period (seconds)

# Function to calculate Mercury's position at a given time
def calculate_position(t):
    n = 2 * np.pi / T  # Mean motion
    M = n * t  # Mean anomaly

    # Solve Kepler's equation iteratively (for accuracy)
    E = M  
    E_next = M + e * np.sin(E) 
    while abs(E - E_next) > 1e-6: 
        E = E_next
        E_next = M + e * np.sin(E)

    true_anomaly = 2 * np.arctan2(np.sqrt(1 + e) * np.tan(E / 2), np.sqrt(1 - e))
    r = a * (1 - e * np.cos(E))  

    x = r * np.cos(true_anomaly)
    y = r * np.sin(true_anomaly)
    z = 0  # Mercury's orbit is roughly in the x-y plane

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
ax.set_title("Visualization of orbits of stars in our Solar System\n", fontsize=14)
ax.title.set_color('white')
ax.xaxis.label.set_color('white')
ax.yaxis.label.set_color('white')
ax.zaxis.label.set_color('white')
ax.tick_params(colors='white')
ax.legend(loc="upper left", fontsize=14)

# Change the plot background color to black
ax.set_facecolor('black')

# Lines to represent the orbits (initialize with empty data)
line1, = ax.plot([], [], [], color="orange", label="Sun")
line2, = ax.plot([], [], [], color="brown", label="Mercury")

# Create representations of the Sun and Mercury 
sun, = ax.plot([], [], [], 'o', color='orange')
mercury, = ax.plot([], [], [], 'o', color='brown', markersize=4)

# Lists to store orbit history
mercury_x = []
mercury_y = []
mercury_z = []

def init():
    # Initialize lines with empty data
    line1.set_data([], []) 
    line1.set_3d_properties([])
    line2.set_data([], []) 
    line2.set_3d_properties([])
    sun.set_data([], [])
    sun.set_3d_properties([])
    mercury.set_data([], [])
    mercury.set_3d_properties([])

    return line1, line2, sun, mercury

# Animation function (called repeatedly)
def animate(i):
    x, y, z = calculate_position(i * T / 50)  # Update positions

    sun.set_data(0, 0)  
    sun.set_3d_properties(0) 

    mercury.set_data(x, y)
    mercury.set_3d_properties(z)

    # Store positions for the orbit path
    mercury_x.append(x)
    mercury_y.append(y)
    mercury_z.append(z)

    # Plot the orbit history 
    line2.set_data(mercury_x, mercury_y)
    line2.set_3d_properties(mercury_z)

    
    ax.set_xlim(-1.5 * a, 1.5 * a) 
    ax.set_ylim(-1.5 * a, 1.5 * a)
    ax.set_zlim(-1.5 * a, 1.5 * a)

    return sun, mercury

# Add the legend
ax.legend()

# Create and run the animation
animation = animation.FuncAnimation(fig, animate, frames=50, interval=30, blit=True)
plt.show()

# Save the animation
animation.save("C:/Users/aloha/OneDrive/Data/nth-body-sim/solar_sys_simulation.gif", writer=PillowWriter(fps=24))
print("GIF Save Attempted")