from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtGui import QPainter, QBrush
from PyQt5.QtCore import QPointF, QRectF, Qt

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

    max_speed = 10
    max_accel = 1

    radius = 5

    def __init__(self, parameters, x, y):

        super(Boid, self).__init__()
        
        self.setPos(x, y)

        self.vx = random.uniform(-10,10)
        self.vy = random.uniform(-10,10)

        self.ax = 0
        self.ay = 0

        self.parameters = parameters

    # paint() and boundingRect() are QGraphicsItem methods

    def paint(self, painter, options, widget):
        painter.setBrush(Qt.white)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawEllipse(0, 0, 2*self.radius, 2*self.radius)


    def boundingRect(self):
        penWidth = 1
        # The following margin makes the scene expand before the boids hit the border
        margin = self.radius * 10
        return QRectF(-self.radius - penWidth/2 - margin, -self.radius - penWidth/2 - margin, 2*self.radius + penWidth + margin*2, 2*self.radius + penWidth + margin*2)
    

    def update_self(self, neighbours):
        self.ax, self.ay = self.calculate_acceleration(neighbours)
        self.vx += self.ax
        self.vy += self.ay
        vx_r, vy_r = self.randomize()
        self.vx += vx_r
        self.vy += vy_r
        self.vx, self.vy = truncate_vector(self.vx, self.vy, self.max_speed)


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

        ax, ay = truncate_vector((ax_c + ax_s + ax_a)/sum_weights, (ay_c + ay_s + ay_a)/sum_weights, self.max_accel)
        return ax, ay


    def calculate_cohesion_preference(self, neighbours):
        x = y = 0
        for boid in neighbours:
            x += boid.pos().x()
            y += boid.pos().y()
        x /= len(neighbours)
        y /= len(neighbours)
        ax = (x - self.pos().x()) / 3
        ay = (y - self.pos().y()) / 3
        return ax, ay


    def calculate_separation_preference(self, neighbours):
        ax = ay = 0
        for boid in neighbours:
            x = self.pos().x() - boid.pos().x()
            y = self.pos().y() - boid.pos().y()
            x, y = normalize_vector(x, y)
            dist = math.sqrt((boid.pos().x() - self.pos().x())**2 + (boid.pos().y() - self.pos().y())**2) - 2*self.radius
            if dist > 0:
                x /= dist
                y /= dist
            else:
                x /= 0.000001
                y /= 0.000001
            ax += x
            ay += y
        return ax*20, ay*20


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


    def randomize(self):
        upper = self.parameters.random_effect
        v_term = math.sqrt(self.vx**2+self.vy**2) / self.max_speed
        vx = random.uniform(-upper, upper) * v_term
        vy = random.uniform(-upper, upper) * v_term
        return vx, vy

    
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

