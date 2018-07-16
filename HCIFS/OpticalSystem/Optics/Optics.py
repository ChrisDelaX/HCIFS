import importlib

class Optics():
    
    def __init__(self, **keywords):
        
        self.specs = {'type': None, 'dist2prev': 0, 'name': None,
                      'defaultPosition': (0, 0), 'stageType': None,
                      'stageSerial': 'None', 'focal': None}
        self.specs.update(keywords)
        self.pos = self.specs['defaultPosition']
        self.dist2prev = self.specs['dist2prev']

        if self.specs.get('stageType') != None:
            moduleName = self.specs['stageType']
            importName = 'OpticalSystem.MotorStage.' + moduleName
            importlib.import_module(importName)
            stageClass = getattr(importName, moduleName)
            self.stage = stageClass(self.specs['stageSerial'])
    
    def position(self):
        if self.specs.get('stageType') != None:
            self.pos = self.specs.get('stage').position()
            return self.pos
        else:
            return self.specs.get('defaultPosition')