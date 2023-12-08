import unittest
import math
from tcsw_train_attributes import *
from tcsw_functions import *

class TestTrainControllerSW(unittest.TestCase):
    def test_headlights(self):
        train = Train("green_test")
        functions = TCFunctions()
        train.block["isTunnel"] = True

        functions.add_train(train)
        functions.automatic_operations(train)

        self.assertEqual(train.get_headlights(), True)  # add assertion here

    def test_announcement(self):
        train = Train("green_test")
        functions = TCFunctions()
        train.block["isStation"] = True
        train.beacon["currStop"] = "Central"
        train.set_authority(False)
        train.set_currentSpeed(0)

        functions.add_train(train)
        functions.automatic_operations(train)

        check = False
        if train.get_announcement() == "This is Central.":
            check = True

        self.assertEqual(check, True)

    # when emergency brake is pulled
    def test_ebrake(self):
        train = Train("green_test")
        functions = TCFunctions()
        train.set_authority(True)
        train.set_currentSpeed(0)
        train.set_commandedSpeed(30)
        train.set_driverEbrake(True)

        functions.add_train(train)
        functions.automatic_operations(train)
        functions.regular_operations(functions.greenBlockDict, train)

        check = False
        if train.get_powerCommand() == 0:
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
