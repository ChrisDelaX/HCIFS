from HCIFS.Device.Mask.Mask import Mask


class Ripple3(Mask):
    """Shaped Pupil
    """
    
    def __init__(self, **keywords):
        defaults = {'type': 'Ripple3'}
        self.specs = keywords
        self.specs.update(defaults)
        self.specs.update(keywords)
        super().__init__(**self.specs)