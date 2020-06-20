import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from astroquery.jplhorizons import Horizons
from mpl_toolkits.mplot3d import Axes3D
import time
import csv

from body import body

mpl.rcParams['text.usetex'] = True


class nbody_system:
	def __init__(self, body_list, G=1):
		self.body_list = body_list
		self.n = len(body_list)
		self.G = G

		self.time = 0

		# get dimension from pos of first body
		self.dimension = len(self.body_list[0].pos)

		# Data logging
		self.xs = [[] for i in range(self.n)]
		self.ys = [[] for i in range(self.n)]
		self.zs = [[] for i in range(self.n)]
		self.E_data = []
		self.L_data = []
		self.times = []

		self.log_data()

		# update inital gravitational accelerations
		self.update_acc()
	
	def log_data(self):
		
		# log position data for each body
		for i in range(self.n):
			self.xs[i].append(self.body_list[i].pos[0])
			self.ys[i].append(self.body_list[i].pos[1])

			if self.dimension == 3:
				# add z-dimension
				self.zs[i].append(self.body_list[i].pos[2])
	
		# log total energy and time
		self.E_data.append(self.total_energy())
		self.L_data.append(self.total_ang_momentum())
		self.times.append(self.time)



	def update_acc(self):
		# calculate gravitational interaction between each body
		for i in range(self.n):
			# forces on body i
			body_i = self.body_list[i]
			# save previous acceleration
			body_i.last_acc = np.copy(body_i.acc)

			# reset current acceleration and sum:
			body_i.acc *= 0
			for j in range(self.n):
				if j != i:
					# every other body
					body_j = self.body_list[j]
					# calculate acceleration
					
					body_i.acc -= body_j.GM * (body_i.pos - body_j.pos) / (np.linalg.norm(body_i.pos - body_j.pos)**3)


	def euler(self, dt=0.005):
		# calculate new gravitational acceleration for each body.
		self.update_acc()

		for i in range(self.n):
			body_i = self.body_list[i]

			#position full-step
			body_i.pos += dt * body_i.vel

			# velocity step
			body_i.vel += dt * body_i.acc

		self.time += dt
		self.log_data()


	def symplectic_euler(self, dt=0.005):
		# calculate new gravitational acceleration for each body.
		self.update_acc()

		for i in range(self.n):
			body_i = self.body_list[i]
			# velocity half-step
			body_i.vel += dt * body_i.acc

			#position full-step
			body_i.pos += dt * body_i.vel
		
		self.time += dt
		self.log_data()

	def verlet(self, dt=0.005):
		
		for i in range(self.n):
			# velocity half-step
			body_i = self.body_list[i]
			body_i.vel += dt/2 * body_i.acc

			#position full-step
			body_i.pos += dt * body_i.vel

		# calculate new gravitational acceleration for each body.
		self.update_acc()

		
		for i in range(self.n):
			# final velocity half-step
			body_i = self.body_list[i]
			body_i.vel += dt/2 * body_i.acc

		self.time += dt
		self.log_data()

	def ruth3(self, dt=0.005):
		# 3rd order symplectic integrator
		c = [7/24, 3/4, -1/24]
		d = [2/3, -2/3, 1]

		for idx in range(3):
			# update acceleration for new pos
			self.update_acc()

			for i in range(self.n):
				body_i = self.body_list[i]
				# update pos and vel using coeffecients
				body_i.vel += body_i.acc * c[idx] * dt
				body_i.pos += body_i.vel * d[idx] * dt

		self.time += dt
		self.log_data()

	def ruth4(self, dt=0.005):
		# 4rd order symplectic integrator
		c = [+0.6756035959798288170,-0.1756035959798288170,-0.1756035959798288170,+0.6756035959798288170]
		d = [+1.3512071919596576340,-1.7024143839193152681,+1.3512071919596576340,+0.0]

		for idx in range(4):
			# update acceleration for new pos
			self.update_acc()

			for i in range(self.n):
				body_i = self.body_list[i]
				# update pos and vel using coeffecients
				body_i.vel += body_i.acc * c[idx] * dt
				body_i.pos += body_i.vel * d[idx] * dt

		self.time += dt
		self.log_data()

	def total_energy(self):
		E_total = 0
		
		for i in range(self.n):
			body_i = self.body_list[i]
			#kinetic energy
			E_total += 1/2 * body_i.GM * np.linalg.norm(body_i.vel)**2

			for j in range(i+1, self.n):
				body_j = self.body_list[j]
				E_total -= body_i.GM * body_j.GM/(np.linalg.norm(body_i.pos - body_j.pos))


		return E_total/self.G

	def total_ang_momentum(self):
		L_total = np.array([0, 0, 0], dtype=np.float64)

		for i in range(self.n):
			body_i = self.body_list[i]
			#kinetic energy

			p = body_i.GM * body_i.vel / self.G
			L_total += np.cross(body_i.pos, p)


		return np.linalg.norm(L_total)


	def show_system_ang_momentum(self, plot_samle_interval = 1):
		
		# Plotting options
		mpl.rcParams['text.usetex'] = True
		mpl.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})

		fig, ax = plt.subplots(1, 1, figsize=(6,3))

		ax.set_title("Angular momentum")
		ax.set_xlabel('Time')
		ax.set_ylabel('L')
		ax.grid(True)

		
		print("Plotting {} datapoints".format(int(len(self.L_data)/plot_samle_interval)))

		ax.plot(self.times[::plot_samle_interval], self.L_data[::plot_samle_interval])

		fig.tight_layout()
		plt.show()

	def show_system_energy(self, plot_samle_interval = 1):

		# Plotting options
		mpl.rcParams['text.usetex'] = True
		mpl.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})

		fig, ax = plt.subplots(1, 1, figsize=(6,3))

		ax.set_title("Energy")
		ax.set_xlabel('Time')
		ax.set_ylabel('E')
		ax.grid(True)

		
		print("Plotting {} datapoints".format(int(len(self.E_data)/plot_samle_interval)))

		ax.plot(self.times[::plot_samle_interval], self.E_data[::plot_samle_interval])

		fig.tight_layout()
		plt.show()

	def show_system_2d(self, plot, plot_samle_interval = 1):
		plot.set_title("Position")
		plot.set_xlabel('$x$')
		plot.set_ylabel('$y$')
		plot.grid(True)

		for i in range(self.n):
			# plot position history
			plot.plot(self.xs[i][::plot_samle_interval], self.ys[i][::plot_samle_interval])

			# Same color as lines
			# ax1.scatter(self.xs[i][-1],self.ys[i][-1])


		# plot last positions, all blue
		last_xs = [x[-1] for x in self.xs]
		last_ys = [y[-1] for y in self.ys]

		plot.scatter(last_xs,last_ys)
		plot.axis('equal')



	def show_system_2d_energy(self, plot_samle_interval = 1):
		
		# Plotting options
		mpl.rcParams['text.usetex'] = True
		mpl.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})

		fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6,3))

		ax1.set_title("Position")
		ax1.set_xlabel('$x$')
		ax1.set_ylabel('$y$')
		ax1.grid(True)


		ax2.set_title("Energy")
		ax2.set_xlabel('Iteration')
		ax2.set_ylabel('E')
		ax2.grid(True)

		


		for i in range(self.n):
			# plot position history
			ax1.plot(self.xs[i][::plot_samle_interval], self.ys[i][::plot_samle_interval])

			# Same color as lines
			# ax1.scatter(self.xs[i][-1],self.ys[i][-1])


		# plot last positions, all blue
		last_xs = [x[-1] for x in self.xs]
		last_ys = [y[-1] for y in self.ys]

		ax1.scatter(last_xs,last_ys)
		ax1.axis('equal')


		print("Plotting {} datapoints".format(int(len(self.E_data)/plot_samle_interval)))

		ax2.plot(self.times[::plot_samle_interval], self.E_data[::plot_samle_interval])

		fig.tight_layout()
		plt.show()

	def show_system_3d(self, plot, plot_samle_interval):
		for i in range(self.n):
			# plot position history
			plot.plot(self.xs[i][::plot_samle_interval], self.ys[i][::plot_samle_interval], self.zs[i][::plot_samle_interval], linewidth=1, alpha=0.6)

			# Same color as lines
			plot.scatter(self.xs[i][-1],self.ys[i][-1], self.zs[i][-1], [0.3])

	def show_system_3d_multi(self, plot_samle_interval = 1):

		fig = plt.figure(figsize=(5.8, 3.0))

		ax = fig.add_subplot(121, autoscale_on=False, projection='3d')
		ax.set_xlim3d(-20, 20)
		ax.set_ylim3d(-20,20)
		ax.set_zlim3d(-20,20)

		ax.set_aspect('equal')
		ax.grid()

		self.show_system_3d(ax, plot_samle_interval)

		ax2 = fig.add_subplot(122, autoscale_on=False, projection='3d')
		ax2.set_xlim3d(-2, 2)
		ax2.set_ylim3d(-2,2)
		ax2.set_zlim3d(-2,2)

		ax2.set_aspect('equal')
		ax2.grid()
		self.show_system_3d(ax2, plot_samle_interval)

		plt.show()





if __name__ == "__main__":

	body_list = []
	body_list.append(body(1, [0, 1], [1, 0], [0, 0]))
	body_list.append(body(5, [0, 0], [-1/5, 0], [0, 0]))

	system = nbody_system(body_list)

	xs = [[],[]]
	ys = [[],[]]

	Edat = []

	for i in range(600):
		system.ruth3()
		xs[0].append(body_list[0].pos[0])
		ys[0].append(body_list[0].pos[1])
		xs[1].append(body_list[1].pos[0])
		ys[1].append(body_list[1].pos[1])

		Edat.append(system.total_energy())

	plt.plot(xs[0], ys[0])
	plt.plot(xs[1], ys[1])
	plt.scatter([xs[0][-1],xs[1][-1]],[ys[0][-1], ys[1][-1]])
	plt.axis('equal')
	plt.show()
	plt.plot(Edat)
	plt.show()