import unittest
import sys
from src.main.TrainModel.TrainModel_Functions import TrainModelAttributes

sys.path.append("../../main")
from signals import (
    trainControllerSWToTrainModel
)


class TestTrainModel(unittest.TestCase):

    def test_signal_interior_lights(self):
        #train_model_value = TrainModelAttributes("id")
        masterSignal()
        trainControllerSWToTrainModel.sendInteriorLightState.emit("id", True)

        result1 = train_model_value.passenger_status["lights_status"]

        self.assertEqual(result1, True)

    def test_signal_headlights(self):
        train_model_value = TrainModelAttributes("id")

        trainControllerSWToTrainModel.sendHeadlightState.emit("id", True)

        result2 = train_model_value.navigation_status["headlights"]

        self.assertEqual(result2, True)


if __name__ == '__main__':
    unittest.main()
