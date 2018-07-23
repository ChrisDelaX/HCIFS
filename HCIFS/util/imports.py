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
        for fp, mn, ispkg in pkgutil.walk_packages([path]):
            if not ispkg and mn.endswith(modname):
                full_path = fp.path
                break
        else:
            # if no module found, look for a package
            for fp, mn, ispkg in pkgutil.walk_packages([path]):
                if ispkg and mn.endswith(modname):
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

