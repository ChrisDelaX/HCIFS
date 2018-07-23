#from Hardware.Camera import Camera
#from Hardware.Laser import Laser
#from Hardware.Motor import Motor
import os.path, json, inspect, glob
from HCIFS.util.imports import get_module
import numpy as np

class Experiment(object):
    
    def __init__(self, jsonfile=None, labExperiment=False, nbIter=30, **specs):
    
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
        # update local variable 'specs'
        specs = self.specs
        
        # create the Devices dictionary of modules (Source, Camera, DM, Mask, ...)
        self.Devices = dict()
        # loop through the list of dictionaries in 'Devices'
        devs = 'Devices'
        assert devs in specs, "'%s' not defined in 'specs'."%devs
        for ID, device in enumerate(specs[devs]):
            assert isinstance(device, dict), "'%s' must be defined as a list of dicts."%devs
            assert ('name' in device) and isinstance(device['name'], str), \
                    "All elements of '%s' must have key 'name'."%devs
            # update the device dictionary with useful keys
            dev = dict({**device, 'ID':ID, 'labExperiment':labExperiment})
            # get the specified module, or use the default 'Device' module
            modname = device.get('type', 'Device')
            module = get_module(modname)
            self.Devices[device['name']] = getattr(module, modname)(**dev)
        
        # Load the loops array, or create a default loop of Devices sorted by ID
        loops = np.array(specs.get('loops', [dev.name for dev \
                in sorted(self.Devices.values(), key=lambda dev: dev.ID)]), ndmin=2)
        # create the FPWC and IFS loops.
        if loops.shape[0] >= 2:
            self.loop_FPWC = loops[0]
            self.loop_IFS = loops[1]
        else:
            self.loop_FPWC = self.loop_IFS = loops
        # Load the distances array, must be the size of loops minus 1. Default to zeros.
        distances = np.array(specs.get('distances', np.zeros(loops.shape[1]-1)), ndmin=2)
        # create the FPWC and IFS distances.
        if distances.shape[0] >= 2:
            self.distances_FPWC = distances[0]
            self.distances_IFS = distances[1]
        else:
            self.distances_FPWC = self.distances_IFS = loops

#### ADD assert shapes distances vs loops

        
    def moveDevice(self, name, movement):
        """Check for motorized stages on a device, then change the position of the 
        device by introducing a relative movement in x,y,z.
        """
        for i, (type, serial) in enumerate(zip(stageTypes, stageSerials)):
            # get the specified module, or use the default 'Stage' module
            type = type if type is not None else 'Stage'
            # create a Stage
            module = get_module(type, 'Stage')
            Stage = getattr(module, type)(type=type, serial=serial)
            Stage.moveDevice(movement)
            # update the distances array
            deltaZ = movement[2]
            if deltaZ != 0:
                if ID == 0:
                    device.dist2next -= deltaZ
                    self.distances[0] += deltaZ
                    self.distances[1] -= deltaZ
                else:
                    self.optics[ID - 1].dist2next += deltaZ
                    device.dist2next -= deltaZ
                    self.distances[ID] += deltaZ
                    self.distances[ID + 1] -= deltaZ   


                
        
        

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