import serial
import time


class HWTrainController:
    def __init__(self, _id="", line=0, auth=1, speed=10):
        # Control variables
        self._authority = auth  # 1 means go
        self._commandedSpeed = speed
        self._currentSpeed = int(0)
        self._setpointSpeed = int(0)
        self._SBrake = 0
        self._EBrake = 0
        self._EBrakeLock = False

        # Location Variables
        self._currentBlock = 0
        self._currentPolarity = 0
        self._whichLine = line # 0 for red, 1 for green
        self._redStations = [7, 16, 21, 25, 35, 45, 48, 60]
        self._redSensList = [7, 9, 15, 16, 21, 25, 27, 32, 35, 38, 43, 45, 48, 52, 60]
        self._greenStations = [2, 9, 16, 22, 31, 38, 47, 56, 65, 73, 77, 88, 96, 105, 114, 122, 131, 141]
        self._greenSensList = [2, 9, 12, 16, 19, 22, 29, 31, 38, 47, 56, 58, 62, 65, 73, 76, 77, 85, 88, 96, 105, 114,
                               122, 131, 141]

        # Train State Variables
        self._leftDoor = 0  # 0 for closed or Off
        self._rightDoor = 0
        self._headlights = 0
        self._inLights = 1
        self._mode = 1  # 0 for manual, 1 for automatic
        self._thisStation = ""
        self._nextStation = ""
        self._lastStation = "Yard"
        self._currentTemp = 70
        self._trainID = _id
        self._nextDoors = '00'
        self._announcement = "test"

        # Arduino variables
        self._powerToSend = 0
        self._arduino = serial.Serial(port='COM4', baudrate=115200, timeout=.1)

        # Failure Variables
        self._isFailed = False

    def enable(self):
        self._arduino.write(bytes("33333333", 'utf-8'))  # starts the arduino's loop

    def sendPower(self):
        return self._powerToSend

    # function to send beacon data
    def SetBeaconData(self, neighbor1, thisSt, neighbor2, doors):  # stations will be sent in order of increasing
        if self._lastStation == neighbor1:  # distance from Yard, will be up to hwtc to
            self._nextStation = neighbor2  # determine which is next and last based on travel
        elif self._lastStation == neighbor2:  # direction
            self._nextStation = neighbor1

        if self._thisStation == thisSt:
            self._lastStation = self._thisStation
        else:
            self._thisStation = thisSt
            self._nextDoors = doors

    def setEBrake(self, brake):
        if brake:
            self._EBrake = brake
            self._EBrakeLock = True
        else:
            if not self._EBrakeLock:
                self._EBrake = brake
            else:
                return

    def PassengerHitEBrake(self):
        self._EBrake = 1

    def atStation(self, currentBlock):
        result = False
        if self._whichLine:
            for i in self._greenStations:
                if currentBlock == i:
                    result = True
        else:
            for i in self._redStations:
                if currentBlock == i:
                    result = True
        return result

    def nearStop(self, currentBlock):
        result = False
        if self._whichLine:
            for i in self._greenSensList:
                if abs(currentBlock - i) < 4:
                    result = True
        else:
            for i in self._redSensList:
                if abs(currentBlock - i) < 4:
                    result = True
        return result

    def station_operations(self):
        self._inLights = True
        self._leftDoor = int(self._nextDoors[0])
        self._rightDoor = int(self._nextDoors[1])
        self._announcement = "This is " + self._thisStation + "."

    def SendData(self, auth, cmdSpd, curSpd):
        authStr = str(auth)
        if curSpd < 10:
            curSpdStr = "0" + str(curSpd)
        else:
            curSpdStr = str(curSpd)
        if cmdSpd < 10:
            cmdSpdStr = "0" + str(curSpd)
        else:
            cmdSpdStr = str(cmdSpd)
        data = "1" + curSpdStr + cmdSpdStr + "00" + authStr
        self._arduino.write(bytes(data, 'utf-8'))

    def ReceiveData(self):
        data = self._arduino.readline()
        decoded_data = int(data)
        if not self._mode:
            self._headlights = decoded_data - decoded_data % 100000000000
            self._EBrake = decoded_data - decoded_data % 10000000000
            self._SBrake = decoded_data - decoded_data % 1000000000
            self._mode = decoded_data - decoded_data % 100000000
            self._leftDoor = decoded_data - decoded_data % 10000000
            self._rightDoor = decoded_data - decoded_data % 1000000
            self._inLights = decoded_data - decoded_data % 100000
        self._powerToSend = (decoded_data % 10000)/100

    def StoppedHandler(self):
        print("Train is Stopped")
        self._EBrakeLock = False
        if self.atStation(self._currentBlock):
            self.station_operations()

    def FailureHandler(self, failures):  # Power Failure at index 2
        for i in range(3):
            if failures[i]:
                self.setEBrake(1)
                self._isFailed = True
        if failures[2]:
            self._inLights = 0
            self._headlights = 0

    def UpdateUI(self):
        toSend = "0" + (str(self._headlights) + str(self._EBrake) + str(self._SBrake)
                        + str(self._leftDoor) + str(self._rightDoor) + str(self._inLights))
        self._arduino.write(bytes(toSend, 'utf-8'))

    def UpdateBoard(self):
        if self.nearStop(self._currentBlock):
            self._setpointSpeed = 20
        else:
            self._setpointSpeed = self._commandedSpeed
        if self._currentSpeed == 0 and not self._authority:
            self.StoppedHandler()
        else:
            self.SendData(self._authority, self._setpointSpeed, self._currentSpeed)
            time.sleep(5)
            self.ReceiveData()

    def UpdateController(self, newAuth, newSpdCmd, currentSpeed, blockPolarity, failures):
        self._authority = newAuth
        self._commandedSpeed = newSpdCmd
        self._currentSpeed = int(currentSpeed)
        if self._commandedSpeed < self._currentSpeed:
            self._SBrake = 1
        self.FailureHandler(failures)
        if not self._isFailed:
            if self._currentPolarity != blockPolarity:
                self._currentBlock += 1
                self._currentPolarity = blockPolarity
            self.UpdateBoard()
        self.UpdateUI()

    def BrakeStates(self):
        return [self._EBrake, self._SBrake]
