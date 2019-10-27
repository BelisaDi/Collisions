import disk as dk
import system as sy
import event as ev

ball = dk.Disk("pelotita", 5, 5, 10, 0, 1, 0.5, (255, 0 ,0))
ball2 = dk.Disk("pelotita 2", 10, 5, -5, 0, 1, 0.5, (0, 255, 0))
ball3 = dk.Disk("pelotita 3", 1, 3, 5, 2, 1, 0.5, (0, 0, 255))
sistema = sy.System(100, [ball, ball2, ball3])
sistema.create_events(sistema.particles, [])
sistema.build_binary_heap()
print(sistema.minpq)
