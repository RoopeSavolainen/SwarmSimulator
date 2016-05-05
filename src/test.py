import unittest
import simulation, boid, parameters

from math import sqrt

class Test(unittest.TestCase):

    def test_normalize_truncate(self):
        x1, y1 = -7, 3
        x2, y2 = boid.normalize_vector(x1,y1)
        erotus = sqrt(x2**2+y2**2) - 1
        self.assertTrue( abs(erotus) < 0.1 )

        x3, y3 = boid.truncate_vector(x1,y1,5.8)
        erotus = sqrt(x3**2+y3**2) - 5.8
        self.assertTrue( abs(erotus) < 0.1 )

        # Here truncate should do nothing
        x1, y1 = 1, 2
        x4, y4 = boid.truncate_vector(x1,y1,13)
        erotus = sqrt(x4**2+y4**2) - sqrt(1**2+2**2)
        self.assertTrue( abs(erotus) < 0.1 )
        self.assertEqual(x1, x4)
        self.assertEqual(y1, y4)


    def test_separation(self):
        p = parameters.Parameters()
        b = boid.Boid(p, 0, 0)
        n = [boid.Boid(p, -1, -1), boid.Boid(p, -1, 0), boid.Boid(p, 0, -1)]

        a_x, a_y = b.calculate_separation_preference(n)
        
        self.assertTrue(a_x > 0)
        self.assertTrue(a_y > 0)


    def test_neighbors(self):
        p = parameters.Parameters()
        s = simulation.Simulation(p)
        
        s.boids = [boid.Boid(p, 0, 0), boid.Boid(p, -1, -1), boid.Boid(p, -1, 0), boid.Boid(p, 0, -1), boid.Boid(p, -9, -3), boid.Boid(p, -28, 0)]
        neighbours = s.get_neighbours(s.boids[0], n=3)

        self.assertEqual(len(neighbours), 3)
        self.assertTrue(s.boids[1] in neighbours)
        self.assertFalse(s.boids[0] in neighbours and s.boids[2] in neighbours and s.boids[3] in neighbours)


unittest.main()
