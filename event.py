import disk as dk
import system as sy
import numpy as np

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
            self.TOTAL_COLLS = disk_a.disk_colls + disk_a.wall_colls + disk_b.disk_colls + disk_b.wall_colls
        elif disk_a == None and disk_b != None:
            self.TOTAL_COLLS = disk_b.disk_colls + disk_b.wall_colls
        else:
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

if __name__ == "__main__":
    ball = dk.Disk("pelotita", 5, 5, 2.314, 1.29, 1, 0.5, (255, 0 ,0))
    ball2 = dk.Disk("pelotita 2", 1, 2, 0.8, -3.4, 1, 0.5, (255, 0, 0))
    list = []
    ev1 = Event(ball, ball2)
    ev2 = Event(None, ball)
    ev3 = Event(ball, None)
    ev4 = Event(None, ball2)
    ev5 = Event(ball2, None)
    print(ev1.calculate_time())
    print(ev2.calculate_time())
    print(ev3.calculate_time())
    print(ev4.calculate_time())
    print(ev5.calculate_time())
    list.append(ev1)
    list.append(ev2)
    list.append(ev3)
    list.append(ev4)
    list.append(ev5)
    heapq.heapify(list)
    # if ev1.time != np.inf:
    #     heapq.heappush(list, ev1)
    # if ev2.time != np.inf:
    #     heapq.heappush(list, ev2)
    # if ev3.time != np.inf:
    #     heapq.heappush(list, ev3)
    # if ev4.time != np.inf:
    #     heapq.heappush(list, ev4)
    # if ev5.time != np.inf:
    #     heapq.heappush(list, ev5)
    for evento in list:
        print(evento)
