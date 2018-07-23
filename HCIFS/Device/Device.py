from HCIFS.util.imports import get_module

class Device(object):
    
    def __init__(self, type=None, ID=0, stageTypes=[None,None,None], 
            stageSerials=[None,None,None], labExperiment=False, **specs):
        """
        Creates an instance of the Prototype class within the Device module.
        The 'name' attribute is the only one that MUST be defined in the scriptfile.
        Examples of Source names: 'Star', 'Planet'.
        Examples of Optics names: 'DM1', 'SP', 'FPM' (deformable mirror, shaped pupil, focal plane mask).
        Examples of Camera names: 'FPWC', 'IFS'.
        """
        # default attributes of all devices
        self.name = specs.get('name')                           # device name
        self.type = specs.get('type', type)                     # device type
        self.ID = int(specs.get('ID', ID))                      # identification number
        self.stageTypes = specs.get('stageTypes', stageTypes)   # (motor)stage types (x,y,z)
        self.stageSerials = specs.get('stageSerials', stageSerials)# (motor)stage serials (x,y,z)
        self.labExperiment = bool(specs.get('labExperiment', labExperiment))# lab flag
        
