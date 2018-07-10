# Camera - provides basic control of QSI RS 6.1s CCD camera
#
# Matthew Grossman from Princeton HCIL - Jun. 5, 2018
# Based on a Matlab function developed by He Sun
#
#Brief Usage:
#    Connect the camera:
#       camera = Camera()
#       camera.name = 'QSICamera.CCDCamera'
#       camera.connect()
#    Disconect the camera:
#       camera.disconnect()
#       # Runs the finalize and disable functions
#    Setup the camera:
#       camera.setup()
#    Initilialization:
#        camera.init()
#    Stop fan and cooler:
#        camera.finalize()
#    Disable the camera:
#        camera.disable()
#    Open or close shutter:
#        camera.shutter(openflag) 
#        # openflag: True for open, False for close
#    Set readout speed:
#        camera.readoutspeed(readoutflag)
#        # readout flag: 1 for fast readout, 0 for high image quality
#    Exposure properties:
#        camera.exposureproperties(startPos, imgSize, bunPix)
#            # the last three inputs are all tuples with default values of 
#            # (0,0), (2758, 2208), and (1,1)
#    Set shutter priority:
#        camera.shutterpriority(shutterflag)
#        # shutterflag: 0 for mechanical, 1 for electrical
#    Take a picture:
#        img = camera.exposure(expTime)
#        # exptime is the exposure time you can change
#    Take an average image:
#        img = camera.avgimg(expTime, numIm)
#        # takes numIm exposures of exposure time expTime and averages them
#    Show camera realtime picture:
#        camera.realtime()
#        # can be used during calibration 

from matplotlib import pyplot as plt
import numpy as np
import win32com.client
import os

class Camera(object):
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
                'name': 'QSICamera.CCDCamera', 'newDarkFrame': True,
                'darkCam': None, 'binXiL': 4, 'binEta': 4
                }
        self.handle = None
        self.specs = defaults
        self.specs.update(keywords)
            
    def connect(self):
        """
        Connects the camera, opens the shutter, and sets variables
        to camera defaults.
        """

        try:
            # get a handle of the camera
            if self.handle == None:
                self.handle = win32com.client.Dispatch(self.specs['name'])
            # connect the camera
            if self.handle.Connected == False:
                print('Connecting camera')
                self.handle.Connected = True
            else:
                print('Camera is already connected.')
            # get serial number from the camera
            self.specs['serialnum'] = self.handle.SerialNumber;
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
                
    def disconnect(self):
        """
        Disconnects the camera and also calls the finalize and disable
        functions in this class.
        """
        if self.handle == None:
            raise Exception('Camera not connected.')
        # close shutter
        self.shutter(False)
        self.finalize()
        self.disable()
        print('Disconnecting camera')
        self.handle = None
    
    def init(self):
        """
        Turns on the fan and cooler. It also sets the temperature to ccdtemp.
        """
        if self.handle == None:
            raise Exception('Camera not connected.')
        ccdtemp = self.specs['ccdtemp']
        if (ccdtemp < -50) or (ccdtemp > 50):
            raise ValueError('Temperature is not in the correct range.')
        # sets the current camera as the main camera
        if self.handle.IsMainCamera == False:
            self.handle.IsMainCamera = True
        # turns on the camera fan
        if self.handle.FanMode != 2:
            self.handle.FanMode = 2
        # enable the CCD cooler
        if self.handle.CoolerOn != True:
            self.handle.CoolerOn = True
        # set camera cooling temperature and update ccdtemp attribute
        if self.handle.CanSetCCDTemperature == True:
            self.handle.SetCCDTemperature = ccdtemp
        # set camera gain to self gain
        if self.handle.CameraGain != 1:
            self.handle.CameraGain = 1
        # set camera shutter priority to electrical
        # 0 for mechanical, 1 for electical
        self.handle.ShutterPriority = 1
    
    def shutter(self, openflag):
        """
        Changes the status of the shutter. If openflag is True, opens the
        shutter. If it is False, closes the shutter.
        """
        if self.handle == None:
            raise Exception('Camera not connected.')
        if openflag == True:
            # Set the camera to manual shutter mode.
            self.handle.ManualShutterMode = True
            # Open the shutter as specified
            self.handle.ManualShutterOpen = True
            self.specs['shutterStatus'] = True
        elif openflag == False:
            # Set the camera to manual shutter mode
            self.handle.ManualShutterMode = True
            # Close the shutter as specified
            self.handle.ManualShutterOpen = False
            # Set the camera to auto shutter mode
            self.handle.ManualShutterMode = False
            self.specs['shutterStatus'] = False;
        else:
            raise ValueError('Openflag must be True or False.')
            
    def exposureproperties(self, startPos, imgSize, binPix):
        """
        Changes the three exposure properties: start position, image size
        and binned pixels based on three command-line arguments.
        """
        if self.handle == None:
            raise Exception('Camera not connected.')
        if len(startPos) != 2:
            raise ValueError('Wrong dimension of start position')
        if len(imgSize) != 2:
            raise ValueError('Wrong dimension of picture size')  
        if len(binPix) != 2:
            raise ValueError('Wrong dimension of binned pixels')
        # sends the exposure properties to the camera
        self.handle.StartX = startPos[0]
        self.handle.StartY = startPos[1]
        self.handle.NumX = imgSize[0]
        self.handle.NumY = imgSize[1]
        self.handle.BinX = binPix[0]
        self.handle.BinY = binPix[1]
        # update the camera attributes
        self.specs['startPos'] = (self.handle.StartX, self.handle.StartY)
        self.specs['imgSize'] = (self.handle.NumX, self.handle.Numy)
        self.specs['binPix'] = (self.handle.BinX, self.handle.BinY)
    
    def avgimg(self, expTime, numIm):
        """
        Uses this class's exposure function to take numIm imgaes of exposure
        time expTime. It then returns the mean of the images.
        """
        darkCam = self.specs['darkCam']
        if self.handle == None:
            raise Exception('Camera not connected.')
        # checks to see if a darkCam has been provided
        if darkCam == None:
            # no darkCam is provided so it takes a new one with current camera
            # settings
            darkCam = self.takeDarkCam(.1, 30, self.binPix[0], self.binPix[1])
        elif reversed(np.shape(darkCam)) != self.imgSize:
            # darkCam properties and current image size don't match. Raises an 
            # errror
            raise Exception("Provided dark cam image does not have the same "
                            "dimensions as the exposure properties. Change one "
                            "or the other, or take a new dark cam.")
        self.handle.ReadoutSpeed = 1
