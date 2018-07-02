from Hardware.Camera import Camera
import json


class HCIL(object):
    
    def __init__(self, JSONfile=None):
    
        # default JSON script file
        if JSONfile is None:
            JSONfile = 'C:/Lab/HCIL/Scripts/test.json'
        # load JSON script file
        specs = json.loads(open(JSONfile).read())
            

    def RunLabExperiment(self, **specs):
        
        
        pass
    

    
    
    def closeLab(self, **specs):
        
        pass
    
    def RunSimulation(self, **specs):
        
        pass
    
    