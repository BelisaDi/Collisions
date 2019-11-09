"""Animation of the trajectories of artists using matplotlib.

The Animator class takes a tuple of pairs, each pair corresponds to an
artist. Each pair (artist) contains the trajectory, as a list, in the
x and y directions, respectively. Both lists are parametrized using the
same variable (typically time).

The trajectory followed by the artists is assumed to be in two spatial
dimensions.

With this tuple of tuples the class is capable of showing an animation
of all of the artists in a frame set using matplotlib's pyplot. This
class is very useful when animating physical systems such as planets,
balls, charges, etc. Specially if you do not want to worry about little
details like axes, titles, labels, etc.

For more details on how to use matplotlib to do animations, visit
https://matplotlib.org/api/animation_api.html

Classes
-------
Animator : Sets, runs or saves animations of a tuple of artists.
"""


import matplotlib.pyplot as plt
import matplotlib.animation as animation


class Animator:
    """Set, run or save animations of artists given their trajectories.

    Attributes
    ----------
    artists : tuple of pairs
        Time step of the integration. It does not only mean time, it is
        just the independent variable of the differential equation.
    art_num : int
        Number of artists. It is the len(self.artists).
    fig : matplotlib.figure.Figure
        Figure that will frame the animation.
    ax : matplotlib.axes._subplots.AxesSubplot
        Axes related to self.fig.
    lines : list of matplotlib.lines.Line2D
        Trajectories or lines to be drawn, one for each artist.
    points : list of matplotlib.lines.Line2D
        The beginning of the trajectory of each artist is represented
        with a point in the Figure. Each pair of lists contains only
        one data in each list.
    time_template : str
        Template that saves the current time of the simulation. It is
        passed over to self.time_text so it can be printed in the
        Figure. It specifies the format in which the time will be printed.
    time_text : matplotlib.text.Text
        Text that will show the current time of the simulation in the
        Figure using the information provided by self.time_template.
    """

    def __init__(self, objs):  # file=None
        """Construct an Animator instance given a tuple of artists.

        objs - tuple of pairs to be drawn (artists trajectories).
        """
        self.artists = objs
        self.art_num = len(objs)
        self.fig = self.ax = None
        self.lines, self.points = [], []
        self.time_template = self.time_text = None

    def setup_anime(self, xmin_off=0, ymin_off=0, xmax_off=0, ymax_off=0):
        """Set up the animation.

        xmin_off - offset for the xmin limit calculated below.
        ymin_off - offset for the ymin limit calculated below.
        xmax_off - offset for the xmax limit calculated below.
        ymax_off - offset for the ymax limit calculated below.

        First, it finds out the limits of the Figure, setting up the
        figure, axes, background color of plot, etc.

        Second, sets up the color for the trajectory of each artist and
        appends the plot line to self.lines. Then, something similar is
        done for self.points.

        Finally, the time_template is defined and the text that will
        print the current time is set.
        """
        xmin = 0
        ymin = 0
        xmax = 10
        ymax = 10

        self.fig = plt.figure()
        self.ax = plt.axes(xlim=(xmin, xmax), ylim=(ymin, ymax),
                           autoscale_on=False)
        self.ax.set_facecolor('k')
        self.ax.set(xlabel='x', ylabel='y',
                    title='Intento 1')
        self.ax.set_aspect('equal')
        self.ax.grid()

        plt.gca().set_prop_cycle(None)

        for a in range(self.art_num):
            pt, = self.ax.plot([], [], 'o', markersize = 25)
            pt.set_clip_on(False)
            self.points.append(pt)

    def init_anime(self):
        """Initialize animation, used to draw a clear frame.

        It will be passed over to the parameter init_func defined in
        matplotlib.animation.FuncAnimation.
        """
        for a in range(self.art_num):
            self.points[a].set_data([], [])
        return self.points

    def animate(self, idx):
        """Initialize animation, used to draw a clear frame.

        idx - argument will be the next value in frames.

        It will be passed over as the function to call at each frame
        defined as func in matplotlib.animation.FuncAnimation.
        """
        for a in range(self.art_num):
            if idx < len(self.artists[a][0]):
                xc, yc = self.artists[a][0][idx], self.artists[a][1][idx]
                self.points[a].set_data(xc, yc)
        return self.points

    def run_anime(self, inval=10, rep=True, blitit=False):
        """Invoke matplotlib.animation.FuncAnimation and display animation.

        inval - delay between frames in milliseconds (default 200).
        rep - whether to repeat the animation in repeated (default True).
        blitit - controls whether blitting is used to optimize drawing
            (default False).
        """
        ani = animation.FuncAnimation(self.fig, self.animate,
                                      len(self.artists[0][0]), repeat=rep,
                                      interval=inval, blit=blitit,
                                      init_func=self.init_anime)
        plt.show()

    def save_anime(self, filename, inval=10, rep=True, blitit=False):
        """Invoke matplotlib.animation.FuncAnimation and save animation.

        inval - delay between frames in milliseconds (default 200).
        rep - whether to repeat the animation in repeated (default True).
        blitit - controls whether blitting is used to optimize drawing
            (default False).

        Notice that the animation is saved using imagemagick; however,
        other writers can be used. Available writers can be found calling
        animation.writers.list().
        """
        print(animation.writers.list())
        ani = animation.FuncAnimation(self.fig, self.animate,
                                      len(self.artists[0][0]), repeat=rep,
                                      interval=inval, blit=blitit,
                                      init_func=self.init_anime)
        ani.save(filename, writer='imagemagick', fps=inval)


if __name__ == "__main__":
    anime = Animator((([5,9.5,5.92,0.5,9.5], [5,7.5,9.5,6.47,1.45]),))
    #anime = Animator((([2],[2]),))
    anime.setup_anime()
    anime.run_anime(inval=1000, rep=False)
