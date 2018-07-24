from HCIFS.Device.Device import Device


class Stage(Device):
    
    def __init__(self, device, axis, type=None, serial=None):
        
        self.type = type
        self.serial = serial
        self.handle = None
        self.vel = None
        self.accel = None
        self.position = None
        
    def getPos(self):
        """
        returns the current position of the stage
        """
        return self.position

    def moveDevice(self, movement):
        """
        moves the stage relative to its current position
        """
        self.position += movement
    
    def gotoHome(self):
        """
        moves the stage to its home position
        """
        self.position = 0
