import disk as dk
import numpy as np
import heapq

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
                self.time = (dk.LX - self.disk_b.RADIUS - self.disk_b.x)/(self.disk_b.vx)
                return self.time
            else:
                self.time = np.inf
                return self.time

        else: #DISCO CON MURO HORIZONTAL
            if self.disk_a.vy < 0:
                self.time = (self.disk_a.RADIUS - self.disk_a.y)/(self.disk_a.vy)
                return self.time
            elif self.disk_a.vy > 0:
                self.time = (dk.LY - self.disk_a.RADIUS - self.disk_a.y)/(self.disk_a.vy)
                return self.time
            else:
                self.time = np.inf
                return self.time

    def __lt__(self, ev):
        return self.time < ev.time

    def __str__(self):
        strng = "Evento entre: "
        if self.disk_a != None and self.disk_b != None:
            strng += self.disk_a.TAG
            strng += " y "
            strng += self.disk_b.TAG
        elif self.disk_a == None and self.disk_b != None:
            strng += self.disk_b.TAG
            strng += " y "
            strng += "muro vertical"
        else:
            strng += self.disk_a.TAG
            strng += " y "
            strng += "muro horizontal"
        strng += ", con tiempo: "
        strng += str(self.time)
        return strng

if __name__ == "__main__":
    ball = dk.Disk("pelotita", 5, 5, 10, 0, 1, 0.5, (255, 0 ,0))
    ball2 = dk.Disk("pelotita 2", 10, 5, -5, 0, 1, 0.5, (0, 255, 0))
    ball3 = dk.Disk("pelotita 3", 1, 3, 5, 2, 1, 0.5, (0, 0, 255))
    list = []
    ev1 = Event(ball, ball2)
    ev2 = Event(None, ball)
    print(ev1.calculate_time())
    print(ev2.calculate_time())
    heapq.heappush(list, ev1)
    heapq.heappush(list, ev2)
    print(list)
    for evento in list:
        print(evento)
