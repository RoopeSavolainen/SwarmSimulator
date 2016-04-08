from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtGui import QPainter, QBrush
from PyQt5.QtCore import QRectF, Qt

import random


class Boid(QGraphicsItem):

    # Position
    x = None
    y = None

    # Velocity
    vx = None
    vy = None

    # Acceleration
    ax = None
    ay = None

    parameters = None


    def __init__(self, x, y, parameters):
        self.x = x
        self.y = y

        super(Boid, self).__init__()

        self.vx = random.randint(-5,5)
        self.vy = random.randint(-5,5)

        self.ax = 0
        self.ay = 0

        self.parameters = parameters

    
    def paint(self, painter, options, widget):
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawEllipse(self.x, self.y, 10, 10)


    def boundingRect(self):
        return QRectF(self.x-5, self.y-5, 10, 10)
    

    def update_self(self):
        self.x += self.vx
        self.y += self.vy


    def calculate_acceleration():
        pass


    def calculate_cohesion_preference():
        pass


    def calculate_separation_preference():
        pass


    def calculate_alignment_preference():
        pass


