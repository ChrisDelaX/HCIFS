from HCIFS.Device.Device import Device

class DM(Device):
    """Deformable Mirrors
    """
    def __init__(self, **specs):
        
        super().__init__(**specs)
