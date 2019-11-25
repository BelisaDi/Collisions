import numpy as np
import matplotlib.pyplot as plt

free_time = [0.139933818693439,
0.095442228988502,
0.073468020539357,
0.059336955261389,
0.045372225632173,
0.038341354479555,
0.031813278548385,
0.025830457414469,
0.022112497562373,
0.02002006057597,
0.017709371990366
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
ax.plot(num_particles, free_time, 'o-')

ax.set(xlabel='Número de partículas', ylabel='Tiempo libre medio',
       title='Relación entre tiempo libre medio y densidad')
ax.grid()

plt.show()
