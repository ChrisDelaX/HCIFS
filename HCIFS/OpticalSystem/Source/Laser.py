# Laser - provides basic control of ThorLabs 4-Channel Fiber-Coupled Laser Source
#
# Matthew Grossman from Princeton HCIL - Jun. 5, 2018
# Based on a Matlab function developed by He Sun
#Brief Usage:
#    To enable the laser:
#       # specs is an optional dictionary of default values to change
#        laser = Laser(specs) 
#        laser.enable()
#    To disable the laser:
#        laser.disable()
#    To get the status of the laser:
#        status = laser.status
#    To change the current of the laser:
#        laser.changeCurrent(current, channel)
#        # Channel   |   Max Current
#        # 1         |   68.09
#        # 2         |   63.89
#        # 3         |   41.59
#        # 4         |   67.39
#    To calibrate the laser:
#        center, secondary = laser.calibrate(image, length, camera)
#       # length defines the size of the area that is searched for a guassian
#       # length = 10 seems to work. camera is the an isntance of Camera class 

class Laser(object):
    
    def __init__(self):
        """
        Creats an instance of the Laser class. Creates a port attribute to
        hold the connection to the laser.
        """
        self.specs = {}
        self.port = None
    def enable(self):
        """
        Enables the laser.
        """
        pass
        
    def disable(self):
        """
        Disables the laser.
        """
        pass
        
    def status(self):
        """
        Gets the status of the laser and returns it.
        """
        status = "status"
        return status
    
    def changeCurrent(self, current):
        """
        Changes the current (in mA) of a specific channel of the laser
        """
        pass
    
    def calibrate(self, camera):
        """
        Calibrates the laser so that the central peak is overasaturated, and
        the second peaks are just below saturated. It then returns two tuples
        with the x and y coordinates and the intensity for first the central
        peak and then the secondary one
        """
        centerX, centerY, newCenterPeak = 0, 0, 0
        secondX, secondY, newSecondPeak = 0, 0, 0
        return (centerX, centerY, newCenterPeak), (secondX, secondY, newSecondPeak)