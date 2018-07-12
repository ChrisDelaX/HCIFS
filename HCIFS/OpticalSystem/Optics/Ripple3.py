from OpticalSystem.Optics.Optics import Optics

class Ripple3(Optics):
    def __init__(self, **keywords):
        defaults = {'type': 'Ripple3'}
        self.specs.update(defaults)
        self.specs.update(keywords)
        super().__init__(**self.specs)