# importing libraries
import sys
import math
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from tcsw_input import *
from tcsw_output import *
from tcsw_internal import *
import time

# Set the initial time to 00:00:00
current_time = 0

# Define the time increment to make time appear to go faster
time_increment = 0  # You can decrease this value to make time go faster

# Calculate the total seconds in a day
total_seconds_in_a_day = 24 * 60 * 60

freeze = False

while current_time < 1:
    if current_time == total_seconds_in_a_day:
        current_time = 0
    hours = current_time // 3600
    minutes = (current_time % 3600) // 60
    seconds = current_time % 60
    military_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    print("Current Time (Military Time):", military_time)
    if freeze:
        current_time += 0
    else:
        current_time += 1
    time.sleep(time_increment)  # Simulate the passage of real-time seconds

inputs = TCInput()
outputs = TCOutput()
test = TCInternal()

# UPDATE POWER ##
# Update Setpoint Speed #
# Manual Mode #
if inputs.mode == 0:
    inputs.set_drvrSpSpd(inputs.drvrSpSpd)

# Automatic Mode #
else:
    inputs.set_drvrSpSpd(inputs.cmdSpd)
    if test.stop_train(inputs.auth):
        inputs.set_sbrk(test.sbrkStatus)

# Regardless of mode #
# based on service brake status:
if test.is_sbrk(inputs.sbrk, inputs.currSpd):
    print("sbrk")
    inputs.set_drvrSpSpd(test.sbrkSpd)

# based on emergency brake status:
if test.is_ebrk(inputs.paxEbrk, inputs.drvrEbrk, inputs.currSpd):
    print("ebrk")
    inputs.set_drvrSpSpd(test.ebrkSpd)
    inputs.set_drvrEbrk(test.ebrkStatus)

# based on failures:
if test.is_fail(
    inputs.engnFail, inputs.sgnlFail, inputs.brkFail, inputs.drvrEbrk, inputs.currSpd
):
    print("fail")
    inputs.set_drvrSpSpd(test.ebrkSpd)
    inputs.set_drvrEbrk(test.ebrkStatus)

test.pi_ctrl(inputs.kp, inputs.ki, inputs.currSpd, outputs.spSpd, 1)
outputs.set_pwr_cmd(outputs.pwrCmd + test.pwrCmd)

# UPDATE STATION RELATED STUFF ##
# Manual mode #
if inputs.mode == 0:
    outputs.set_l_door(inputs.drvrLDoor)
    outputs.set_r_door(inputs.drvrRDoor)
    outputs.set_anncmnt(inputs.drvrAnncmnt)

# Automatic mode #
else:
    if test.is_station(
        inputs.tnl,
        inputs.upd,
        inputs.prevStop,
        inputs.nextStop,
        inputs.leftDoor,
        inputs.rightDoor,
        inputs.auth,
    ):
        outputs.set_l_door(test.station["leftDoor"])
        outputs.set_r_door(test.station["rightDoor"])
        outputs.set_anncmnt(test.station["announcement"])
        inputs.set_drvr_lDoor(test.station["leftDoor"])
        inputs.set_drvr_rDoor(test.station["rightDoor"])
        inputs.set_drvr_anncmnt(test.station["announcement"])

# UPDATE LIGHTS ##
# Manual mode #
if inputs.mode == 0:
    outputs.set_hdlt(inputs.drvrHdlt)
    outputs.set_ilt(inputs.drvrIlt)

# Automatic mode #
else:
    if test.is_lights(inputs.tnl, 1000):
        outputs.set_hdlt(test.lights["headlights"])
        outputs.set_ilt(test.lights["interiorlights"])
        inputs.set_drvr_hdlt(test.lights["headlights"])
        inputs.set_drvr_ilt(test.lights["interiorlights"])

# Misc. ##
# Manual Mode #
if inputs.mode == 0:
    outputs.set_sp_temp(inputs.drvrTemp)
    outputs.set_ad(inputs.drvrAd)

# Automatic Mode #
else:
    outputs.set_sp_temp(70)
    outputs.set_ad("")

# test
print(inputs.currSpd)
print(outputs.spSpd)
print(test.pwrCmd)
