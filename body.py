import numpy as np
import constants

class body:
	def __init__(self, GM, position, velocity, acceleration, name="body"):
		self.GM = GM
		self.mass = GM / constants.G
		self.pos = np.array(position, dtype=np.float64)
		self.vel = np.array(velocity, dtype=np.float64)
		self.acc = np.array(acceleration, dtype=np.float64)
		self.last_acc = np.array(acceleration, dtype=np.float64)
		self.name = name
		
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
