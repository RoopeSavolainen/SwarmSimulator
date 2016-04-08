from parameters import Parameters
from boid import Boid
from PyQt5.QtCore import pyqtSlot


class Simulation:

    boids = []
    params = None

    def __init__(self, params):
        self.params = params
        self.reset()

    def reset(self):
        self.boids = []
        for i in range(self.params.boid_count):
            self.boids.append(Boid(0, 0, self.params))


    def refresh(self):
        for boid in self.boids:
            boid.update_self()


    def stop_simulation(self):
        self.reset()


