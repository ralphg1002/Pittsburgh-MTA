# importing libraries
import sys
import math
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import time


class SystemTime:
    def __init__(self):
        # Set the initial time to 00:00:00
        self.currentTime = 0

        # Define the time increment to make time appear to go faster
        self.timeIncrement = 1  # You can decrease this value to make time go faster

        # Calculate the total seconds in a day
        self.totalSecondsinADay = 24 * 60 * 60

        self.freeze = False

    def start(self):
        while True:
            # reset the time
            if self.currentTime == self.totalSecondsinADay:
                self.currentTime = 0

            # if time is ever stopped
            if self.freeze:
                self.currentTime += 0
            else:
                self.currentTime += 1
            print(self.convert_to_military())
            # delay based on time increment
            time.sleep(self.timeIncrement)

    def convert_to_military(self):
        hours = self.currentTime // 3600
        minutes = (self.currentTime % 3600) // 60
        seconds = self.currentTime % 60
        militaryTime = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        return militaryTime

    def set_timeIncrement(self, timeIncrement):
        self.timeIncrement = timeIncrement

    def set_freeze(self, freeze):
        self.freeze = freeze


sysTime = SystemTime()
sysTime.set_timeIncrement(10)
sysTime.start()
