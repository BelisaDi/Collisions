import sys
import heapq
import random
import numpy as np 
sys.path.insert(0, 'C:\\Users\\Isabella\\Documents\\Elementos de Física\\Collisions\\disk')
sys.path.insert(0, 'C:\\Users\\Isabella\\Documents\\Elementos de Física\\Collisions\\event')

import disk as dk
import event as ev

"""
DEFINA EL TAMAÑO DEL CONTENEDOR.
"""

LX = 100
LY = 100

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

        self.minpq = []
        self.events = []
        self.particles = disks
        self.lista_grande = []
        self.N = len(disks)
        for disco in self.particles:
            self.lista_grande.append([[],[]])

        self.momentos_x = []
        self.momentos_y = []
        self.temperaturas = []
        self.pressures = []
        self.cumulative_pressure = 0
        self.free_time = []
        self.free_time_val = 0
        self.res_mean_vel_2 = []
        self.l1 = 0
        self.l2 = 0

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

    def initialize(self):
        self.set_random_velocities()
        self.set_random_positions()

    def set_random_velocities(self):
        for disco in self.particles:
            disco.vx = random.uniform(-5, 5)
            disco.vy = random.uniform(-5, 5)

    def set_velocities(self, in_kinetic):
        vxSum = 0
        vySum = 0
        for disco in self.particles:
            disco.vx = np.random.random() - 0.5
            disco.vy = np.random.random() - 0.5
            vxSum += disco.vx
            vySum += disco.vy
        vxCM = vxSum / len(self.particles)
        vyCM = vySum / len(self.partciles)
        for disco in self.particles:
            disco.vx -= vxCM
            disco.vy -= vyCM
        v2Sum = 0
        for disco in self.particles:
            v2Sum += disco.vx**2 + disco.vy**2
        k_energy_per_particle = (0.5) * v2Sum / len(self.particles)
        rescale = np.sqrt(in_kinetic / k_energy_per_particle)
        for disco in self.particles:
            disco.vx *= rescale
            disco.vy *= rescale

    def set_random_positions(self):
        self.particles[0].x = LX/2
        self.particles[0].y = LY/2

        for idx, idish in enumerate(self.particles[1:], start = 1):
            irad, overlap = idish.RADIUS, True

            while overlap:
                jdx, overlap = 0, False
                dicex = (LX - 2.0 * irad) * np.random.random() + irad
                dicey = (LY - 2.0 * irad) * np.random.random() + irad
                tmp_pos = np.array([dicex, dicey])

                while jdx < idx and not overlap:
                    jdish = self.particles[jdx]
                    otro = np.array([jdish.x, jdish.y])
                    metric = np.linalg.norm(tmp_pos - otro)

                    if metric <= irad + jdish.RADIUS:
                        overlap = True
                    jdx += 1
                idish.x, idish.y = tmp_pos[0], tmp_pos[1]

    """
    Para la red rectangular:
    -n es el número de discos por fila, es decir, el número de columnas.
    -m es el número de discos por columnas, es decir, el número de filas.
    """

    def set_rect_red(self, n, m):
        step_x = LX/n
        step_y = LY/m
        center = (step_x/2, step_y/2)
        if center[0] < self.particles[0].RADIUS or center[1] < self.particles[0].RADIUS:
            print("No puedo hacer la malla! #Falta corregir este caso")
            return
        else:
            k = 0
            for i in range(n):
                for j in range(m):
                    self.particles[k].x = center[0] + ((i) * step_x)
                    self.particles[k].y = center[1] + ((j) * step_y)
                    k += 1
        for disco in self.particles:
            print(disco)

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

    def momentum(self):
        Sum = np.array([0., 0.])
        for disco in self.particles:
            m = disco.MASS
            v = np.array([disco.vx, disco.vy])
            Sum += m*v
        return Sum / len(self.particles)

    def momentum_2part(self, evn):
        if evn.disk_a != None and evn.disk_b != None:
            va = np.array([evn.disk_a.vx, evn.disk_a.vy])
            vb = np.array([evn.disk_b.vx, evn.disk_b.vy])
            return (evn.disk_a.MASS * va + evn.disk_b.MASS * vb)
        elif evn.disk_a == None and evn.disk_b != None:
            vb = np.array([evn.disk_b.vx, evn.disk_b.vy])
            return evn.disk_b.MASS * vb
        else:
            va = np.array([evn.disk_a.vx, evn.disk_a.vy])
            return evn.disk_a.MASS * va

    """
    La temperatura se maneja en kB por T.
    """
    def temperatura(self):
        Sum = 0
        for disco in self.particles:
            v = disco.vx**2 + disco.vy**2
            Sum += (disco.MASS/2)*v
        return Sum / len(self.particles)

    def cum_pre(self, evn, vel_bef):
        vi_p = np.array([evn.disk_a.vx, evn.disk_a.vy])
        vj_p = np.array([evn.disk_b.vx, evn.disk_b.vy])
        vi = np.array(vel_bef[0])
        vj = np.array(vel_bef[1])
        delta_v = vi_p - vi - (vj_p - vj)
        rij = np.array([evn.disk_a.x - evn.disk_b.x , evn.disk_a.y - evn.disk_b.y])
        self.cumulative_pressure += (evn.disk_a.MASS/2) * np.dot(delta_v, rij)

    def free_t(self):
        sum = 0
        for disco in self.particles:
            sum += disco.wall_colls + disco.disk_colls
        res = self.time_sim / sum
        self.free_time.append(res)
        #print(res)

    def mean_vel_2(self):
        sum = 0
        for disco in self.particles:
            v = np.array([disco.vx, disco.vy])
            sum += np.dot(v,v)
        res = sum / self.N
        self.res_mean_vel_2.append(res)
        #print(res)

    def main_loop(self):
        run = True
        self.fill_list()

        mtum = self.momentum()
        self.momentos_x.append(mtum[0])
        self.momentos_y.append(mtum[1])
        self.temperaturas.append(self.temperatura())

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
                vel_before = evn.get_velocities()
                self.res_collision(evn)
                self.free_t()

                self.mean_vel_2()
                if evn.CLASS == 0:
                    self.cum_pre(evn, vel_before)
                    
                self.new_colls(evn)
                self.fill_list()

                mtum = self.momentum()
                self.momentos_x.append(mtum[0])
                self.momentos_y.append(mtum[1])
                temp = self.temperatura()
                print(temp)
                self.temperaturas.append(temp)
                if evn.CLASS == 0:
                    p = (len(self.particles)*temp/(LX*LY)) + (self.cumulative_pressure/(LX*LY*self.time_sim))
                    self.pressures.append(p)

        self.free_time_val = self.free_time[-1]
        #self.l1 = self.free_time_val * np.sqrt(sum(self.res_mean_vel_2) / self.time_sim)
        self.l2 = self.free_time_val * np.sqrt(self.res_mean_vel_2[-1])
