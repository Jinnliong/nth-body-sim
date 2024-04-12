# Let's journey through the cosmos with Python!

import scipy.integrate  # For numerical integration (ODE Solvers)
import numpy as np  # For numerical calculations
import matplotlib.pyplot as plt  # For plotting
from mpl_toolkits.mplot3d import Axes3D  # For 3D plots
from matplotlib import animation  # For creating animations
from matplotlib.animation import PillowWriter  # For saving GIFs


# Constants and Initial Conditions

# Define the universal gravitation constant
G = 6.67408e-11  # N-m2/kg2

# Constants related to the Alpha Centauri system
# Reference quantities
m_nd = 1.989e+30  # kg - mass of the sun
r_nd = 5.326e+12  # m - distance between stars in Alpha Centauri
v_nd = 30000  # m/s - relative velocity of earth around the sun
t_nd = 79.91 * 365 * 24 * 3600 * 0.51  # s - orbital period of Alpha Centauri

# Normalized constants
K1 = G * t_nd * m_nd / (r_nd ** 2 * v_nd)
K2 = v_nd * t_nd / r_nd

# Masses of the stars
m1 = 1.1  # Alpha Centauri A
m2 = 0.907  # Alpha Centauri B
m3 = 1  # Third star

# Initial positions of the stars (think of this as a starting snapshot)
r1 = [-0.5, 0, 0]
r2 = [0.5, 0, 0]
r3 = [0, 0, 1]

# Initial velocities of the stars (how fast and in what direction they start moving)
r1 = np.array(r1, dtype="float64")
r2 = np.array(r2, dtype="float64")
r3 = np.array(r3, dtype="float64")

# Find the Centre of Mass
r_com = (m1 * r1 + m2 * r2 + m3 * r3) / (m1 + m2 + m3)

# Define initial velocities
v1 = [0.01, 0.01, 0]  # m/s
v2 = [-0.05, 0, -0.1]  # m/s
v3 = [0, -0.01, 0]  # m/s

# Convert velocity vectors to arrays
v1 = np.array(v1, dtype="float64")
v2 = np.array(v2, dtype="float64")
v3 = np.array(v3, dtype="float64")

# Find velocity of the Centre of Mass
v_com = (m1 * v1 + m2 * v2 + m3 * v3) / (m1 + m2 + m3)

# Equations of Motion: The Core Logic
def ThreeBodyEquations(w, t, G, m1, m2, m3):
    r1 = w[:3]  # Extract the first three elements of w (x, y, z coordinates of star 1)
    r2 = w[3:6]  # Extract elements 3, 4, 5 from w (x, y, z coordinates of star 2)
    r3 = w[6:9]  # Extract elements 6, 7, 8 from w (x, y, z coordinates of star 3)
    v1 = w[9:12]  # Extract elements 9, 10, 11 from w (velocity components of star 1)
    v2 = w[12:15]  # Extract elements 12, 13, 14 from w (velocity components of star 2)
    v3 = w[15:18]  # Extract elements 15, 16, 17 from w (velocity components of star 3)

    # Calculate distances between each pair of stars
    r12 = np.linalg.norm(r2 - r1)  # Distance between star 1 and 2
    r13 = np.linalg.norm(r3 - r1)  # Distance between star 1 and 3
    r23 = np.linalg.norm(r3 - r2)  # Distance between star 2 and 3

    # Calculate gravitational forces based on Newton's Law of Gravitation
    dv1bydt = K1 * m2 * (r2 - r1) / r12 ** 3 + K1 * m3 * (r3 - r1) / r13 ** 3
    dv2bydt = K1 * m1 * (r1 - r2) / r12 ** 3 + K1 * m3 * (r3 - r2) / r23 ** 3
    dv3bydt = K1 * m1 * (r1 - r3) / r13 ** 3 + K1 * m2 * (r2 - r3) / r23 ** 3

    # Calculate changes in position based on velocity (including COM adjustment)
    dr1bydt = K2 * v1 - v_com  # Adjust for center of mass motion
    dr2bydt = K2 * v2 - v_com
    dr3bydt = K2 * v3 - v_com

    # Combine changes for solving
    r12_derivs = np.concatenate((dr1bydt, dr2bydt))  # Changes for stars 1 & 2
    r_derivs = np.concatenate((r12_derivs, dr3bydt))  # Changes for all 3 stars (positions)
    v12_derivs = np.concatenate((dv1bydt, dv2bydt))  # Changes for stars 1 & 2
    v_derivs = np.concatenate((v12_derivs, dv3bydt))  # Changes for all 3 stars (velocities)
    derivs = np.concatenate((r_derivs, v_derivs))  # All changes for the solver

    return derivs


# Package initial parameters
init_params = np.array([r1, r2, r3, v1, v2, v3])  # Initial parameters
init_params = init_params.flatten()  # Flatten to make 1D array
time_span = np.linspace(0, 30, 750)  # 30 orbital periods and 750 points

