from parameters import Parameters
from boid import Boid

from math import sqrt, floor
import statistics, random

class Simulation:

    boids = []
    params = None

    view_x = view_y = view_w = view_h = None

    def __init__(self, params):
        self.params = params
        self.reset()


    def reset(self):
        self.boids = []
        upper = self.params.boid_count * 10
        for i in range(self.params.boid_count):
            x = random.uniform(-upper, upper)
            y = random.uniform(-upper, upper)
            b = Boid(self.params, x, y)
            self.boids.append(b)

        self.update_viewport()


    def refresh(self, advance=False):
        if advance:
            n = floor(len(self.boids) / 4)
            for boid in self.boids:
                boid.update_self(self.get_neighbours(boid, n))
                boid.setPos(boid.pos().x() + boid.vx, boid.pos().y() + boid.vy)
            self.update_viewport()


    def stop_simulation(self):
        self.reset()


    # Returns a list containing a maximum of n nearest boids
    def get_neighbours(self, boid, n=None):
        
        if n == None:
            n = len(self.boids)

        x1 = boid.pos().x()
        y1 = boid.pos().y()

        # Stores distance:boid pairs
        neighbours = {}

        for b in self.boids:
            if b != boid:
                x2 = b.pos().x()
                y2 = b.pos().y()
                dist = sqrt((x1-x2)**2 + (y1-y2)**2)
                neighbours[dist] = b
        
        return [neighbours[i] for i in sorted(neighbours)][0:n]


    def update_viewport(self):
        x = [b.pos().x() for b in self.boids]
        y = [b.pos().y() for b in self.boids]
        
        x_mean = statistics.mean(x)
        y_mean = statistics.mean(y)
        x_dev = statistics.stdev(x)
        y_dev = statistics.stdev(y)

        self.view_x = x_mean - x_dev*4
        self.view_y = y_mean - y_dev*4
        self.view_w = x_dev * 6
        self.view_h = y_dev * 6

