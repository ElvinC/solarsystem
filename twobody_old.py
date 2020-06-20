import matplotlib as mpl
import matplotlib.pyplot as plt
from gravitational_system import nbody_system
from body import body

mpl.rcParams['text.usetex'] = True


body_list = []
body_list.append(body(5, [0, 0], [-1/5, 0], [0, 0]))
body_list.append(body(1, [0, 1], [1, 0], [0, 0]))

system = nbody_system(body_list)

def reset_system(integrator_num):
    body_list = []
    body_list.append(body(5, [0, 0], [-1/5, 0], [0, 0]))
    body_list.append(body(1, [0, 1], [1, 0], [0, 0]))

    system = nbody_system(body_list)


    xs = []
    ys = []
    Edat = []

    n = len(body_list)

    # lists for saving position data
    for i in range(n):
        xs.append([])
        ys.append([])

    for iteration in range(500):
        integrator = [system.euler, system.verlet, system.ruth3][integrator_num]

        integrator(0.005)

        for i in range(n):
            xs[i].append(body_list[i].pos[0])
            ys[i].append(body_list[i].pos[1])

        Edat.append(system.total_energy())

    for i in range(n):
        plt.plot(xs[i], ys[i])

    # plot last points
    last_xs = [x[-1] for x in xs]
    last_ys = [y[-1] for y in ys]


    plt.scatter(last_xs,last_ys)

    return xs, ys, Edat

for i in range(1,3):
    reset_system(i)

plt.axis('equal')
plt.show()
#plt.plot(Edat)