from HCIFS.Device.DM.DM import DM

class BM1k(DM):
    def __init__(self, **keywords):
        defaults = {'type': 'BM1k'}
        self.specs = keywords
        self.specs.update(defaults)
        self.specs.update(keywords)
        super().__init__(**self.specs)