from HCIFS.Device.Device import Device

class FilterWheel(Device):
    """
    A class for representing a generic filterwheel
    """
    
    def __init__(self, numOfFilters=0, **specs):
        """
        Constructor for the 'FilterWheel' class
        Inputs:
            numOfFilters: number of filters on wheel (int)
        """
        # call the 'Device' __init__
        super().__init__(**specs)
    
    def getFilter(self):
        """
        Dummy function for getting current filter
        """
        assert not self.labExperiment, "Can't use 'getFilter' with default 'FilterWheel' class."
        print("Turn 'labExperiment = True' to run the lab.")
        return 0
    
    def setFilter(self, filterNum):
        """
        Dummy class for changing which filter is active
        Inputs:
            filterNum - the filter to use (int)
        """
        assert not self.labExperiment, "Can't use 'setFilter' with default 'FilterWheel' class."
        print("Turn 'labExperiment = True' to run the lab.")
    
    def moveUp(self):
        """
        Dummy class for moving the filterwheel up one position
        """
        if self.labExperiment:
            currentFilter = int(self.getFilter())
            if currentFilter == self.numOfFilters:
                currentFilter = 0
            self.setFilter(currentFilter + 1)
        else:
            raise Exception("Can't use 'moveUp' with default 'Camera' class.")
            print("Turn 'labExperiment = True' to run the lab.")
    def moveDown(self):
        """
        Dummy class for moving the filterwheel up one position
        """
        if self.labExperiment:
            currentFilter = int(self.getFilter())
            if currentFilter == 1:
                currentFilter = self.numOfFilters + 1
            self.setFilter(currentFilter - 1)
        else:
            raise Exception("Can't use 'realTime' with default 'Camera' class.")
            print("Turn 'labExperiment = True' to run the lab.")
