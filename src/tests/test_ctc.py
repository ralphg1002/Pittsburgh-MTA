import unittest
from src.main.CTC.CTC_UI import CTCWindow
from src.main.signals import ctcToTrackController
from unittest.mock import patch

class TestCTC(unittest.TestCase):

    @patch('src.main.signals.ctcToTrackController.sendTrainDispatched')
    def testDispatchTrain1(self, mock_sendTrainDispatched):
        ctc = CTCWindow()

        # Example parameters for dispatching a train
        line = 1
        wayside_number = 1 
        train_id = "Train123" 
        authority = True

        ctc.dispatch_train(line, wayside_number, train_id, authority)

        # Check if the signal was correctly sent with the expected parameters
        mock_sendTrainDispatched.assert_called_with(line, wayside_number, train_id, authority)


if __name__ == '__main__':
    unittest.main()