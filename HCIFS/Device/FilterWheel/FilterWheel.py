from HCIFS.Device.Device import Device

class FilterWheel(Device):
    
    def __init__(self, **keywords):
        """
        Creats an instance of the FilterWheel class. Creates a port attribute to
        hold the connection to the filter wheel.
        """
        self.specs = {}
        self.port = None
        self.position
        
    def getPosition(self):
        """
        Gets the current position of the filter wheel
        Returns an integer from 1 - 12
        """
        self.position = 0
        return self.position
    
    def setPosition(self, position):
        """
        Changes the position of the filter wheel
        pos must be an integer from 1 - 12
        """
        self.position = position
    
    def moveUp(self):
        """
        Moves the filterwheel up one position
        """
        currentPosition = int(self.getPosition())
        if currentPosition == 12:
            currentPosition = 0
        self.setPosition(currentPosition + 1)
        self.position = currentPosition + 1
        
    def moveDown(self):
        """
        Moves the filterwheel down one position
        """
        currentPosition = int(self.getPosition())
        if currentPosition == 1:
            currentPosition = 13
        self.setPosition(currentPosition - 1)
        self.position = currentPosition - 1