# Motor - provides basic control of a single Thorlabs LTS 300 motor stage.
#
# Matthew Hasselfield - Nov. 26, 2008
# Revised and tested by He Sun in Princeton HCIL - Sep. 2, 2015
# Revised and converted to Python by Matt Grossman - Jun. 28, 2018
# Brief usage:
#   Connect:
#       motor = Motor
#       sn = 45862339 or sn = 83815669 horiz. or sn = 83815646 vert.
#       motor.connect(sn)
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
# Notes:
#   The motor contains a few useful fields:
#       motor.stage     the activeX object for the Thorlabs control top-leve 
#       motor.ctrl      the activeX object for the stage we're controlling
#       motor.figure    the handle of the hidden figure where our controls live

from matplotlib import pyplot as plt
import win32com.client
import time
help(win32com.client.DispatchWithEvents)
help(win32com.client.DispatchEx)
help(win32com.client.Dispatch)

class Motor:
    
    def __init__(self):
        self.figure = None
        self.stage = None
        self.ctrl = None
        self.motor_id = 0
        self.serial_number = None
        
    def connect(self, sn):
        # create controls
        plt.close('all')
        self.figure = plt.figure(figsize = (650, 450))
        plt.title('Camera Stage APT GUI')
        # start system
        # creates an ActiveX controller for the APT system and starts it
        self.ctrl = win32com.client.Dispatch('MG17SYSTEM.MG17SystemCtrl.1')
        self.ctrl.StartCtrl()
        a, n_motor = self.ctrl.GetNumHWUnits(6,0)
        if n_motor == 0:
            print('No motors found!')
#        if n_motor != 1:
#            print('Wrong number of motors found...')
        self.serial_number = sn
        # creates an ActiveX controller for the specific motor
        self.stage = win32com.client.Dispatch('MGMOTOR.MGMotorCtrl.1')
        # sets the motors serial number so the connection can be established
        self.stage.HWSerialNum = self.serial_number
        # starts the controller for the motor
        self.stage.StartCtrl()
        # Flases the lights on hardware unit so it can be identified
        self.stage.Identify()
        
    def pos(self):
        """
        returns the current position of the motor
        """
        return self.stage.GetPosition_Position(self.motor_id)
    
    def goto_wait(self, position):
        """
        moves the motor to the given position and the program execution stops
        while the motor is moving.
        """
        # sets position the motor will move to next time MoveAbsolute is called
        self.stage.SetAbsMovePos(self.motor_id, position)
        # moves to the position set above and execution pauses until it arrives
        self.stage.MoveAbsolute(self.motor_id, True)
    
    def goto(self, position):
        """
        moves the motor to the given position and the program execution 
        continues while the motor is moving.
        """
        # sets position the motor will move to next time MoveAbsolute is called
        self.stage.SetAbsMovePos(self.motor_id, position)
        # moves to the position set above and execution continues
        self.stage.MoveAbsolute(self.motor_id, False) 
        
    def goto_home(self):
        """
        The motor moves to the zero position
        """
        self.stage.MoveHome(self.motor_id, True)
        
    def stop(self):
        """
        Stops the motor where it is
        """
########### not working in original code
        self.stage.StopProfiled(self.motor_id)
        pass
    
    def get_vel(self):
        """
        returns the current max velocity setting of the motor
        """
        # gets the current velocity parameters
        status, min_v, accel, max_v = self.stage.GetVelParams(self.motor_id,
                                                              0,0,0)
        # returns the current maximum velocity
        return max_v
    
    def set_vel(self, new_max_vel, *args):
        """
        Sets a new max velocity for the motor. An optional second argument will
        change the minimum velocity
        """
        # gets the current velocity parameters
        status, min_v, accel, max_v = self.stage.GetVelParams(self.motor_id, 
                                                              0, 0, 0)
        # changes the minimum velocity if one optional argument is used 
        if len(args) == 1:
            min_v = args[0]
        elif len(args) > 1:
            print('Wrong number of input arguments!')
        # updates the velocity parameters    
        self.stage.SetVelParams(self.motor_id, min_v, accel, new_max_vel)
            
    def get_accel(self):
        """
        returns the current acceleration setting of the motor
        """
        # gets the current velocity parameters
        status, min_v, accel, max_v = self.stage.GetVelParams(self.motor_id, 
                                                              0, 0, 0)
        # returns the acceleartion
        return accel
        
    def set_accel(self, new_accel):
        """
        sets a new acceleration setting for the motor
        """
        # gets the current velocity parameters
        status, min_v, accel, max_v = self.stage.GetVelParams(self.motor_id, 
                                                              0, 0, 0)
        # updates the acceleration
        self.stage.SetVelParams(self.motor_id, min_v, new_accel, max_v)
        
    def wait_free(self, *args):
        while abs(self.pos() - args[0]) < args[1]:
            time.sleep(0.1)
        return self.pos()
        
    def cleanup(self):
        """
        Closes both ActiveX controllers
        """
        self.ctrl.StopCtrl()
        self.stage.StopCtrl()
    def changeFocalPlaneMask(self, num):
        if num == 1:
            pass
        elif num == 2:
            pass
        elif num == 3:
            pass
        elif num == 4:
            pass
        elif num == 5:
            pass
        elif num == 6:
            pass
        elif num == 7:
            pass
        elif num == 8:
            pass
        elif num == 9:
            pass
        else:
            raise Exception("Focal Plane Mask number must be 1 - 9.")