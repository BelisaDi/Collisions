import disk as dk
import event as ev
import numpy as np
import animator
import heapq

LX = 10
LY = 10

class System:

    """
    Representa al sistema de discos. La lista de discos es representada por su atributo particles.
    El atributo minpq es un min binary heap que guarda todos los tiempos de colisiones distintos a -1
    (infinito) de todas las interacciones posibles entre los discos y entre cada disco con el muro vertical
    y horizontal.

    """

    def __init__(self, time, disks):
        self.TIME_MAX = time
        self.time_sim = 0
        self.minpq = [] #heapq
        self.events = [] #lista con los eventos posibles
        self.particles = disks #Lista de discos
        self.lista_grande = []
        for disco in self.particles:
            self.lista_grande.append([[],[]])

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
        print("CONSTRUCCIÓN INICIAL DEL BINARY HEAP: ")
        for evento in self.events:
            evn = ev.Event(evento[0], evento[1])
            evn.calculate_time()
            print("EVENTO ACTUAL: ")
            print(evn)
            if evn.time != np.inf:
                heapq.heappush(self.minpq, evn)
            print("minpq: ")
            for i in self.minpq:
                print(i)
        print("---------------------------------------")

    def valid(self, evn):
        if evn.disk_a != None and evn.disk_b != None:
            if evn.TOTAL_COLLS == evn.disk_a.disk_colls + evn.disk_a.wall_colls + evn.disk_b.disk_colls + evn.disk_b.wall_colls:
                evn.valid = True
        elif evn.disk_a == None and evn.disk_b != None:
            if evn.TOTAL_COLLS == evn.disk_b.disk_colls + evn.disk_b.wall_colls:
                evn.valid = True
        else:
            if evn.TOTAL_COLLS == evn.disk_a.disk_colls + evn.disk_a.wall_colls:
                evn.valid = True

    def res_collision(self, evn):
        if evn.disk_a != None and evn.disk_b != None: #DISCO CON DISCO
            Vij = [evn.disk_a.vx - evn.disk_b.vx , evn.disk_a.vy - evn.disk_b.vy] #Vector Vi - Vj
            Vji = [evn.disk_b.vx - evn.disk_a.vx , evn.disk_b.vy - evn.disk_a.vy]
            Rij = [evn.disk_a.x - evn.disk_b.x , evn.disk_a.y - evn.disk_b.y] #Vector Ri - Rj
            Rji = [evn.disk_b.x - evn.disk_a.x , evn.disk_b.y - evn.disk_a.y]
            Vij_Rij = Vij[0]*Rij[0] + Vij[1]*Rij[1] #Producto punto
            Vji_Rji = Vji[0]*Rji[0] + Vji[1]*Rji[1]
            ci = (2*evn.disk_a.MASS)/(evn.disk_a.MASS + evn.disk_b.MASS)
            cj = (2*evn.disk_b.MASS)/(evn.disk_a.MASS + evn.disk_b.MASS)
            evn.disk_a.vx = (-(cj)/(evn.disk_a.RADIUS + evn.disk_b.RADIUS)**2)*Vij_Rij*Rij[0] + evn.disk_a.vx
            evn.disk_a.vy = (-(cj)/(evn.disk_a.RADIUS + evn.disk_b.RADIUS)**2)*Vij_Rij*Rij[1] + evn.disk_a.vy
            evn.disk_b.vx = (-(ci)/(evn.disk_a.RADIUS + evn.disk_b.RADIUS)**2)*Vji_Rji*Rji[0] + evn.disk_b.vx
            evn.disk_b.vy = (-(ci)/(evn.disk_a.RADIUS + evn.disk_b.RADIUS)**2)*Vji_Rji*Rji[1] + evn.disk_b.vy
            evn.disk_a.disk_colls += 1
            evn.disk_b.disk_colls += 1

        elif evn.disk_a == None and evn.disk_b != None: #DISCO CON MURO VERTICAL
             evn.disk_b.vx = -1*evn.disk_b.vx
             evn.disk_b.wall_colls += 1

        else: #DISCO CON MURO HORIZONTAL
            evn.disk_a.vy = -1*evn.disk_a.vy
            evn.disk_a.wall_colls += 1

    def new_colls(self, evn):
        if evn.disk_a != None and evn.disk_b != None:
            aux = [x for x in self.particles if x != evn.disk_a]
            for disco in aux:
                event_new = ev.Event(evn.disk_a, disco)
                event_new.calculate_time()
                event_new.time += self.time_sim
                if event_new.time != np.inf:
                    heapq.heappush(self.minpq, event_new)
            event_a_wall_1 = ev.Event(evn.disk_a, None)
            event_a_wall_2 = ev.Event(None, evn.disk_a)
            event_a_wall_1.calculate_time()
            event_a_wall_1.time += self.time_sim
            event_a_wall_2.calculate_time()
            event_a_wall_2.time += self.time_sim

            if event_a_wall_1.time != np.inf:
                heapq.heappush(self.minpq, event_a_wall_1)
            if event_a_wall_2.time != np.inf:
                heapq.heappush(self.minpq, event_a_wall_2)

            aux.remove(evn.disk_b)
            aux.append(evn.disk_a)
            for disco in aux:
                event_new = ev.Event(evn.disk_b, disco)
                event_new.calculate_time()
                event_new.time += self.time_sim
                if event_new.time != np.inf:
                    heapq.heappush(self.minpq, event_new)
            event_b_wall_1 = ev.Event(evn.disk_b, None)
            event_b_wall_2 = ev.Event(None, evn.disk_b)
            event_b_wall_1.calculate_time()
            event_b_wall_1.time += self.time_sim
            event_b_wall_2.calculate_time()
            event_b_wall_2.time += self.time_sim

            if event_b_wall_1.time != np.inf:
                heapq.heappush(self.minpq, event_b_wall_1)
            if event_b_wall_2.time != np.inf:
                heapq.heappush(self.minpq, event_b_wall_2)

        elif evn.disk_a == None and evn.disk_b != None: #DISCO CON MURO VERTICAL
             aux = [x for x in self.particles if x != evn.disk_b]
             for disco in aux:
                 event_new = ev.Event(evn.disk_b, disco)
                 event_new.calculate_time()
                 event_new.time += self.time_sim
                 if event_new.time != np.inf:
                     heapq.heappush(self.minpq, event_new)
             event_b_wall_1 = ev.Event(evn.disk_b, None)
             event_b_wall_2 = ev.Event(None, evn.disk_b)
             event_b_wall_1.calculate_time()
             event_b_wall_1.time += self.time_sim
             event_b_wall_2.calculate_time()
             event_b_wall_2.time += self.time_sim

             if event_b_wall_1.time != np.inf:
                heapq.heappush(self.minpq, event_b_wall_1)
             if event_b_wall_2.time != np.inf:
                heapq.heappush(self.minpq, event_b_wall_2)

        else: #DISCO CON MURO HORIZONTAL
            aux = [x for x in self.particles if x != evn.disk_a]
            for disco in aux:
                event_new = ev.Event(evn.disk_a, disco)
                event_new.calculate_time()
                event_new.time += self.time_sim
                if event_new.time != np.inf:
                    heapq.heappush(self.minpq, event_new)
            event_a_wall_1 = ev.Event(evn.disk_a, None)
            event_a_wall_2 = ev.Event(None, evn.disk_a)
            event_a_wall_1.calculate_time()
            event_a_wall_1.time += self.time_sim
            event_a_wall_2.calculate_time()
            event_a_wall_2.time += self.time_sim

            if event_a_wall_1.time != np.inf:
                heapq.heappush(self.minpq, event_a_wall_1)
            if event_a_wall_2.time != np.inf:
                heapq.heappush(self.minpq, event_a_wall_2)

    def fill_list(self):
        i = 0
        for disco in self.particles:
            x, y = disco.get_state()
            self.lista_grande[i][0].append(x)
            self.lista_grande[i][1].append(y)
            i += 1

    def main_loop_2(self):
        val = True
        self.fill_list()
        while(val):
            if len(self.minpq) == 0:
                val = False
            if self.time_sim >= self.TIME_MAX:
                val = False
            print("BINARY HEAP: ")
            for evento in self.minpq:
                print(evento)
            evn = heapq.heappop(self.minpq)
            self.valid(evn)
            if evn.time > self.time_sim and evn.valid:
                print("SUCEDIÓ ESTE EVENTO: ")
                print("OJO, LA SIMULACIÓN VA EN: ", self.time_sim)
                print(evn)
                print("POSICIONES ANTES: ")
                for disk in self.particles:
                    print(disk)
                for disk in self.particles:
                    disk.move(evn.time - self.time_sim)
                self.time_sim += evn.time
                self.res_collision(evn)
                self.new_colls(evn)
                self.fill_list()
                print("POSICIONES DESPUÉS: ")
                for disk in self.particles:
                    print(disk)
                print("----------------------------------------\n")


if __name__ == "__main__":
    ball = dk.Disk("pelotita", 5, 5, 2.314, 1.29, 1, 0.5, (255, 0 ,0))
    ball_2 = dk.Disk("pelotita 2", 1, 2, 0.8, -3.4, 1, 0.5, (255, 0, 0))
    sistema = System(20, [ball, ball_2])
    sistema.create_events(sistema.particles, [])
    sistema.build_binary_heap()
    for i in sistema.minpq:
        print(i)
    # sistema.main_loop_2()
    # i = 0
    # while i < len(sistema.lista_grande):
    #     sistema.lista_grande[i] = tuple(sistema.lista_grande[i])
    #     i += 1
    # for lista in sistema.lista_grande:
    #     print(lista)
    #     print("////////////////////////////////////////")
    # anime = animator.Animator(sistema.lista_grande)
    # anime.setup_anime()
    # anime.run_anime(inval = 1000, rep = True)
