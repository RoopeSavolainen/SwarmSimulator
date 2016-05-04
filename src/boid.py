from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtGui import QPainter, QBrush
from PyQt5.QtCore import QRectF, Qt

import random, math


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

    max_speed = 5
    max_accel = 5

    def __init__(self, x, y, parameters):
        self.x = x
        self.y = y

        super(Boid, self).__init__()

        self.vx = random.randint(-5,5)
        self.vy = random.randint(-5,5)

        self.ax = 0
        self.ay = 0

        self.parameters = parameters

    # paint() and boundingRect() are QGraphicsItem methods

    def paint(self, painter, options, widget):
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawEllipse(self.x, self.y, 10, 10)


    def boundingRect(self):
        return QRectF(self.x-5, self.y-5, 10, 10)
    

    def update_self(self, neighbours):
        self.ax, self.ay = self.calculate_acceleration(neighbours)
        self.vx += self.ax
        self.vy += self.ay
        self.vx, self.vy = truncate_vector(self.vx, self.vy, self.max_speed)
        self.x += self.vx
        self.y += self.vy


    def calculate_acceleration(self, neighbours):
        ax_c, ay_c = self.calculate_cohesion_preference(neighbours)
        ax_c *= self.parameters.weight_cohesion
        ay_c *= self.parameters.weight_cohesion

        ax_s, ay_s = self.calculate_separation_preference(neighbours)
        ax_s *= self.parameters.weight_separation
        ay_s *= self.parameters.weight_separation
        
        ax_a, ay_a = self.calculate_alignment_preference(neighbours)
        ax_a *= self.parameters.weight_alignment
        ay_a *= self.parameters.weight_alignment
        
        sum_weights = self.parameters.weight_cohesion + self.parameters.weight_separation + self.parameters.weight_alignment
        return truncate_vector((ax_c + ax_s + ax_a)/sum_weights, (ay_c + ay_s + ay_a)/sum_weights, self.max_accel)


    def calculate_cohesion_preference(self, neighbours):
        x = y = 0
        for boid in neighbours:
            x += boid.x
            y += boid.y
        x /= len(neighbours)
        y /= len(neighbours)
        ax = x - self.x
        ay = y - self.y
        return ax, ay


    def calculate_separation_preference(self, neighbours):
        ax = ay = 0
        for boid in neighbours:
            x = self.x - boid.x
            y = self.y - boid.y
            x, y = normalize_vector(x, y)
            dist = math.sqrt((boid.x - self.x)**2 + (boid.y - self.y)**2)
            x /= dist
            y /= dist
            ax += x
            ay += y
        return ax, ay


    def calculate_alignment_preference(self, neighbours):
        vx = vy = 0
        for boid in neighbours:
            vx += boid.vx
            vy += boid.vy
        vx /= len(neighbours)
        vy /= len(neighbours)
        ax = vx - self.vx
        ay = vy - self.vy
        return ax, ay

    
def truncate_vector(x, y, max_value):
    val = math.sqrt(x**2+y**2)
    if val >= max_value:
        ratio = max_value / val
        x *= ratio
        y *= ratio
    return x,y


def normalize_vector(x, y):
    val = math.sqrt(x**2+y**2)
    if val == 0:
        return 0, 0
    ratio = 1 / val
    x *= ratio
    y *= ratio
    return x, y

