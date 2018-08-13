from HCIFS.Device.Stage.MTS50 import MTS50


class LTS300(MTS50):
    
    def __init__(self, **specs):
        
        # call the MTS50 Stage constructor
        super().__init__(**specs)
