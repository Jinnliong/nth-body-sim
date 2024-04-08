import scipy.integrate # Library for numerical integration (ODE Solvers)
import numpy as np  # Library for numerical calculations
import matplotlib.pyplot as plt  # Library for plotting
from mpl_toolkits.mplot3d import Axes3D  # For 3D plots
from matplotlib import animation  # For creating animations
from matplotlib.animation import PillowWriter


# Constants and Initial Conditions

# Define universal gravitation constant
G = 6.67408e-11 # N-m2/kg2
AU = 1.496e11    # Meters in one Astronomical Unit
year = 365.25 * 24 * 3600  # Seconds in a year

# Constants related to the Alpha Centauri system
# Reference quantities
m_sun = 1.989e30  # kg 
m_mercury = 3.301e23  # kg
r_sun = np.array([0, 0, 0])  # Sun at the origin (approximately)
v_sun = np.array([0, 0, 0])   # Sun mostly stationary (for simplification)
r_mercury = np.array([0.3075, 0, 0])  # Initial position (AU)
v_mercury = np.array([0, 58980, 0])   # Initial velocity (m/s)
t_nd = 79.91 * 365 * 24 * 3600 * 0.51 # s - orbital period of Alpha Centauri

# New K1 (note the unit cancellations)
K1 = G * m_sun * year**2 / AU**3  

# New K2 
K2 = AU / year

# Masses of the stars
m1 = 1.1  # Alpha Centauri A
m2 = 0.907  # Alpha Centauri B

# Initial positions of the stars (think of this as a starting snapshot)
r1 = [-0.5, 0, 0]
r2 = [0.5, 0, 0]

# Initial velocities of the stars (how fast and in what direction they start moving)
r1 = np.array(r1, dtype="float64")
r2 = np.array(r2, dtype="float64")

# Find Centre of Mass
r_com = (m1 * r1 + m2 * r2) / (m1 + m2)

# Define initial velocities
v1 = [0, 0, 0] # m/s
v2 = [-0.05, 0, -0.1] # m/s

# Convert velocity vectors to arrays
v1 = np.array(v1, dtype="float64")
v2 = np.array(v2, dtype="float64")

# Find velocity of COM
v_com = (m1 * v1 + m2 * v2) / (m1 + m2)

# Equations of Motion: The Core Logic
def PlanetaryEquations(w, t, G, m_sun, m_mercury):
    r_mercury = w[:3]
    v_mercury = w[3:]

    r = np.linalg.norm(r_mercury - r_sun)  # Distance between Sun and Mercury

    dv_mercury_by_dt = -G * m_sun * (r_mercury - r_sun) / r**3  
    dr_mercury_by_dt = v_mercury

    derivs = np.concatenate((dr_mercury_by_dt, dv_mercury_by_dt))
    return derivs


# Package initial parameters
init_params = np.concatenate((r_mercury, v_mercury))
init_params = init_params.flatten()

# Time span (let's simulate for a few Mercury years)
mercury_year = 0.241 # Earth years 
time_span = np.linspace(0, 5 * mercury_year, 500)  

# Run the ODE solver
mercury_sol = scipy.integrate.odeint(PlanetaryEquations, init_params, time_span, args=(G, m_sun, m_mercury))
r_mercury_sol = mercury_sol[:, :3]

r1_sol = mercury_sol[:, :3]
r2_sol = mercury_sol[:, 3:6]

# Create figure
fig = plt.figure(figsize=(15, 15))

# Create 3D axes
ax = fig.add_subplot(111, projection="3d")

# Add labels and title
ax.set_xlabel("x-coordinate", fontsize=14)
ax.set_ylabel("y-coordinate", fontsize=14)
ax.set_zlabel("z-coordinate", fontsize=14)
ax.set_title("Visualization of orbits of stars in a two-body system\n", fontsize=14)
ax.legend(loc="upper left", fontsize=14)

# Lines to represent the orbits (initialize with empty data)
line1, = ax.plot([], [], [], color="Orange", label="Sun")
line2, = ax.plot([], [], [], color="tab:Brown", label="Mercury")
 
# Scatter objects to represent stars
star1, = ax.plot([], [], [], 'o', color="Orange")
star2, = ax.plot([], [], [], 'o', color="tab:Brown")

def init():
    # Initialize lines with empty data
    line1.set_data([], []) 
    line1.set_3d_properties([])
    line2.set_data([], []) 
    line2.set_3d_properties([])
    star1.set_data([], [])
    star1.set_3d_properties([])
    star2.set_data([], [])
    star2.set_3d_properties([])

    buffer = 2  # Adjust this value as needed
    max_range = np.array([r1_sol.max(), r2_sol.max()]).max() + buffer
    min_range = np.array([r1_sol.min(), r2_sol.min()]).min() - buffer
    ax.set_xlim(min_range, max_range)
    ax.set_ylim(min_range, max_range)
    ax.set_zlim(min_range, max_range)

    print("r1_sol max:", r1_sol.max())
    print("r1_sol min:", r1_sol.min())
    print("r2_sol max:", r2_sol.max())
    print("r2_sol min:", r2_sol.min())
  
    return line1, line2, star1, star2

def animate(i):
    # Extract trajectories up to frame i
    x1, y1, z1 = r1_sol[:i, 0], r1_sol[:i, 1], r1_sol[:i, 2]
    x2, y2, z2 = r2_sol[:i, 0], r2_sol[:i, 1], r2_sol[:i, 2]

    if x1.size > 0 and y1.size > 0 and z1.size > 0:  # Check if arrays have data
        line1.set_data(x1, y1)
        line1.set_3d_properties(z1)
        line2.set_data(x2, y2)
        line2.set_3d_properties(z2)

        # Update star positions
        star1.set_data(x1[-1], y1[-1])
        star1.set_3d_properties(z1[-1])
        star2.set_data(x2[-1], y2[-1])
        star2.set_3d_properties(z2[-1])

    return line1, line2, star1, star2

# Create animation
ani = animation.FuncAnimation(fig, animate, frames=len(time_span), interval=20, blit=True, init_func=init)

# Add the legend
ax.legend()

# Display the animation
plt.show()

# Save the animation
ani.save("C:/Users/aloha/OneDrive/Data/nth-body-sim/solar_sys_simulation.gif", writer=PillowWriter(fps=24))
print("GIF Save Attempted")