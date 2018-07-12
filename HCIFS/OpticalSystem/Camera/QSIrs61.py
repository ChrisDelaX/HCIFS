from OpticalSystem.Camera import Camera
import numpy as np
import win32com.client
from OpticalSystem.Control import ActiveX

class QSIrs61(Camera):
    """
    A class that represents the camera connected to the
    computer. It has functions for connecting and disconnecting, changing
    settings, and taking images.
    """
    
    def __init__(self, **keywords):
        """
        Creates an instance of the Camera class, and initializes the
        default value.
        """
        defaults = {
                'serialnum': '0', 'shutterStatus': True,'startPos': (0, 0),
                'imgSize': (500, 500), 'binPix': (4, 4), 'ccdtemp': -15,
                'progID': 'QSICamera.CCDCamera', 'newDarkFrame': True,
                'darkCam': None, 'binXiL': 4, 'binEta': 4, 'type': 'QSIrs61'
                }
        self.handle = None
        self.specs = defaults
        self.specs.update(keywords)
        super().__init__(**keywords)
            
    def connect(self):
        """
        Connects the camera, opens the shutter, and sets variables
        to camera defaults.
        """
        super().connect()
        try:
            # get a handle of the camera
            if self.handle == None:
                self.handle = ActiveX(self.specs['progID'])
            # connect the camera
            if self.handle.query('Connected') == False:
                print('Connecting camera')
                self.handle.sets('Connected', True)
            else:
                print('Camera is already connected.')
            # get serial number from the camera
            self.specs['serialnum'] = self.handle.query('SerialNumber');
            # set specs parameters to the camera
            self.exposureproperties(self.specs.get('startPos'), 
                                    self.specs.get('imgSize'), 
                                    self.specs.get('binPix'))
            # open the shutter
            self.shutter(True)
        except Exception as ex:
            if ex == AttributeError:
                print('Lost handle of camera, unplug USB manually!')
                self.handle = None
            elif ex == win32com.client.pywintypes.com_error:
                print('Wrong camera name!')       
            else:
                raise ex
    
    def init(self):
        """
        Turns on the fan and cooler. It also sets the temperature to ccdtemp.
        """
        super().init()
        ccdtemp = self.specs.get('ccdtemp')
        if (ccdtemp < -50) or (ccdtemp > 50):
            raise ValueError('Temperature is not in the correct range.')
        # sets the current camera as the main camera
        if self.handle.query('IsMainCamera') == False:
            self.handle.sets('IsMainCamera', True)
        # turns on the camera fan
        if self.handle.query('FanMode') != 2:
            self.handle.sets('FanMode', 2)
        # enable the CCD cooler
        if self.handle.query('CoolerOn') != True:
            self.handle.sets('CoolerOn', True)
        # set camera cooling temperature and update ccdtemp attribute
        if self.handle.query('CanSetCCDTemperature') == True:
            self.handle.sets('SetCCDTemperature', ccdtemp)
        # set camera gain to self gain
        if self.handle.query('CameraGain') != 1:
            self.handle.sets('CameraGain', 1)
        # set camera shutter priority to electrical
        # 0 for mechanical, 1 for electical
        self.handle.sets('ShutterPriority', 1)
    
    def shutter(self, openflag):
        """
        Changes the status of the shutter. If openflag is True, opens the
        shutter. If it is False, closes the shutter.
        """
        super().shutter()
        if openflag == True:
            # Set the camera to manual shutter mode.
            self.handle.sets('ManualShutterMode', True)
            # Open the shutter as specified
            self.handle.sets('ManualShutterOpen', True)
            self.specs['shutterStatus'] = True
        elif openflag == False:
            # Set the camera to manual shutter mode
            self.handle.sets('ManualShutterMode', True)
            # Close the shutter as specified
            self.handle.sets('ManualShutterOpen', False)
            # Set the camera to auto shutter mode
            self.handle.sets('ManualShutterMode', False)
            self.specs['shutterStatus'] = False;
        else:
            raise ValueError('Openflag must be True or False.')
            
    def exposureproperties(self, startPos, imgSize, binPix):
        """
        Changes the three exposure properties: start position, image size
        and binned pixels based on three command-line arguments.
        """
        super().exposureproperties(startPos, imgSize, binPix)
        # sends the exposure properties to the camera
        self.handle.sets('StartX', startPos[0])
        self.handle.sets('StartY', startPos[1])
        self.handle.sets('NumX', imgSize[0])
        self.handle.sets('NumY', imgSize[1])
        self.handle.sets('BinX', binPix[0])
        self.handle.sets('BinY', binPix[1])
        # update the camera attributes
        self.specs['startPos'] = (self.handle.query('StartX'),
                  self.handle.query('StartY'))
        self.specs['imgSize'] = (self.handle.query('NumX'),
                  self.handle.query('NumY'))
        self.specs['binPix'] = (self.handle.query('BinX'),
                  self.handle.query('BinY'))
    
    def exposure(self, expTime):
        """
        Returns an image from the camera with exposure time expTime.
        """
        super().exposure()
        # Starts an exposure on the camera
        self.handle.command('StartExposure', expTime, self.specs['shutterStatus'])
        # Wait for the exposure to complete
        done = self.handle.query('ImageReady')
        while done != True:
            done = self.handle.query('ImageReady')
        # it's a nested tuple of size 2758
        # converts it to  an int32 array (2758, 2208)
        exp = self.handle.query('ImageArray')
        return np.array(exp)
    
    def readoutspeed(self, readoutflag):
        """
        Changes the readout speed of the camera. 1 for fast readout, 
        0 for high image quality.
        """
        super().readoutspeed()
        # sends the readout speed to the camera
        self.handle.sets('ReadoutSpeed', readoutflag)
        
    def shutterpriority(self, shutterflag):
        """
        Changes the shutter priority of the camera. 0 for mechanical, 
        1 for electrical
        """
        super().shutterpriority()
        # sends the shutter pririty to the camera
        self.handle.sets('ShutterPriority', shutterflag)
    
    def finalize(self):
        """
        Finalizes the camera by turning off the fan, disbaling the cooler
        and closing the shutter
        """
        super().finalize()
        # turn off the camera fan
        if self.handle.query('FanMode') != 0:
            self.handle.sets('FanMode', 0)
        # disable the CCD cooler
        if self.handle.query('CoolerOn') != False:
            self.handle.sets('CoolerOn', False)        
        
    def disable(self):
        """
        Disables the camera by disconnecting it from the computer.
        """
        super().disable()
        # disconnects camera
        if self.handle.query('Connected') == True:
            self.handle.sets('Connected', False)