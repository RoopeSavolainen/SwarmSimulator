from parameters import Parameters
from boid import Boid


class Simulation:

    boids = []
    params = None

    def __init__(self, params):
        if not isinstance(params, Parameters):
            raise Exception("Faulty Parameters object")
        else:
            self.params = params

        self.boids = []
        for i in range(params.boid_count):
            self.boids.append(Boid(0, 0, self.params))
