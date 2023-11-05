from PyQt5.QtCore import QObject, pyqtSignal


##########################################################################################
class TrackControllerToCTC(QObject):
    occupancyState = pyqtSignal(int, int, bool)  # line, block number, state
    failureState = pyqtSignal(int, int, bool)  # line, block number, state
    switchState = pyqtSignal(int, int, bool)  # line, block number, state
    requestSpeed = pyqtSignal(int, int)  # line, block number


class TrackControllerToTrackModel(QObject):
    switchState = pyqtSignal(int, int, int, bool)  # line, block number, state
    lightState = pyqtSignal(int, int, int, str)  # line, block number, state
    crossingState = pyqtSignal(int, int, int, bool)  # line, block number, state
    suggestedSpeed = pyqtSignal(
        int, int, int, float
    )  # line, block number, suggested speed
    authority = pyqtSignal(int, int, int, int)  # line, block number, authority
    maintenance = pyqtSignal(int, int, int, bool)


##########################################################################################
class TrainModelToTrackModel(QObject):
    sendCurrentPassengers = pyqtSignal(int)
    sendMaxPassengers = pyqtSignal(int)


class TrainModelToTrainController(QObject):
    sendSpeedLimit = pyqtSignal(int)
    sendAuthority = pyqtSignal(int)
    sendLeftDoor = pyqtSignal(bool)
    sendRightDoor = pyqtSignal(bool)
    sendNextStation = pyqtSignal(str)
    sendPrevStation = pyqtSignal(str)
    sendEnterTunnel = pyqtSignal(bool)
    sendCommandedSpeed = pyqtSignal(int)
    sendBlockLength = pyqtSignal(int)
    sendCurrentPassengers = pyqtSignal(int)
    sendMaxPassengers = pyqtSignal(int)
    sendCurrentSpeed = pyqtSignal(int)
    sendTemperature = pyqtSignal(int)
    sendPassengerEmergencyBrake = pyqtSignal(bool)
    sendEngineFailure = pyqtSignal(bool)
    sendSignalPickupFailure = pyqtSignal(bool)
    sendBrakeFailure = pyqtSignal(bool)


##########################################################################################


# Instantiate timing signals
timingMultiplier = pyqtSignal(float)
clockSignal = pyqtSignal(str)

# Instantiation for signals sent from Track Controller
trackControllerToCTC = TrackControllerToCTC()
trackControllerToTrackModel = TrackControllerToTrackModel()


# Instantiation for signals sent from Train Model
trainModelToTrackModel = TrainModelToTrackModel()
trainModelToTrainController = TrainModelToTrainController()
