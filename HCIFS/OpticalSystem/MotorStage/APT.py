from OpticalSystem.MotorStage.Motor import Motor
from OpticalSystem.Control import PyAPT

class APT(Motor):
    
    def __init__(self, serial_number):
        super().__init__()
        self.specs = {'serial_number': None, 'HWTYPE': 42}
        self.specs['serial_number'] = serial_number

    def connect(self):
        """
        connects the camera and gets current position, velocity, and acceleration
        """
        # connects to the camera
        self.handle = PyAPT(self.specs['serial_number'], self.specs['HWTYPE'])
        
        # makes sure max position is set to 30
        info = self.handle.query('getStageAxisInformation')
        info[1] = 30.0
        self.handle.command('setStageAxisInformation', info)
        
        super().connect()
        
    def position(self):
        """
        returns the current position of the stage
        """
        super().position()
        return self.handle.query('getPos')
    
    def goto(self, position):
        """
        moves the stage to position
        """
        self.handle.command('mAbs', position)
        super().goto(position)
    
    def gotoHome(self):
        """
        moves the stage to its home position
        """
        self.handle.query('go_home')
        super().gotoHome()
        
    def get_vel(self):
        """
        gets the current max velocity of the stage
        """
        super().get_vel()
        return self.handle.query('getVel')
    
    def set_vel(self, velocity):
        """
        sets the max velocity of the stage to velocity
        """
        self.handle.command('setVel', velocity)
        super().set_vel(velocity)
    
    def get_accel(self):
        """
        gets the current acceleration of the stage
        """
        super().get_accel()
        return self.handle.query('getVelocityParameters')[1]
    
    def set_accel(self, acceleration):
        """
        sets the accleration of the stage to accleration
        """
        # get current velocity parameters
        params = self.handle.query('getVelocityParameters')
        # update acceleration paramter
        params[1] = acceleration
        # change the paramters
        self.handle.command('setVelocityParameters', *params)
        super().set_accel(acceleration)
    
    def cleanup(self):
        """
        releases the connection to the stage
        """
        super().cleanup()
        self.handle.query('cleanUpAPT')
        
