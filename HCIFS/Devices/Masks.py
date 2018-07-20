from HCIFS.Devices import Mask

class BowtieSet(Mask):
    """Focal Plane mask (set of 9 'openings')
    """
    
    def __init__(self, **keywords):
        defaults = {'type': 'BowtieSet', 'position': 9}
        self.specs = keywords
        self.specs.update(defaults)
        self.specs.update(keywords)
        super().__init__(**self.specs)
        

class Ripple3(Mask):
    """Shaped Pupil
    """
    
    def __init__(self, **keywords):
        defaults = {'type': 'Ripple3'}
        self.specs = keywords
        self.specs.update(defaults)
        self.specs.update(keywords)
        super().__init__(**self.specs)