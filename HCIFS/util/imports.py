import os.path
import glob
import pkgutil
import importlib
import imp
import ast
import inspect

def get_folder(folder=''):
    """Get the path to a specific HCIFS module folder. Defaults to HCIFS GitHub repository.
    """
    assert isinstance(folder, str), "'folder' must be defined as a string."
    
    # get path to the HCIFS GitHub repository
    HCIFS_path = importlib.import_module('HCIFS').__path__[0]
    root_path = os.path.join(os.path.dirname(HCIFS_path), '')
    
    # find all module directories named after folder
    paths = glob.glob(os.path.join(root_path + '/**/', folder), recursive=True)
    if not paths:
        raise IndexError("'%s' is not a valid HCIFS directory."%folder)
    
    # choose the first directory
    path = os.path.join(paths[0], '')
    
    return path

def get_full_modname(pypath=''):
    """Get the full module name of a python file (*.py).
    """
    assert isinstance(pypath, str), "'pypath' must be defined as a string."
    
    # first expand ~/..., $HOME/..., etc.
    pypath = os.path.normpath(os.path.expandvars(os.path.expanduser(pypath)))
    if not (os.path.isfile(pypath) and pypath[-3:].lower() == '.py'):
        raise ValueError("Not an existing python file (*.py): '%s'."%pypath)
    
    # package (modname/__init__.py) or module (modname.py)?
    basename = os.path.basename(pypath)
    path = os.path.dirname(pypath) if basename == '__init__.py' else pypath[:-3]
    
    # create full module name
    root_path = get_folder()
    full_modname = path.replace(root_path, '').replace('/', '.') if root_path \
                in path else os.path.basename(path)
    
    return full_modname

def get_module(modname, folder=''):
    """Get an HCIFS module, from an optional folder.
    """
    assert modname and isinstance(modname, str), "'modname' must be defined as a non-empty string."
    
    # case 1: modname is given as a path to a *.py file
    if modname.endswith('.py'):
        # expand ~/..., $HOME/..., etc.
        pypath = os.path.normpath(os.path.expandvars(os.path.expanduser(modname)))
    
    # case 2: modname is the name of a module or package
    else:
        # locate the optional folder, defaults to HCIFS GitHub repository
        path = get_folder(folder)
        # in the given folder, locate the desired module
        for fp, mn, _ in pkgutil.walk_packages([path]):
            if mn.endswith(modname):
                full_path = fp.path
                break
        else:
            raise RuntimeError("Could not find '%s' module%s" \
                    %(modname," in '" + folder + "' folder." if folder else '.'))
        # find the module pyfile
        pypath = os.path.join(full_path, modname + '.py')
        # if the module is a package, get the __init__ pyfile
        if not os.path.isfile(pypath):
            pypath = os.path.join(full_path, modname + '/__init__.py')
    
    # get the full module name
    full_modname = get_full_modname(pypath)
    # finally, load the module
    module = imp.load_source(full_modname, pypath)
    
    return module

def get_class(classname, modname='', **specs):
    """Get an HCIFS class, from an optional module or package.
    """
    assert classname and isinstance(classname, str), "'classname' must be defined as a non-empty string."
    
    # load the optional module
    if any(modname):
        module = get_module(modname)
        desired_class = getattr(module, classname, None)
        # return the desired class
        if inspect.isclass(desired_class):
            return desired_class
        # if could't find the class, get the path of modname
        path = os.path.dirname(module.__file__)
    else:
        # if no modname, get the root path
        path = get_folder()
    
    # examine all modules from path, and look for classes
    for filename in glob.iglob(os.path.join(path, '**/*.py'), recursive=True):
        with open(filename,'r') as f:
            p = ast.parse(f.read())
            if classname in [node.name for node in ast.walk(p) if isinstance(node, ast.ClassDef)]:
                module = get_module(filename)
                desired_class = getattr(module, classname, None)
                # return the desired class
                if inspect.isclass(desired_class):
                    return desired_class
    else:
        raise RuntimeError("Could not find '%s' class%s" \
                %(classname, " in '" + modname + "' module." if modname else '.'))



def MakeModuleName(*names): 
    """ 
    Helper function: make a qualified module name
    e.g., ('Devices', 'Sources', 'MCLS1') -> 'Devices.Sources.MCLS1'
    """
    return '.'.join(names)

def Module(name, type=None):
    
    assert hasattr(full_module, module_name), \
            "Module name is incorrect.  This is not a valid EXOSIMS class."
    # extract the particular class from the full module's namespace
    desired_module = getattr(full_module, module_name)
    
    return desired_module


def DictOfModules(devices, labExperiment=False, **specs):
    """
    Creates a dictionary containing all the devices of a type (Sources, Optics,
    Cameras, Stages), and optionnally adds it to an existing dict. 
    
    Each device is an object imported from the module specified by the 
    keyword 'type'. If no module was specified, the object is created with 
    the default module: Sources, Optics, Cameras, Stages.
    """
    
    # check the devices have been defined.
    assert devices in specs, "'%s' not defined in 'specs'."%devices
    listdicts = specs[devices]
    
    # initialize dictionary
    mods = dict()
    # loop through the list of dictionaries
    for ID, device in enumerate(listdicts):
        assert isinstance(device, dict), "'%s' must be defined as list of dicts in the jsonfile."%devices
        assert ('name' in device) and isinstance(device['name'], str), \
                "All elements of '%s' must have key 'name'."%devices
        # get the specified module, or use the default module
        folder = 'HCIFS.' + devices + '.'
        try:
            moduleName = device['type']
            module = import_module(folder + moduleName)
        except:
            moduleName = devices
            module = import_module(folder + moduleName)
        # update the device dictionary with useful keys
        specs = dict({**device, 'ID':ID, 'labExperiment':labExperiment})
        # create the module and add to the dictionary of devices
        mods[device['name']] = getattr(module, moduleName)(**specs)
        
    return mods

