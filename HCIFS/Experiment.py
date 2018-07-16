#from Hardware.Camera import Camera
#from Hardware.Laser import Laser
#from Hardware.Motor import Motor
import os.path, json, inspect
from HCIFS.OpticalSystem.OpticalSystem import OpticalSystem


class Experiment(object):
    
    def __init__(self, jsonfile=None, nbIter=30, **specs):
    
        # ensure JSON filename extension
        if jsonfile[-5:].lower() != '.json':
            jsonfile = jsonfile + '.json'
        # ensure JSON file location
        if not os.path.isfile(jsonfile):
            jsonfile = os.path.join(os.path.split(inspect.getfile(self.__class__))[0], \
                    'Scripts', jsonfile)
        try:
            # load JSON script file
            self.specs = json.loads(open(jsonfile).read())
            # use specs keyword arguments to override JSON script
            self.specs.update(specs)
        except IOError:
            raise IOError("'%s' is not a file."%jsonfile)
        except ValueError:
            raise ValueError("Error: script file is formatted incorrectly.")
        
        # initialize the Optical System
        self.OpticalSystem = OpticalSystem(**self.specs)
        
        
        

    def runLaboratory(self):
        
        # win32com package must be installed to run the lab (Windows platform only)
        try:
            import win32com.client
        except ImportError:
            raise ImportError("Can't control the camera without win32com package.")

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