import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

fig = plt.figure()
fig.set_dpi(100)
fig.set_size_inches(7, 6.5)

ax = plt.axes(xlim=(0, 10), ylim=(0, 10))
patch = plt.Circle((5, -5), 0.75, fc='y')
patch2 = plt.Circle((4,6), 0.75, fc = 'c')

def init():
    patch.center = (5, 5)
    patch2.center = (4,6)
    ax.add_patch(patch)
    ax.add_patch(patch2)
    a = (patch, patch2)
    return a

def animate(i):
    x, y = patch.center
    x2, y2 = patch2.center
    x = 5 + 3 * np.sin(np.radians(i))
    y = 5 + 3 * np.cos(np.radians(i))
    x2 = 1 + 3 * np.sin(np.radians(i))
    y2 = 2 + 3 * np.cos(np.radians(i))
    patch.center = (x,y)
    patch2.center = (x2, y2)
    a = (patch, patch2)
    return a

anim = animation.FuncAnimation(fig, animate,
                               init_func=init,
                               frames=360,
                               interval=20,
                               blit=True)

plt.show()
