# uses michael leung's pyapt module for controlling thorlabs apt motors
# https://github.com/mcleu/PyAPT
import serial
import win32com.client
from PyAPT.PyAPT import APTMotor
import time

class Control():
    
    def __init__(self):
        self.connection = None
    
    def query(self, attribute):
        """
        gets the value of an attribute given an attribute
        """
        value = getattr(self.connection, attribute)
        return value
    
    def command(self, attribute, *value):
        """
        sets the value of an attribute given the attribute and the value
        """
        request = getattr(self.connection, attribute)
        request(*value)

class PyAPT(Control):
    
    def __init__(self, serial_number, device_type):
        super().__init__()
        self.connection = APTMotor(SerialNum = serial_number,
                                   HWTYPE = device_type)
    def query(self, attribute):
        return super().query(attribute)()

class ActiveX(Control):
    
    def __init__(self, name):
        """
        initiates an activex connection using win32com
        """
        super().__init__()
        self.connection = win32com.client.Dispatch(name)
        
    def sets(self, attribute, value):
        setattr(self.connection, attribute, value)

class SerialPort(Control):
    
    def __init__(self, comPort, baudRate = 115200, byteSize = 8, stopBits = 1):
        """
        initializes a serial port connection and then closes it with the
        defaults or keyword arguments
        """
        super().__init__()
        self.connection = serial.Serial(port = comPort, baudrate = baudRate,
                                        bytesize = byteSize, 
                                        stopbits = stopBits)
        self.connection.close()
        
    
    def query(self, attribute):
        """
        requests the value of an attribute given the attribute
        """
        # opens the serial port connection
        self.connection.open()
        # formats the question
        question = (attribute + '?\r').encode()
        # asks the question and finds out how many characters were written
        queried = self.connection.write(question)
        # determines how many characters are still to be read
        time.sleep(2)
        written = self.connection.in_waiting
        
        response = ""
        # reads all remaining characters except the three end of lien ones
        for i in range(written - 3):
            response += self.connection.read().decode()
        # closes the serial port
        self.connection.close()
        # returns all characters after the ones written by the program
        return response[queried:]
    
    def command(self, attribute, value):
        """
        sets the value of an attribute given the attribute and the value
        """
        # opens the serial port
        self.connection.open()
        # formats the command
        request = (attribute + '=' + str(value) + '\r').encode()
        # writes the command to the serial port
        self.connection.write(request)
        # closes the serial port
        self.connection.close()