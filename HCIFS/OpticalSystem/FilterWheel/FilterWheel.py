import serial as s
import time

class FilterWheel(object):
    
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
        self.port = s.Serial(port = self.specs['port'], 
                             baudrate = self.specs['baudrate'], 
                             bytesize = self.specs['bytesize'],
                             stopbits = self.specs['stopbits']) 
        # cloese the port
        self.port.close()
        
    def getPosition(self):
        """
        Gets the current position of the filter wheel
        Returns an integer from 1 - 12
        """
        # opens the port
        self.port.open()
        # queries for current filter position
        self.port.write('pos?\r'.encode('utf-8'))
        position = ""
        time.sleep(1)
        # finds how many bytes were written to the port
        written = self.port.in_waiting
        # reads in what was written except for the end of line
        for i in range(written - 3):
            position += self.port.read(1).decode()
        # pauses to prevent an error
        time.sleep(1)
        # closes the port
        self.port.close()
        # returns the position which occurs at the end of the string
        return position[5:]
    
    def setPosition(self, pos):
        """
        Changes the position of the filter wheel
        pos must be an integer from 1 - 12
        """
        # opens the port
        self.port.open()
        # makes sure pos is between 1 and 12 inclusive
        if pos < 1 or pos > 12:
            raise ValueError("Position must be an integer from 1 to 12")
        # creates a command to pass to the port
        command = 'pos=' + str(pos) + '\r'
        # writes the command to the port
        self.port.write(command.encode())
        # closes the port
        self.port.close()
    
    def disconnect(self):
        """
        Closes the serial port
        """
        # closes the port
        self.port.close()