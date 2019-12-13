import sys
import numpy as np 
sys.path.insert(0, 'C:\\Users\\Isabella\\Documents\\Elementos de Física\\Collisions\\disk')
sys.path.insert(0, 'C:\\Users\\Isabella\\Documents\\Elementos de Física\\Collisions\\system')

import disk as dk
import system as sy

class Event:

    """
    Dado un par de discos (o un disco respecto al muro vertical y al muro horizontal) calcula el tiempo estimado
    en el que colisionan. La notación utilizada es la siguiente:
    disk_a, disk_b != None (Son dos discos)
    disk_a = None, disk_b != None (Disco con muro vertical)
    disk_a != None, disk_b = None (Disco con muro horizontal)
    """

    def __init__(self, disk_a, disk_b):
        self.time = np.inf
        self.disk_a = disk_a
        self.disk_b = disk_b
        self.valid = False
        if disk_a != None and disk_b != None:
            self.CLASS = 0
            self.TOTAL_COLLS = disk_a.disk_colls + disk_a.wall_colls + disk_b.disk_colls + disk_b.wall_colls
        elif disk_a == None and disk_b != None:
            self.CLASS = 1
            self.TOTAL_COLLS = disk_b.disk_colls + disk_b.wall_colls
        else:
            self.CLASS = 2
            self.TOTAL_COLLS = disk_a.disk_colls + disk_a.wall_colls

    def calculate_time(self):

        if self.disk_a != None and self.disk_b != None: #DISCO CON DISCO
            Vij = [self.disk_a.vx - self.disk_b.vx , self.disk_a.vy - self.disk_b.vy] #Vector Vi - Vj
            Rij = [self.disk_a.x - self.disk_b.x , self.disk_a.y - self.disk_b.y] #Vector Ri - Rj
            Vij_Rij = Vij[0]*Rij[0] + Vij[1]*Rij[1] #Producto punto
            dij = (Vij_Rij)**2 - (np.sqrt(Vij[0]**2 + Vij[1]**2)**2)*(np.sqrt(Rij[0]**2 + Rij[1]**2)**2 - (self.disk_a.RADIUS + self.disk_b.RADIUS)**2) #Determinante
            if np.sqrt(Vij[0]**2 + Vij[1]**2) == 0:
                self.time = np.inf
                return self.time
            elif Vij_Rij > 0:
                self.time = np.inf
                return self.time
            elif dij < 0:
                self.time = np.inf
                return self.time
            else:
                self.time = -(Vij_Rij + np.sqrt(dij))/(np.sqrt(Vij[0]**2 + Vij[1]**2)**2)
                return self.time

        elif self.disk_a == None and self.disk_b != None: #DISCO CON MURO VERTICAL
            if self.disk_b.vx < 0:
                self.time = (self.disk_b.RADIUS - self.disk_b.x)/(self.disk_b.vx)
                return self.time
            elif self.disk_b.vx > 0:
                self.time = (sy.LX - self.disk_b.RADIUS - self.disk_b.x)/(self.disk_b.vx)
                return self.time
            else:
                self.time = np.inf
                return self.time

        else: #DISCO CON MURO HORIZONTAL
            if self.disk_a.vy < 0:
                self.time = (self.disk_a.RADIUS - self.disk_a.y)/(self.disk_a.vy)
                return self.time
            elif self.disk_a.vy > 0:
                self.time = (sy.LY - self.disk_a.RADIUS - self.disk_a.y)/(self.disk_a.vy)
                return self.time
            else:
                self.time = np.inf
                return self.time

    def __lt__(self, other):
        return self.time < other.time

    def __str__(self):
        strng = "Evento entre: "
        if self.disk_a != None and self.disk_b != None:
            strng += self.disk_a.TAG + " y " + self.disk_b.TAG
        elif self.disk_a == None and self.disk_b != None:
            strng += self.disk_b.TAG + " y muro vertical"
        else:
            strng += self.disk_a.TAG + " y muro horizontal"
        strng += ", con tiempo: " + str(self.time) + " y colisiones totales: " + str(self.TOTAL_COLLS)
        return strng

    def get_velocities(self):
        if self.disk_a != None and self.disk_b != None:
            return [[self.disk_a.vx, self.disk_a.vy], [self.disk_b.vx, self.disk_b.vy]]
        elif self.disk_a == None and self.disk_b != None:
            return [[None, None], [self.disk_b.vx, self.disk_b.vy]]
        else:
            return [[self.disk_a.vx, self.disk_a.vy], [None, None]]

