import matplotlib as mpl
import matplotlib.pyplot as plt
from gravitational_system import nbody_system
from body import body
import numpy as np

from astroquery.jplhorizons import Horizons

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

BodyID=3

years = 10
stepperday = 4

stepsize = 1/stepperday # days

plot_interval = 1 # log once every x days

offset = 5 # leap days etc

focus_pos = []
earth_data = []

xval = []

earth_data.append(np.copy(body_list[2].pos))
focus_pos.append(np.copy(body_list[BodyID].pos))
xval.append(system.time)

for i in range(int(365 * years) + offset):

    if i % int(365) == 0:
        print("Year {}/{}".format(i/365, years))

    
    for j in range(stepperday):
        system.ruth3(stepsize)

    focus_pos.append(np.copy(body_list[BodyID].pos))
    earth_data.append(np.copy(body_list[2].pos))
    xval.append(system.time/365)

focus_data = np.stack(focus_pos, axis=0)
earth_data = np.stack(earth_data, axis=0)

#print(mars_data)


# get mars horizons data
body = Horizons(id="301", location='@ssb', epochs={'start':'1970-1-1', 'stop':'2000-1-1', 'step':'1d'}, id_type="majorbody")
vecs = body.vectors()


jpldat = vecs["x", "y", "z"]

jpl_pos = np.array(jpldat).view((float, len(jpldat.dtype.names)))

print("Dat{}, jpl:{}".format(focus_data.shape[0], jpl_pos.shape[0]))

min_len = min(jpl_pos.shape[0], focus_data.shape[0])
jpl_pos = jpl_pos[:min_len]
focus_data = focus_data[:min_len]
earth_data = earth_data[:min_len]
xval = xval[:min_len]


diff = (earth_data - focus_data) * 149597870.700

real_diff = (earth_data - jpl_pos) * 149597870.700

diff_mag = np.linalg.norm(diff, axis=1)

real_diff_mag = real_diff

# diff to nasa
nasa_diff =  np.linalg.norm((focus_data - jpl_pos) * 149597870.700, axis=1)


# plotting
mpl.rcParams['text.usetex'] = True
mpl.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})


fig = plt.figure(figsize=(8, 4))

ax = fig.add_subplot(122) # 121
#system.show_system_2d(ax, 10)


ax2 = fig.add_subplot(121, autoscale_on=False, projection='3d')

ax2.set_xlim3d(-400000, 400000)
ax2.set_ylim3d(-400000,400000)
ax2.set_zlim3d(-400000,400000)

ax2.set_aspect('equal')

fig.suptitle("Månen position relativ til Jorden")
#ax2.set_xlabel('tid [dage]')
#ax2.set_ylabel('$\Delta r$ [km]')

#ax2.grid(True)



#ax2.plot(xval[::plot_interval], diff_mag[::plot_interval])
starttime = 1500

ax2.plot(diff[starttime::plot_interval,0], diff[starttime::plot_interval,1], diff[starttime::plot_interval,2], linewidth=0.1, alpha=0.6)

ax2.plot(real_diff[starttime::plot_interval,0], real_diff[starttime::plot_interval,1], real_diff[starttime::plot_interval,2], linewidth=0.1, alpha=0.6)

ax2.scatter(diff[-1,0], diff[-1,1], diff[-1,2], label='Simulation')
ax2.scatter(real_diff[-1,0], real_diff[-1,1], real_diff[-1,2], label='Horizons data')
ax2.legend()

ax2.scatter([0], [0], [0])

ax.set_xlabel('tid [år]')
ax.set_ylabel('$\Delta r$ [km]')

ax.set_title("Afvigelse")
ax.plot(xval[::5*plot_interval], nasa_diff[::5*plot_interval])
ax.grid(True)
#ax2.scatter([0], [0], [0])

fig.tight_layout(pad=1.01)

plt.savefig("test.pgf",bbox_inches='tight', pad_inches = 0)

plt.show()