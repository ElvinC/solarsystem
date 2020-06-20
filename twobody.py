import matplotlib as mpl
import matplotlib.pyplot as plt
from gravitational_system import nbody_system
from body import body


body_list = []
body_list.append(body(5, [0, 0], [-1/5, 0], [0, 0]))
body_list.append(body(1, [0, 1], [1, 0], [0, 0]))

system = nbody_system(body_list)


xs = []
ys = []
E_data = []
n = len(body_list)

# lists for saving position data
for i in range(n):
    xs.append([])
    ys.append([])


for iteration in range(500):
    # Choose numerical method; verlet, euler, ruth3
    system.ruth3(0.005)

    for i in range(n):
        xs[i].append(body_list[i].pos[0])
        ys[i].append(body_list[i].pos[1])

    E_data.append(system.total_energy())


# Plotting options
mpl.rcParams['text.usetex'] = True
mpl.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6,3))

ax1.set_title("Position")
ax1.set_xlabel('$x$')
ax1.set_ylabel('$y$')
ax1.grid(True)


ax2.set_title("Energi")
ax2.set_xlabel('iteration')
ax2.set_ylabel('E')
ax2.grid(True)

plot_samle_interval = 1


for i in range(n):
    ax1.plot(xs[i][::plot_samle_interval], ys[i][::plot_samle_interval])

# plot last positions
last_xs = [x[-1] for x in xs]
last_ys = [y[-1] for y in ys]

ax1.scatter(last_xs,last_ys)
ax1.axis('equal')

iteration_list = [x for x in range(len(E_data))]
print("Plotting {} datapoints".format(int(len(E_data)/plot_samle_interval)))

ax2.plot(iteration_list[::plot_samle_interval], E_data[::plot_samle_interval])

fig.tight_layout()
plt.show()