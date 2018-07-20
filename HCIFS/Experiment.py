#from Hardware.Camera import Camera
#from Hardware.Laser import Laser
#from Hardware.Motor import Motor
import os.path, json, inspect, glob
import HCIFS.util.imports as imports


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
        
        # create the Devices dictionary of modules (Device, Source, Camera, DM)
        self.Devices = dict()
        # loop through the list of dictionaries in 'Devices'
        devs = 'Devices'
        assert devs in specs, "'%s' not defined in 'specs'."%devs
        for device in specs[devs]:
            assert isinstance(device, dict), "'%s' must be defined as a list of dicts."%devs
            assert ('name' in device) and isinstance(device['name'], str), \
                    "All elements of '%s' must have key 'name'."%devs
            # update the device dictionary with useful keys
            dev = dict({**device, 'labExperiment':labExperiment})
            # get the specified class, or use the default 'Device' class
            classname = device.get('type', 'Device')
            self.Devices[device['name']] = imports.get_class(classname)(**dev)

        
        # create the distances array
        #self.distances = np.array([x-y for device in ])
        

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
    


    def moveDevice(self, name, movement):
        for i in range(len(self.optics)):
            if name == self.optics[i].name:
                ID = i
        device = self.optics[ID]
        stage = createStage(device)
        stage.goto(movement)
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






    def closeLab(self, ):
        # disconnect and shut off the camera
        self.Camera.disconnect()
        # change the current on the laser to zero
        self.Laser.changeCurrent(0, self.laser.specs['channel'])
        # turn off and disconnect the laser
        self.Laser.disbale()
    
    def runSimulation(self, **specs):
        
        pass