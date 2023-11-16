# Importing Libraries
import sys
import math
import re

class TrainModelAttributes:
    def __init__(self, trainID):
        self.vehicle_status = {"speed_limit": 0,
                               "current_speed": 0,
                               "setpoint_speed": 0,
                               "commanded_speed": 0,
                               "acceleration": 0,
                               "brakes": 0,
                               "power": 0,
                               "power_limit": 0}

        self.failure_status = {"engine_failure": False,
                               "signal_pickup_failure": False,
                               "brake_failure": False,
                               "emergency_brake": False}
        
        self.passenger_status = {"passengers": 6,
                                "passenger_limit": 74,
                                "left_door": False,
                                "right_door": False,
                                "lights_status": False,
                                "announcements": "",
                                "temperature": 0,
                                "air_conditioning": False,
                                "advertisements": 0}
        
        self.navigation_status = {"authority": 0,
                                 "beacon": 0,
                                 "block_length": 0,
                                 "block_grade": 0,
                                 "next_station": "",
                                 "prev_station": "",
                                 "headlights": False,
                                 "passenger_emergency_brake": False}
        
        self.calculations = {"cars": 5,
                            "mass": 5 * 56700,
                            "length": 5 * 105.6,
                            "currVelocity": 0,
                            "currForce": 0,
                            "currAcceleration": 0,
                            "lastVelocity": 0,
                            "lastAcceleration": 0,
                            "lastPosition": 0,
                            "nextBlock": 0,
                            "currBlock": 0,
                            "prevBlock": 0,
                            "nextStation1": "",
                            "nextStation2": "",
                            "currStation": "",
                            "doorSide": "",
                            "line": "Green",
                            "distance": 0,
                            "initialized": True,
                            "polarity": True,
                            "setpoint_temp": 0,
                            "leftDoor": False,
                            "rightDoor": False,
                            "trainID": trainID}