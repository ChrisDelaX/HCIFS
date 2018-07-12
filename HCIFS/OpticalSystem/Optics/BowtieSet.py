from OpticalSystem.Optics.Optics import Optics

class BowtieSet(Optics):
    def __init__(self, **keywords):
        defaults = {'type': 'BowtieSet', 'position': 9}
        self.specs.update(defaults)
        self.specs.update(keywords)
        super().__init__(**self.specs)