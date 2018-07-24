from HCIFS.Device.Device import Device

class FilterWheel(Device):
    
    def __init__(self, **keywords):
        """
            Creats an instance of the FilterWheel class. Creates a port attribute to
            hold the connection to the filter wheel.
            """
        self.specs = {}
        self.port = None
        self.filterNum = None
    
    def getFilter(self):
        """
            Gets the current position of the filter wheel
            Returns an integer from 1 - 12
            """
        self.filterNum = 0
        return self.filterNum
    
    def setFilter(self, filterNum):
        """
            Changes the position of the filter wheel
            pos must be an integer from 1 - 12
            """
        self.filterNum = filterNum
    
    def moveUp(self):
        """
            Moves the filterwheel up one position
            """
        currentFilter = int(self.getFilter())
        if currentFilter == 12:
            currentFilter = 0
        self.setFilter(currentFilter + 1)
        self.filterNum = currentFilter + 1
    
    def moveDown(self):
        """
            Moves the filterwheel down one position
            """
        currentFilter = int(self.getFilter())
        if currentFilter == 1:
            currentFilter = 13
        self.setFilter(currentFilter - 1)
        self.filterNum = currentFilter - 1
