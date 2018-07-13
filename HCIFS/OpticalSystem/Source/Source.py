class Source(object):
    
    def __init__(self, **specs):
        """
        Creates an instance of the Source class. Creates a port attribute to
        hold the connection to the laser.
        """
        self.specs = {}
        self.port = None
    
    def enable(self):
        """
        Enables the source.
        """
        pass
    
    def disable(self):
        """
        Disables the source.
        """
        pass
    
    def status(self):
        """
        Gets the status of the source and returns it.
        """
        status = "status"
        return status
    
    def changeCurrent(self, current):
        """
        Changes the current (in mA) of a specific channel of the source
        """
        pass
    
    def calibrate(self, camera):
        """
        Calibrates the source so that the central peak is overasaturated, and
        the second peaks are just below saturated. It then returns two tuples
        with the x and y coordinates and the intensity for first the central
        peak and then the secondary one
        """
        centerX, centerY, newCenterPeak = 0, 0, 0
        secondX, secondY, newSecondPeak = 0, 0, 0
        return (centerX, centerY, newCenterPeak), (secondX, secondY, newSecondPeak)
