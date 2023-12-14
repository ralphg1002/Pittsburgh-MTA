import unittest
import math
from tcsw_train_attributes import *
from tcsw_functions import *

class TestTrainControllerSW(unittest.TestCase):
    def test_setpointSpeed(self):
        train = Train("green_test")
        train.set_authority(True)
        train.set_commandedSpeed(10)
        train.set_speedLimit(30)

        functions = TCFunctions()
        functions.add_train(train)
        functions.automatic_operations(train)

        self.assertEqual(train.get_setpointSpeed()==10, True)

    def test_setpointTemp(self):
        train = Train("green_test")
        train.set_auto(False)
        train.set_setpointTemp(50)

        self.assertEqual(train.setpointTemp==50, True)

        # when emergency brake is pulled

    def test_ebrake(self):
        train = Train("green_test")
        functions = TCFunctions()
        train.set_authority(True)
        train.speedLimit = 30
        train.set_currentSpeed(20)
        train.set_commandedSpeed(30)
        train.set_driverEbrake(True)

        functions.add_train(train)
        functions.automatic_operations(train)
        functions.regular_operations(functions.greenBlockDict, train)

        check = False
        if train.get_powerCommand() == 0:
            check = True

        self.assertEqual(check, True)

    def test_sbrake(self):
        train = Train("green_test")
        train.set_authority(True)
        train.set_commandedSpeed(30)
        train.set_speedLimit(30)
        train.set_currentSpeed(20)
        train.set_auto(False)
        train.set_driverSbrake(1)

        functions = TCFunctions()
        functions.add_train(train)
        functions.automatic_operations(train)
        functions.regular_operations(functions.greenBlockDict, train)

        self.assertEqual(train.powerCommand == 0, True)

    def test_kpki(self):
        train = Train("green_test")
        train.set_kp(2)
        train.set_ki(2)

        functions = TCFunctions()
        functions.add_train(train)
        functions.automatic_operations(train)
        functions.regular_operations(functions.greenBlockDict, train)

        self.assertEqual(train.ki == 2 and train.kp == 2, True)

    def test_setpointSpeedManual(self):
        train = Train("green_test")
        train.set_authority(False)
        train.set_commandedSpeed(10)
        train.set_speedLimit(10)
        train.set_setpointSpeed(10)
        if train.setpointSpeed != 10:
            self.assertEqual(False, True)

        train.set_setpointSpeed(8)
        if train.setpointSpeed != 8:
            self.assertEqual(False, True)

        train.set_setpointSpeed(11)
        if train.setpointSpeed != 8:
            self.assertEqual(False, True)

        functions = TCFunctions()
        functions.add_train(train)
        functions.automatic_operations(train)
        functions.regular_operations(functions.greenBlockDict, train)

        self.assertEqual(True, True)

    def test_interiorLights(self):
        train = Train("green_test")
        functions = TCFunctions()
        train.block["isTunnel"] = True

        functions.add_train(train)
        functions.automatic_operations(train)

        self.assertEqual(train.get_interiorLights(), True)

    def test_headlights(self):
        train = Train("green_test")
        functions = TCFunctions()
        train.block["isTunnel"] = True

        functions.add_train(train)
        functions.automatic_operations(train)

        self.assertEqual(train.get_headlights(), True)  # add assertion here

    def test_station(self):
        train = Train("green_test")
        functions = TCFunctions()
        train.set_authority(False)
        train.speedLimit = 30
        train.set_currentSpeed(0)
        train.set_commandedSpeed(0)
        train.block["isStation"] = True
        train.beacon["currStop"] = "GLENBURY"
        train.beacon["leftStation"] = True

        functions.add_train(train)
        functions.automatic_operations(train)
        functions.regular_operations(functions.greenBlockDict, train)

        check = False
        if(train.leftDoor == True and train.announcement == "This is GLENBURY." and train.powerCommand == 0):
            check = True

        self.assertEqual(check, True)

    # emergency brake not pulled, but commanded speed is different from current speed
    # automatic mode
    def test_power(self):
        train = Train("green_test")
        functions = TCFunctions()
        train.block["isStation"] = True
        train.beacon["currStop"] = "Central"
        train.set_authority(True)
        train.set_speedLimit(30)
        train.set_currentSpeed(0)
        train.set_commandedSpeed(30)

        functions.add_train(train)
        functions.automatic_operations(train)
        functions.regular_operations(functions.greenBlockDict, train)
        print(train.get_powerCommand())

        check = False
        if math.floor(train.get_powerCommand()) == 20:
            check = True

        self.assertEqual(check, True)


if __name__ == '__main__':
    unittest.main()
