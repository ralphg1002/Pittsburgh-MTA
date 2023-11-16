# Importing Libraries
import sys
import math
import re


class Calculations:
    def __init__(self):
        placeholder = True

    # Sets the power of the train through the train controller
    def power(self, trainObject):
        # Ensure that power does not exceed 120
        trainObject.vehicle_status["power"] /= 1000
        currPower = min(trainObject.vehicle_status["power"], 120)

        # Update the "vehicle_status" of "Train 1" in self.trains
        trainObject.vehicle_status["power"] = currPower

        # Calculate current_speed using the updated power
        self.current_speed(trainObject, currPower)

        print("Power =", trainObject.vehicle_status["power"])

    def current_speed(self, trainObject, currPower):
        # Retrieve necessary values from self.trains
        lastVelocity = trainObject.calculations["lastVelocity"]
        mass = trainObject.calculations["mass"]

        if lastVelocity == 0:
            lastVelocity = 0.001

        currForce = currPower / lastVelocity

        # Set calculated force and apply force limit
        trainObject.calculations["currForce"] = currForce

        self.limit_force(trainObject)

        # Calculate acceleration from force and set it, applying acceleration limit
        trainObject.calculations["currAcceleration"] = (
            trainObject.calculations["currForce"] / mass
        )
        self.limit_acceleration(trainObject)

        # Calculate velocity using the velocity function and set it
        self.velocity(trainObject)

        # Calculate the distance traveled and set it
        self.total_distance(trainObject)

    def limit_force(self, trainObject):
        # Retrieve necessary values from self.trains
        emergency_brake = trainObject.failure_status["emergency_brake"]
        mass = trainObject.calculations["mass"]
        force = trainObject.calculations["currForce"]
        power = trainObject.vehicle_status["power"]
        lastVelocity = trainObject.calculations["lastVelocity"]

        # Limit the force of the train
        if force > (mass * 0.5):
            force = mass * 0.5
        elif (power == 0 and lastVelocity == 0) or emergency_brake:
            force = 0
        elif lastVelocity == 0:
            force = mass * 0.5

        # Set the limited force value
        trainObject.calculations["currForce"] = force

    def limit_acceleration(self, trainObject):
        # Retrieve necessary values from self.trains
        failure_1 = trainObject.failure_status["engine_failure"]
        failure_2 = trainObject.failure_status["signal_pickup_failure"]
        failure_3 = trainObject.failure_status["brake_failure"]
        brakes = trainObject.vehicle_status["brakes"]
        emergency_brake = trainObject.failure_status["emergency_brake"]
        force = trainObject.calculations["currForce"]
        mass = trainObject.calculations["mass"]
        power = trainObject.vehicle_status["power"]
        currVelocity = trainObject.calculations["currVelocity"]

        # Limit the acceleration of the train based on various conditions
        if (failure_1 or failure_2 or failure_3) and (brakes or emergency_brake):
            acceleration = (force - (0.01 * mass * 9.8)) / mass
        elif power == 0 and currVelocity > 0:
            if emergency_brake:
                acceleration = -2.73
            else:
                acceleration = -1.2
        elif power != 0:
            if force > 0.5:
                acceleration = 0.5
            else:
                acceleration = force / mass
        else:
            acceleration = 0

        # Set the limited acceleration value
        trainObject.calculations["currAcceleration"] = acceleration

    def velocity(self, trainObject):
        # Retrieve necessary values from self.trains
        brake = trainObject.vehicle_status["brakes"]
        emergency_brake = trainObject.failure_status["emergency_brake"]
        last_acceleration = trainObject.calculations["lastAcceleration"]
        curr_acceleration = trainObject.calculations["currAcceleration"]
        last_velocity = trainObject.calculations["lastVelocity"]

        # Calculate the total acceleration and update velocity
        total_acceleration = last_acceleration + curr_acceleration
        velocity = (
            last_velocity
            + (trainObject.calculations["timeInterval"] / 2) * total_acceleration
        )

        # Limit velocity so that it doesn't go below 0
        if velocity < 0:
            velocity = 0

        # If the train is stopped and brakes or emergency brake are applied, set velocity to 0
        if last_velocity <= 0 and (brake or emergency_brake):
            velocity = 0

        # Set the calculated velocity value
        trainObject.calculations["currVelocity"] = velocity

    def total_distance(self, trainObject):
        # Retrieve necessary values from self.trains
        curr_velocity = trainObject.calculations["currVelocity"]
        last_position = trainObject.calculations["lastPosition"]

        # Update total_velocity using the current velocity (consider whether this is necessary)
        total_velocity = curr_velocity

        # Correct the distance calculation (multiply, not divide)
        distance = (
            last_position
            + (trainObject.calculations["timeInterval"] * 2) * total_velocity
        )

        trainObject.calculations["distance"] = distance

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
