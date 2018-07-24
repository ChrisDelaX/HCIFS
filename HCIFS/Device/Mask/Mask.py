from HCIFS.Device.Device import Device
import astropy.units as u

class Mask(Device):
    """Example: Shaped Pupil, Focla Plane Mask.
    """
    
    def __init__(self, posON=[0,0,0], posOFF=[0,0,0], **specs):
        
        # call the Device constructor
        super().__init__(**specs)
        
        # load specific Mask attributes
        self.posON = specs.get('posON', posON)*u.mm     # position of the mask ON in mm
        self.posOFF = specs.get('posOFF', posOFF)*u.mm  # position of the mask OFF in mm

