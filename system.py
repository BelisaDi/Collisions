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
        for pair in self.events:
            evn = ev.Event(pair[0], pair[1])
            evn.calculate_time()
            if evn.time != np.inf:
                heapq.heappush(self.minpq, evn)

    def valid(self, evn):
        print("\n")
        print("Vamos a revisar el evento...")
        if evn.disk_a != None and evn.disk_b != None:
            print("Son dos discos!")
            print("Colisiones reales: ", evn.disk_a.disk_colls + evn.disk_a.wall_colls + evn.disk_b.disk_colls + evn.disk_b.wall_colls)
            if evn.TOTAL_COLLS == evn.disk_a.disk_colls + evn.disk_a.wall_colls + evn.disk_b.disk_colls + evn.disk_b.wall_colls:
                evn.valid = True
                print("Es valido!")
            else:
                print("No es valido!")
        elif evn.disk_a == None and evn.disk_b != None:
            print("Es un disco con un muro vertical!")
            print("Colisiones reales: ", evn.disk_b.disk_colls + evn.disk_b.wall_colls)
            if evn.TOTAL_COLLS == evn.disk_b.disk_colls + evn.disk_b.wall_colls:
                evn.valid = True
                print("Es valido!")
            else:
                print("No es valido!")
        else:
            print("Es un disco con un muro horizontal!")
            print("Colisiones reales: ", evn.disk_a.disk_colls + evn.disk_a.wall_colls)
            if evn.TOTAL_COLLS == evn.disk_a.disk_colls + evn.disk_a.wall_colls:
                evn.valid = True
                print("Es valido!")
            else:
                print("No es valido!")

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
            print("BINARY HEAP: ")
            for evento in self.minpq:
                print(evento)
            print("\n")
            evn = heapq.heappop(self.minpq)
            print("PRIMER EVENTO DE LA COLA: ")
            print(evn)
            self.valid(evn)
            print("\n")
            if evn.time > self.time_sim and evn.valid:
                print("SUCEDIÓ ESTE EVENTO: ")
                print("OJO, LA SIMULACIÓN VA EN: ", self.time_sim)
                print(evn)
                print("\n")

                print("POSICIONES ANTES: ")
                for disk in self.particles:
                    print(disk)

                self.move_particles(evn.time - self.time_sim)
                print("MOVÍ LAS PARTICULAS UN DELTA DE: ", evn.time - self.time_sim, "\n")

                self.time_sim = evn.time
                self.res_collision(evn)

                print("POSICIONES DESPUÉS: ")
                for disk in self.particles:
                    print(disk)
                print("\n")

                self.new_colls(evn)
                self.fill_list()

                print("AHORA LA SIMULACIÓN VA EN: ", self.time_sim)
                print("----------------------------------------\n")


if __name__ == "__main__":
    ball = dk.Disk("pelotita", 5, 5, 0.125, 5.127, 1, 0.5, (255, 0 ,0))
    ball2 = dk.Disk("pelotita 2", 1, 2, -2.406, -3.4549, 1, 0.5, (255, 0, 0))
    ball3 = dk.Disk("pelotita 3", 7, 8, 2.6755, 3.6581, 1, 0.5, (255, 0, 0))
    sistema = System(10, [ball, ball2, ball3])
    sistema.create_events(sistema.particles, [])
    sistema.build_binary_heap()
    sistema.main_loop()
    i = 0
    while i < len(sistema.lista_grande):
        sistema.lista_grande[i] = tuple(sistema.lista_grande[i])
        i += 1
    anime = animator.Animator(sistema.lista_grande)
    anime.setup_anime()
    anime.run_anime(inval = 1000, rep = True)
