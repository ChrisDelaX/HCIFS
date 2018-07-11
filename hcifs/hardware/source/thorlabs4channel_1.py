# Laser - provides basic control of ThorLabs 4-Channel Fiber-Coupled Laser Source
#
# Matthew Grossman from Princeton HCIL - Jun. 5, 2018
# Based on a Matlab function developed by He Sun
#Brief Usage:
#    To enable the laser:
#       # specs is an optional dictionary of default values to change
#        laser = Laser(specs) 
#        laser.enable()
#    To disable the laser:
#        laser.disable()
#    To get the status of the laser:
#        status = laser.status
#    To change the current of the laser:
#        laser.changeCurrent(current, channel)
#        # Channel   |   Max Current
#        # 1         |   68.09
#        # 2         |   63.89
#        # 3         |   41.59
#        # 4         |   67.39
#    To calibrate the laser:
#        center, secondary = laser.calibrate(image, length, camera)
#       # length defines the size of the area that is searched for a guassian
#       # length = 10 seems to work. camera is the an isntance of Camera class 

import serial as s
import time
from ImageProcessing import fit_gauss_2D
import numpy as np

class Laser:
    
    def __init__(self, **keywords):
        """
        Creats an instance of the Laser class. Creates a port attribute to
        hold the connection to the laser.
        """
        defaults = {
                'port': 'COM3', 'baudrate': 115200, 'bytesize': 8,
                'stopbits': 1, 'current': 50, 'channel': 1, 
                'lengthOfCalibrationArea': 10
                }
        self.specs = defaults
        self.specs.update(keywords)
        # connects to the laser
        self.port = s.Serial(port = self.specs['port'], 
                             baudrate = self.specs['baudrate'], 
                             bytesize = self.specs['bytesize'],
                             stopbits = self.specs['stopbits'])
        self.port.close()
    def enable(self):
        """
        Enables the laser.
        """
        # opens the serial port
        self.port.open()
        # turns the system on by writing to the port
        self.port.write('system=1\r'.encode('utf-8'))
        print('Laser is now enabled')
        # closes the port
        self.port.close()
        time.sleep(3)
        
    def disbale(self):
        """
        Disables the laser.
        """
        # opens the serial port
        self.port.open()
        # turns off the channels and disconnects the laser
        self.port.write('enable=0\r'.encode('utf-8'))
        self.port.write('system=0\r'.encode('utf-8'))
        print('Laser is now disabled')
        # closes the port
        self.port.close()
        time.sleep(3)
        
    def status(self):
        """
        Gets the status of the laser and returns it.
        """
        # opens the serial port
        self.port.open()
        # asks the laser's status
        self.port.write('statword?\r'.encode('utf-8'))
        time.sleep(2)
        # reads in the status one bit at a time
        statword = ""
        while self.port.in_waiting > 0:
            statword += str(self.port.read(1))
        time.sleep(1)
        # closes the port
        self.port.close()
        return statword
    
    def changeCurrent(self, current, channel):
        """
        Chagces the current (in mA) of a specific channel of the laser
        """
        # opens the serial port
        self.port.open()
        
        # sets the max current level
        if channel == 1:
            max_current = 68.09
        elif channel == 2:
            max_current = 63.89
        elif channel == 3:
            max_current = 41.59
        elif channel == 4:
            max_current = 67.39
        else:
            print('No Way! channel shall be 1, 2, 3, or 4 only!')
            max_current = 0
        # checks to make sure the new current is below the max current and 
        # then sets the new current on the correct channel
        if current > max_current:
            print('No Way! current must be less than ' + max_current + ' mA only.')
        elif current == 0:
            # sets the channel
            self.port.write(('channel=' + str(channel) + '\r').encode('utf-8'))
            time.sleep(2)
            # turns off the channel because currrent = 0
            self.port.write('enable=0\r'.encode('utf-8'))
            time.sleep(1)
        else:
            # changes the channel
            self.port.write(('channel=' + str(channel) + '\r').encode('utf-8'))
            self.specs['channel'] = channel
            time.sleep(2)
            # turns on the correct channel
            self.port.write(('enable=' + str(channel) + '\r').encode('utf-8'))
            time.sleep(2)
            # changes the current on the channel
            self.port.write(('current=' + str(current) + '\r').encode('utf-8'))
            self.specs['current'] = current
            time.sleep(1)
        # closes the serial port
        self.port.close()
    
    def calibrate(self, camera):
        """
        Calibrates the laser so that the central peak is overasaturated, and
        the second peaks are just below saturated. It then returns two tuples
        with the x and y coordinates and the intensity for first the central
        peak and then the secondary one
        """
        length = self.specs['length']
        SATURATION =30900
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
        while intensity < .7 * SATURATION or intensity > .8 * SATURATION:
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
        return (centerX, centerY, newCenterPeak), (secondX, secondY, newSecondPeak)