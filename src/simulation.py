from parameters import Parameters
from boid import Boid
from PyQt5.QtCore import QTimer, pyqtSlot


class Simulation:

    boids = []
    params = None

    def __init__(self, params, canvas):
        self.params = params
        self.canvas = canvas

        self.timer = QTimer()
        self.timer.setInterval(1000/60)
        self.timer.timeout.connect(self.refresh_canvas)
        self.timer.start()

    def reset(self):
        self.running = False
        self.boids = []
        for i in range(params.boid_count):
            self.boids.append(Boid(0, 0, self.params))


    @pyqtSlot()
    def refresh_canvas(self):
        pass

    def reload_config(self, params):
        pass


    def start_simulation(self):
        self.running = True


    def pause_simulation(self):
        self.running = False


    def stop_simulation(self):
        self.reset()
        self.running = False
