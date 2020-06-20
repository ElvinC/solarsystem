import matplotlib as mpl
import matplotlib.pyplot as plt
from gravitational_system import nbody_system
from body import body
import numpy as np

import csv

# list containing all celestial bodies
body_list = []

np.set_printoptions(15)

# load initial conditions from file
input_file = csv.DictReader(open("initial.csv", encoding="utf8"))

for b in input_file:
    pos = [float(x) for x in [b["x"], b["y"], b["z"]]]
    vel = [float(x) for x in [b["vx"], b["vy"], b["vz"]]]
    GM = float(b["GM"])
    name = b["name"]
    body_list.append(body(GM, pos, vel, [0, 0, 0], name))


system = nbody_system(body_list, 1.4881852e-34)

years = 10
stepsize = 1 # days

for i in range(int(365 * years/stepsize)):
    if i % int(365/stepsize) == 0:
        print("Year {}/{}".format(i/365 * stepsize, years))

    system.ruth4(stepsize)
    

fig = plt.figure(figsize=(5.8, 3.0))

ax = fig.gca(projection='3d')

# equal axis sizes
ax.set_xlim(-18, 18)
ax.set_ylim(-18,18)
ax.set_zlim(-18,18)

ax.set_aspect('equal') # Doesn't work with newest matplotlib version. I was using mpl 2.2.3
ax.grid()

# Visualize simulation
system.show_system_3d(ax, 10)

plt.show()

# Show total energy and angular momentum
system.show_system_ang_momentum()
system.show_system_energy()
