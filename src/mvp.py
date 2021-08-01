class MVP:
    def __init__(self, location, dt):
        self.location = location
        self.dt = dt
    
    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        return f'{self.location}: {self.dt}'