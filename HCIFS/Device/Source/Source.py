from HCIFS.Device.Device import Device

class Source(Device):
    """
    A class used to represent sources.
    """
    def __init__(self, npixCalib=10, **specs):
        """
        Constructor of the dummy class for source.
        
        Inputs:
            npixCalib: half the length in pixels of the squares used for calibration
        """
        super().__init__(**specs)
        
        # default attributes specific to Sources
        self.npixCalib = int(specs.get('npixCalib', npixCalib)) # length of calibration area
    
    def status(self):
        """
        Dummy method for getting status
        
        Outpus: status
        """
        assert not self.labExperiment, "Can't use 'status' with default 'Source' class."
        print("Turn 'labExperiment = True' to run the lab.")
        return 'no status'
    
    def changeCurrent(self, current):
        """
        Dummy method for changing current
        
        Input: the current in milliAmps
        """
        assert not self.labExperiment, "Can't 'change current' with default 'Source' class."
        print("Turn 'labExperiment = True' to run the lab.")
    
    def calibrate(self, camera):
        """
        Dummy method for calibration.
        
        Inputs: The camera object used for calibration
        
        Output:
            Tuple: (x-coordinate of central peak, y-coordinate of central peak,
                    intensity of the central peak)
            Tuple: (x-coordinate of second peak, y-coordinate of sedond peak,
                    intensity of the second peak)
        """
        centerX, centerY, newCenterPeak = 0, 0, 0
        secondX, secondY, newSecondPeak = 0, 0, 0
        return (centerX, centerY, newCenterPeak), (secondX, secondY, newSecondPeak)
