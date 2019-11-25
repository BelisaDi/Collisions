class Disk:

    """
    Clase que representa un disco impenetrable.
    """

    def __init__(self, tag, x0 = 0, y0 = 0, v0x = 0, v0y = 0, mass = 1, radius = 0.5):
        self.TAG = tag
        self.MASS = mass
        self.RADIUS = radius

        self.x, self.y = x0, y0
        self.vx, self.vy = v0x, v0y

        self.disk_colls, self.wall_colls = 0, 0

    def __str__(self):
        strng = self.TAG + "\n"
        strng += "mass = {}\n".format(self.MASS)
        strng += "position = ({:.4f}, {:.4f})\n".format(self.x, self.y)
        strng += "velocity = ({:.4f}, {:.4f})\n".format(self.vx, self.vy)
        return strng

    def get_state(self):
        return self.x, self.y

    def move(self, deltat):
        self.x = self.x + self.vx*deltat
        self.y = self.y + self.vy*deltat