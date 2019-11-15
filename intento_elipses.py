import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation


fig = plt.figure()
fig.set_dpi(100)
fig.set_size_inches(7, 6.5)

ax = plt.axes(xlim=(0, 10), ylim=(0, 10))
ax.set_facecolor('k')
pos = ([ [1,2], [1,2] ],[ [1,2], [3,4] ])
patches = []
for i in range(len(pos)):
    color = np.random.random(3)
    color_t = tuple(color)
    patches.append(plt.Circle((5,5), 0.75))

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
                               interval=200,
                               blit=True)
                               
plt.show()
