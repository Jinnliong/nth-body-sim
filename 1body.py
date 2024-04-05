import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import scipy.integrate

G = 6.6743e-11  # Gravitational constant

# Simplified Planetary Data (Name, Mass, Initial Position (x, y, z), Initial Velocity (vx, vy, vz))
planets = [
    ("Sun", 1.989e30, [0, 0, 0], [0, 0, 0]),
    ("Mercury", 3.3011e23, [0.4, 0, 0], [0, 47360, 0]), 
    # ... Add data for other planets
]

def gravitational_force(state, t, G, planets):
    """Calculates total gravitational force on each body"""
    forces = np.zeros_like(state)

    for i, (_, mass_i, pos_i, _) in enumerate(planets):
        for j, (_, mass_j, pos_j, _) in enumerate(planets):
            if i != j:
                dist_vec = pos_j - pos_i
                dist = np.linalg.norm(dist_vec)
                forces[i*6:i*6+3] += G * mass_i * mass_j * dist_vec / dist**3

    return forces

# State vector: [x1, y1, z1, vx1, vy1, vz1, x2, y2, ... ] 
initial_state = np.array([item for planet in planets for item in planet[2] + planet[3]])

# ODE Solver
time_span = np.linspace(0, 10*365.25*24*3600, 5000)  # Simulate for 10 years
solution = scipy.integrate.odeint(gravitational_force, initial_state, time_span, args=(G, planets))

# Extract planetary trajectories
trajectories = []
num_planets = len(planets)
for i in range(num_planets):
    trajectories.append(solution[:, i*6:i*6+3])  

# ... (Previous code: imports, data, equations of motion, ODE solver) ...

# Animation Setup
fig = plt.figure(figsize=(15, 15))
ax = fig.add_subplot(111, projection="3d")

# Lines to represent planetary orbits
lines = [ax.plot([], [], [], color=f"C{i}")[0] for i in range(num_planets)] 
points, = ax.plot([], [], [], 'o', color='black')  # Points for planets

# Axis labels, title, etc.
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.set_title("Solar System Simulation")

# ... (Calculate axis limits based on your planetary data) ...

# Initialization function 
def init():
    for line in lines:
        line.set_data([], [])
        line.set_3d_properties([])
    points.set_data([], [])
    points.set_3d_properties([])
    return lines + [points]

# Animation function
def animate(i):
    for j, line in enumerate(lines):
        x, y, z = trajectories[j][:i, 0], trajectories[j][:i, 1], trajectories[j][:i, 2]
        line.set_data(x, y)
        line.set_3d_properties(z)

    x_planets, y_planets, z_planets = [traj[i, 0] for traj in trajectories], \
                                      [traj[i, 1] for traj in trajectories], \
                                      [traj[i, 2] for traj in trajectories]
    points.set_data(x_planets, y_planets)
    points.set_3d_properties(z_planets)

    return lines + [points] 

# Create the animation
ani = animation.FuncAnimation(fig, animate, frames=len(time_span), interval=30, blit=True, init_func=init)
plt.show()