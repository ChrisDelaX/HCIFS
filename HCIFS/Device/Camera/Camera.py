from HCIFS.Device.Device import Device

class Camera(Device):
    """
    A class that represents the camera connected to the
    computer. It has functions for connecting and disconnecting, changing
    settings, and taking images.
    """
    
    def __init__(self, **specs):
        """
        Creates an instance of the Cameras class. The 'name' attribute is the only one 
        that MUST be defined in the scriptfile, e.g., 'DM1', 'SP', 'FPM' (for deformable
        mirror 1, shaped pupil, focal plane mask).
        """
        # call the Device constructor
        super().__init__(**specs)

        self.specs = {'type': None, 'dist2prev': 0, 'name': None,
                      'defaultPosition': (0, 0), 'stageType': None,
                      'stageSerial': 'None'}
        self.handle = None
        
        if self.specs.get('stageType') != None:
            moduleName = self.specs['stageType']
            importName = 'OpticalSystem.MotorStage.' + moduleName
            importlib.import_module(importName)
            stageClass = getattr(importName, moduleName)
            self.stage = stageClass(self.specs['stageSerial'])
            
    def position(self):
        if self.specs.get('stageType') != None:
            self.pos = self.specs.get('stage').position()
            return self.pos
        else:
            return self.specs.get('defaultPosition')
            
    def connect(self):
        """
        Connects the camera, opens the shutter, and sets variables
        to camera defaults.
        """
        pass
    
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
    
    def shutter(self):
        """
        Changes the status of the shutter. If openflag is True, opens the
        shutter. If it is False, closes the shutter.
        """
        if self.handle == None:
            raise Exception('Camera not connected.')
            
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
            darkCam = self.takeDarkCam(.1, 30, self.specs['binPix'][0], 
                                       self.specs['binPix'][1])
        elif reversed(np.shape(darkCam)) != self.specs['imgSize']:
            # darkCam properties and current image size don't match. Raises an 
            # errror
            raise Exception("Provided dark cam image does not have the same "
                            "dimensions as the exposure properties. Change one "
                            "or the other, or take a new dark cam.")
        self.handle.sets('ReadoutSpeed', 1)
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
    
    def exposure(self, exptime):
        """
        Returns an image from the camera with exposure time expTime.
        """
        if self.handle == None:
            raise Exception('Camera not connected.')
        img = np.array()
        return img
    
    def realtime(self):
        """
        Uses the exposure function of this class to display a realitme feed
        of the camera. The feed will end when the figure window is closed.
        """
        if self.handle == None:
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
    
    def readoutspeed(self, readoutflag):
        """
        Changes the readout speed of the camera. 1 for fast readout, 
        0 for high image quality.
        """
        if self.handle == None:
            raise Exception('Camera not connected.')
        
    def shutterpriority(self, shutterflag):
        """
        Changes the shutter priority of the camera. 0 for mechanical, 
        1 for electrical
        """
        if self.handle == None:
            raise Exception('Camera not connected.')
    
    def finalize(self):
        """
        Finalizes the camera by turning off the fan, disbaling the cooler
        and closing the shutter
        """
        if self.handle == None:
            raise Exception('Camera not connected.')
        self.shutter(False)
        self.specs['shutterStatus'] = False
        
    def disable(self):
        """
        Disables the camera by disconnecting it from the computer.
        """
        if self.handle == None:
            raise Exception('Camera not connected.')

