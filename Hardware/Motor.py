# Motor - provides basic control of a single Thorlabs LTS 300 motor stage.
#
# Matthew Hasselfield - Nov. 26, 2008
# Revised and tested by He Sun in Princeton HCIL - Sep. 2, 2015
# Revised and converted to Python by Matt Grossman - Jun. 28, 2018
# Brief usage:
#   Connect:
#       motor = Motor(which, **keywords)
#       which = "h", "v", or "o" to indicate which motor it is
#       keywords are changes to default specs
#       motor.connect()
#   Motion:
#       motor.goto(pos)  # Ranges from 0 to 300
#       motor.goto_wait(pos)  # careful this times out
#       motor.goto_home()
#       motor.stop()
#       current_pos = motor.pos()
#   Velocity and aceleration control:
#       max_vel = motor.get_vel()
#       motor.set_vel(new_max_vel)
#       accel = motor.get_accel()
#       motor.set_accel(new_accel)
#   Clean up:
#       motor.cleanup()
#   Notes:
#       requires APTSystem class to create activex containter for motor

from PyQt5 import QAxContainer
from PyQt5 import QtWidgets
from PyQt5.QtCore import QVariant
import time
import sys
import APTSystem

class Motor():
    
    def __init__(self, which, **keywords):
        
        # get the correct serial number
        if which == "h":
            self.serial_number = 83815669
        elif which == "v":
            self.serial_number = 83815646
        else:
            self.serial_number = 45862339
        
        # creates the active x control to hold the motor
        app = QtWidgets.QApplication(sys.argv)        
        self.control = APTSystem(app)
        self.motor_id = QVariant(0)
    
    def connect(self):
         # required by device

        # args must be list of QVariants
        typ = QVariant(6)
        num = QVariant(0)
        args = [typ, num]

        self.control.dynamicCall('GetNumHWUnits(int, int&)', args)
        if args[1] == 0:
            print("Wrong number of motors found")
        
        # set the serial number of the device
        self.control.dynamicCall('HWSerialNum', self.serial_number)
        # start the control
        self.control.dynamicCall('StartCtrl()')
        self.control.dynamicCall('Identify')
        
    def pos(self):
        """
        returns the current position of the motor
        """
        motor_id = QVariant(0)
        return self.control.dynamicCall('GetPosition_Position(int)', motor_id)
    
    def goto_wait(self, position):
        """
        moves the motor to the given position and the program execution stops
        while the motor is moving.
        """
        position = QVariant(position)
        # sets position the motor will move to next time MoveAbsolute is called
        self.control.dynamicCall('SetAbsMovePos(int, int)', self.motor_id, position)
        # moves to the position set above and execution pauses until it arrives
        self.control.dynamicCall('MoveAbsolute(int, bool)', self.motor_id, QVariant(True))
    
    def goto(self, position):
        """
        moves the motor to the given position and the program execution 
        continues while the motor is moving.
        """
        position = QVariant(position)
        # sets position the motor will move to next time MoveAbsolute is called
        self.control.dynamicCall('SetAbsMovePos(int, int)', self.motor_id, position)
        # moves to the position set above and execution pauses until it arrives
        self.control.dynamicCall('MoveAbsolute(int, bool)', self.motor_id, QVariant(False))
    
    def goto_home(self):
        """
        The motor moves to the zero position
        """
        self.control.dynamicCall('MoveHome(int, bool)', self.motor_id, QVariant(True))
        
    def stop(self):
        """
        Stops the motor where it is
        """
########### not working in original code
        self.control.dynamicCall('StopProfiled(int)', self.motor_id)
        
    def get_vel(self):
        """
        returns the current max velocity setting of the motor
        """
        z = QVariant(0)
        # gets the current velocity parameters
        status, min_v, accel, max_v = self.control.dynamicCall(
                'GetVelParams(int, int,int, int)', self.motor_id, z, z, z)
        # returns the current maximum velocity
        return max_v
    
    def set_vel(self, new_max_vel, *args):
        """
        Sets a new max velocity for the motor. An optional second argument will
        change the minimum velocity
        """
        z = QVariant(0)        
        # gets the current velocity parameters
        status, min_v, accel, max_v = self.control.dynamicCall(
                'GetVelParams(int, int, int, int)', self.motor_id, z, z, z)
        # changes the minimum velocity if one optional argument is used 
        if len(args) == 1:
            min_v = args[0]
        elif len(args) > 1:
            print('Wrong number of input arguments!')
        # converts velocity parameters to QVariants
        min_v = QVariant(min_v)
        accel = QVariant(accel)
        new_max_vel = QVariant(new_max_vel)
        # updates the velocity parameters    
        self.control.dynamicCall('SetVelParams(int, int, int, int)',
                         self.motor_id, min_v, accel, new_max_vel)
    
    def get_accel(self):
        """
        returns the current acceleration setting of the motor
        """
        z = QVariant(0)
        # gets the current velocity parameters
        status, min_v, accel, max_v = self.control.dynamicCall(
                'GetVelParams(int, int,int, int)', self.motor_id, z, z, z)
        # returns the acceleartion
        return accel
    
    def set_accel(self, new_accel):
        """
        sets a new acceleration setting for the motor
        """
        z = QVariant(0)
        # gets the current velocity parameters
        status, min_v, accel, max_v = self.control.dynamicCall(
                'GetVelParams(int, int, int, int)', self.motor_id, z, z, z)
        # converts velocity parametrs to QVariants
        min_v = QVariant(min_v)
        new_accel = QVariant(new_accel)
        max_v = QVariant(max_v)
        # updates the acceleration
        self.control.dynamicCall('SetVelParams(int, int, int, int)',
                         self.motor_id, min_v, new_accel, max_v)
    
    def wait_free(self, *args):
        while abs(self.pos() - args[0]) < args[1]:
            time.sleep(0.1)
        return self.pos()
    
    def cleanup(self):
        """
        Closes the ActiveX controllers
        """
        self.control.dynamicCall('StopCtrl()')