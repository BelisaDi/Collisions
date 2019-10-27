import disk as dk
import event as ev
import heapq

class System:

    """
    Representa al sistema de discos. La lista de discos es representada por su atributo particles.
    El atributo mainpq es un min binary heap que guarda todos los tiempos de colisiones distintos a -1
    (infinito) de todas las interacciones posibles entre los discos y entre cada disco con el muro vertical
    y horizontal.

    """

    def __init__(self, time, disks):
        self.time = time
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
            tim = evn.calculate_time()
            if tim != -1:
                self.minpq.append(tim)
        heapq.heapify(self.minpq)
