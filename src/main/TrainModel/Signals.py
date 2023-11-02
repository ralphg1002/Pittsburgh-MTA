from PyQt5.QtCore import QObject, pyqtSignal

class TrackModelSignals(QObject):
    sendCurrentPassengers = pyqtSignal(int)
    sendMaxPassengers = pyqtSignal(int)

class TrainControllerSignals(QObject):
    sendLeftDoor = pyqtSignal(bool)
    sendRightDoor = pyqtSignal(bool)
    sendNextStation = pyqtSignal("")
    sendPrevStation = pyqtSignal("")
    sendEnterTunnel = pyqtSignal(bool)
    sendCurrentSpeed = pyqtSignal(int)
    sendTemperature = pyqtSignal(int)
    sendPassengerEmergencyBrake = pyqtSignal(bool)
    sendEngineFailure = pyqtSignal(bool)
    sendSignalPickupFailure = pyqtSignal(bool)
    sendBrakeFailure = pyqtSignal(bool)
