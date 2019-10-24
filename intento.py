import numpy as np

LX = 10
LY = 10

class Disk:

    def __init__(self, tag, x0, y0, v0x, v0y, mass, radius, color):
        self.TAG = tag
        self.COLOR = color
        self.MASS = mass
        self.RADIUS = radius

        self.x, self.y = x0, y0
        self.vx, self.vy = v0x, v0y

        self.disk_colls, self.wall_colls = 0, 0

    def get_state(self):
        return self.x, self.y, self.vx, self.vy, self.color

    def set_state(self, x, y, vx, vy):
        self.x, self.y, self.vx, self.vy = x, y, vx, vy

class System:

    def __init__(self, disks):
        self.time = 0
        self.minpq = [] #heapq
        self.particles = disks #Lista de discos

    # Animator

class Event:
    # disk_a, disk_b != None (Son dos discos)
    # disk_a = None, disk_b != None (Disco con muro vertical)
    # disk_a != None, disk_b = None (Disco con muro horizontal)
    def __init__(self, disk_a, disk_b):
        self.time = -1
        self.disk_a = disk_a
        self.disk_b = disk_b

    def calculate_time(self):
        Vij = [self.disk_a.vx - self.disk_b.vx , self.disk_a.vy - self.disk_b.vy]
        Rij = [self.disk_a.x - self.disk_b.x , self.disk_a.y - self.disk_b.y]
        Vij_Rij = Vij[0]*Rij[0] + Vij[1]*Rij[1]
        dij = (Vij_Rij)**2 - (np.sqrt(Vij[0]**2 + Vij[1]**2)**2)*(np.sqrt(Rij[0]**2 + Rij[1]**2)**2 - (self.disk_a.RADIUS + self.disk_b.RADIUS)**2)
        if self.disk_a != None and self.disk_b != None:  #DISCO CON DISCO
            if np.sqrt(Vij[0]**2 + Vij[1]**2) == 0:
                self.time = -1
                return self.time
            elif Vij_Rij > 0:
                self.time = -1
                return self.time
            elif dij < 0:
                self.time = -1
                return self.time
            else:
                self.time = -(Vij_Rij + np.sqrt(dij))/(np.sqrt(Vij[0]**2 + Vij[1]**2)**2)
                return self.time
