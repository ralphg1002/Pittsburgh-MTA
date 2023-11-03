# importing libraries
import sys
import math
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import time


class TCFunctions:
    def __init__(self):
        self.trainList = []
        self.piVariables = {
            "powerLimit": 120000,
            "uk": 0,
            "prevError": 0,
            "ek": 0,
            "samplePeriod": 1,
        }
        self.advertisementCounter = 1

    def set_samplePeriod(self, samplePeriod):
        self.piVariables["samplePeriod"] = samplePeriod

    def add_train(self, trainObject):
        self.trainList.append(trainObject)

    def stopping_operations(self, trainObject):
        if trainObject.get_authority() < 0.1 and trainObject.get_authority() > 0:
            # assuming using imperial units
            # mph to m/s
            currentSpeed = trainObject.get_currentSpeed() / 2.237
            # mi to m
            distance = trainObject.get_authority() * 1609

            deceleration = currentSpeed * currentSpeed / 2 / distance

            if deceleration < 0:
                efficacy = 0
            elif deceleration > 1.2:
                trainObject.set_driverEbrake(True)
                return
            else:
                efficacy = deceleration / 1.2

            trainObject.set_driverSbrake(efficacy)

    def station_operations(self, trainObject):
        if trainObject.beacon["isStation"]:
            trainObject.set_interiorLights(True)
            trainObject.set_leftDoor(trainObject.beacon["leftStation"])
            trainObject.set_rightDoor(trainObject.beacon["rightStation"])
            trainObject.set_announcement(
                "This is " + trainObject.beacon["currStop"] + "."
            )
        else:
            trainObject.set_interiorLights(False)
            trainObject.set_leftDoor(False)
            trainObject.set_rightDoor(False)
            trainObject.set_announcement("")

    def tunnel_operations(self, trainObject):
        if trainObject.beacon["isTunnel"]:
            trainObject.set_headlights(True)
        else:
            trainObject.set_headlights(False)

    def advertisement_rotation(self, trainObject):
        if self.advertisementCounter == 1:
            trainObject.set_advertisement(1)
            self.advertisementCounter = 2
        if self.advertisementCounter == 2:
            trainObject.set_advertisement(2)
            self.advertisementCounter = 3
        if self.advertisementCounter == 3:
            trainObject.set_advertisement(3)
            self.advertisementCounter = 1

    def pi_control(self, trainObject):
        # calculate new velocity error
        newError = trainObject.get_setpointSpeed() - trainObject.get_currentSpeed()

        # calculate new uk
        if newError == 0 and self.piVariables["prevError"] == 0:
            trainObject.set_powerCommand(0)
            return
        elif trainObject.get_powerCommand() < self.piVariables["powerLimit"]:
            newUk = self.piVariables["uk"] + self.piVariables["samplePeriod"] / 2 * (
                newError + self.piVariables["prevError"]
            )
        else:
            newUk = self.piVariables["uk"]

        # power equation
        newPowerCommand = trainObject.get_kp() * newError + trainObject.get_ki() * newUk

        # bounds
        if newPowerCommand < 0:
            trainObject.set_powerCommand(0)
        elif newPowerCommand > self.piVariables["powerLimit"]:
            trainObject.set_powerCommand(self.piVariables["powerLimit"])
        else:
            trainObject.set_powerCommand(newPowerCommand)

        # update uk and velocity error variables
        self.piVariables["uk"] = newUk
        self.piVariables["prevError"] = newError

    def failure_operations(self, trainObject):
        if trainObject.get_engineFailure():
            trainObject.set_driverEbrake(True)
        elif trainObject.get_brakeFailure():
            trainObject.set_driverEbrake(True)
        elif trainObject.get_signalFailure():
            trainObject.set_driverEbrake(True)

    def sbrake_operations(self, trainObject):
        if trainObject.get_driverSbrake():
            trainObject.set_powerCommand(0)

    def ebrake_operations(self, trainObject):
        if trainObject.get_paxEbrake():
            trainObject.set_driverEbrake(True)

        if trainObject.get_driverEbrake():
            trainObject.set_powerCommand(0)

    def automatic_operations(self, trainObject):
        self.station_operations(trainObject)
        self.tunnel_operations(trainObject)
        self.advertisement_rotation(trainObject)
        trainObject.set_setpointSpeed(trainObject.get_commandedSpeed())
        trainObject.set_setpointTemp(70)
        self.stopping_operations(trainObject)
        self.failure_operations(trainObject)

    def regular_operations(self, trainObject):
        self.pi_control(trainObject)
        self.sbrake_operations(trainObject)
        self.ebrake_operations(trainObject)
