import disk as dk
import event as ev
import numpy as np
import heapq

class System:

    """
    Representa al sistema de discos. La lista de discos es representada por su atributo particles.
    El atributo mainpq es un min binary heap que guarda todos los tiempos de colisiones distintos a -1
    (infinito) de todas las interacciones posibles entre los discos y entre cada disco con el muro vertical
    y horizontal.

    """

    def __init__(self, time, disks):
        self.TIME_MAX = time
        self.time_sim = 0
        self.minpq = [] #heapq
        self.events = [] #lista con los eventos posibles
        self.particles = disks #Lista de discos

    def create_events(self, list, list_pairs):
        if len(list) == 0:
            self.events = list_pairs
            return list_pairs
        else:
            i = list[0]
            list = list[1:]
            if len(list) != 0:
                for j in list:
                    list_pairs.append([i,j])
                    list_pairs.append([None, i])
                    list_pairs.append([i, None])
            else:
                list_pairs.append([None, i])
                list_pairs.append([i, None])
            return self.create_events(list, list_pairs)

    def build_binary_heap(self):
        for evento in self.events:
            evn = ev.Event(evento[0], evento[1])
            evn.calculate_time()
            if evn.time != np.inf:
                heapq.heappush(self.minpq, evn)

    # def main_loop(self):
    #     while len(self.minpq) != 0 or self.time_sim >= self.TIME_MAX:
    #         evn = heapq.heappop(self.minpq)
    #             if evn.time > self.time_sim:
    #                 for disk in self.particles:
    #                     disk.move(evn.time)
    #                 if evn.disk_a != None and evn.disk_b != None:



if __name__ == "__main__":
    ball = dk.Disk("pelotita", 5, 5, 10, 0, 1, 0.5, (255, 0 ,0))
    ball2 = dk.Disk("pelotita 2", 10, 5, -5, 0, 1, 0.5, (0, 255, 0))
    ball3 = dk.Disk("pelotita 3", 1, 3, 5, 2, 1, 0.5, (0, 0, 255))
    sistema = System(100, [ball, ball2, ball3])
    sistema.create_events(sistema.particles, [])
    sistema.build_binary_heap()
    print(sistema.minpq)
    for evento in sistema.minpq:
        print(evento)
