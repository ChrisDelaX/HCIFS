class Sources(object):
    
    def __init__(self, labExperiment=False, **specs):
        """
        Creates an instance of the Sources class. Creates a port attribute to
        hold the connection to the laser.
        """
        
        # get the laboratory experiment flag
        self.labExperiment = bool(specs.get('labExperiment', labExperiment))
    
    def enable(self):
        """
        Enables the source.
        """
        assert labExperiment is False, "Can't 'enable' the default 'Sources' module."
        print("Turn 'labExperiment = True' to run the lab.")
    
    def disable(self):
        """
        Disables the source.
        """
        assert labExperiment is False, "Can't 'disable' the default 'Sources' module."
        print("Turn 'labExperiment = True' to run the lab.")
    
    def status(self):
        """
        Gets the status of the source and returns it.
        """
        assert labExperiment is False, "Can't use 'status' with default 'Sources' module."
        print("Turn 'labExperiment = True' to run the lab.")
        return 'no status'
    
    def changeCurrent(self, current):
        """
        Changes the current (in mA) of a specific channel of the source
        """
        assert labExperiment is False, "Can't 'change current' with default 'Sources' module."
        print("Turn 'labExperiment = True' to run the lab.")
    
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
