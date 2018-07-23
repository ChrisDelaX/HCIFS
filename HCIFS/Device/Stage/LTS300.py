from HCIFS.Device.Stage.MTS50 import MTS50
from HCIFS.util.LabControl import PyAPT


class LTS300(MTS50):
    
    def __init__(self, type=None, serial=None):
    
        super().__init__(type=type, serial=serial)