# Run the ODE solver
three_body_sol = scipy.integrate.odeint(ThreeBodyEquations, init_params, time_span, args=(G, m1, m2, m3))

r1_sol = three_body_sol[:, :3]
r2_sol = three_body_sol[:, 3:6]
r3_sol = three_body_sol[:, 6:9]

# Create figure
fig = plt.figure(figsize=(15, 15))

# Create 3D axes
ax = fig.add_subplot(111, projection="3d")

# Add a touch of cosmic flair to the plot

# Plot the final positions of the stars before animation
#ax.scatter(0, 0, 0, color="black", marker="*", s=200, label="Center of Mass")
#ax.scatter(r1_sol[-1, 0], r1_sol[-1, 1], r1_sol[-1, 2], color="darkblue", marker="o", s=100, label="Alpha Centauri A")
#ax.scatter(r2_sol[-1, 0], r2_sol[-1, 1], r2_sol[-1, 2], color="tab:red", marker="o", s=100, label="Alpha Centauri B")
#ax.scatter(r3_sol[-1, 0], r3_sol[-1, 1], r3_sol[-1, 2], color="tab:green", marker="o", s=100, label="Third Celestial Body")

# Add labels and title
fig.patch.set_facecolor('black')
ax.set_xlabel("x-coordinate", fontsize=14)
ax.set_ylabel("y-coordinate", fontsize=14)
ax.set_zlabel("z-coordinate", fontsize=14)
ax.set_title("Dance of the Stars: A Three-Body System\n", fontsize=14)
ax.title.set_color('white')
ax.xaxis.label.set_color('white')
ax.yaxis.label.set_color('white')
ax.zaxis.label.set_color('white')
ax.tick_params(colors='white')
ax.legend(loc="upper left", fontsize=14)

# Change the plot background color to black
ax.set_facecolor('black')

# Lines to represent the orbits (initialize with empty data)
line1, = ax.plot([], [], [], color="darkblue", label="Alpha Centauri A")
line2, = ax.plot([], [], [], color="tab:red", label="Alpha Centauri B")
line3, = ax.plot([], [], [], color="tab:green", label="Third Celestial Body")

# Scatter objects to represent stars
star1, = ax.plot([], [], [], 'o', color="darkblue")
star2, = ax.plot([], [], [], 'o', color="tab:red")
star3, = ax.plot([], [], [], 'o', color="tab:green")


def init():
    # Initialize lines with empty data
    line1.set_data([], [])
    line1.set_3d_properties([])
    line2.set_data([], [])
    line2.set_3d_properties([])
    line3.set_data([], [])
    line3.set_3d_properties([])
    star1.set_data([], [])
    star1.set_3d_properties([])
    star2.set_data([], [])
    star2.set_3d_properties([])
    star3.set_data([], [])
    star3.set_3d_properties([])

    buffer = 0.1  # Adjust this value as needed
    max_range = np.array([r1_sol.max(), r2_sol.max(), r3_sol.max()]).max() + buffer
    min_range = np.array([r1_sol.min(), r2_sol.min(), r3_sol.min()]).min() - buffer
    ax.set_xlim(min_range, max_range)
    ax.set_ylim(min_range, max_range)
    ax.set_zlim(min_range, max_range)

    return line1, line2, line3, star1, star2, star3


def animate(i):
    # Extract trajectories up to frame i
    x1, y1, z1 = r1_sol[:i, 0], r1_sol[:i, 1], r1_sol[:i, 2]
    x2, y2, z2 = r2_sol[:i, 0], r2_sol[:i, 1], r2_sol[:i, 2]
    x3, y3, z3 = r3_sol[:i, 0], r3_sol[:i, 1], r3_sol[:i, 2]

    if x1.size > 0 and y1.size > 0 and z1.size > 0:  # Check if arrays have data
        line1.set_data(x1, y1)
        line1.set_3d_properties(z1)
        line2.set_data(x2, y2)
        line2.set_3d_properties(z2)
        line3.set_data(x3, y3)
        line3.set_3d_properties(z3)

        # Update star positions
        star1.set_data(x1[-1], y1[-1])
        star1.set_3d_properties(z1[-1])
        star2.set_data(x2[-1], y2[-1])
        star2.set_3d_properties(z2[-1])
        star3.set_data(x3[-1], y3[-1])
        star3.set_3d_properties(z3[-1])

    return line1, line2, line3, star1, star2, star3


# Create animation
ani = animation.FuncAnimation(fig, animate, frames=len(time_span), interval=20, blit=True, init_func=init)

# Add the legend
ax.legend()

# Save the animation
ani.save("3body.gif", writer=PillowWriter(fps=24))
print("GIF Saved Successfully!")

# Display the animation
plt.show()