from HCIFS.Device.FilterWheel.FilterWheel import FilterWheel
from HCIFS.util.LabControl import SerialPort

class FW212b(FilterWheel):
    
    def __init__(self, **keywords):
        """
        Creats an instance of the FilterWheel class. Creates a port attribute to
        hold the connection to the filter wheel.
        """
        defaults = {
                'port': 'COM12', 'baudrate': 115200, 'bytesize': 8,
                'stopbits': 1,
                }
        self.specs = defaults
        self.specs.update(keywords)
        # connects to the filter wheel
        self.port = SerialPort(comPort = self.specs.get('port'),
                               baudRate = self.specs.get('baudrate'),
                               byteSize = self.specs.get('bytesize'),
                               stopBits = self.specs.get('stopbits'))
        self.filterNum = 0
    
    def getFilter(self):
        """
        Gets the current position of the filter wheel
        Returns an integer from 1 - 12
        """
        super().getFilter()
        # queries for current filter position
        self.filterNum = self.port.query('pos')
        return self.filterNum
    
    def setFilter(self, filterNum):
        """
        Changes the position of the filter wheel
        pos must be an integer from 1 - 12
        """
        super().setFilter(filter)
        # makes sure pos is between 1 and 12 inclusive
        if filterNum < 1 or filterNum > 12:
            raise ValueError("Filter number must be an integer from 1 to 12")
        # writes the command to the port
        self.port.command('pos', filterNum)
