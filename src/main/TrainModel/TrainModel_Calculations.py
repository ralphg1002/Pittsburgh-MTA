# Importing Libraries
from decimal import DivisionByZero
import sys
import math
import re

from sklearn.model_selection import train_test_split


class Calculations:
    def __init__(self):
        placeholder = True

    def TrainModelCalculations(self, trainObject):
        self.updateMass(trainObject)
        self.checkFailureModes(trainObject)
        self.calculateAccelerationSum(trainObject)
        self.calculateEngineForce(trainObject)
        self.calculateSlopeForce(trainObject)
        self.calculateFrictionForce(trainObject)
        self.calculateNetForce(trainObject)
        self.calculateAcceleration(trainObject)
        self.calculateCurrentSpeed(trainObject)
        self.updatePosition(trainObject)

    def updateMass(self, trainObject):
        trainObject.calculations["mass"] = trainObject.calculations["empty_mass"] + (trainObject.passenger_status["passengers"] * 45)
        if trainObject.calculations["mass"] >= trainObject.calculations["full_mass"]:
            trainObject.calculations["mass"] = trainObject.calculations["full_mass"]

    def checkFailureModes(self, trainObject):
        if trainObject.failure_status["signal_pickup_failure"]:
            trainObject.navigation_status["beacon"] = ""

    def calculateAccelerationSum(self, trainObject):
        trainObject.calculations["lastAcceleration"] = trainObject.calculations["currAcceleration"]

    def calculateEngineForce(self, trainObject):
        try:
            trainObject.calculations["currEngineForce"] = abs(trainObject.vehicle_status["power"] / trainObject.vehicle_status["current_speed"])
        except ZeroDivisionError:
            if trainObject.vehicle_status["power"] > 0:
                trainObject.vehicle_status["current_speed"] = 0.01

    def calculateSlopeForce(self, trainObject):
        trainObject.calculations["currAngle"] = math.atan(trainObject.navigation_status["block_grade"] / 100)
        trainObject.calculations["slopeForce"] = trainObject.calculations["mass"] * 9.8 * math.sin(trainObject.calculations["currAngle"])

    def calculateFrictionForce(self, trainObject):
        trainObject.calculations["frictionForce"] = 1000

    def calculateBrakes(self, trainObject):
        if (trainObject.vehicle_status["brakes"] and not trainObject.failure_status["emergency_brake"]):
            trainObject.calculations["brakeForce"] = 1.2
        
        if (trainObject.failure_status["emergency_brake"] == True):
            trainObject.calculations["brakeForce"] = 2.73
        
        if (not trainObject.vehicle_status["brakes"] and not trainObject.failure_status["emergency_brake"]):
            trainObject.calculations["brakeForce"] = 0
    
    def calculateNetForce(self, trainObject):
        try:
            trainObject.calculations["totalForce"] = trainObject.calculations["currEngineForce"] - trainObject.calculations["slopeForce"] - trainObject.calculations["brakeForce"] - trainObject.calculations["frictionForce"]
            if trainObject.vehicle_status["current_speed"] != 0:
                if trainObject.calculations["totalForce"] > 120 / trainObject.vehicle_status["current_speed"]:
                    trainObject.calculations["totalForce"] = 120 / trainObject.vehicle_status["current_speed"]
        except ZeroDivisionError:
            # Handle division by zero here, if necessary
            pass

    def calculateAcceleration(self, trainObject):
        trainObject.calculations["currAcceleration"] = trainObject.calculations["totalForce"] / trainObject.calculations["mass"]

    def calculateCurrentSpeed(self, trainObject):
        if trainObject.vehicle_status["power"] / 1000 <= 120:
            trainObject.vehicle_status["current_speed"] = trainObject.vehicle_status["current_speed"] + (trainObject.calculations["timeInterval"] / 2) * (trainObject.calculations["currAcceleration"] + trainObject.calculations["lastAcceleration"])

        if trainObject.vehicle_status["current_speed"] < 0:
            trainObject.vehicle_status["current_speed"] = 0

        if trainObject.vehicle_status["current_speed"] > 40:
            trainObject.vehicle_status["current_speed"] = 40

        if trainObject.vehicle_status["current_speed"] > trainObject.vehicle_status["speed_limit"]:
            trainObject.vehicle_status["current_speed"] = trainObject.vehicle_status["speed_limit"]

    def updatePosition(self, trainObject):
        # self.distanceFromYard += self.currentSpeed * (trainObject.calculations["timeInterval"] * 0.001)
        # self.distanceFromBlockStart += self.currentSpeed * (trainObject.calculations["timeInterval"] * 0.001)
        trainObject.calculations["distance"] += trainObject.vehicle_status["current_speed"] * (trainObject.calculations["timeInterval"])

    def blockID(
        self,
        trainObject,
        next_block,
        length,
        grade,
        speed_limit,
        suggested_speed,
        authority,
    ):
        trainObject.calculations["nextBlock"] = next_block
        trainObject.navigation_status["length"] = length
        trainObject.navigation_status["grade"] = grade
        trainObject.vehicle_status["speed_limit"] = speed_limit
        trainObject.vehicle_status["suggested_speed"] = suggested_speed
        trainObject.navigation_status["authority"] = authority

        self.occupancy(trainObject, next_block)

        # # Send train controller information
        # trainModelToTrainController.sendBlockLength.emit(length)
        # trainModelToTrainController.sendSpeedLimit.emit(train, speed_limit)
        # trainModelToTrainController.sendCommandedSpeed.emit(train, suggested_speed)
        # trainModelToTrainController.sendAuthority.emit(train, authority)

    def failures(self, trainObject):
        # trainModelToTrainController.sendEngineFailure.emit(trainObject.calculations["trainID"], trainObject.failure_status["engine_failure"])
        # trainModelToTrainController.sendSignalPickupFailure.emit(trainObject.calculations["trainID"], trainObject.failure_status["signal_pickup_failure"])
        # trainModelToTrainController.sendBrakeFailure.emit(trainObject.calculations["trainID"], trainObject.failure_status["brake_failure"])
        # trainModelToTrainController.sendPassengerEmergencyBrake.emit(trainObject.calculations["trainID"], trainObject.failure_status["passenger_emergency_brake"])
        return

    def temperature(self, trainObject):
        set_temp = trainObject.calculations["setpoint_temp"]
        curr_temp = trainObject.passenger_status["temperature"]
        train = trainObject.calculations["trainID"]

        if curr_temp < set_temp:
            while curr_temp < set_temp:
                curr_temp += 1
                trainObject.passenger_status["temperature"] = curr_temp
                # trainModelToTrainController.sendTemperature.emit(train, curr_temp)

        elif set_temp < curr_temp:
            while set_temp < curr_temp:
                curr_temp -= 1
                trainObject.passenger_status["temperature"] = curr_temp
                # trainModelToTrainController.sendTemperature.emit(train, curr_temp)

        else:
            trainObject.passenger_status["temperature"] = curr_temp
            # trainModelToTrainController.sendTemperature.emit(train, curr_temp)

        return

    # Calculate the current number of passengers from the track model
    def passengers(self, trainObject):
        # trainModelToTrackModel.sendCurrentPassengers.emit(trainObject.passenger_status["passengers"], trainObject.calculations["trainID"])
        return

    def occupancy(self, trainObject, next_block):
        # if trainObject.calculations["initialized"]:
        #     trainModelToTrackModel.sendPolarity.emit(line, curr_block, prev_block)

        # if trainObject.calculations["distance"] == trainObject.navigation_status["block_length"]:
        #     trainObject.calculations["distance"] = 0
        #     trainObject.calculations["polarity"] = not trainObject.calculations["polarity"]
        #     trainModelToTrackModel.sendPolarity.emit(line, curr_block, prev_block)
        #     trainModelToTrainController.sendPolarity.emit(trainID, polarity)
        #
        #     trainObject.calculations["currBlock"] = trainObject.calculations["nextBlock"]
        #     trainObject.navigation_status["prevBlock"] = trainObject.navigation_status["currBlock"]

        # trainObject.calculations["initialized"] = False
        return

    def beacon(self, trainObject):
        if trainObject.calculations["doorSide"] == "Left":
            trainObject.calculations["leftDoor"] = True
            trainObject.calculations["rightDoor"] = False
        elif trainObject.calculations["doorSide"] == "Right":
            trainObject.calculations["leftDoor"] = False
            trainObject.calculations["rightDoor"] = True
        else:
            trainObject.calculations["leftDoor"] = True
            trainObject.calculations["rightDoor"] = True
