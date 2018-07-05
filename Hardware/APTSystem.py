# APTSystem - creates an activex container to control Thorlabs LTS 300 motor

from PyQt5 import QAxContainer

class APTSystem(QAxContainer.QAxWidget):

    def __init__(self, parent):

        super(APTSystem, self).__init__()

        # connect to control
        self.setControl('{B74DB4BA-8C1E-4570-906E-FF65698D632E}')
