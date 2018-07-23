from HCIFS.Device.Mask.Mask import Mask

class BowtieSet(Mask):
    """Focal Plane mask (set of 9 'openings')
    """
    
    def __init__(self, **keywords):
        defaults = {'type': 'BowtieSet', 'position': 9}
        self.specs = keywords
        self.specs.update(defaults)
        self.specs.update(keywords)
        super().__init__(**self.specs)
        

