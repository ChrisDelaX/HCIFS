from HCIFS.util.LabControl import ActiveX
from HCIFS.Device.Camera.Camera import Camera
import numpy as np
import time

class SXvrh9(Camera):
    """
    A class for controlling an SXvrh9 camera
    """
    def __init__(self, saturation=64000, progID='MaxIm.CCDCamera', ccdtemp = -5, **specs):
        """
        Constructor for the SXvrh9 camera. Uses the parent 'Camera' and 'Device' classes
        Inputs:
            saturation - saturation value for the SXvrh9 (int)
            progID - used for connecting to camera (string)
            ccdtemp - the celsius temperature the camera is set to in (number)
        """
        
        # call the 'Camera' constructor
        super().__init__(**specs)
        
        # ensure image size is correct (instance variables created in 'Camera' constructor
        if self.imgSize[0] > 1392 or self.imgSize[1] > 1040:
            raise ValueError('image size must be less than 1392 X 1040')
        
        # set up time variables
        self.msec = 0.001;
        
        #set up instance variables
        self.saturation = int(specs.get('saturation', saturation)
        self.progID = specs.get('progID', progID)
        self.ccdtemp = int(specs.get('ccdtemp', ccdtemp))
        
        # Connect to the camera
        if self.labExperiment is True:
            from HCIFS.Utils.LabControl import ActiveX
            self.connection = ActiveX(progID)
    
    def enable(self):
        """
        Enables the camera and turns AutoDownload on. It also calls exposure
        properties so that user inputs are sent to the camera
        """
        if not self.labExperiment:
            super().enable()
        else:
            # enables the link to the camera
            self.connection.command('LinkEnabled', True)
            # turns on autodownload, allowing captured images to be sent immediately
            self.connection.command('AutoDownload', True)
            # sets the exposure properties to the correct values
            self.exposureproperties(self.originPix, self.imgSize, self.binPix)
            # turns on the camera cooler
            # TODO: find correct default temp to enable following line
#            self.setTemperature(self.temperature)
            print("'StarlightXpress' is now enabled")
    
    def disable(self):
        """
        Disables the camera by closing the link connecting to it
        """
        if not self.labExperiment:
            super().disable()
        else:
            if self.connection == None:
                raise Exception('Camera not connected.')
            # disables the link to the camera and deletes the connection
            self.connection.command('LinkEnabled', False)
            print("'StarlightXpress' is now disabled'")

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
            # converts cropping numbers to binned pixels
            
            Xc = Xc / self.binPix[0]
            Yc = Yc / self.binPix[1]
            Rx = Rx / self.binPix[0]
            Ry = Ry / self.binPix[1]
            # if cropping numbers given, whole image is used
            if Xc is None:
                Xc = self.binnedImgSize[0] / 2
            if Yc is None:
                Yc = self.binnedImgSize[1] / 2
            if Rx is None:
                Rx = self.binnedImgSize[0] / 2
            if Ry is None:
                Ry = self.binnedImgSize[1] / 2
            # takes new dark image if needed
            if self.darkCam == None:
                assert Source != None, 'Must pass a source to take new dark image'
                # takes new darkCam
                self.darkCam = self.takeDarkCam(.1, 30, Xc = Xc * self.binPix[0],
                          Yc = Yc * self.binPix[1], Rx = Rx * self.binPix[0],
                          Ry = Ry * self.binPix[1])
            elif self.darkCam is 0:
                pass
            elif np.shape(self.darkCam) != self.binnedImgSize:
                # darkCam properties and current image size don't match. Raises an
                # errror
                raise Exception("Provided dark cam image does not have the same "
                                "dimensions as the exposure properties. Change one "
                                "or the other, or take a new dark cam.")
            self.readoutspeed(1)
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
            if np.max(img) >= self.saturation:
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
        if not self.labExperiment:
            super().exposure(expTime)
        else:
            if self.connection == None:
                raise Exception('Camera not connected.')
            # converts exposure time from seconds to milliseconds
            expTimeMS = expTime * self.msec
            # takes a single exposure
            expose = self.connection.query('Expose')
            status = expose(expTimeMS, 1, 0)
            # ensures image was successfully taken
            assert status is True, "Image capture failed."
            # downloads image once the camera has finished
            while self.connection.query('ImageReady') is False:
                time.sleep(0.1)
            exp = self.connection.query('ImageArray')
            # returns the image
            return np.array(exp)

    def exposureProperties(self, originPix, imgSize, binPix):
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
            # sets attributes
            self.originPix = originPix
            self.imgSize = imgSize
            self.binPix = binPix
            # sets binned attributes
            self.binnedOriginPix = (originPix[0] / binPix[0], originPix[1] / binPix[1])
            self.binnedImgSize = (imgSize[0] / binPix[0], imgSize[1] / binPix[1])
            # sends exposure properties to camera
            self.connection.command('StartX', self.binnedOriginPix[0])
            self.connection.command('StartY', self.binnedOriginPix[1])
            self.connection.command('NumX', self.binnedImgSize[0])
            self.connection.command('NumY', imgSize[1])
            self.connection.command('BinX', binPix[0])
            self.connection.command('BinY', binPix[1])
    
    def setTemperature(self, temperature):
        """
        Sets the temperature of the camera's cooler
        
        Inputs:
            temperature - temperature in degrees celsius (num)
        """
        if not self.labExperiment:
            super().setTemperature(temperature)
        else:
            # turns the cooler on
            self.connection.command('CoolerOn', True)
            # sends the new temperature to the camera as a float
            self.connection.command('TemperatureSetpoint', float(temperature))

    def takeDarkCam(self, expTime, numIm, Source = None, Xc = None, Yc = None,
                    Rx = None, Ry = None, display = False):
        """
        Takes a dark cam. Uses the average image function.
        
        See average image function for inputs and outputs
        
        Inputs:
        display - if True displays the darkCam after it is taken (bool)
        """
        # set the properties necessary to take dark image
        self.readoutSpeed(0)
        # turns current of laser to 0
        current = Source.current
        Source.changeCurrent(0)
        #self.exposureproperties((0,0,), (500, 500), (BinX, BinY))
        # take dark image
        self.darkCam = 0
        darkCam = self.avgimg(expTime, numIm, Xc = Xc, Yc = Yc, Rx = Rx,
                              Ry = Ry)
        self.darkCam = darkCam[0]
        # returns current to original value
        Source.changeCurrent(current)
        # displays image if flag is not false
        if display != False:
            import matplotlib.pyplot as plt
            plt.imshow(darkCam)
        return darkCam[0]
