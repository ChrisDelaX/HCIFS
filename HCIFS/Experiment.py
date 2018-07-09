#from Hardware.Camera import Camera
#from Hardware.Laser import Laser
#from Hardware.Motor import Motor
import os.path
import json


class Experiment(object):
    
    def __init__(self, JSONfile=None, **specs):
    
        # default JSON script file
        if JSONfile is None:
            JSONfile = 'sampleScript_Lab_FPWC.json'
        # expand environmental variables
        JSONfile = os.path.expandvars(JSONfile)
        # asserts given file is a file
        assert os.path.isfile(JSONfile), "%s is not a file."%JSONfile
        
        try:
            # load JSON script file
            self.specs = json.loads(open(JSONfile).read())
            # use specs keyword arguments to override JSON script
            self.specs.update(specs)
        except ValueError as error:
            print("Error: script file is formatted incorrectly.")
            raise ValueError(error)
        
        
        
        # initialize hardware
#        self.Camera = Camera(**self.specs)
#        self.Laser = Laser(**self.specs)
#        self.HorizontalMotor = Motor("h", **specs)
#        self.VeritcalMotor = Motor("v", **specs)
        
        

    def runLaboratory(self):
        # connect the camera
        self.Camera.connect()
        # initiate the camera
        self.Camera.init()
        # enable the laser
        self.Laser.enable()
        # change the focal plane mask
        # calibrate the laser
        center, secondary = self.Laser.calibrate()
    
    def closeLab(self, ):
        # disconnect and shut off the camera
        self.Camera.disconnect()
        # change the current on the laser to zero
        self.Laser.changeCurrent(0, self.laser.specs['channel'])
        # turn off and disconnect the laser
        self.Laser.disbale()
    
    def runSimulation(self, **specs):
        
        pass