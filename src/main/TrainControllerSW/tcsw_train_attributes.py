import sys
import math
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import time


class Train:
    def __init__(self, trainID):
        # system inputs
        self.trainID = trainID
        self.block = {
            "blockNumber": 0,
            "blockLength": 0,
            "isStation": False,
            "isTunnel": False,
        }

        # train model inputs
        self.speedLimit = 0
        self.authority = False
        self.commandedSpeed = 0
        self.currentSpeed = 0
        self.engineFailure = False
        self.brakeFailure = False
        self.signalFailure = False
        self.currentTemp = 0
        self.paxEbrake = False
        self.beacon = {
            "currStop": "",
            "nextStop": ["", ""],
            "leftStation": False,
            "rightStation": False,
        }
        self.polarity = False

        # train controller inputs
        self.auto = True
        self.kp = 0
        self.ki = 0
        self.setpointSpeed = 0
        self.driverEbrake = False
        self.driverSbrake = 0
        self.announcement = ""
        self.headlights = False
        self.interiorLights = False
        self.leftDoor = False
        self.rightDoor = False
        self.setpointTemp = 0
        self.advertisement = 0

        # train controller internal inputs
        self.powerCommand = 0
        self.prevStop = ""
        self.nextStop = ""
        self.prevPolarity = False
        self.stationDistance = 0
        self.distanceTravelled = 0
        self.distanceRatio = 0

    # setters and getters
    def get_trainID(self):
        return self.trainID

    def set_speedLimit(self, speedLimit):
        self.speedLimit = speedLimit

    def get_speedLimit(self):
        return self.speedLimit

    def set_authority(self, authority):
        self.authority = authority

    def get_authority(self):
        return self.authority

    def set_commandedSpeed(self, commandedSpeed):
        self.commandedSpeed = commandedSpeed

    def get_commandedSpeed(self):
        return self.commandedSpeed

    def set_currentSpeed(self, currentSpeed):
        self.currentSpeed = currentSpeed

    def get_currentSpeed(self):
        return self.currentSpeed

    def set_engineFailure(self, engineFailure):
        self.engineFailure = engineFailure

    def get_engineFailure(self):
        return self.engineFailure

    def set_brakeFailure(self, brakeFailure):
        self.brakeFailure = brakeFailure

    def get_brakeFailure(self):
        return self.brakeFailure

    def set_signalFailure(self, signalFailure):
        self.signalFailure = signalFailure

    def get_signalFailure(self):
        return self.signalFailure

    def set_currentTemp(self, currentTemp):
        self.currentTemp = currentTemp

    def get_currentTemp(self):
        return self.currentTemp

    def set_paxEbrake(self, paxEbrake):
        self.paxEbrake = paxEbrake

    def get_paxEbrake(self):
        return self.paxEbrake

    def set_beacon(self, beacon):
        self.beacon = beacon

    def get_beacon(self):
        return self.beacon

    def set_auto(self, auto):
        self.auto = auto

    def get_auto(self):
        return self.auto

    def set_setpointSpeed(self, setpointSpeed):
        self.setpointSpeed = setpointSpeed

    def get_setpointSpeed(self):
        return self.setpointSpeed

    def set_driverEbrake(self, driverEbrake):
        self.driverEbrake = driverEbrake

    def get_driverEbrake(self):
        return self.driverEbrake

    def set_driverSbrake(self, driverSbrake):
        self.driverSbrake = driverSbrake

    def get_driverSbrake(self):
        return self.driverSbrake

    def set_announcement(self, announcement):
        self.announcement = announcement

    def get_announcement(self):
        return self.announcement

    def set_headlights(self, headlights):
        self.headlights = headlights

    def get_headlights(self):
        return self.headlights

    def set_interiorLights(self, interiorLights):
        self.interiorLights = interiorLights

    def get_interiorLights(self):
        return self.interiorLights

    def set_leftDoor(self, leftDoor):
        self.leftDoor = leftDoor

    def get_leftDoor(self):
        return self.leftDoor

    def set_rightDoor(self, rightDoor):
        self.rightDoor = rightDoor

    def get_rightDoor(self):
        return self.rightDoor

    def set_setpointTemp(self, setpointTemp):
        self.setpointTemp = setpointTemp

    def get_setpointTemp(self):
        return self.setpointTemp

    def set_kp(self, kp):
        self.kp = kp

    def get_kp(self):
        return self.kp

    def set_ki(self, ki):
        self.ki = ki

    def get_ki(self):
        return self.ki

    def set_advertisement(self, advertisement):
        self.advertisement = advertisement

    def get_advertisement(self):
        return self.advertisement

    def set_powerCommand(self, powerCommand):
        self.powerCommand = powerCommand

    def get_powerCommand(self):
        return self.powerCommand
