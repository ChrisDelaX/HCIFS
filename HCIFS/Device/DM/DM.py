from HCIFS.Device.Device import Device

class DM(Device):
    """
    class for representing deformable mirrors
    """
    def __init__(self, maxVoltage=0, flatMap=None, numAct=0, numActProfile = 0, **specs):
        """
        Constructor for the 'DM' class
        Inputs:
            maxVoltage - the maximum allowable voltage for the DM (int)
            flatMap - path for file containing flatmap (str)
            numAct - real number of actuators on DM (int)
            numActProfile - the number of actuators included in the profile (int)
        """
        # call the Device constructor
        super().__init__(**specs)
        
        # load DM attributes
        self.maxVoltage = int(specs.get('maxVoltage', maxVoltage))
        self.flatMap = specs.get('flatMap', flatMap)
        self.numAct = int(specs.get('numAct', numAct))
        self.numActProfile = int(specs.get('numActProfile', numActProfile))
    
    def zero(self):
        """
        Dummy function for zeroing DM
        """
        assert not self.labExperiment, "Can't use 'zero' with default 'DM' class."
        print("Turn 'labExperiment = True' to run the lab.")
    
    def sendData(self, data):
        """
        Dummy function for passing data to DM
        """
        assert not self.labExperiment, "Can't use 'sendData' with default 'DM' class."
        print("Turn 'labExperiment = True' to run the lab.")
    
    def flatten(self):
        """
        Dummy function for flattening the DM using self.flatMap
        """
        assert not self.labExperiment, "Can't use 'flatten' with default 'DM' class."
        print("Turn 'labExperiment = True' to run the lab.")
    
    def getCurrentData(self):
        """
        Dummy function for getting current voltage data
        """
        assert not self.labExperiment, "Can't use 'zero' with default 'DM' class."
        print("Turn 'labExperiment = True' to run the lab.")
        return np.zeros(self.numAct)
    def changeActuator(self, actuator, command):
        """
        Dummy function for changing the voltage on a single actuator
        """
        assert not self.labExperiment, "Can't use 'zero' with default 'DM' class."
        print("Turn 'labExperiment = True' to run the lab.")
