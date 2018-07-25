from HCIFS.Device.Stage.Stage import Stage
from HCIFS.util.LabControl import PyAPT
import astropy.units as u

class MTS50(Stage):
    
    def __init__(self, HWTYPE=42, maxtravel=30, **specs):
        
        # call the Stage constructor
        super().__init__(**specs)
        
        # load specific MTS50 attributes
        self.HWTYPE = int(specs.get('HWTYPE', HWTYPE))
        
        # connect to the stage and get its position
        if self.labExperiment:
            self.enable()
            self.pos = self.getPos()
            self.vel = self.getVel()
            self.acc = self.getAcc()
    
    def enable(self):
        """
        Enables the stage and sets it up
        """
        if not self.labExperiment:
            super().enable()
        else:
            self.handle = PyAPT(self.serial, self.HWTYPE)
            info = self.handle.query('getStageAxisInformation')
            info[1] = self.maxtravel.to('mm').value
            self.handle.command('setStageAxisInformation', info)
    
    def disable(self):
        """
        releases the connection to the stage
        """
        if not self.labExperiment:
            super().disable()
        else:
            self.handle.query('cleanUpAPT')
    
    def gotoHome(self):
        """
        moves the stage to its home position
        """
        # call the prototype method to set position to 0
        super.gotoHome()
        # then move the motorized stage
        if self.labExperiment:
            self.handle.query('go_home')
    
    def setPos(self, pos):
        """
        sets the position of the stage to pos
        """
        assert type(pos) == u.Quantity, "pos must be an astropy Quantity."
        if not self.labExperiment:
            super().enable()
        else:
            self.handle.command('mAbs', pos.to('mm').value)
    
    def setVel(self, vel):
        """
        sets the velocity of the stage to vel
        """
        assert type(vel) == u.Quantity, "vel must be an astropy Quantity."
        if not self.labExperiment:
            super().enable()
        else:
            self.handle.command('setVel', vel.to('mm/s').value)
    
    def setAcc(self, acc):
        """
        sets the accleration of the stage to acc
        """
        assert type(acc) == u.Quantity, "acc must be an astropy Quantity."
        if not self.labExperiment:
            super().enable()
        else:
            # get current velocity parameters
            params = self.handle.query('getVelocityParameters')
            # update acceleration paramter
            params[1] = acc.to('mm/s2').value
            # change the paramters
            self.handle.command('setVelocityParameters', *params)
    
    def getPos(self):
        """
        returns the current position of the stage in units of mm
        """
        if self.labExperiment:
            self.pos = self.handle.query('getPos')*u.mm
        return self.pos
    
    def getVel(self):
        """
        gets the current velocity of the stage in units of mm/s
        """
        if self.labExperiment:
            self.vel = self.handle.query('getVel')*u.mm/u.s
        return self.vel
    
    def getAcc(self):
        """
        gets the current acceleration of the stage in units of mm/s2
        """
        if self.labExperiment:
            self.acc = self.handle.query('getVelocityParameters')[1]*u.mm/u.s**2
        return self.acc
