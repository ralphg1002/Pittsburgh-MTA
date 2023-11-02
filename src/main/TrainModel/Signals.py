from PyQt5.QtCore import QObject, pyqtSignal

class TrackModelSignals(QObject):
    sendCurrentPassengers = pyqtSignal(int)
    sendMaxPassengers = pyqtSignal(int)

class TrainControllerSignals(QObject):
    sendSpeedLimit = pyqtSignal(int)
    sendAuthority = pyqtSignal(int)
    sendLeftDoor = pyqtSignal(bool)
    sendRightDoor = pyqtSignal(bool)
    sendNextStation = pyqtSignal("")
    sendPrevStation = pyqtSignal("")
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
