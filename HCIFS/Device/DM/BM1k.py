from HCIFS.Device.DM.DM import DM
import numpy as np
from HCIFS.util.LabControl import BMC

class BM1k(DM):
    """
    Class for controlling each BMC BM1k DMs with 952 actuators in a 2 DM set up
    DM1 serial number: '25CW004#014'
    DM2 serial number: '25CW018#040'
    """
    
    def __init__(self, numAct=952, numActProfile=2048, maxVoltage=185,
                 DMserial=0, **specs):
        """
        BM1k constructor.
        Inputs:
            maxVoltage - the maximum allowable voltage for the DM (int)
            numAct - real number of actuators on DM (int)
            numActProfile - the number of actuators included in the profile (int)
            DMserial - the serial number of the DM (str (11 characters))
        """
        # call the DM constructor
        super().__init__(**specs)
        
        # determine the correct DM
        self.allNums = {'25CW004#014': 1, '25CW018#040': 2}
        self.DMserial = specs.get('DMserial', DMserial)
        self.DMnum = self.allNums.get(self.DMserial, 0)
        
        # load BM1k attributes
        self.connection = BMC()
        self.numActProfile = int(specs.get('numActProfile', numActProfile))
        self.numAct = int(specs.get('numAct', numAct))
        self.maxVoltage = int(specs.get('maxVoltage', maxVoltage))
        
        # get the flatmaps if running an actual experiment
        if self.labExperiment == True:
            assert self.DMnum != 0, 'Must provide a valid serial number when running lab experiment'
            if self.DMnum == 1:
                self.flatMap = np.loadtxt('C:/Program Files/Boston Micromachines/Shapes/C25CW004#14_CLOSED_LOOP_200nm_Voltages_DM#1.txt')
            elif self.DMnum == 2:
                self.flatMap = np.loadtxt('C:/Program Files/Boston Micromachines/Shapes/C25CW018#40_CLOSED_LOOP_200nm_Voltages_DM#2.txt')
    
    def enable(self):
        """
        Connects to the DM and enables it
        """
        if not self.labExperiment:
            super().enable()
        else:
            self.connection.command('open_dm', self.DMserial)
            status = self.connection.query('get_status')
            assert status == 0, 'Error connecting to DM. Error: ' + str(status)
            numActProfile = self.connection.query('num_actuators')
            assert numActProfile == self.numActProfile, 'Wrong number of profile actuators entered'

    def zero(self):
        """
        Zeros the voltage on all actuators
        """
        if not self.labExperiment:
            super().zero()
        else:
            num_actuators = self.connection.query('num_actuators')
            data = np.zeros(num_actuators)
            self.connection.command('send_data', data)
            if self.name is None:
                self.name = 'DM' + self.DMnum
            print(self.name + ' zeroed')

    def sendData(self, data):
        """
        Sends data to every actuator on the DM.
        Inputs:
            data - the actuator voltages to be sent (np array)
                    array of one dimension with a size greater than numActProfile
                    do not normalize data beforehand
        Note: data processing is specific to the DMs in the lab
        and the way the profiles from BMC are set up
        """
        if not self.labExperiment:
            super().sendData(data)
        else:
            # make sure data is correct size
            assert np.size(data) >= self.numActProfile, 'data is too small'
            data = data[:self.numActProfile]
            # normalize data
            data = data / self.maxVoltage
            # process data for different dms
            if self.DMnum == 1:
                data = np.append(data[:self.numAct],
                                 np.zeros(int(self.numActProfile - self.numAct)))
            elif self.DMnum == 2:
                data = np.append(np.zeros(int(self.numActProfile / 2)),
                                 np.append(data[:self.numAct],
                                           np.zeros(int(self.numActProfile/2 - self.numAct))))
            else:
                raise Exception('Serial number not recognized')
            self.connection.command('send_data', data)
    
    def changeActuator(self, actuator, command):
        """
        Changes the voltage on a single actator
        Inputs:
            actuator - the number of the actuator to be changed (int)
            command - the voltage to be applied to the actuator (int)
        """
        if not self.labExperiment:
            super().changeActuator(actuator, command)
        else:
            assert actuator < self.numActProfile, 'actuator number must be less than 2048'
            assert actuator > 0, 'actuator number must be greater than 0'
            self.connection.command('poke', actuator, command/self.maxVoltage)

    def getCurentData(self):
        """
        Gets the current voltage on each actuator
        Output:
            data - voltage on each actuator (np array)
        """
        if not self.labExperiment:
            super().getCurentData()
        else:
            return np.array(self.connection.query('get_actuator_data'))
    
    def flatten(self):
        """
        Flattens the DM using the provided flatmaps
        """
        if not self.labExperiment:
            super().flatten()
        else:
            self.sendData(self.flatMap)
    
    def disable(self):
        """
        Disables the laser by zeroing the DM and then closing the connection.
        """
        if not self.labExperiment:
            super().disable()
        else:
            self.zero()
            self.connection.query('close_dm')
