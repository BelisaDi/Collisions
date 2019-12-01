import numpy as np
import matplotlib.pyplot as plt

pressure = [0.039515175132574,
0.054739703376101,
0.067877832583021,
0.071682545226674,
0.088096596866131,
0.093095851931048,
0.108443307107272,
0.111169206019357,
0.117254462227126,
0.136609898735556,
0.148503580599711
]

num_particles=[50,
60,
70,
80,
90,
100,
110,
120,
130,
140,
150
]

fig, ax = plt.subplots()
ax.plot(num_particles, pressure, 'o-')

ax.set(xlabel='Número de partículas', ylabel='Presión',
       title='Relación entre presión y densidad')
ax.grid()

plt.show()
