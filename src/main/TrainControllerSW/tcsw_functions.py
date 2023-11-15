# importing libraries
import sys
import math
import re
import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import time


class TCFunctions:
    def __init__(self):
        self.trainList = []
        self.time = 0

        self.power1 = {"powerValue": 0, "uk": 0, "prevError": 0}
        self.power2 = {"powerValue": 0, "uk": 0, "prevError": 0}
        self.power3 = {"powerValue": 0, "uk": 0, "prevError": 0}
        self.advertisementCounter = 1
        self.blockDict = {
            "block1": {"stationName": "station1", "blockNumber": 1, "blockLength": 50},
            "block2": {"stationName": "station2", "blockNumber": 1, "blockLength": 50},
        }
        self.redBlockDict = self.parse_trackLayout(r"src\main\TrainControllerSW\track_layout.xlsx", "Red Line")
        self.greenBlockDict = self.parse_trackLayout(r"src\main\TrainControllerSW\track_layout.xlsx", "Green Line")

    def parse_trackLayout(self, file_path, sheet):
        # Read the Excel file into a pandas DataFrame
        df = pd.read_excel(file_path, sheet_name=sheet)

        df = df.fillna('')

        # Convert the DataFrame to a list of dictionaries (one dictionary per row)
        data = df.to_dict(orient='records')

        modifiedData = []
        affectedBlocks = []
        firstStationName = ""

        for block in data:
            switchBlocks = []
            modifiedBlock = {"Line": "line",
                             "Section": "letter",
                             "Number": 0,
                             "Length": 0,
                             "isStation": False,
                             "isTunnel": False,
                             "stationName": "",
                             "firstStation": "",
                             "Infrastructure": "",
                             "Limit": False}
            modifiedBlock["Line"] = block["Line"]
            modifiedBlock["Section"] = block["Section"]
            modifiedBlock["Number"] = block["Block Number"]
            modifiedBlock["Length"] = block["Block Length (m)"]
            if "STATION" in block["Infrastructure"]:
                modifiedBlock["isStation"] = True
                modifiedStationName = block["Infrastructure"]
                modifiedStationName = modifiedStationName.replace("STATION; ", "")
                modifiedStationName = modifiedStationName.replace("; UNDERGROUND", "")
                modifiedStationName = modifiedStationName.replace(" (First)", "")
                modifiedBlock["stationName"] = modifiedStationName
                modifiedBlock["Infrastructure"] = modifiedStationName
            if "UNDERGROUND" in block["Infrastructure"]:
                modifiedBlock["isTunnel"] = True
            if "SWITCH" in block["Infrastructure"]:
                modifiedBlock["Infrastructure"] = "SWITCH"
                affectedBlocks = re.findall(r'\d+', block["Infrastructure"])
                affectedBlocks = [int(num) for num in affectedBlocks]
            if "RAILWAY CROSSING" in block["Infrastructure"]:
                modifiedBlock["Infrastructure"] = "RAILWAY CROSSING"
            if "(First)" in block["Infrastructure"]:
                firstStationName = modifiedBlock["stationName"]
            if modifiedBlock["Infrastructure"] != "":
                affectedBlocks.append(modifiedBlock["Number"] - 1)
                affectedBlocks.append(modifiedBlock["Number"] + 1)
            affectedBlocks = list(set(affectedBlocks))
            for affected in affectedBlocks:
                if affected == modifiedBlock["Number"]:
                    modifiedBlock["Limit"] = True

            modifiedData.append(modifiedBlock)

        for block in modifiedData:
            block["firstStation"] = firstStationName

        return modifiedData

    def set_samplePeriod(self, trainObject, samplePeriod):
        trainObject.piVariables["samplePeriod"] = samplePeriod

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
                distance = (trainObject.block["blockLength"] + trainLength) / 2

                deceleration = currentSpeed * currentSpeed / 2 / distance

                if deceleration < 0:
                    efficacy = 0
                elif deceleration > 1.2:
                    trainObject.set_driverEbrake(True)
                    return
                else:
                    efficacy = deceleration / 1.2

                trainObject.set_driverSbrake(efficacy)

            if trainObject.get_speedLimit() > 20:
                trainObject.set_speedLimit(20)

    def station_operations(self, trainObject):
        if (
            (trainObject.block["isStation"])
            and (trainObject.get_currentSpeed() == 0)
            and (not trainObject.get_authority())
        ):
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

    def find_block_by_stationName(self, blockDict, stationName):
        for block in blockDict:
            if block["stationName"] == stationName:
                return block["Number"]

    def find_station_by_section(self, blockDict, section):
        for block in blockDict:
            if block["Section"] == section and block["isStation"] == True:
                return block["stationName"]

    def distance_between(self, blockDict, start, end):
        distanceCounter = 0
        if start < end:
            for block in blockDict:
                if start <= block["Number"] <= end:
                    distanceCounter += block["Length"]
        else:
            for block in blockDict:
                if end <= block["Number"] <= start:
                    distanceCounter += block["Length"]

        return distanceCounter

    def location_tracker(self, blockDict, trainObject):
        self.timeTravelled = 0
        self.nextInfrastructure = ""
        self.distanceToNextStation = 0
        self.distanceToInfrastructure = 0
        self.distanceTravelled = 0
        self.distanceRatio = 0
        if trainObject.block["isStation"]:
            trainObject.distanceTravelled = 0
            trainObject.distanceRatio = 0
        #if trainObject.block["infrastructure"] == trainObject.nextInfrastructure:


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
            blockDict,
            self.find_block_by_stationName(blockDict, trainObject.prevStop),
            self.find_block_by_stationName(blockDict, trainObject.nextStop),
        )
        trainObject.distanceTravelled = self.distance_between(
            blockDict,
            self.find_block_by_stationName(blockDict, trainObject.prevStop),
            trainObject.block["blockNumber"],
        )
        trainObject.distanceRatio = (
            trainObject.distanceTravelled / trainObject.stationDistance
        )

    def update_block_info(self, blockDict, trainObject):
        if trainObject.prevPolarity != trainObject.polarity:
            if trainObject.prevStop == trainObject.nextStop:
                trainObject.block["blockNumber"] += 0
            elif self.find_block_by_stationName(blockDict, trainObject.prevStop) < self.find_block_by_stationName(
                    blockDict, trainObject.nextStop):
                trainObject.block["blockNumber"] += 1
            else:
                trainObject.block["Number"] -= 1
            trainObject.prevPolarity = trainObject.polarity

        for block in blockDict:
            if block["Number"] == trainObject.block["blockNumber"]:
                trainObject.block["blockLength"] = block["Length"]
                trainObject.block["isStation"] = block["isStation"]
                trainObject.block["isTunnel"] = block["isTunnel"]

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
        if newError == 0 and trainObject.piVariables["prevError"] == 0:
            # trainObject.set_powerCommand(0)
            powerDict["powerValue"] = 0
            return
        elif trainObject.get_powerCommand() < trainObject.piVariables["powerLimit"]:
            newUk = trainObject.piVariables["uk"] + trainObject.piVariables["samplePeriod"] / 2 * (
                newError + trainObject.piVariables["prevError"]
            )
        else:
            newUk = trainObject.piVariables["uk"]

        # power equation
        newPowerCommand = trainObject.get_kp() * newError + trainObject.get_ki() * newUk

        # bounds
        if newPowerCommand < 0:
            # trainObject.set_powerCommand(0)
            powerDict["powerValue"] = 0
        elif newPowerCommand > trainObject.piVariables["powerLimit"]:
            # trainObject.set_powerCommand(trainObject.piVariables["powerLimit"])
            powerDict["powerValue"] = trainObject.piVariables["powerLimit"]
        else:
            # trainObject.set_powerCommand(newPowerCommand)
            powerDict["powerValue"] = newPowerCommand

        # update uk and velocity error variables
        # trainObject.piVariables["uk"] = newUk
        # trainObject.piVariables["prevError"] = newError
        powerDict["uk"] = newUk
        powerDict["prevError"] = newError

    def pi_control(self, trainObject):
        self.pi_calculation(trainObject, self.power1)
        self.pi_calculation(trainObject, self.power2)
        self.pi_calculation(trainObject, self.power3)
        if self.power1["powerValue"] <= self.power2["powerValue"]:
            if self.power1["powerValue"] <= self.power3["powerValue"]:
                trainObject.set_powerCommand(self.power1["powerValue"])
                trainObject.piVariables["uk"] = self.power1["uk"]
                trainObject.piVariables["prevError"] = self.power1["prevError"]
            else:
                trainObject.set_powerCommand(self.power3["powerValue"])
                trainObject.piVariables["uk"] = self.power3["uk"]
                trainObject.piVariables["prevError"] = self.power3["prevError"]
        elif self.power2["powerValue"] <= self.power3["powerValue"]:
            trainObject.set_powerCommand(self.power2["powerValue"])
            trainObject.piVariables["uk"] = self.power2["uk"]
            trainObject.piVariables["prevError"] = self.power2["prevError"]
        else:
            trainObject.set_powerCommand(self.power3["powerValue"])
            trainObject.piVariables["uk"] = self.power3["uk"]
            trainObject.piVariables["prevError"] = self.power3["prevError"]

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
        self.location_tracker(blockDict, trainObject)
        self.update_block_info(blockDict, trainObject)
        self.failure_operations(trainObject)
        self.stopping_operations(trainObject)
        self.pi_control(trainObject)
        self.sbrake_operations(trainObject)
        self.ebrake_operations(trainObject)
