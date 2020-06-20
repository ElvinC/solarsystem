import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from astroquery.jplhorizons import Horizons

from mpl_toolkits.mplot3d import Axes3D

mpl.rcParams['text.usetex'] = True

class body:
	def __init__(self, mass, position, velocity, acceleration, GM=0):
		self.mass = mass
		self.GM = GM
		self.pos = np.array(position, dtype=np.float64)
		self.vel = np.array(velocity, dtype=np.float64)
		self.acc = np.array(acceleration, dtype=np.float64)
		self.last_acc = np.array(acceleration, dtype=np.float64)
		self.sum_forces = np.array([0, 0])

	def iterate(self, dt=0.02):

		sun_center = np.array([0, 0, 0])
		sun_mass = 100
		G = 0.1e4
		GM = 132712440041.93938 # km^3/s^2

		#self.acc = self.sum_forces / self.mass
		self.pos += self.vel * dt + 0.5 * self.acc * dt**2
		self.acc = (-GM / ((self.pos**2).sum()))  * self.pos / (self.pos**2).sum()**0.5

		self.vel += 0.5 * (self.acc + self.last_acc) * dt

		self.last_acc = np.copy(self.acc)

		self.sum_forces *= 0

	def add_force(self, force):
		self.sum_forces += np.array(force, dtype=np.float64)




earth = Horizons(id='399', location='@ssb', epochs={'start':'1970-1-1', 'stop':'1972-1-1', 'step':'1d'}, id_type="majorbody")




vecs = earth.vectors()
print(vecs)

print(earth.uri)
JPLXs = vecs["x"]
JPLYs = vecs["y"]
JPLZs = vecs["z"]
JPLvx = vecs["vx"]
JPLvy = vecs["vy"]
JPLvz = vecs["vz"]


testobj = body(5.972e24, [JPLXs[0] * 149597870.7, JPLYs[0] * 149597870.7,  JPLZs[0] * 149597870.7], [JPLvx[0] * 149597870.7 / 86400, JPLvy[0] * 149597870.7 / 86400,  JPLvz[0] * 149597870.7 / 86400], [0, 0, 0])


print("object generated")

pos_lst = []
time_lst = []
vel_lst = []


fig = plt.figure()
ax = fig.add_subplot(111, autoscale_on=False, xlim=(-10, 10), ylim=(-10, 10))

#ax2 = fig.add_subplot(212, autoscale_on=False, xlim=(0, 7), ylim=(0, 8))

ax.axis('equal')
ax.grid()

ax.scatter([0], [0])

ax.plot(JPLXs, JPLYs, lw=3)

line, = ax.plot([], [], lw=2, dash_capstyle= 'butt')
ends = ax.scatter([], [], marker='o', color='green', zorder=2)

time_template = 'time = %.1fy'
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)


def init():
    line.set_data([], [])
    ends.set_offsets([0, 0])
    time_text.set_text('')
    return line, time_text


def animate(i):
	 # 1 day
	for y in range(20):
		testobj.iterate(86400/5)
	pos_lst.append(np.copy(testobj.pos))
	vel_lst.append((testobj.vel**2).sum()**0.5)
	time_lst.append(i)

	#if i == int(6.8/0.02):
	#	testobj.vel[0] += 1

	#line.set_data(time_lst, vel_lst)
	line.set_data([x[0]/1.496e8 for x in pos_lst], [x[1]/1.496e8 for x in pos_lst])
	ends.set_offsets([pos_lst[-1][0], pos_lst[-1][1]])
	time_text.set_text(time_template % (i*4 / 365))
	return line, time_text, ends


ani = animation.FuncAnimation(fig, animate, range(1, 365 * 30), interval=0.01*1000, blit=True, init_func=init)

plt.show()

plt.plot(time_lst, vel_lst)
plt.grid(axis='both')


plt.show()