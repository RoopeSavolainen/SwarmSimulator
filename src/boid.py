class Boid:

    # Position
    x = None
    y = None

    # Velocity
    _vx = None
    _vy = None

    '''
    # Acceleration
    _ax = None
    _ay = None
    '''

    parameters = None


    def __init__(self, x, y, parameters):
        self.x = x
        self.y = y

        self._vx = 0
        self._vy = 0

        '''
        self._ax = 0
        self._ay = 0
        '''

        self.parameters = parameters


    def update_self():
        pass


    def calculate_acceleration():
        pass


    def calculate_cohesion_preference():
        pass


    def calculate_separation_preference():
        pass


    def calculate_alignment_preference():
        pass


