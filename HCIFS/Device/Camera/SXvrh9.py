from HCIFS.util.LabControl import ActiveX
from HCIFS.Device.Camera.Camera import Camera

class SXvrh9(Camera):

    def __init__(self, **keywords):
        
        self.specs = keywords
        super().__init__(**self.specs)
        