##### ask christain about switching these
        img = np.zeros((self.imgSize[0], self.imgSize[1]), np.int32)
        for i in range(numIm):
            img = img + self.exposure(expTime)
        # output is a float64 (2758, 2208) array
        avgImg = img/numIm
        avgImgCorrected = avgImg - darkCam
        return np.rot90(avgImgCorrected)
    
    def takeDarkCam(self, expTime, numIm, BinX, BinY):
        """
        Takes DarkCam image using avgimg function. It saves the image and then
        returns it
        """
        # get the current directory and set it to folder
        folder = os.getcwd()
        # set the properties necessary to take dark image
        self.shutter(False)
        self.shutterpriority(0)
        self.readoutspeed(0)
        #self.exposureproperties((0,0,), (500, 500), (BinX, BinY))
        # take dark image
        darkCam = self.avgimg(expTime, numIm)
        self.specs['darkCam'] = darkCam
        # save picture
        os.chdir('C:\Lab\HCIL\hardware')
######### confirm format for saving picture and then save it
#        np.savetxt('darkCam.txt', darkCam)
        np.save('darkCam.npy', darkCam)
        os.chdir(folder)
        return darkCam
    
    def exposure(self, expTime):
        """
        Returns an image from the camera with exposure time expTime.
        """
        if self.handle == None:
            raise Exception('Camera not connected.')
        # Starts an exposure on the camera
        self.handle.StartExposure(expTime, self.specs['shutterStatus'])
        # Wait for the exposure to complete
        done = self.handle.ImageReady
        while done != True:
            done = self.handle.ImageReady
        # it's a nested tuple of size 2758
        # converts it to  an int32 array (2758, 2208)
        exp = self.handle.ImageArray
        return np.array(exp)
    
    def realtime(self):
        """
        Uses the exposure function of this class to display a realitme feed
        of the camera. The feed will end when the figure window is closed.
        """
       # creates the figure
        plt.figure(100)
        plt.title('Real Time Picture')
        plt.tight_layout()
        # updates the figure with the current image until the figure is closed
        while plt.fignum_exists(100):
            img = self.exposure(0.0003)
            plt.imshow(img, origin = 'lower')
            cb = plt.colorbar()
            plt.pause(.1)
            cb.remove()
    
    def readoutspeed(self, readoutflag):
        """
        Changes the readout speed of the camera. 1 for fast readout, 
        0 for high image quality.
        """
        if self.handle == None:
            raise Exception('Camera not connected.')
        # sends the readout speed to the camera
        self.handle.ReadoutSpeed = readoutflag
        
    def shutterpriority(self, shutterflag):
        """
        Changes the shutter priority of the camera. 0 for mechanical, 
        1 for electrical
        """
        if self.handle == None:
            raise Exception('Camera not connected.')
        # sends the shutter pririty to the camera
        self.handle.ShutterPriority = shutterflag
    
    def finalize(self):
        """
        Finalizes the camera by turning off the fan, disbaling the cooler
        and closing the shutter
        """
        if self.handle == None:
            raise Exception('Camera not connected.')
        # turn off the camera fan
        if self.handle.FanMode != 0:
            self.handle.FanMode = 0
        # disable the CCD cooler
        if self.handle.CoolerOn != False:
            self.handle.CoolerOn = False
        # closes the shutter
        self.shutter(False)
        self.specs['shutterStatus'] = False
        
    def disable(self):
        """
        Disables the camera by disconnecting it from the computer.
        """
        if self.handle == None:
            raise Exception('Camera not connected.')
        # disconnects camera
        if self.handle.Connected == True:
            self.handle.Connected = False
    
    def setup(self):
        """
        Sets up the camera, after it has been connected by setting the shutter
        priority and exposure properties and taking a new dark frame
        """
        # initializes the camrea and sets its temperature
        self.init(-15)
        # sets the shutter priority
        self.ShutterPriority(1)
        # sets the exposure properties
        self.exposureproperties(self.startPos, self.imgSize, self.binPix)
        # takes a new dark frame, if needed
####### get more details on this
        if self.newDarkFrame == True:
            numIm = 30
            self.darkFrame = self.takeDarkCam(self.expTime, numIm, 
                                              self.binXi, self.binEta)
        else:
            self.darkFrame = np.load('darkCam.npy')
            # use below if numpy format is no good
#            self.darkFrame = np.loadtxt('darkCam.txt')