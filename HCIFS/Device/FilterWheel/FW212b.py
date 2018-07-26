from HCIFS.Device.FilterWheel.FilterWheel import FilterWheel
from HCIFS.util.LabControl import SerialPort

class FW212b(FilterWheel):
    """
    Controls the Thorlabs FW212b filterwheel
    
    Device Info:
        Dimensions (L x W x H)  5.44" x 1.85" x 4.39"   (138 x 47 x 112 mm)
    
    Filters Installed (Andover Corporation, 12.5mm dia.):

        #1:  550FS10-12.5 (Q342-29)   550nm Bandpass,   FWHM 10nm,     $69

        #2:  577FS10-12.5 (Q342-06)   577nm Bandpass,   FWHM 10nm,  (obsolete)             

        #3:  600FS10-12.5 (Q342-10)   600nm Bandpass,   FWHM 10nm,     $69

        #4:  620FS10-12.5 (Q342-20)   620nm Bandpass,   FWHM 10nm,     $69

        #5:  633FS03-12.5 (R014-52)   632.8nm Bandpass, FWHM 3nm,      $107

        #6:  640FS10-12.5 (Q342-06)   640nm Bandpass,   FWHM 10nm,     $69

        #7:  650FS10-12.5 (Q342-54)   650nm Bandpass,   FWHM 10nm,     $69

        #8:  670FS10-12.5 (Q342-02)   670nm Bandpass,   FWHM 10nm,     $69

        #9:  694FS10-12.5 (Q342-01)   694.3nm Bandpass, FWHM 10nm,     $69

        #10: 720FS10-12.5 (Q342-05)   720nm Bandpass,   FWHM 10nm,     $69

        #11: 740FS10-12.5 (Q342-01)   740nm Bandpass,   FWHM 10nm,     $69

        #12: 650FS80-12.5 (****-**)   650nm Bandpas,    FWHM 80nm,     $72 	 
        
        
    """
    def __init__(self, port='COM12', numOfFilters=12, **specs):
        """
        Constructor for the 'FW212b' class.
        Inputs:
            port: the COM port the FW212b is attached to (str)
            numOfFilters: number of filters on wheel (int)
        """
        # call the 'FilterWheel' class __init__
        super().__init__(**specs)
        
        # create attributes
        self.port = specs.get('port', port)
        self.numOfFilters = int(specs.get('numOfFilters', numOfFilters))
        
        # connects to the filter wheel
        if self.labExperiment == True:
            self.port = SerialPort(comPort = self.port)
    
    def getFilter(self):
        """
        Gets the current position of the filter wheel
        Returns an integer from 1 - 12
        """
        if not self.labExperiment:
            super().getFilter()
        else:
            # queries for current filter
            return self.port.query('pos')
    
    def setFilter(self, filterNum):
        """
        Changes the position of the filter wheel
        pos must be an integer from 1 - 12
        """
        if not self.labExperiment:
            super().setFilter(filter)
        else:
            # makes sure pos is between 1 and 12 inclusive
            if filterNum < 1 or filterNum > self.numOfFilters:
                raise ValueError("Filter number must be an integer from 1 to 12")
            # writes the command to the port
            self.port.command('pos', filterNum)
