import numpy as np
import importlib
import astropy.units as u



class OpticalSystem(object):
    """
    Attributes:
        lam (astropy Quantity):
            Central wavelength in units of nm
    """
    def __init__(self, labExperiment=False, Source=None, Optics=None, Camera=None,\
            type=None, lam=635, dist2prev=100, **specs):
        
        # load attributes from specs
        print(Source)
        self.Source = Source
        self.Optics = Optics
        self.Camera = Camera
        
        # create object attributes
        self.Source = self.getModule('Source')
#        self.Optics = self.getModule('Optics')
#        self.Camera = self.getModule('Camera')
        

    def getModule(self, name):
        """
        Creates a list of objects corresponding to the list of dictionaries 
        stored in the OpticalSystem attribute 'name' (e.g. Source, Optics, Camera). 
        Each dictionary is replaced by an object, by importing the module specified 
        in the element 'type'. If no module was specified, the object is created with 
        the default module called 'name' (Source, Optics, Camera). 
        """
        listdicts = getattr(self, name)
        assert listdicts, "'%s' not defined."%name
        
        # initialize a list of objects
        atts = []
        # loop through the list of dictionaries
        for natt, att in enumerate(listdicts):
            print(att)
            assert isinstance(att, dict), "'%s' must be defined as list of dicts in the jsonfile."%name
            assert att.has_key('name') and isinstance(att['name'], basestring), \
                    "All elements of '%s' must have key 'name'."%name
            # get the specified module, or use the module 'name' by default
            folder = 'HCIFS.OpticalSystem.' + name + '.'
            try:
                moduleName = att['type']
                module = importlib.import_module(folder + moduleName)
            except:
                moduleName = name
                module = importlib.import_module(folder + moduleName)
            # add the created object to the list
            atts.append(getattr(module, name)(**att))
        
        return atts

            # loop through all optics (must have one defined)
#             self.distances = np.array([])
#             for nopt, opt in enumerate(self.optics):
# 
#                 # load methods from module
#                 importName = 'HCIFS.OpticalSystem.Optics.'
#                 try:
#                     moduleName = opt['type']
#                     importlib.import_module(importName + moduleName)
#                 except:
#                     moduleName = 'Optics'
#                     importlib.import_module(importName + moduleName)
#                 opt = getattr(importName, moduleName)(opt)
#                 
#                 # if it is the first optics, store its focal length in distances.
#                 if nopt == 0:
#                     assert opt['focal'] != 0, "First optics must have a focal length."
#                     self.distances = np.append(distances, opt.dist2next)
#                 # store the distance to next optics in the distances array.
#                 self.distances = np.append(distances, opt.dist2next)
#                 




