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
        self.position = 0
        
    def getPosition(self):
        """
        Gets the current position of the filter wheel
        Returns an integer from 1 - 12
        """
        super().getPosition()
        # queries for current filter position
        self.position = self.port.query('pos')
        return self.position
    
    def setPosition(self, position):
        """
        Changes the position of the filter wheel
        pos must be an integer from 1 - 12
        """
        super().setPosition(position)
        # makes sure pos is between 1 and 12 inclusive
        if position < 1 or position > 12:
            raise ValueError("Position must be an integer from 1 to 12")
        # writes the command to the port
        self.port.command('pos', position)
