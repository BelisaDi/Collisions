import disk as dk
import system as sy
import event as ev
import random
import numpy as np

#Esto es una prueba!

def generar_discos(n, radio):
	print("Vamos a generar discos!")
	list = []
	i = 0
	while i < n:
		x = random.uniform(radio, sy.LX - radio)
		y = random.uniform(radio, sy.LY - radio)
		vx = random.uniform(-5, 5)
		vy = random.uniform(-5, 5)
		disco = dk.Disk(str(i), x, y, vx, vy, 1, radio)
		print("Generé este disco: ")
		print(disco)
		if len(list) != 0:
			for disco2 in list:
				print(disco2)
				Rij = [disco2.x - disco.x, disco2.y - disco.y]
				dist = np.sqrt(Rij[0]**2 + Rij[1]**2)
				print(dist)
				if dist < disco.RADIUS + disco2.RADIUS:
					print("Error con: ")
					print(disco2)
					break
			print("Disco generado!")
			list.append(disco)
			i += 1

		else:
			print("No hay discos para comparar...")
			list.append(disco)
			i += 1
	return list

prueba_2 = generar_discos(5, 1)
print("/////////////////////////////////")
for disco in prueba_2:
	print(disco)
print("/////////////////////////////////")