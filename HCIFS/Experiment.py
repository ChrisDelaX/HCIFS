#from Hardware.Camera import Camera
#from Hardware.Laser import Laser
#from Hardware.Motor import Motor
import os.path, json, inspect, glob
from HCIFS.util.imports import get_module
import numpy as np
import astropy.units as u


class Experiment(object):
    
    def __init__(self, jsonfile=None, labExperiment=False, nbIter=30, **specs):
    
        # ensure JSON filename extension
        if jsonfile[-5:].lower() != '.json':
            jsonfile = jsonfile + '.json'
        # ensure JSON file location
        if not os.path.isfile(jsonfile):
            jsonfile = os.path.join(os.path.split(inspect.getfile(self.__class__))[0], \
                    'script', jsonfile)
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
        
        # load the labExperiment flag
        self.labExperiment = bool(specs.get('labExperiment', labExperiment))
        
        # check format of the Devices list of dictionaries from specs
        assert 'Devices' in specs, "Devices not defined in specs."
        devs = specs['Devices']
        assert isinstance(devs, list) and all([isinstance(dev, dict) for dev in devs]), \
                "Devices must be defined as a list of dicts."
        assert all('name' in dev for dev in devs), "Each Device must have key 'name'."
        assert len(devs) == len(set(dev['name'] for dev in devs)), \
                "All Devices must have a unique name."
        
        # create the Devices dictionary of modules (Source, Camera, DM, Mask, ...)
        self.Devices = dict()
        for ID, dev in enumerate(devs):
            # create device dictionary with additional useful keys
            devspecs = dict({**dev, 'ID':ID, 'labExperiment':labExperiment})
            # get the specified module, or use the default 'Device' module
            modname = dev.get('device', 'Device')
            module = get_module(modname)
            self.Devices[dev['name']] = getattr(module, modname)(**devspecs)
        
        # create the distance-to-previous arrays for both FPWC and IFS loops
        # default loop: all devices sorted by ID, with distances equal zero
        default =[[dev.name for dev in sorted(self.Devices.values(), \
                key=lambda dev: dev.ID)], [0]*len(self.Devices)]
        self.dist2prev_Imag = specs.get('dist2prev_Imag', default).copy()
        self.dist2prev_Spec = specs.get('dist2prev_Spec', default).copy()
        # set the units to mm
        self.dist2prev_Imag[1] *= u.mm
        self.dist2prev_Spec[1] *= u.mm

    def closeLab(self):
        """ Disconnect all devices from the lab. 
        """
        for dev in self.Devices.values():
            dev.disable()

    def moveStage(self, name, movement):
        """Check for motorized stages on a device, then change the position of the 
        device by introducing a relative movement in x,y,z.
        """
        # get device, stage types, and stage serials
        dev = self.Devices[name]
        stages = dev.stageTypes
        serials = dev.stageSerials
        # loop through axes x,y,z
        for i, (mvt, stage, serial) in enumerate(zip(movement, stages, serials)):
            # for each axis, check if there is any movement, and change position
            if mvt != 0:
                dev.position[i] += mvt
                # get the specified module, or use the default 'Stage' module
                stage = stage if stage is not None else 'Stage'
                # enable the Stage, move the Device, then disable the Stage
                module = get_module(stage, 'Stage')
                stagespecs = {'stageType':stage, 'serial':serial, 'labExperiment':self.labExperiment}
                Stage = getattr(module, stage)(**stagespecs)
                Stage.move(mvt)
                Stage.disable()
                # if device moves along z axis, update the dist2prev arrays
                if i == 2:
                    # FPWC loop
                    for i, devname in enumerate(self.dist2prev_Imag[0]):
                        if devname == name:
                            self.dist2prev_Imag[1][i] += mvt
                            if i < len(self.dist2prev_Imag[0]) - 1:
                                self.dist2prev_Imag[1][i+1] -= mvt
                    # IFS loop
                    for i, devname in enumerate(self.dist2prev_Spec[0]):
                        if devname == name:
                            self.dist2prev_Spec[1][i] += mvt
                            if i < len(self.dist2prev_Spec[0]) - 1:
                                self.dist2prev_Spec[1][i+1] -= mvt
    
    def turnWheel(self, name, number):
        """
        Check for wheel on a device, then rotate the wheel to the correct number
        
        Inputs:
            name - the name of the device with an attached wheel (str)
            number - the position to rotate the wheel to (int)
        """
        
        # get the device, wheel type, and the wheel's port
        dev = self.Devices[name]
        FWtype = dev.FWtype
        FWport = dev.FWport
        # creates a wheel object
        module = get_module(FWtype, 'FilterWheel')
        wheelspecs = {'port': FWport, 'labExperiment': self.labExperiment}
        FilterWheel = getattr(module, FWtype)(**wheelspecs)
        # changes the filter
        FilterWheel.setFilter(number)
        # corrects source's lamda and bandwidth if necessary
        devMax = dev.lam + dev.bandwidth / 2
        devMin = dev.lam - dev.bandwidth / 2
        filterMax = FilterWheel.lam + FilterWheel.bandwidth / 2
        filterMin = FilterWheel.lam  - FilterWheel.bandwidth / 2
        newMax = min([devMax, filterMax])
        newMin = max([devMin, filterMin])
        assert newMin <= newMax, "Filter selection would block all light"
        dev.bandwidth = newMax - newMin
        dev.lam = newMin + dev.bandwidth / 2
        

    def runFPWC(self, mode):
        
        # connect the camera
        self.Camera.connect()
        # initiate the camera
        self.Camera.init()
        # enable the laser
        self.Laser.enable()
        # change the focal plane mask
        # calibrate the laser
        center, secondary = self.Laser.calibrate()

    def getDataCube(self):
        
        pass