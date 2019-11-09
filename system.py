import disk as dk
import event as ev
import numpy as np
import animator
import heapq
import random

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
        for pair in self.events:
            evn = ev.Event(pair[0], pair[1])
            evn.calculate_time()
            if evn.time != np.inf:
                heapq.heappush(self.minpq, evn)

    def valid(self, evn):

        if evn.disk_a != None and evn.disk_b != None:
            if evn.TOTAL_COLLS == evn.disk_a.disk_colls + evn.disk_a.wall_colls + evn.disk_b.disk_colls + evn.disk_b.wall_colls:
                evn.valid = True
            else:
                evn.valid = False
        elif evn.disk_a == None and evn.disk_b != None:
            if evn.TOTAL_COLLS == evn.disk_b.disk_colls + evn.disk_b.wall_colls:
                evn.valid = True
            else:
                evn.valid = False
        else:
            if evn.TOTAL_COLLS == evn.disk_a.disk_colls + evn.disk_a.wall_colls:
                evn.valid = True
            else:
                evn.valif = False

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
            for disco in self.particles:
                if disco != evn.disk_a and disco != evn.disk_b:
                    ev1 = ev.Event(evn.disk_a, disco)
                    ev1.calculate_time()
                    ev1.time += self.time_sim

                    ev2 = ev.Event(evn.disk_b, disco)
                    ev2.calculate_time()
                    ev2.time += self.time_sim

                    if ev1.time != np.inf:
                        heapq.heappush(self.minpq, ev1)
                    if ev2.time != np.inf:
                        heapq.heappush(self.minpq, ev2)

            ev1_vert = ev.Event(None, evn.disk_a)
            ev1_vert.calculate_time()
            ev1_vert.time += self.time_sim

            ev1_horz = ev.Event(evn.disk_a, None)
            ev1_horz.calculate_time()
            ev1_horz.time += self.time_sim

            ev2_vert = ev.Event(None, evn.disk_b)
            ev2_vert.calculate_time()
            ev2_vert.time += self.time_sim

            ev2_horz = ev.Event(evn.disk_b, None)
            ev2_horz.calculate_time()
            ev2_horz.time += self.time_sim

            if ev1_vert.time != np.inf:
                heapq.heappush(self.minpq, ev1_vert)
            if ev1_horz.time != np.inf:
                heapq.heappush(self.minpq, ev1_horz)
            if ev2_vert.time != np.inf:
                heapq.heappush(self.minpq, ev2_vert)
            if ev2_horz.time != np.inf:
                heapq.heappush(self.minpq, ev2_horz)

        elif evn.disk_a == None and evn.disk_b != None: #DISCO CON MURO VERTICAL
            for disco in self.particles:
                if disco != evn.disk_b:
                    ev1 = ev.Event(evn.disk_b, disco)
                    ev1.calculate_time()
                    ev1.time += self.time_sim

                    if ev1.time != np.inf:
                        heapq.heappush(self.minpq, ev1)

            ev1_vert = ev.Event(None, evn.disk_b)
            ev1_vert.calculate_time()
            ev1_vert.time += self.time_sim

            ev1_horz = ev.Event(evn.disk_b, None)
            ev1_horz.calculate_time()
            ev1_horz.time += self.time_sim

            if ev1_vert.time != np.inf:
                heapq.heappush(self.minpq, ev1_vert)
            if ev1_horz.time != np.inf:
                heapq.heappush(self.minpq, ev1_horz)

        else: #DISCO CON MURO HORIZONTAL
            for disco in self.particles:
                if disco != evn.disk_a:
                    ev1 = ev.Event(evn.disk_a, disco)
                    ev1.calculate_time()
                    ev1.time += self.time_sim

                    if ev1.time != np.inf:
                        heapq.heappush(self.minpq, ev1)

            ev1_vert = ev.Event(None, evn.disk_a)
            ev1_vert.calculate_time()
            ev1_vert.time += self.time_sim

            ev1_horz = ev.Event(evn.disk_a, None)
            ev1_horz.calculate_time()
            ev1_horz.time += self.time_sim

            if ev1_vert.time != np.inf:
                heapq.heappush(self.minpq, ev1_vert)
            if ev1_horz.time != np.inf:
                heapq.heappush(self.minpq, ev1_horz)

    def fill_list(self):
        i = 0
        for disco in self.particles:
            x, y = disco.get_state()
            self.lista_grande[i][0].append(x)
            self.lista_grande[i][1].append(y)
            i += 1

    def move_particles(self, deltat):
        for disco in self.particles:
            disco.move(deltat)

    def main_loop(self):
        run = True
        self.fill_list()
        while(run):
            if len(self.minpq) == 0:
                break
            if self.time_sim >= self.TIME_MAX:
                break
            evn = heapq.heappop(self.minpq)
            self.valid(evn)
            if evn.time > self.time_sim and evn.valid:
                self.move_particles(evn.time - self.time_sim)
                self.time_sim = evn.time
                self.res_collision(evn)
                self.new_colls(evn)
                self.fill_list()

if __name__ == "__main__":

    def create_disks(n, sigma):
        list = []
        for i in range(n):
            x = random.uniform(sigma, LX - sigma)
            y = random.uniform(sigma, LY - sigma)
            vx = random.uniform(-5, 5)
            vy = random.uniform(-5, 5)
            list.append(dk.Disk(str(i), x, y, vx, vy))
        return list

    def check_overlap(list):
        for disco in list:
            aux = [x for x in list if x != disco]
            for disco2 in aux:
                Rij = [disco2.x - disco.x , disco2.y - disco.y]
                dist = np.sqrt(Rij[0]**2 + Rij[1]**2)
                if dist < disco.RADIUS + disco2.RADIUS:
                    print("Error con: ")
                    print(disco)
                    print(disco2)
                    return False
        return True

    def run(time, N, radius):
        pelotitas = create_disks(N, radius)
        if check_overlap(pelotitas):
            sistema = System(time, pelotitas)
            sistema.create_events(sistema.particles, [])
            sistema.build_binary_heap()
            sistema.main_loop()
            i = 0
            while i < len(sistema.lista_grande):
                sistema.lista_grande[i] = tuple(sistema.lista_grande[i])
                i += 1
            anime = animator.Animator(sistema.lista_grande)
            anime.setup_anime(10, 10, 25)
            anime.run_anime(inval = 300, rep = False)
        else:
            return run(time, N, radius)

    run(1000, 10, 0.5)
