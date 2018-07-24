from HCIFS.Device.Stage.Stage import Stage
from HCIFS.util.LabControl import PyAPT


class MTS50(Stage):
    
    def __init__(self, type=None, serial=None):
        super().__init__(type=type, serial=serial)
        self.HWTYPE = 42

 def enable(self):
        """
        connects the camera and gets current position, velocity, and acceleration
        """
        # connects to the camera
        self.handle = PyAPT(self.serial, self.HWTYPE)
        
        # makes sure max position is set to 30
        info = self.handle.query('getStageAxisInformation')
        info[1] = 30.0
        self.handle.command('setStageAxisInformation', info)
        
    def getPos(self):
        """
        returns the current position of the stage
        """
        if not self.labExperiment:
            super().getPos()
        else:
            self.position = self.handle.query('getPos')
            return self.position
    
    def moveDevice(self, movement):
        """
        moves the stage to position
        """
        if not self.labExperiment:
            super.moveDevice()
        else:
            currentPosition = self.getPos()
            self.handle.command('mAbs', currentPosition + movement)
            self.position = currentPosition + movement
    
    def gotoHome(self):
        """
        moves the stage to its home position
        """
        if not self.labExperiment:
            super().gotoHome()
        else:
            self.position = 0
            self.handle.query('go_home')
    
    
    def getVel(self):
        """
        gets the current max velocity of the stage
        """
        return self.handle.query('getVel')
    
    def setVel(self, velocity):
        """
        sets the max velocity of the stage to velocity
        """
        self.handle.command('setVel', velocity)
    
    def getAccel(self):
        """
        gets the current acceleration of the stage
        """
        return self.handle.query('getVelocityParameters')[1]
    
    def setAccel(self, acceleration):
        """
        sets the accleration of the stage to accleration
        """
        # get current velocity parameters
        params = self.handle.query('getVelocityParameters')
        # update acceleration paramter
        params[1] = acceleration
        # change the paramters
        self.handle.command('setVelocityParameters', *params)
    
    def disable(self):
        """
        releases the connection to the stage
        """
        super().disable()
        self.handle.query('cleanUpAPT')
        
