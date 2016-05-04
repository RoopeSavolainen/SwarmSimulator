from parameters import Parameters
from boid import Boid
from PyQt5.QtCore import pyqtSlot

from math import sqrt, floor

class Simulation:

    boids = []
    params = None

    def __init__(self, params):
        self.params = params
        self.reset()

    def reset(self):
        self.boids = []
        col = floor(sqrt(self.params.boid_count))
        for i in range(self.params.boid_count):
            x = i % col
            y = i // col
            self.boids.append(Boid(x*20, y*20, self.params))


    def refresh(self):
        for boid in self.boids:
            boid.update_self(self.get_neighbours(boid))


    def stop_simulation(self):
        self.reset()


    # Returns a list containing a maximum of n nearest boids
    def get_neighbours(self, boid, n=10):
        x1 = boid.x
        y1 = boid.y

        # Stores distance:boid pairs
        neighbours = {}

        for b in self.boids:
            if b != boid:
                x2 = b.x
                y2 = b.y
                dist = sqrt((x1-x2)**2 + (y1-y2)**2)
                neighbours[dist] = b
        
        return [neighbours[i] for i in sorted(neighbours)][0:n]
