from HCIFS.util.LabControl import ActiveX
from HCIFS.Device.Camera.Camera import Camera
import numpy as np
import time

class QSIrs61(Camera):
    """
    A class for controlling a QSIrs61 camera
    """
    
    def __init__(self, serialnum = '0', progID = 'QSICamera.CCDCamera', **specs):
        """
        Constructor for the QSIrs61 camera
        Inputs:
            serialnum - used for identifying the correct camera
            progID - used for connecting to camera (string)
        """
        super().__init__(**specs)
        
        self.serialnum = str(specs.get('serialnum', serialnum))
        self.progId = str(specs.get('progID', progID))
    
    def enable(self):
        """
        Enables the camera and sets it up
        """
        if not self.labExperiment:
            super().enable()
        else:
            try:
                # get a connection of the camera
                if self.connection == None:
                    self.connection = ActiveX(self.progID)
                # connect the camera
                if self.connection.query('Connected') == False:
                    print('Connecting camera')
                    self.connection.command('Connected', True)
                else:
                    print('Camera is already connected.')
                # get serial number from the camera
                self.serialnum = self.connection.query('SerialNumber');
                # set specs parameters to the camera
                self.exposureproperties(self.originPix, self.imgSize, self.binPix)
                # open the shutter
                self.shutter(True)
                # sets the current camera as the main camera
                if self.connection.query('IsMainCamera') == False:
                    self.connection.command('IsMainCamera', True)
                # set the correct ccdtemperature
                self.setTemperature(self.temperature)
                # set the shutter priority to electrical
                self.shutterPriotiry(1)
                # set camera gain to self gain
                if self.connection.query('CameraGain') != 1:
                    self.connection.command('CameraGain', 1)
            # handles problems connecting to the camera
            except Exception as ex:
                if ex == AttributeError:
                    print('Lost connection of camera, unplug USB manually!')
                    self.connection = None
                else:
                    raise ex

    def disable(self):
        """
        Disables the camera by disconnecting it from the computer.
        """
        if not self.labExperiment:
            super().disable()
        else:
            # turn off the camera fan
            if self.connection.query('FanMode') != 0:
                self.connection.command('FanMode', 0)
            # disable the CCD cooler
            if self.connection.query('CoolerOn') != False:
                self.connection.command('CoolerOn', False)
            # disconnects camera
            if self.connection.query('Connected') == True:
                self.connection.command('Connected', False)
                    
    def avgImg(self, expTime, numIm, Source = None, Xc = None, Yc = None,
               Rx = None, Ry = None):
        """
        Takes an averaged image with the camera. Uses the exposure
        properties already passed to exposure properties. The current darkCam is used.
        If one is not found, a new one is taken. It also crops the image based
        on the X, Y and R parameters. The defaults for these paramters will keep simply
        not crop the image.
        
        Inputs:
            expTime - the exposure time in seconds for each image taken (num)
            numIm - the number of images to take and then average (num)
            Xc - the x-coordinate of center of the image after it is cropped in pixels (num)
            Yc - the y-coordinate of center of the image after it is cropped in pixels (num)
            Rx - the x radius of the rectangle used for cropping in pixels (num)
            Ry - the y radius of the rectangle used for cropping in pixels (num)
            Source - used only for taking Starlight's dark image (Source)
        
        Outputs:
            image - The averaged image. It's size matches the imgSize attribute (np array)
            saturated - True if image has reached saturation level, False otherwise (bool)
        
        """
        if not self.labExperiment:
            super().avgImg(expTime, numIm, Source = None, Xc = None, Yc = None,
                 Rx = None, Ry = None)
        else:
            if self.connection == None:
                raise Exception('Camera not connected.')
            # if cropping numbers given, whole image is used
            if Xc is None:
                Xc = self.imgSize[0] / 2
            if Yc is None:
                Yc = self.imgSize[1] / 2
            if Rx is None:
                Rx = self.imgSize[0] / 2
            if Ry is None:
                Ry = self.imgSize[1] / 2
            # takes new dark image if needed
            if self.darkCam == None:
                # takes new darkCam
                self.darkCam = self.takeDarkCam(.1, 30, Xc = Xc, Yc = Yc,
                                                Rx = Rx, Ry = Ry )
            elif self.darkCam is 0:
                pass
            elif np.shape(self.darkCam) != self.binnedImgSize:
                # darkCam properties and current image size don't match. Raises an
                # errror
                raise Exception("Provided dark cam image does not have the same "
                                "dimensions as the exposure properties. Change one "
                                "or the other, or take a new dark cam.")
            self.readoutSpeed(1)
            # creates a blank image as a placeholder
            img = np.zeros((int(self.binnedImgSize),
                               int(self.binnedImgSize)), np.int32)
            # takes numIm images and adds them together
            for i in range(numIm):
                img = img + self.exposure(expTime)
            # calculates the average image
            avgImg = img/numIm
            # subtracts the darkCam from the image
            avgImgCorrected = avgImg - self.darkCam
            # crops the image
            avgImgCropped = avgImgCorrected[int(Xc - Rx) : int(Xc + Rx),
                                            int(Yc - Ry) : int(Yc + Ry)]
            # checks to see if image is saturated
            saturated = False
            if np.max(img) >= 30900:
                saturated = True

            return avgImgCropped, saturated

    def exposure(self, expTime):
        """
        Takes an image
        
        Inputs:
            exptime - exposure time in seconds for the image (num)
            
        Outputs:
            image - image captured by camera (numpy array)
        """
        if not self.labExperimetn:
            super().exposure(expTime)
        else:
            # Starts an exposure on the camera
            StartExposure = self.connection.query('StartExposure')
            StartExposure(expTime, self.shutterStatus)
            # Wait for the exposure to complete
            done = self.connection.query('ImageReady')
            while done != True:
                done = self.connection.query('ImageReady')
            # it's a nested tuple of size 2758
            # converts it to  an int32 array (2758, 2208)
            exp = self.connection.query('ImageArray')
            return np.array(exp)

    def exposureproperties(self, originPix, imgSize, binPix):
        """
        Changes the exposure properties of the camera
        
        Input:
            originPix - starting location for the image (tuple len.2)
            imgSize - image size in pixels (tuple len. 2)
            binPix - number of pixels binned together (tuple len. 2)
        """
        if not self.labExperiment:
            super().exposureProperties(originPix, imgSize, binPix)
        else:
            # sends the exposure properties to the camera
            self.connection.command('StartX', originPix[0])
            self.connection.command('StartY', originPix[1])
            self.connection.command('NumX', imgSize[0])
            self.connection.command('NumY', imgSize[1])
            self.connection.command('BinX', binPix[0])
            self.connection.command('BinY', binPix[1])
            # update the camera attributes
            self.imgSize = imgSize
            self.originPix = originPix
            self.binPix = binPix

    def readoutSpeed(self, readout_flag):
        """
        Changes the readout speed of the camera
        
        Inputs:
            readout_flag - 0 high image quality, 1 fast readout (num)
        """
        if not self.labExperiment:
            super().readoutSpeed(readout_flag)
        else:
            # sends the readout speed to the camera
            self.connection.command('ReadoutSpeed', readout_flag)

    def shutter(self, openflag):
        """
        Opens or closes the shutter
        Input:
            openflag - True to open, False to close (bool)
        """
        if openflag == True:
            # Set the camera to manual shutter mode.
            self.connection.command('ManualShutterMode', True)
            # Open the shutter as specified
            self.connection.command('ManualShutterOpen', True)
            self.shutterStatus = True
        elif openflag == False:
            # Set the camera to manual shutter mode
            self.connection.command('ManualShutterMode', True)
            # Close the shutter as specified
            self.connection.command('ManualShutterOpen', False)
            # Set the camera to auto shutter mode
            self.connection.command('ManualShutterMode', False)
            self.shutterStatus = False;
        else:
            raise ValueError('Openflag must be True or False.')

    def shutterPriority(self, shutter_flag):
        """
        Changes the shutter priority of the camera
        
        Inputs:
            shutter_flag - 0 for mechanical, 1 for electrical (num)
        """
        self.connection.command('ShutterPriority', shutter_flag)

    def setTemperature(self, temperature):
        """
        Sets the temperature of the camera's cooler
        
        Inputs:
            temperature - temperature in degrees celsius (num)
        """
        if not self.labExperiment:
            super().setTemperature()
        else:
            if (temperature < -50) or (temperature > 50):
                raise ValueError('Temperature is not in the correct range.')
            # sets the current camera as the main camera
            # turns on the camera fan
            if self.connection.query('FanMode') != 2:
                self.connection.command('FanMode', 2)
            # enable the CCD cooler
            if self.connection.query('CoolerOn') != True:
                self.connection.command('CoolerOn', True)
            # set camera cooling temperature and update ccdtemp attribute
            if self.connection.query('CanSetCCDTemperature') == True:
                self.connection.command('SetCCDTemperature', temperature)
    
    def takeDarkCam(self, expTime, numIm, Source = None, Xc = None, Yc = None,
                    Rx = None, Ry = None, display = False):
        """
        Takes a dark cam. Uses the average image function.
        
        See average image function for inputs and outputs
        
        Inputs:
        display - if True displays the darkCam after it is taken (bool)
        """
        # set the properties necessary to take dark image
        self.shutter(False)
        self.shutterpriority(0)
        self.readoutSpeed(0)
        # take dark image
        self.darkCam = 0
        darkCam = self.avgimg(expTime, numIm, Xc = Xc, Yc = Yc, Rx = Rx,
                              Ry = Ry)
        self.darkCam = darkCam[0]
        # display image if flag is not false
        if display != False:
            import matplotlib.pyplot as plt
            plt.imshow(darkCam)
        return darkCam[0]


