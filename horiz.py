from astroquery.jplhorizons import Horizons
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#obj = Horizons(id='599', location='@ssb', epochs={'start':'2018-1-01', 'stop':'2019-12-09', 'step':'20d'}, id_type="majorbody")

obj = Horizons(id='301', location='@ssb', epochs={'start':'2019-1-01', 'stop':'2019-12-09', 'step':'1d'}, id_type="majorbody")

earth = Horizons(id='399', location='@ssb', epochs={'start':'2019-1-01', 'stop':'2019-12-09', 'step':'1d'}, id_type="majorbody")


vectors = obj.vectors()

xpos = vectors["x"]
ypos = vectors["y"]
zpos = vectors["z"]

print(vectors[0])

print([[xpos[i], ypos[i]] for i in range(len(xpos))])

plt.plot(xpos, ypos)


vectors = earth.vectors()

xpos = vectors["x"]
ypos = vectors["y"]
zpos = vectors["z"]
plt.plot(xpos, ypos)
plt.axis('equal')
plt.show()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.plot(xpos, ypos, zpos)
ax.scatter([0], [0], [0])

ax.set_xlim3d(-1.5, 1.5)
ax.set_ylim3d(-1.5,1.5)
ax.set_zlim3d(-1.5,1.5)

ax.set_aspect('equal')
plt.show()

