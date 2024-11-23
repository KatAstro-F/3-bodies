import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

# Constants
time_step = 0.005 
steps = 20000  
G = 1.0  

# Masses of the three bodies
m1, m2, m3 = 1.0, 1.0, 1.0  

# Carefully chosen initial positions (x, y) for equilateral triangle configuration
pos1 = np.array([0.0, 1.0])
pos2 = np.array([np.sqrt(3)/2, -0.5])
pos3 = np.array([-np.sqrt(3)/2, -0.5])

# Initial velocities (vx, vy) chosen to balance centrifugal force
vel1 = np.array([-0.5, 0.0])
vel2 = np.array([0.25, 0.433])
vel3 = np.array([0.25, -0.433])

# Arrays to store trajectories
trail1 = []
trail2 = []
trail3 = []

# Function to calculate gravitational force
def calculate_gravitational_force(pos1, pos2, m1, m2):
    r_vec = pos2 - pos1
    r_mag = np.linalg.norm(r_vec)
    if r_mag == 0:
        return np.array([0.0, 0.0])  # Avoid division by zero
    force_mag = G * m1 * m2 / r_mag**2
    force_vec = force_mag * (r_vec / r_mag)
    return force_vec

# Simulation function
def simulate():
    global pos1, pos2, pos3, vel1, vel2, vel3

    for _ in range(steps):
        # Check if all particles are out of bounds
        if (np.all(np.abs(pos1) > 2) and
            np.all(np.abs(pos2) > 2) and
            np.all(np.abs(pos3) > 2)):
            break

        # Calculate forces on each body
        force_on_1 = calculate_gravitational_force(pos1, pos2, m1, m2) + calculate_gravitational_force(pos1, pos3, m1, m3)
        force_on_2 = calculate_gravitational_force(pos2, pos1, m2, m1) + calculate_gravitational_force(pos2, pos3, m2, m3)
        force_on_3 = calculate_gravitational_force(pos3, pos1, m3, m1) + calculate_gravitational_force(pos3, pos2, m3, m2)

        # Update velocities
        vel1 += force_on_1 / m1 * time_step
        vel2 += force_on_2 / m2 * time_step
        vel3 += force_on_3 / m3 * time_step

        # Update positions
        pos1 += vel1 * time_step
        pos2 += vel2 * time_step
        pos3 += vel3 * time_step

        # Store positions for visualization
        trail1.append(pos1.copy())
        trail2.append(pos2.copy())
        trail3.append(pos3.copy())

# Run the simulation
simulate()

# Convert trails to arrays for plotting
trail1 = np.array(trail1)
trail2 = np.array(trail2)
trail3 = np.array(trail3)

# Plotting setup
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_aspect('equal')
ax.set_facecolor('black')
ax.axis('off')  # Turn off the axis

particle1, = ax.plot([], [], 'o', color='cyan', markersize=8)
particle2, = ax.plot([], [], 'o', color='magenta', markersize=8)
particle3, = ax.plot([], [], 'o', color='yellow', markersize=8)
trail1_line, = ax.plot([], [], '-', color='cyan', linewidth=2, alpha=0.7)
trail2_line, = ax.plot([], [], '-', color='magenta', linewidth=2, alpha=0.7)
trail3_line, = ax.plot([], [], '-', color='yellow', linewidth=2, alpha=0.7)

# Animation function
def update(frame):
    particle1.set_data(trail1[frame, 0], trail1[frame, 1])
    particle2.set_data(trail2[frame, 0], trail2[frame, 1])
    particle3.set_data(trail3[frame, 0], trail3[frame, 1])
    trail1_line.set_data(trail1[:frame, 0], trail1[:frame, 1])
    trail2_line.set_data(trail2[:frame, 0], trail2[:frame, 1])
    trail3_line.set_data(trail3[:frame, 0], trail3[:frame, 1])
    return particle1, particle2, particle3, trail1_line, trail2_line, trail3_line

# Adjust interval to maintain playback speed
total_duration_seconds = 10  # GIF duration in s
frame_interval = total_duration_seconds * 1000 / len(trail1)

ani = FuncAnimation(fig, update, frames=len(trail1), interval=frame_interval, blit=True)

# Save animation as GIF
ani.save("three_body_simulation.gif", writer=PillowWriter(fps=30), savefig_kwargs={'facecolor':'black'})

plt.show()
