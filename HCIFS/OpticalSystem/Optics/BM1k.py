from OpticalSystem.Optics.Optics import Optics

class BM1k(Optics):
    def __init__(self, **keywords):
        defaults = {'type': 'BM1k'}
        self.specs.update(defaults)
        self.specs.update(keywords)
        super().__init__(**self.specs)