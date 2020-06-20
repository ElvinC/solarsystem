
class jpl_loader:
	def __init__(self, id_list, start='2000-1-1', stop='2002-1-1',step='1d'):
		self.id_list = id_list

		self.data_list = []

		for jpl_id in id_list:

			body = Horizons(id=jpl_id, location='@ssb', epochs={'start':start, 'stop':stop, 'step':step}, id_type="majorbody")
			vecs = body.vectors()
			self.data_list.append(vecs)
			print(vecs[0])
			print(body.uri)


	def plot_orbits(self, plot):
		for vectors in self.data_list:
			# extract relevant values
			xs = vectors["x"]
			ys = vectors["y"]
			zs = vectors["z"]
			vxs = vectors["vx"]
			vys = vectors["vy"]
			vys = vectors["vz"]

			plot.plot(xs, ys, zs, lw=1.5)


id_list = [
	"Sun",
	"199", # Mercury
	"299", # Venus
	"Geocenter", # earth
	"499", # Mars
	"599", #jupiter
	"699", # Saturn
	"799", #Uranus
	"899", # Neptune
	"999", # Pluto
]

if __name__ == "__main__":
