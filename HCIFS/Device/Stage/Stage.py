import astropy.units as u

class Stage(object):
    
    def __init__(self, type='Stage', serial=None, pos=0, vel=0, acc=0, 
            maxtravel=100, labExperiment=False, **specs):
        
        self.type = specs.get('type', type)
        self.serial = specs.get('serial', serial)
        self.pos = specs.get('pos', pos)*u.mm
        self.vel = specs.get('vel', vel)*u.mm/u.s
        self.acc = specs.get('acc', acc)*u.mm/u.s**2
        self.maxtravel = specs.get('maxtravel', maxtravel)*u.mm
        self.labExperiment = bool(specs.get('labExperiment', labExperiment))# lab flag
    
    def enable(self):
        assert not self.labExperiment, "Can't 'enable' with a default stage class."
        print("Turn 'labExperiment = True' to enable a Stage.")
    
    def disable(self):
        pass
    
    def move(self, movement):
        """
        moves the stage relative to its current position
        """
        assert type(movement) == u.Quantity, "movement must be an astropy Quantity."
        self.setPos(self.pos + movement)
    
    def gotoHome(self):
        """
        moves the stage to its home position
        """
        self.pos = 0*u.mm
    
    def setPos(self, pos):
        """
        sets the position of the stage to pos
        """
        assert type(pos) == u.Quantity, "pos must be an astropy Quantity."
        self.pos = pos
    
    def setVel(self, vel):
        """
        sets the velocity of the stage to vel
        """
        assert type(vel) == u.Quantity, "vel must be an astropy Quantity."
        self.vel = vel
    
    def setAcc(self, acc):
        """
        sets the acceleration of the stage to acc
        """
        assert type(acc) == u.Quantity, "acc must be an astropy Quantity."
        self.acc = acc
