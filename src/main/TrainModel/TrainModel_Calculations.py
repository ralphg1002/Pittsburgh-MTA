# Importing Libraries
import sys
import math
import re

class Calculations:
    def __init__(self, time_interval, sys_time, trains):
        self.time_interval = time_interval
        self.sys_time = sys_time
        self.trains = trains

    # Sets the power of the train through the train controller
    def power(self, trainObject, power):
        # Ensure that power does not exceed 120
        power /= 1000
        currPower = min(power, 120)

        # Update the "vehicle_status" of "Train 1" in self.trains
        trainObject.vehicle_status["power"] = currPower

        # Calculate current_speed using the updated power
        self.current_speed(trainObject, currPower)

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
        trainObject.calculations["currAcceleration"] = trainObject.calculations["currForce"] / mass
        currAcceleration = self.limit_acceleration(trainObject)

        # Calculate velocity using the velocity function and set it
        currVelocity = self.velocity()
        self.trains.set_value("Train 1", "calculations", "currVelocity", currVelocity)

        # Calculate the distance traveled and set it
        new_position = self.total_distance()

        # Return the current velocity
        return currVelocity

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
        power = self.trains.get_value("Train 1", "vehicle_status", "power")
        currVelocity = self.trains.get_value("Train 1", "calculations", "currVelocity")

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
        self.trains.set_value("Train 1", "calculations", "currAcceleration", acceleration)

        return acceleration

    def velocity(self):
        # Retrieve necessary values from self.trains
        brake = self.trains.get_value("Train 1", "vehicle_status", "brakes")
        emergency_brake = self.trains.get_value("Train 1", "failure_status", "emergency_brake")
        last_acceleration = self.trains.get_value("Train 1", "calculations", "lastAcceleration")
        curr_acceleration = self.trains.get_value("Train 1", "calculations", "currAcceleration")
        last_velocity = self.trains.get_value("Train 1", "calculations", "lastVelocity")

        # Calculate the total acceleration and update velocity
        total_acceleration = last_acceleration + curr_acceleration
        velocity = last_velocity + (self.time_interval / 2) * total_acceleration

        # Limit velocity so that it doesn't go below 0
        if velocity < 0:
            velocity = 0

        # If the train is stopped and brakes or emergency brake are applied, set velocity to 0
        if last_velocity <= 0 and (brake or emergency_brake):
            velocity = 0

        # Set the calculated velocity value
        velocity = self.trains.set_value("Train 1", "calculations", "currVelocity", velocity)

        return velocity

    def total_distance(self):
        # Retrieve necessary values from self.trains
        curr_velocity = self.trains.get_value("Train 1", "calculations", "currVelocity")
        last_position = self.trains.get_value("Train 1", "calculations", "lastPosition")

        # Update total_velocity using the current velocity (consider whether this is necessary)
        total_velocity = curr_velocity

        # Correct the distance calculation (multiply, not divide)
        distance = last_position + (self.time_interval * 2) * total_velocity

        return distance

    def blockID(
            self, next_block, length, grade, speed_limit, suggested_speed, authority
    ):
        self.trains.set_value("Train 1", "calculations", "nextBlock", next_block)
        self.trains.set_value("Train 1", "navigation_status", "length", length)
        self.trains.set_value("Train 1", "navigation_status", "grade", grade)
        self.trains.set_value("Train 1", "vehicle_status", "speed_limit", speed_limit)
        self.trains.set_value("Train 1", "vehicle_status", "suggested_speed", suggested_speed)
        self.trains.set_value("Train 1", "navigation_status", "authority", authority)

        train = self.trains.get_value("Train 1", "calculations", "trainID")

        self.occupancy(next_block)

        # Send train controller information
        trainModelToTrainController.sendBlockLength.emit(length)
        trainModelToTrainController.sendSpeedLimit.emit(train, speed_limit)
        trainModelToTrainController.sendCommandedSpeed.emit(train, suggested_speed)
        trainModelToTrainController.sendAuthority.emit(train, authority)

        return next_block, length, grade, speed_limit, suggested_speed, authority

    def failures(self):
        engine_failure = self.trains.get_value("Train 1", "failure_status", "engine_failure")
        signal_pickup_failure = self.trains.get_value("Train 1", "failure_status", "signal_pickup_failure")
        brake_failure = self.trains.get_value("Train 1", "failure_status", "brake_failure")
        pass_emergency_brake = self.trains.get_value("Train 1", "failure_status", "passenger_emergency_brake")
        train = self.trains.get_value("Train 1", "calculations", "trainID")

        if (
                engine_failure == True
                or signal_pickup_failure == True
                or brake_failure == True
        ):
            trainModelToTrainController.sendEngineFailure.emit(train, engine_failure)
            trainModelToTrainController.sendSignalPickupFailure.emit(
                train, signal_pickup_failure
            )
            trainModelToTrainController.sendBrakeFailure.emit(train, brake_failure)

        if pass_emergency_brake == True:
            trainModelToTrainController.sendPassengerEmergencyBrake.emit(
                train, pass_emergency_brake
            )

        return (
            engine_failure,
            signal_pickup_failure,
            brake_failure,
            pass_emergency_brake,
        )

    def temperature(self, temp):
        set_temp = temp
        curr_temp = self.trains.get_value("Train 1", "vehicle_status", "temperature")
        train = self.trains.get_value("Train 1", "calculations", "trainID")

        if curr_temp < set_temp:
            while curr_temp < set_temp:
                curr_temp += 1
                self.trains.set_value("Train 1", "vehicle_status", "temperature", curr_temp)
                trainModelToTrainController.sendTemperature.emit(train, curr_temp)

        elif set_temp > curr_temp:
            while curr_temp > set_temp:
                curr_temp -= 1
                self.trains.set_value("Train 1", "vehicle_status", "temperature", curr_temp)
                trainModelToTrainController.sendTemperature.emit(train, curr_temp)

        elif set_temp == curr_temp:
            self.trains.set_value("Train 1", "vehicle_status", "temperature", curr_temp)
            trainModelToTrainController.sendTemperature.emit(train, curr_temp)

        return curr_temp

    # Calculate the current number of passengers from the track model
    def passengers(self, passengers):
        curr_passengers = self.trains.get_values("Train 1", "passenger_status", "passengers")
        trainModelToTrackModel.sendCurrentPassengers.emit(curr_passengers, "Train 1")

        self.trains.set_values("Train 1", "passenger_status", "passengers", passengers)

        return passengers

    def occupancy(self, next_block):
        distance = 0
        polarity = 0
        initialized = 0
        # distance = self.total_distance()
        block_length = self.trains.get_value("Train 1", "navigation_status", "block_length")
        next_block = self.trains.set_value("Train 1", "calculations", "nextBlock", next_block)
        curr_block = self.trains.get_value("Train 1", "calculations", "currBlock")
        prev_block = self.trains.get_value("Train 1", "calculations", "prevBlock")
        trainID = self.trains.get_value("Train 1", "calculations", "trainID")
        line = self.trains.get_value("Train 1", "calculations", "line")

        if initialized == 0:
            trainModelToTrackModel.sendPolarity.emit(line, curr_block, prev_block)

        if distance == block_length:
            distance = 0
            polarity = 1
            trainModelToTrackModel.sendPolarity.emit(line, curr_block, prev_block)
            trainModelToTrainController.sendPolarity.emit(trainID, polarity)

            curr_block = next_block
            prev_block = curr_block

        initialized += 1
        if initialized >= 999:
            initialized = 1

    def beacon(self, beacon):
        next_station1 = beacon["Next Station1"]
        next_station2 = beacon["Next Station2"]
        current_station = beacon["Current Station"]
        door_side = beacon["Door Side"]
        train = self.trains.get_value("Train 1", "calculations", "trainID")

        trainModelToTrainController.sendNextStation1.emit(train, next_station1)
        trainModelToTrainController.sendNextStation2.emit(train, next_station2)
        trainModelToTrainController.sendCurrStation.emit(train, current_station)

        if door_side == "Left":
            trainModelToTrainController.sendLeftDoor.emit(train, door_side)
        elif door_side == "Right":
            trainModelToTrainController.sendRightDoor.emit(train, door_side)
        else:
            trainModelToTrainController.sendLeftDoor.emit(train, door_side)
            trainModelToTrainController.sendRightDoor.emit(train, door_side)

        return next_station1, next_station2, current_station, door_side
