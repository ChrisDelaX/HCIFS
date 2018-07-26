from HCIFS.util.imports import get_module
import astropy.units as u

class Device(object):
    
    def __init__(self, device='Device', ID=0, labExperiment=False, position=[0,0,0], 
            stageTypes=[None,None,None], stageSerials=[None,None,None], **specs):
        """
        Creates an instance of the Prototype class within the Device module.
        The 'name' attribute is the only one that MUST be defined in the scriptfile.
        Examples of Source names: 'Star', 'Planet'.
        Examples of Mask names: 'SP', 'FPM' (shaped pupil, focal plane mask).
        Examples of Camera names: 'FPWC', 'IFS'.
        """
        
        # default attributes of all devices
        self.name = specs.get('name')                              # device name
        assert self.name != None, "Must provide a name"
        self.device = specs.get('device', device)                        # device type
        self.ID = int(specs.get('ID', ID))                         # identification number
        self.labExperiment = bool(specs.get('labExperiment', labExperiment))# lab flag
        self.position = specs.get('position', position)*u.mm       # default device position
        # loop through axes x,y,z, look for any stages, and get real position
        self.stageTypes = specs.get('stageTypes', stageTypes)      # (motor)stage types (x,y,z)
        self.stageSerials = specs.get('stageSerials', stageSerials)# (motor)stage serials (x,y,z)
        for i, (stageType, serial) in enumerate(zip(self.stageTypes, self.stageSerials)):
            # get the specified module, or use the default 'Stage' module
            stageType = stageType if stageType is not None else 'Stage'
            # enable the Stage, get the position, then disable the Stage
            module = get_module(stageType, 'Stage')
            stagespecs = {'stageType':stageType, 'serial':serial, 'labExperiment':self.labExperiment}
            Stage = getattr(module, stageType)(**stagespecs)
            self.position[i] = Stage.pos
            Stage.disable()
    
    def enable(self):
        assert not self.labExperiment, "Can't 'enable' with a default device class."
        print("Turn 'labExperiment = True' to enable a Device.")
    
    def disable(self):
        pass