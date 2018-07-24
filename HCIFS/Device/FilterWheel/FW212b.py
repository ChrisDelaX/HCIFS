from HCIFS.Device.FilterWheel.FilterWheel import FilterWheel
from HCIFS.util.LabControl import SerialPort

class FW212b(FilterWheel):
    """
    Controls the Thorlabs FW212b filterwheel
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
        if self.LabExperiment == True:
            self.port = SerialPort(comPort = self.specs.get('port', port))
    
    def getFilter(self):
        """
        Gets the current position of the filter wheel
        Returns an integer from 1 - 12
        """
        if not self.LabExperiment:
            super().getFilter()
        else:
            # queries for current filter
            return self.port.query('pos')
    
    def setFilter(self, filterNum):
        """
        Changes the position of the filter wheel
        pos must be an integer from 1 - 12
        """
        if not self.LabExperiment:
            super().setFilter(filter)
        else:
            # makes sure pos is between 1 and 12 inclusive
            if filterNum < 1 or filterNum > self.numOfFilters:
                raise ValueError("Filter number must be an integer from 1 to 12")
            # writes the command to the port
            self.port.command('pos', filterNum)
