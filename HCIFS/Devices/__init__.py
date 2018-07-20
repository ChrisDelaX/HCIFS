from HCIFS import Device

class Mask(Device):
    """Example: Shaped Pupil, Focla Plane Mask.
    """
    pass

class DM(Device):
    """Deformable Mirrors
    """
    pass

class Source(Device):
    
    def __init__(self, npixCalib=10, **specs):
        
        super().__init__(**specs)
        
        # default attributes specific to Sources
        self.npixCalib = int(specs.get('npixCalib', npixCalib)) # length of calibration area
    
    def enable(self):
        """
        Enables the source.
        """
        assert not self.labExperiment, "Can't 'enable' with default 'Sources' module."
        print("Turn 'labExperiment = True' to run the lab.")
    
    def disable(self):
        """
        Disables the source.
        """
        assert not self.labExperiment, "Can't 'disable' with default 'Sources' module."
        print("Turn 'labExperiment = True' to run the lab.")
    
    def status(self):
        """
        Gets the status of the source and returns it.
        """
        assert not self.labExperiment, "Can't use 'status' with default 'Sources' module."
        print("Turn 'labExperiment = True' to run the lab.")
        return 'no status'
    
    def changeCurrent(self, current):
        """
        Changes the current (in mA) of a specific channel of the source
        """
        assert not self.labExperiment, "Can't 'change current' with default 'Sources' module."
        print("Turn 'labExperiment = True' to run the lab.")
    
    def calibrate(self, camera):
        """
        Calibrates the source so that the central peak is overasaturated, and
        the second peaks are just below saturated. It then returns two tuples
        with the x and y coordinates and the intensity for first the central
        peak and then the secondary one
        """
        centerX, centerY, newCenterPeak = 0, 0, 0
        secondX, secondY, newSecondPeak = 0, 0, 0
        return (centerX, centerY, newCenterPeak), (secondX, secondY, newSecondPeak)


class Stage(Device):
    
    def __init__(self):
        self.specs = {}
        self.pos = None
        self.handle = None
        self.vel = None
        self.accel = None
        
    def connect(self):
        """
        connects the camera and gets current position, velocity, and acceleration
        """
        self.pos = self.position()
        self.vel = self.get_vel()
        self.accel = self.get_accel()
    def position(self):
        """
        returns the current position of the stage
        """
        return 0
    
    def goto(self, position):
        """
        moves the stage to position
        """
        self.pos = self.position()
    
    def gotoHome(self):
        """
        moves the stage to its home position
        """
        self.pos = self.position()
        
    def get_vel(self):
        """
        gets the current max velocity of the stage
        """
        return 0
    
    def set_vel(self, velocity):
        """
        sets the max velocity of the stage to velocity
        """
        self.vel = self.get_vel()
    
    def get_accel(self):
        """
        gets the current acceleration of the stage
        """
        return 0
        
    def set_accel(self, acceleration):
        """
        sets the accleration of the stage to accleration
        """
        self.accel = self.get_accel()
    
    def cleanup(self):
        """
        releases the connection to the stage
        """
        pass
        
        

class Camera(Device):
    """
    A class that represents the camera connected to the
    computer. It has functions for connecting and disconnecting, changing
    settings, and taking images.
    """
    
    def __init__(self, type=None, ID=0, stageTypes=[None,None,None], 
            stageSerials=[None,None,None], **specs):
        """
        Creates an instance of the Cameras class. The 'name' attribute is the only one 
        that MUST be defined in the scriptfile, e.g., 'DM1', 'SP', 'FPM' (for deformable
        mirror 1, shaped pupil, focal plane mask).
        """

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

class FilterWheel(Device):
    
    def __init__(self, **keywords):
        """
        Creats an instance of the FilterWheel class. Creates a port attribute to
        hold the connection to the filter wheel.
        """
        self.specs = {}
        self.port = None
        self.position
        
    def getPosition(self):
        """
        Gets the current position of the filter wheel
        Returns an integer from 1 - 12
        """
        self.position = 0
        return self.position
    
    def setPosition(self, position):
        """
        Changes the position of the filter wheel
        pos must be an integer from 1 - 12
        """
        self.position = position
    
    def moveUp(self):
        """
        Moves the filterwheel up one position
        """
        currentPosition = int(self.getPosition())
        if currentPosition == 12:
            currentPosition = 0
        self.setPosition(currentPosition + 1)
        self.position = currentPosition + 1
        
    def moveDown(self):
        """
        Moves the filterwheel down one position
        """
        currentPosition = int(self.getPosition())
        if currentPosition == 1:
            currentPosition = 13
        self.setPosition(currentPosition - 1)
        self.position = currentPosition - 1