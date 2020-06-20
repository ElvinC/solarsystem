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

years = 10
stepsize = 1 # days

offset = 50 # leap days etc

mars_pos = []


mars_pos.append(np.copy(body_list[5].pos))

for i in range(int(365 * years/stepsize) + offset):
    if i % int(365/stepsize) == 0:
        print("Year {}/{}".format(i/365 * stepsize, years))

    system.ruth3(stepsize)
    mars_pos.append(np.copy(body_list[5].pos))

mars_data = np.stack(mars_pos, axis=0)

#print(mars_data)


# get mars horizons data
body = Horizons(id="499", location='@ssb', epochs={'start':'1970-1-1', 'stop':'2000-1-1', 'step':'1d'}, id_type="majorbody")
vecs = body.vectors()


jpldat = vecs["x", "y", "z"]

jpl_mars_pos = np.array(jpldat).view((float, len(jpldat.dtype.names)))

print("Dat{}, jpl:{}".format(mars_data.shape[0], jpl_mars_pos.shape[0]))

min_len = min(jpl_mars_pos.shape[0], mars_data.shape[0])
jpl_mars_pos = jpl_mars_pos[:min_len]
mars_data = mars_data[:min_len]


diff = (jpl_mars_pos - mars_data) * 149597870.700

diff_mag = np.linalg.norm(diff, axis=1)



# plotting
mpl.rcParams['text.usetex'] = True
mpl.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})


fig = plt.figure(figsize=(5.8, 3.0))

#ax = fig.add_subplot(111) # 121
#system.show_system_2d(ax, 10)


ax2 = fig.add_subplot(111)

ax2.set_title("Afvigelse")
ax2.set_xlabel('tid [år]')
ax2.set_ylabel('$\Delta r$ [km]')

ax2.grid(True)
xval = [x/365 for x in system.times][:min_len:5] # convert to years

ax2.plot(xval, diff_mag[::5])

fig.tight_layout(pad=1.01)

plt.show()