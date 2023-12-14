# Importing Libraries
from decimal import DivisionByZero
import sys
import math
import re


class Calculations:
    def __init__(self):
        placeholder = True

    def TrainModelCalculations(self, trainObject):
        self.updateMass(trainObject)
        self.checkFailureModes(trainObject)
        self.calculateBrakes(trainObject)
        self.calculateEngineForce(trainObject)
        self.calculateSlopeForce(trainObject)
        self.calculateFrictionForce(trainObject)
        self.calculateNetForce(trainObject)
        self.calculateAcceleration(trainObject)
        self.calculateCurrentSpeed(trainObject)
        self.updatePosition(trainObject)

    def updateMass(self, trainObject):
        trainObject.calculations["mass"] = trainObject.calculations["empty_mass"] + (trainObject.passenger_status["passengers"] * 150)

        print("mass:", trainObject.calculations["mass"])

        if trainObject.calculations["mass"] >= trainObject.calculations["full_mass"]:
            trainObject.calculations["mass"] = trainObject.calculations["full_mass"]

    def checkFailureModes(self, trainObject):
        if trainObject.failure_status["engine_failure"] == True:
            trainObject.vehicle_status["power"] = 0
            trainObject.failure_status["emergency_brake"] = True
        
        if trainObject.failure_status["signal_pickup_failure"] == True:
            trainObject.navigation_status["beacon"] = ""
            trainObject.navigation_status["next_station"] = ""
            trainObject.navigation_status["prev_station"] = ""

        if trainObject.failure_status["brake_failure"] == True:
            trainObject.vehicle_status["power"] = 0
            trainObject.failure_status["emergency_brake"] = True

        # if not trainObject.failure_status["engine_failure"]:


    def calculateAcceleration(self, trainObject):
        trainObject.calculations["currAcceleration"] = trainObject.calculations["totalForce"] / trainObject.calculations["mass"]
        trainObject.calculations["lastAcceleration"] = trainObject.calculations["currAcceleration"]
        trainObject.vehicle_status["acceleration"] = trainObject.calculations["currAcceleration"]

        print("current acceleration:", trainObject.calculations["currAcceleration"])
        print("last acceleration:", trainObject.calculations["lastAcceleration"])

    def calculateEngineForce(self, trainObject):
        try:
        # epsilon = 1e-10
            trainObject.calculations["currEngineForce"] = abs(trainObject.vehicle_status["power"] / (trainObject.vehicle_status["current_speed"] * 1000 / 3600))
        except ZeroDivisionError:
            # trainObject.vehicle_status["current_speed"] = 1*10^-10
            trainObject.calculations["currEngineForce"] = 18.1

        print("current engine force:", trainObject.calculations["currEngineForce"])
        print("power is:", trainObject.vehicle_status["power"])

    def calculateSlopeForce(self, trainObject):
        trainObject.calculations["currAngle"] = math.atan(trainObject.navigation_status["block_grade"] / 100)
        trainObject.calculations["slopeForce"] = trainObject.calculations["mass"] * 0.98 * math.sin(trainObject.calculations["currAngle"]) / 1000

        print("current angle:", trainObject.calculations["currAngle"])
        print("slope force:", trainObject.calculations["slopeForce"])

    def calculateFrictionForce(self, trainObject):
        # trainObject.calculations["frictionForce"] = 1000
        mu = (0.35 + 0.5) / 2
        trainObject.calculations["frictionForce"] = mu * trainObject.calculations["mass"] / 1000

        print("friction force:", trainObject.calculations["frictionForce"])

    def calculateBrakes(self, trainObject):
        if (trainObject.vehicle_status["brakes"] and not trainObject.failure_status["emergency_brake"]):
            trainObject.calculations["brakeForce"] = 1.2 # * trainObject.calculations["mass"]
        
        if (trainObject.failure_status["emergency_brake"] and not trainObject.vehicle_status["brakes"]):
            trainObject.calculations["brakeForce"] = 2.73 # * trainObject.calculations["mass"]
        
        if (not trainObject.vehicle_status["brakes"] and not trainObject.failure_status["emergency_brake"]):
            trainObject.calculations["brakeForce"] = 0 # * trainObject.calculations["mass"]

        if (trainObject.vehicle_status["brakes"] and trainObject.failure_status["emergency_brake"]):
            trainObject.calculations["brakeForce"] = 3.93 # * trainObject.calculations["mass"]
    
    def calculateNetForce(self, trainObject):
        trainObject.calculations["totalForce"] = trainObject.calculations["currEngineForce"] - trainObject.calculations["slopeForce"] - trainObject.calculations["brakeForce"] - trainObject.calculations["frictionForce"]

        print(f"total force is {trainObject.calculations['totalForce']} = to current engine force {trainObject.calculations['currEngineForce']} - slope force {trainObject.calculations['slopeForce']} - brake force {trainObject.calculations['brakeForce']} - friction force {trainObject.calculations['frictionForce']}")
        
        if trainObject.vehicle_status["current_speed"] != 0:
            force_limit = 120 / trainObject.vehicle_status["current_speed"]
            trainObject.calculations["totalForce"] = min(trainObject.calculations["totalForce"], force_limit)

    def calculateCurrentSpeed(self, trainObject):
        if trainObject.vehicle_status["power"] <= 120:
            # trainObject.vehicle_status["current_speed"] = trainObject.vehicle_status["current_speed"] + (trainObject.calculations["timeInterval"] * 0.001 / 2) * (trainObject.calculations["currAcceleration"] + trainObject.calculations["lastAcceleration"])
            trainObject.vehicle_status["current_speed"] = trainObject.vehicle_status["current_speed"] + (trainObject.calculations["timeInterval"] / 2) * (trainObject.calculations["currAcceleration"] + trainObject.calculations["lastAcceleration"])

        if trainObject.vehicle_status["current_speed"] < 0:
            trainObject.vehicle_status["current_speed"] = 0

        if trainObject.vehicle_status["current_speed"] > 70:
            trainObject.vehicle_status["current_speed"] = 70

        if trainObject.vehicle_status["current_speed"] > trainObject.vehicle_status["speed_limit"] * 1.609344:
            trainObject.vehicle_status["current_speed"] = trainObject.vehicle_status["speed_limit"] * 1.609344

        print("current speed:", trainObject.vehicle_status["current_speed"])
        print("time interval:", trainObject.calculations["timeInterval"])
        print("current acceleration:", trainObject.calculations["currAcceleration"])
        print("last acceleration:", trainObject.calculations["lastAcceleration"])

    def updatePosition(self, trainObject):
        # self.distanceFromYard += self.currentSpeed * (trainObject.calculations["timeInterval"] * 0.001)
        # self.distanceFromBlockStart += self.currentSpeed * (trainObject.calculations["timeInterval"] * 0.001)
        # trainObject.calculations["distance"] += trainObject.vehicle_status["current_speed"] * (trainObject.calculations["timeInterval"] * 0.001)
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

    def temperature(self, trainObject):
        set_temp = trainObject.calculations["setpoint_temp"]
        curr_temp = trainObject.passenger_status["temperature"]
        train = trainObject.calculations["trainID"]

        if curr_temp < set_temp:
            while curr_temp < set_temp:
                curr_temp += 1
                trainObject.passenger_status["temperature"] = curr_temp
                # trainModelToTrainController.sendTemperature.emit(train, curr_temp)

        elif set_temp > curr_temp:
            while curr_temp > set_temp:
                curr_temp -= 1
                trainObject.passenger_status["temperature"] = curr_temp
                # trainModelToTrainController.sendTemperature.emit(train, curr_temp)

        elif set_temp == curr_temp:
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