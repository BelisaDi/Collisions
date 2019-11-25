import numpy as np
import matplotlib.pyplot as plt

free_path = [0.5368432035263764,
0.3869522150291964,
0.29786461403544084,
0.22939262181899067,
0.18871211769540178,
0.15390994043771467,
0.12831901158348666,
0.10710041995309928,
0.09327168315750799,
0.08119243247499497,
0.07082434281835434,
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
ax.plot(num_particles, free_path, 'o-')

ax.set(xlabel='Número de partículas', ylabel='Camino libre medio',
       title='Relación entre camino libre medio y densidad')
ax.grid()

plt.show()
