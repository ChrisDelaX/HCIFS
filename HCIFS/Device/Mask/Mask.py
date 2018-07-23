from HCIFS.Device.Device import Device

class Mask(Device):
    """Example: Shaped Pupil, Focla Plane Mask.
    """
    def __init__(self, **specs):
        
        super().__init__(**specs)
