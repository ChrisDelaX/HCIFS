class Motor():
    
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