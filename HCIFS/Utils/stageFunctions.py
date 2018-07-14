def createStage(device):
    stage = []
    for i in range(3):
        if device.stageType[i] == None:
            import OpticalSystem.MotorStage.Stage.Stage as Stage
            stage.append(Stage())
        else:
            moduleName = device.stageType[i]
            importName = 'OpticalSystem.MotorStage.' + moduleName
            importlib.import_module(importName)
            stageClass = getattr(importName, moduleName)
            stage.append(stageClass(device.stageSerial[i]))
    return stage

def getPos(self, name):
    for i in range(len(self.optics)):
        if name == self.optics[i].name:
            ID = i
    device = self.optics[ID]   
    stage = createStage(device)
    return stage[0].getPos(), stage[1].getPos(), stage[2].getPos() 

def moveOptics(self, name, movement):
    for i in range(len(self.optics)):
        if name == self.optics[i].name:
            ID = i
    device = self.optics[ID]
    stage = createStage(device)
    stage.goto(movement)
    deltaZ = movement[2]
    if deltaZ != 0:
        if ID == 0:
            device.dist2next -= deltaZ
            self.distances[0] += deltaZ
            self.distances[1] -= deltaZ
        else:
            self.optics[ID - 1].dist2next += deltaZ
            device.dist2next -= deltaZ
            self.distances[ID] += deltaZ
            self.distances[ID + 1] -= deltaZ   

def homeOptics(self, name):
    for i in range(len(self.optics)):
        if name == self.optics[i].name:
            ID = i
    device = self.optics[ID]
    stage = createStage(device)
    currentPosition = stage.getPos()    
    stage.gotoHome()
    deltaZ = -currentPosition[2]
    if deltaZ != 0:
        if ID == 0:
            device.dist2next -= deltaZ
            self.distances[0] += deltaZ
            self.distances[1] -= deltaZ
        else:
            self.optics[ID - 1].dist2next += deltaZ
            device.dist2next -= deltaZ
            self.distances[ID] += deltaZ
            self.distances[ID + 1] -= deltaZ

