import matplotlib.pyplot as plt
import numpy as np

# Create some data
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Create a figure and axes
fig, ax = plt.subplots()

# Plot the data
ax.plot(x, y, 'white')  # Plot line in white for visibility

# Change the plot background color to black
ax.set_facecolor('black')

# If you want to change the whole figure background color including labels and ticks to black
fig.patch.set_facecolor('black')
ax.tick_params(colors='white')
ax.xaxis.label.set_color('white')
ax.yaxis.label.set_color('white')

plt.show()
