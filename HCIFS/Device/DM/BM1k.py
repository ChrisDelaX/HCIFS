from HCIFS.Device.DM.DM import DM
import numpy as np
from HCIFS.util.LabControl import BMC

class BM1k(DM):
    # SERIAL1: C25CW003010
# SERIAL2: C25CW003014
    def __init__(self, numAct = 952, numActProfile=2048, maxVoltage = 185,
                 labExperiment = True,  **keywords):
        defaults = {'type': 'BM1k'}
        self.specs = defaults
        self.specs.update(keywords)
        super().__init__(**self.specs)
        self.connection = BMC()
        self.serialNum = self.specs.get('DMserial')
        self.numActProfile = self.specs.get('numActProfile', numActProfile)
        self.numAct = self.specs.get('numAct', numAct)
        self.maxVoltage = self.specs.get('maxVoltage', maxVoltage)
        self.labExperiment = labExperiment
        
        if self.labExperiment == True:
            if self.serialNum == '25CW004#014':
#                self.flatMap = np.loadtxt('C:/Lab/HCIFS/HCIFS/Devices/C25CW004#14_CLOSED_LOOP_200nm_Voltages_DM#1.txt')
                self.flatMap = np.loadtxt('C:/Program Files/Boston Micromachines/Shapes/C25CW004#14_CLOSED_LOOP_200nm_Voltages_DM#1.txt')
            elif self.serialNum == '25CW018#040':
#                self.flatMap = np.loadtxt('C:/Lab/HCIFS/HCIFS/Devices/C25CW018#40_CLOSED_LOOP_200nm_Voltages_DM#2.txt')
                self.flatMap = np.loadtxt('C:/Program Files/Boston Micromachines/Shapes/C25CW018#40_CLOSED_LOOP_200nm_Voltages_DM#2.txt')
    
    def enable(self):
        self.connection.command('open_dm', self.serialNum)
        status = self.connection.query('get_status')
        assert status == 0, 'Error connecting to DM. Error: ' + str(status)
        numActProfile = self.connection.query('num_actuators')
        assert numActProfile == self.numActProfile, 'Wrong number of profile actuators entered'

    def zero(self):
        num_actuators = self.connection.query('num_actuators')
        data = np.zeros(num_actuators)
        self.connection.command('send_data', data)
        if self.specs.get('name') is None:
            self.specs['name'] = 'DM'
        print(self.specs.get('name') + ' zeroed')

    def sendData(self, data):
        # make sure data is correct size
        assert np.size(data) >= self.numActProfile, 'data is too small'
        data = data[:self.numActProfile]
        # normalize data
        data = data / self.maxVoltage
        # process data for different dms
        if self.serialNum == '25CW004#014':
            data = np.append(data[:self.numAct],
                             np.zeros(int(self.numActProfile - self.numAct)))
        elif self.serialNum == '25CW018#040':
            data = np.append(np.zeros(int(self.numActProfile / 2)),
                             np.append(data[:self.numAct],
                                       np.zeros(int(self.numActProfile/2 - self.numAct))))
        else:
            raise Exception('Serial number not recognized')
        self.connection.command('send_data', data)
    
    def changeActuator(self, actuator, command):
        assert actuator < 2048, 'actuator number must be less than 2048'
        assert actuator > 0, "actuator number must be greater than 0"
        self.connection.command('poke', actuator, command)

    def getCurentData(self):
        return self.connection.query('get_actuator_data')
    
    def flatten(self):
        self.sendData(self.flatMap)
    
    def disable(self):
        self.zero()
        self.connection.query('close_dm')
