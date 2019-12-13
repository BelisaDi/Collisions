import sys
import random
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from datetime import datetime 
sys.path.insert(
	0, 'C:\\Users\\Isabella\\Documents\\Elementos de Física\\Collisions\\disk')
sys.path.insert(
	0, 'C:\\Users\\Isabella\\Documents\\Elementos de Física\\Collisions\\system')

import disk as dk
import system as sy


def run(time, n, radio):
	startTime = datetime.now()
	list = []
	for i in range(n):
		list.append(dk.Disk(str(i), radius = radio))

	sistema = sy.System(time, list)
	sistema.set_random_velocities()

    #La multiplicación de nxm debe dar el número de particulas.

	sistema.set_rect_red(10,10)
	sistema.create_events(sistema.particles, [])
	sistema.build_binary_heap()
	sistema.main_loop()
	tiempos = []
	for i in range(len(sistema.momentos_x)):
		tiempos.append(i)
	print (datetime.now() - startTime)

	pos = sistema.lista_grande

##############################################

	fig2, ax2 = plt.subplots()
	ax2.plot(tiempos, sistema.momentos_x)

	ax2.set(xlabel='Evento', ylabel='Momentum',
	       title='Conservación de Momentum Lineal')
	ax2.grid()

################################################

	fig = plt.figure()

	ax = plt.axes(xlim=(0, sy.LX), ylim=(0, sy.LY))
	ax.set_facecolor('k')
	ax.set(xlabel='x', ylabel='y',
				title=str(n)+" Partículas")
	ax.set_aspect('equal')

	patches = []
	for i in range(len(pos)):
	    x, y, z = random.uniform(0, 1), random.uniform(0, 1), random.uniform(0.5, 1)
	    color_t = (x,y,z)
	    patches.append(plt.Circle((5,5), radio, color = color_t))

	def init():
	    for i in range(len(patches)):
	        x0 = pos[i][0][0]
	        y0 = pos[i][1][0]
	        patches[i].center = (x0, y0)
	        ax.add_patch(patches[i])
	    a = tuple(patches)
	    return a

	def animate(i):
	    j = 0
	    for patch in patches:
	        x, y = patch.center
	        x = pos[j][0][i]
	        y = pos[j][1][i]
	        patch.center = (x,y)
	        j += 1
	    a = tuple(patches)
	    return a

	anim = animation.FuncAnimation(fig, animate,
	                               init_func=init,
	                               frames=len(pos[0][0]),
	                               interval=20,
	                               blit=True)
	plt.show()

run(100, 100, 0.5)