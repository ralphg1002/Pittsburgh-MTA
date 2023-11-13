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
        self.time = 0
        self.piVariables = {
            "powerLimit": 120000,
            "uk": 0,
            "prevError": 0,
            "ek": 0,
            "samplePeriod": 1,
        }
        self.power1 = {"powerValue": 0, "uk": 0, "prevError": 0}
        self.power2 = {"powerValue": 0, "uk": 0, "prevError": 0}
        self.power3 = {"powerValue": 0, "uk": 0, "prevError": 0}
        self.advertisementCounter = 1
        self.blockDict = {
            "block1": {"stationName": "station1", "blockNumber": 1, "blockLength": 50},
            "block2": {"stationName": "station2", "blockNumber": 1, "blockLength": 50},
        }

    def set_samplePeriod(self, samplePeriod):
        self.piVariables["samplePeriod"] = samplePeriod

    def add_train(self, trainObject):
        self.trainList.append(trainObject)

    def stopping_operations(self, trainObject):
        if not trainObject.get_authority():
            if trainObject.get_auto():
                # assuming using imperial units
                # mph to m/s
                currentSpeed = trainObject.get_currentSpeed() / 2.237

                # assumed in m
                trainLength = 32.2
                distance = (trainObject.block["blockLength"] / 2) + trainLength

                deceleration = currentSpeed * currentSpeed / 2 / distance

                if deceleration < 0:
                    efficacy = 0
                elif deceleration > 1.2:
                    trainObject.set_driverEbrake(True)
                    return
                else:
                    efficacy = deceleration / 1.2

                trainObject.set_driverSbrake(efficacy)

            if trainObject.get_speedLimit() > 15:
                trainObject.set_speedLimit(15)

    def station_operations(self, trainObject):
        if (trainObject.block["isStation"]) and (trainObject.get_currentSpeed() == 0):
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

    def find_block(self, blockDict, stationName):
        for i in blockDict:
            if blockDict[i]["stationName"] == stationName:
                return blockDict[i]["blockNumber"]

    def distance_between(self, blockDict, start, end):
        distanceCounter = 0
        if start < end:
            for i in blockDict:
                if start <= blockDict[i]["blockNumber"] <= end:
                    distanceCounter += blockDict[i]["blockLength"]
        else:
            for i in blockDict:
                if end <= blockDict[i]["blockNumber"] <= start:
                    distanceCounter += blockDict[i]["blockLength"]

        return distanceCounter

    def location_tracker(self, trainObject):
        if trainObject.prevStop != trainObject.beacon["currStop"]:
            if trainObject.prevStop != trainObject.beacon["nextStop"][0]:
                trainObject.nextStop = trainObject.beacon["nextStop"][0]
            else:
                trainObject.nextStop = trainObject.beacon["nextStop"][1]
        trainObject.prevStop = trainObject.beacon["currStop"]

        if (
            trainObject.stationDistance == 0
            or trainObject.prevStop == ""
            or trainObject.nextStop == ""
        ):
            trainObject.distanceRatio = 0
            return

        trainObject.stationDistance = self.distance_between(
            self.blockDict,
            self.find_block(self.blockDict, trainObject.prevStop),
            self.find_block(self.blockDict, trainObject.nextStop),
        )
        trainObject.distanceTravelled = self.distance_between(
            self.blockDict,
            self.find_block(self.blockDict, trainObject.prevStop),
            trainObject.block["blockNumber"],
        )
        trainObject.distanceRatio = (
            trainObject.distanceTravelled / trainObject.stationDistance
        )

    def update_block_info(self, blockDict, trainObject):
        if trainObject.prevPolarity != trainObject.polarity:
            if self.find_block(self.blockDict, trainObject.prevStop) < self.find_block(
                self.blockDict, trainObject.nextStop
            ):
                trainObject.block["blockNumber"] += 1
            else:
                trainObject.block["blockNumber"] -= 1
            trainObject.prevPolarity = trainObject.polarity

        for i in blockDict:
            if blockDict[i]["blockNumber"] == trainObject.block["blockNumber"]:
                trainObject.block["blockLength"] = blockDict[i]["blockLength"]
                trainObject.block["isStation"] = blockDict[i]["isStation"]
                trainObject.block["isTunnel"] = blockDict[i]["isTunnel"]

    def light_operations(self, trainObject):
        if trainObject.block["isTunnel"]:
            trainObject.set_headlights(True)
            trainObject.set_interiorLights(True)
        elif not (21600 <= self.time <= 64800):
            trainObject.set_headlights(False)
            trainObject.set_interiorLights(True)
        else:
            trainObject.set_headlights(False)
            trainObject.set_interiorLights(False)

    def advertisement_rotation(self, trainObject):
        if self.advertisementCounter == 1:
            trainObject.set_advertisement(1)
            self.advertisementCounter = 2
            return
        if self.advertisementCounter == 2:
            trainObject.set_advertisement(2)
            self.advertisementCounter = 3
            return
        if self.advertisementCounter == 3:
            trainObject.set_advertisement(3)
            self.advertisementCounter = 1
            return

    def pi_calculation(self, trainObject, powerDict):
        # calculate new velocity error
        newError = trainObject.get_setpointSpeed() - trainObject.get_currentSpeed()

        # calculate new uk
        if newError == 0 and self.piVariables["prevError"] == 0:
            # trainObject.set_powerCommand(0)
            powerDict["powerValue"] = 0
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
            # trainObject.set_powerCommand(0)
            powerDict["powerValue"] = 0
        elif newPowerCommand > self.piVariables["powerLimit"]:
            # trainObject.set_powerCommand(self.piVariables["powerLimit"])
            powerDict["powerValue"] = self.piVariables["powerLimit"]
        else:
            # trainObject.set_powerCommand(newPowerCommand)
            powerDict["powerValue"] = newPowerCommand

        # update uk and velocity error variables
        # self.piVariables["uk"] = newUk
        # self.piVariables["prevError"] = newError
        powerDict["uk"] = newUk
        powerDict["prevError"] = newError

    def pi_control(self, trainObject):
        self.pi_calculation(trainObject, self.power1)
        self.pi_calculation(trainObject, self.power2)
        self.pi_calculation(trainObject, self.power3)
        if self.power1["powerValue"] <= self.power2["powerValue"]:
            if self.power1["powerValue"] <= self.power3["powerValue"]:
                trainObject.set_powerCommand(self.power1["powerValue"])
                self.piVariables["uk"] = self.power1["uk"]
                self.piVariables["prevError"] = self.power1["prevError"]
            else:
                trainObject.set_powerCommand(self.power3["powerValue"])
                self.piVariables["uk"] = self.power3["uk"]
                self.piVariables["prevError"] = self.power3["prevError"]
        elif self.power2["powerValue"] <= self.power3["powerValue"]:
            trainObject.set_powerCommand(self.power2["powerValue"])
            self.piVariables["uk"] = self.power2["uk"]
            self.piVariables["prevError"] = self.power2["prevError"]
        else:
            trainObject.set_powerCommand(self.power3["powerValue"])
            self.piVariables["uk"] = self.power3["uk"]
            self.piVariables["prevError"] = self.power3["prevError"]

    def failure_operations(self, trainObject):
        if trainObject.get_engineFailure():
            trainObject.set_driverEbrake(True)
        elif trainObject.get_brakeFailure():
            trainObject.set_driverEbrake(True)
        elif trainObject.get_signalFailure():
            trainObject.set_driverEbrake(True)
            trainObject.set_interiorLights(False)
            trainObject.set_headlights(False)

    def sbrake_operations(self, trainObject):
        if trainObject.get_driverSbrake():
            trainObject.set_powerCommand(0)

    def ebrake_operations(self, trainObject):
        if trainObject.get_driverEbrake():
            trainObject.set_powerCommand(0)

    def automatic_operations(self, trainObject):
        self.station_operations(trainObject)
        self.light_operations(trainObject)
        trainObject.set_setpointSpeed(trainObject.get_commandedSpeed())
        trainObject.set_setpointTemp(70)

    def regular_operations(self, blockDict, trainObject):
        self.location_tracker(trainObject)
        self.update_block_info(blockDict, trainObject)
        self.failure_operations(trainObject)
        self.stopping_operations(trainObject)
        self.pi_control(trainObject)
        self.sbrake_operations(trainObject)
        self.ebrake_operations(trainObject)
