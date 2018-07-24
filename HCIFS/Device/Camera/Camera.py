from HCIFS.Device.Device import Device
import numpy as np

class Camera(Device):
    """
    A dummy class to represent a connected camera
    """
    
    def __init__(self, originPix=[0,0], imgSize=[500,500], binPix=[4,4], 
            ccdtemp=0, darkCam=None, saturation = 50000, **specs):
        """
        Constructor for the camera class. Uses the parent 'Device' class.
        Inputs:
            originPix - the starting position of the image (tuple len.2)
            imgSize - the dimensions of the image (tuple len. 2)
            binPix - the number of pixels for binning (tuple len. 2)
            ccdtemp - the celsius temperature the camera is set to (number)
            darkCam - image used to reduce dark current (np array)
            saturation - saturation value for the QSIrs61 (int)
        """
        
        # call the Device constructor
        super().__init__(**specs)
        
        # load specific Camera attributes
        self.connection = None
        self.originPix = np.array(specs.get('originPix', originPix), dtype = 'int')
        self.imgSize = np.array(specs.get('imgSize', imgSize), dtype = 'int')
        self.binPix = np.array(specs.get('binPix', binPix), dtype = 'int')
        self.ccdtemp = int(specs.get('ccdtemp', ccdtemp))
        self.darkCam = specs.get('darkCam', darkCam)
        self.saturation = int(specs.get('saturation', saturation)
    
    def avgImg(self, expTime, numIm, Xc = None, Yc = None, Rx = None,
               Ry = None, Source = None):
        """
        A dummy function for taking an averaged image with the camera. Uses the exposure
        properties already passed to exposure properties. The current darkCam is used.
        If one is not found, a new one is taken. It also crops the image based
        on the X, Y and R parameters. The defaults for these paramters will keep simply
        not crop the image.
        
        Inputs:
            expTime - the exposure time in seconds for each image taken
            numIm - the number of images to take and then average
            Xc - the x-coordinate of center of the image after it is cropped in pixels
            Yc - the y-coordinate of center of the image after it is cropped in pixels
            Rx - the x radius of the rectangle used for cropping in pixels
            Ry - the y radius of the rectangle used for cropping in pixels
            Source - used only for taking Starlight's dark image
        
        Outputs:
            image - a numpy array containing the image. It's size matches the imgSize attribute
            saturated - True if image has reached camera's saturation level, False otherwise
        
        """
        assert not self.labExperiment, "Can't use 'avgImg' with default 'Camera' class."
        print("Turn 'labExperiment = True' to run the lab.")
        return np.zeros(self.imgSize), False
    
    def exposure(self, exptime):
        """
        Dummy function for taking an image
        
        Inputs:
            exptime - exposure time in seconds for the image
        
        Outputs:
            image - a numpy array with properties corresponding to the values passed to exposureProperties
        """
        assert not self.labExperiment, "Can't use 'exposure' with default 'Camera' class."
        print("Turn 'labExperiment = True' to run the lab.")
        return np.zeros(self.imgSize)

    def exposureProperties(self, originPix, imgSize, binPix):
        """
        A dummy function for changing the exposure properties of the camera
        
        Input:
            originPix - tuple of length two of the starting location for the image
            imgSize - tuple of length two of the image size in pixels
            binPix - tuple of length two of the number of pixels binned together
        """
        # makes sure tuple input is all of length two
        if len(originPix) != 2:
            raise ValueError('Wrong dimension of start position')
        if len(imgSize) != 2:
            raise ValueError('Wrong dimension of picture size')
        if len(binPix) != 2:
            raise ValueError('Wrong dimension of binned pixels')
        # sets attributes to be equal to the input values
        self.originPix = originPix
        self.imgSize = imgSize
        self.binPix = binPix
            
    def readoutSpeed(self, readoutflag):
        """
        Dummy function for changing the readout speed of the camera
        
        Inputs:
            readoutflag - 0 for high image quality, 1 for fast readout
        """
        assert not self.labExperiment, "Can't use 'readoutSpeed' with default 'Camera' class."
        print("Turn 'labExperiment = True' to run the lab.")

    def realTime(self):
        """
        Dummy function for creating a realtime feed of the camera in a separate figure window.
        Pauses execution until the figure is closed.
        """
        if self.labExperiment == True:
            if self.connection == None:
                raise Exception('Camera not connected.')
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
        else:
            raise Exception("Can't use 'realTime' with default 'Camera' class.")
            print("Turn 'labExperiment = True' to run the lab.")

    def setTemperature(self, temperature):
        """
        Dummy function for setting camera's cooler temperature
        
        Inputs:
            temperature - temperature in degrees celsius
        """
        assert not self.labExperiment, "Can't use 'setTemperature' with default 'Camera' class."
        print("Turn 'labExperiment = True' to run the lab.")

    def takeDarkCam(self, expTime, numIm, Source = None, Xc = None, Yc = None,
                Rx = None, Ry = None, display = False):
        """
        Dummy function for taking a dark cam. Uses the average image function.
        
        See average image function for inputs and outputs
        
        Inputs:
            display - if True displays the darkCam after it is taken
        """
        assert not self.labExperiment, "Can't use 'takeDarkCam' with default 'Camera' class."
        print("Turn 'labExperiment = True' to run the lab.")
        return np.zeros(self.imgSize)
