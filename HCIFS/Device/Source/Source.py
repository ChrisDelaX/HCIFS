from HCIFS.Device.Device import Device

class Source(Device):
    
    def __init__(self, npixCalib=10, **specs):
        
        super().__init__(**specs)
        
        # default attributes specific to Sources
        self.npixCalib = int(specs.get('npixCalib', npixCalib)) # length of calibration area
    
    def enable(self):
        """
        Enables the source.
        """
        assert not self.labExperiment, "Can't 'enable' with default 'Sources' module."
        print("Turn 'labExperiment = True' to run the lab.")
    
    def disable(self):
        """
        Disables the source.
        """
        assert not self.labExperiment, "Can't 'disable' with default 'Sources' module."
        print("Turn 'labExperiment = True' to run the lab.")
    
    def status(self):
        """
        Gets the status of the source and returns it.
        """
        assert not self.labExperiment, "Can't use 'status' with default 'Sources' module."
        print("Turn 'labExperiment = True' to run the lab.")
        return 'no status'
    
    def changeCurrent(self, current):
        """
        Changes the current (in mA) of a specific channel of the source
        """
        assert not self.labExperiment, "Can't 'change current' with default 'Sources' module."
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
