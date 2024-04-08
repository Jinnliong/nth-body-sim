import scipy.integrate # Library for numerical integration (ODE Solvers)
import numpy as np  # Library for numerical calculations
import matplotlib.pyplot as plt  # Library for plotting
from mpl_toolkits.mplot3d import Axes3D  # For 3D plots
from matplotlib import animation  # For creating animations
from matplotlib.animation import PillowWriter


# Constants and Initial Conditions

# Define universal gravitation constant
G = 6.67408e-11 # N-m2/kg2

# Constants related to the Alpha Centauri system
# Reference quantities
m_nd = 1.989e+30 # kg - mass of the sun
r_nd = 5.326e+12 # m - distance between stars in Alpha Centauri
v_nd = 30000 # m/s - relative velocity of earth around the sun
t_nd = 79.91 * 365 * 24 * 3600 * 0.51 # s - orbital period of Alpha Centauri

# Net constants
K1 = G * t_nd * m_nd / (r_nd**2 * v_nd)
K2 = v_nd * t_nd / r_nd

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
v1 = [0.01, 0.01, 0] # m/s
v2 = [-0.05, 0, -0.1] # m/s

# Convert velocity vectors to arrays
v1 = np.array(v1, dtype="float64")
v2 = np.array(v2, dtype="float64")

# Find velocity of COM
v_com = (m1 * v1 + m2 * v2) / (m1 + m2)

# Equations of Motion: The Core Logic
def TwoBodyEquations(w, t, G, m1, m2):
    r1 = w[:3]      # Extract the first three elements of w (x, y, z coordinates of star 1)
    r2 = w[3:6]     # Extract elements 3, 4, 5 from w (x, y, z coordinates of star 1)
    v1 = w[6:9]     # Extract elements 6, 7, 8 from w (x, y, z coordinates of star 2)
    v2 = w[9:12]    # Extract elements 9, 10, 11 from w (velocity components of star 1)

    # Calculate distances between each pair of stars
    r=np.linalg.norm(r2-r1) #Calculate magnitude or norm of vector

    dv1bydt=K1*m2*(r2-r1)/r**3
    dv2bydt=K1*m1*(r1-r2)/r**3

    dr1bydt=K2*v1
    dr2bydt=K2*v2
    
    r_derivs=np.concatenate((dr1bydt,dr2bydt))
    derivs=np.concatenate((r_derivs,dv1bydt,dv2bydt))
    return derivs 

# Package initial parameters
init_params = np.array([r1, r2, v1, v2]) # Initial parameters
init_params = init_params.flatten() # Flatten to make 1D array
time_span = np.linspace(0, 30, 750) # 30 orbital periods and 750 points

# Run the ODE solver
two_body_sol = scipy.integrate.odeint(TwoBodyEquations, init_params, time_span, args=(G, m1, m2))

r1_sol = two_body_sol[:, :3]
r2_sol = two_body_sol[:, 3:6]

# Create figure
fig = plt.figure(figsize=(15, 15))

# Create 3D axes
ax = fig.add_subplot(111, projection="3d")

# Plot the orbits before animation
#ax.plot(r1_sol[:, 0], r1_sol[:, 1], r1_sol[:, 2], color="darkblue")
#ax.plot(r2_sol[:, 0], r2_sol[:, 1], r2_sol[:, 2], color="tab:red")

# Plot the final positions of the stars before animation
#ax.scatter(0, 0, 0, color="black", marker="*", s=200, label="Center of Mass") 
#ax.scatter(r1_sol[-1, 0], r1_sol[-1, 1], r1_sol[-1, 2], color="darkblue", marker="o", s=100, label="Alpha Centauri A")
#ax.scatter(r2_sol[-1, 0], r2_sol[-1, 1], r2_sol[-1, 2], color="tab:red", marker="o", s=100, label="Alpha Centauri B")

# Add labels and title
fig.patch.set_facecolor('black')
ax.set_xlabel("x-coordinate", fontsize=14)
ax.set_ylabel("y-coordinate", fontsize=14)
ax.set_zlabel("z-coordinate", fontsize=14)
ax.set_title("Visualization of orbits of stars in a two-body system\n", fontsize=14)
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
 
# Scatter objects to represent stars
star1, = ax.plot([], [], [], 'o', color="darkblue")
star2, = ax.plot([], [], [], 'o', color="tab:red")

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

# Save the animation
ani.save("C:/Users/aloha/OneDrive/Data/nth-body-sim/two_body_simulation.gif", writer=PillowWriter(fps=24))
print("GIF Save Attempted")

# Display the animation
plt.show()