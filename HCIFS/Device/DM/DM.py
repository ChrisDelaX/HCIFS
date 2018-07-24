from HCIFS.Device.Device import Device

class DM(Device):
    """
    Deformable Mirrors
    """
    def __init__(self, **specs):
        super().__init__(**specs)
        self.maxVoltage = 0
        self.flatMap = None
        self.numAct = 0
    def zero(self):
        pass
    def sendData(self, data):
        pass
    def flatten(self):
        pass
    def getCurrentData(self):
        return np.zeros(self.numAct)
    def changeActuator(self, actuator, command):
        pass
