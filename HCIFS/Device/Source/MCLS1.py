# MCLS1 - provides basic control of ThorLabs 4-Channel Fiber-Coupled Laser Source

from HCIFS.Device.Source.Source import Source
from HCIFS.util.img_processing import fit_gauss_2D
import time
import numpy as np
import astropy.units as u

class MCLS1(Source):
    """
    A class used to control an MCLS1 laser. The laser must be attached to the
    computer through a com port or com-usb connection. The enable method
    must be called before the source can be used.
    """
    def __init__(self, port='COM3', current=0, channel=1, **specs):
        """
        Constructor for the MCLS1 class.
        
        Inputs:
            port: the COM port the MCLS1 is attached to (str)
            current: the default current for the source in mA (int)
            channel: the channel the object controls (1 - 4) (int)
        
        """
        # call the Sources constructor
        super().__init__(**specs)
        
        # load laser attribute values
        self.port = str(specs.get('port', port))                # the port
        self.current = float(specs.get('current', current))     # source current
        self.channel = int(specs.get('channel', channel))       # selected channel (1-4)
        maxCurrent = {1: 68.09, 2: 63.89, 3: 41.59, 4: 67.39}
        self.maxCurrent = maxCurrent[self.channel]              # max current allowed
        lam =  {1: 635, 2: 658, 3: 670, 4: 705}
        self.lam = lam[self.channel]*u.nm                       # wavelength in nm
        
        # connects to and enables the laser
        if self.labExperiment is True:
            from HCIFS.util.LabControl import SerialPort
            self.port = SerialPort(comPort=self.port)
            self.enable()
            
    
    def enable(self):
        """
        Enables the MCLS1.
        
        Turns the system on and then waits for the laser to warm up.
        """
        if not self.labExperiment:
            super().enable()
        else:
            # turns the system on by writing to the port
            self.port.command('system', 1)
            print('Laser is now enabled')
            # closes the port
            time.sleep(2)
    
    def disable(self):
        """
        Disables the MCLS1.
        
        Turns the system off and then waits for the laser to cool off.
        """
        if not self.labExperiment:
            super().disable()
        else:
            # disables the current channel
            self.port.command('enable', 0)
            # turns off the whole system
            self.port.command('system', 0)
            print('Laser is now disabled')
            time.sleep(2)
        
    def status(self):
        """
        Gets the status of the MCLS1.
        
        Outputs: the status of the laser as a binary number of 8 digits
        """
        if not self.labExperiment:
            super().status()
        else:
            # returns the status of the laser
            return self.port.query('statword')

    def changeCurrent(self, current):
        """
        Changes the current of the MCLS1 on the channel associated with  object.
        
        Input: the current in milliAmps
        """
        if not self.labExperiment:
            super().changeCurrent(current)
        else:
            # checks to make sure the new current is below the max current and
            # then sets the new current on the correct channel
            if current > self.maxCurrent:
                print('No Way! current must be less than ' + self.maxCurrent + ' mA only.')
            elif current == 0:
                # sets the channel
                self.port.command('channel', self.channel)
                # turns off the channel because currrent = 0
                self.port.command('enable', 0)
                self.current = current
            else:
                # changes the channel
                self.port.command('channel', self.channel)
                # turns on the correct channel
                self.port.command('enable', self.channel)
                # changes the current on the channel
                self.port.command('current', current)
                self.current = current
    
    def calibrate(self, camera):
        """
        Calibrates the MCLS1 so that the central peak is overasaturated, and
        the second peaks are just below saturated.
        
        It uses a square of sidelength 2 * self.npixCalib centered on the two
        peaks to fit gaussians and get more accurate information.
        
        Inputs: The camera object used for calibration
        
        Output:
            Tuple: (x-coordinate of central peak, y-coordinate of central peak,
                    intensity of the central peak)
            Tuple: (x-coordinate of second peak, y-coordinate of sedond peak,
                    intensity of the second peak)
        """
        length = self.npixCalib
        saturation = camera.saturation
        # sets the current to a low setting for first image
        self.changeCurrent(10, self.specs['channel'])
### get updated values for taking the first pic
        image = camera.avgimg(.1, 3)
        image = np.transpose(image)
        # finds pixel with highest value
        maximum = np.amax(image)
        max_coordinates = np.where(image == maximum)
        ## numpy puts the y-coordinate first so much of this looks reversed
        # finds the maximum valued point which corresponds to largest peak
        y = max_coordinates[0]
        x = max_coordinates[1]
        # finds a gaussian in the square with side-lengths 2*length around the
        # peak pixel
        centerGauss = image[int(y - length) : int(y + length),
                            int(x - length) : int(x + length)]
        centerParams = fit_gauss_2D(centerGauss)
        # gets the location of the peak of the gaussian
        centerY = centerParams[1] + (y - length)
        centerX = centerParams[2] + (x - length)
        # removes the central gaussian from the image
        image[int(y - length) : int(y + length),
              int(x - length) : int(x + length)] = np.zeros((2*length,2*length))
        # finds the new maximum valued points which corresponds to second-order
        # peak
        maximum = np.amax(image)
        max_coordinates = np.where(image == maximum)
        y = max_coordinates[0][0]
        x = max_coordinates[1][0]
        # fits a gaussian to the second-order peak
        secondGauss = image[int(y - length) : int(y + length),
                            int(x - length) : int(x + length)]
        secondParams = fit_gauss_2D(secondGauss)
        # gets the location of the peak of the gaussian
        secondY = secondParams[1] + (y - length)
        secondX = secondParams[2] + (x - length)
        # changes the current to the higher value
        newCurrent = 40
        intensity = 0
        # changes power until the second peak intensity falls within 70-80%
        # of saturation
        counter = 0
        while intensity < .7 * saturation or intensity > .8 * saturation:
            if intensity < .7:
                newCurrent += 5
            else:
                newCurrent -= 2
            # changes the current
            self.changeCurrent(newCurrent, self.specs['channel'])
            # takes a new image on the camera
            newImage = camera.avgImg(.0001, 3)
            # finds the value of the second peak in the new image
            intensity = newImage[int(secondY)][int(secondX)]
            counter += 1
            if counter == 10:
                raise Exception("Laser calibration timeout. Please try again")
        newSecondPeak = intensity
        # finds a scale factor for the intensities
        scale = newSecondPeak / secondParams[0]
        # calculates the newCenterPeak from the scale
        newCenterPeak = newSecondPeak * scale
        return centerX, centerY, newCenterPeak, secondX, secondY, newSecondPeak
