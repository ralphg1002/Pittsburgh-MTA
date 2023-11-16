import numpy as np
import pyfirmata
import serial
import time


# board = pyfirmata.Arduino() TODO: Implement Arduino Communication
# arduino = serial.Serial(port='COM4', baudrate=11520, timeout=.1)


class HWTrainController:
    def __init__(self, _id="", auth=1, speed=10):
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
        self._stationList = np.zeros(20)  # TODO: Once track model is finalized, hard code this
                                          #       array with all stations' block numbers
        self._stationList[0] = 9

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

        # Power Variables
        self._K_p = 10000  # TODO: Figure out what values these take based on the train
        self._K_i = 900
        self._powerToSend = 5
        self._powerLimit = 1000000000
        self._SerialData = ""
        self._lastError = 0
        self._thisError = 0
        self._uk = 0
        self._samplePd = 1

        # Failure Variables
        self._isFailed = False

    def setAuthority(self, auth):
        self._authority = auth

    def setCommandedSpeed(self, newSpeed):
        self._commandedSpeed = newSpeed

    def sendPower(self):
        return self._powerToSend

    def getCurrentSpeed(self):
        return self._currentSpeed

    def getCurrentBlock(self):
        return self._currentBlock

    def getLeftDoor(self):
        return self._leftDoor

    def getRightDoor(self):
        return self._rightDoor

    def getInLights(self):
        return self._inLights

    def getHeadLights(self):
        return self._headlights

    def getAnnouncement(self):
        return self._announcement

    def getTrainID(self):
        return self._trainID

    def getCurrentTemp(self):
        return self._currentTemp

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
        for i in self._stationList:
            if currentBlock == i:
                result = True
        return result

    def nearStation(self, currentBlock):
        result = False
        for i in self._stationList:
            if abs(currentBlock - i) < 3:
                result = True
        return result

    def station_operations(self):
        self._inLights = True
        self._leftDoor = bool(self._nextDoors[0])
        self._rightDoor = bool(self._nextDoors[1])
        self._announcement = "This is " + self._thisStation + "."

    def StoppedHandler(self):
        self._EBrakeLock = False
        if self.atStation(self._currentBlock):
            self.station_operations()

    def PowerHandler(self):
        newError = (self._setpointSpeed - self._currentSpeed) / 2.237
        if newError == 0 and self._lastError == 0:
            self._powerToSend = 0
            return
        else:
            newUk = self._uk + self._samplePd / 2 * (newError + self._lastError)

        power1 = self._K_p * newError + self._K_i * newUk  # TODO: insert power calculation here
        power2 = self._K_p * newError + self._K_i * newUk
        power3 = self._K_p * newError + self._K_i * newUk
        self._powerToSend = (power1 + power2 + power3) / 3  # TODO: change this from an average to a voting algorithm
        self._uk = newUk
        self._lastError = newError

    def FailureHandler(self, failures=[0, 0, 0]):  # Power Failure at index 2
        for i in range(3):
            if failures[i]:
                self.setEBrake(1)
                self._isFailed = True
        if failures[2]:
            self._inLights = 0
            self._headlights = 0

    # def UpdateUI(self):  # TODO: implement arduino firmata communication for sending and receiving booleans from UI
    #     return board

    def AutoUpdate(self):
        if self.nearStation(self._currentBlock):
            self._setpointSpeed = self._commandedSpeed / 2
        else:
            self._setpointSpeed = self._commandedSpeed
        if self._currentSpeed == 0 and not self._authority:
            self.StoppedHandler()
        else:
            self.PowerHandler()
            # self.UpdateUI()

    def UpdateController(self, newAuth, newSpdCmd, currentSpeed, blockPolarity, failures=[0, 0, 0]):
        self._authority = newAuth
        self._commandedSpeed = newSpdCmd
        self._currentSpeed = currentSpeed
        self.FailureHandler(failures)
        if not self._isFailed:
            if self._currentPolarity != blockPolarity:
                self._currentBlock += 1
                self._currentPolarity = blockPolarity
            if self._mode:
                self.AutoUpdate()

    def BrakeStates(self):
        return [self._EBrake, self._SBrake]
