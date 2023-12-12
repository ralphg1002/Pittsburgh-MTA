from PyQt5.QtCore import *


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
class TrackModelToTrackController(QObject):
    occupancyState = pyqtSignal(
        int, int, int, bool
    )  # line, wayside controller number, block number, occupancy state


class TrackModelToCTC(QObject):
    throughput = pyqtSignal(int)  # line, ticketsales/hr


class TrackModelToTrainModel(QObject):
    blockInfo = pyqtSignal(
        float, float, float, float, int, int
    )  # next block, length, grade, speed limit, suggested speed, authority
    beacon = pyqtSignal(dict)
    newCurrentPassengers = pyqtSignal(int)
    authority_update = pyqtSignal(str, int) # line number, block number


##########################################################################################
class TrainModelToTrackModel(QObject):
    sendCurrentPassengers = pyqtSignal(
        str, str, int
    )  # Line, station name, current passengers
    sendPolarity = pyqtSignal(str, int, int)  # Line, current block, previous block


class TrainModelToTrainController(QObject):
    sendSpeedLimit = pyqtSignal(str, int)
    sendAuthority = pyqtSignal(str, bool)
    sendLeftDoor = pyqtSignal(str, bool)
    sendRightDoor = pyqtSignal(str, bool)
    sendNextStation1 = pyqtSignal(str, str)
    sendNextStation2 = pyqtSignal(str, str)
    sendCurrStation = pyqtSignal(str, str)
    sendEnterTunnel = pyqtSignal(bool)  # Check, can be in block dictionary
    sendCommandedSpeed = pyqtSignal(str, int)
    sendBlockLength = pyqtSignal(int)  # Check
    sendCurrentSpeed = pyqtSignal(str, int)
    sendTemperature = pyqtSignal(str, int)
    sendPassengerEmergencyBrake = pyqtSignal(str, bool)
    sendEngineFailure = pyqtSignal(str, bool)
    sendSignalPickupFailure = pyqtSignal(str, bool)
    sendBrakeFailure = pyqtSignal(str, bool)
    sendPolarity = pyqtSignal(str, bool)
    sendBlockNumber = pyqtSignal(str, int)


##########################################################################################
class TrainControllerSWToTrainModel(QObject):
    sendPower = pyqtSignal(str, float)
    sendDriverEmergencyBrake = pyqtSignal(str, bool)
    sendDriverServiceBrake = pyqtSignal(str, float)
    sendAnnouncement = pyqtSignal(str, str)
    sendHeadlightState = pyqtSignal(str, bool)
    sendInteriorLightState = pyqtSignal(str, bool)
    sendLeftDoorState = pyqtSignal(str, bool)
    sendRightDoorState = pyqtSignal(str, bool)
    sendSetpointTemperature = pyqtSignal(str, int)
    sendAdvertisement = pyqtSignal(str, int)


#########################################################################################
class CTCTrackController(QObject):
    sendAuthority = pyqtSignal(
        int, int, int, int
    )  # line (1 for green, 2 for red), wayside, block number, authority
    sendSuggestedSpeed = pyqtSignal(
        int, int, int, int
    )  # line, wayside, block number, suggested speed
    sendMaintenance = pyqtSignal(
        int, int, int, bool
    )  # line, wayside, block number, 1 if disabled, 0 if enabled
    sendTrainDispatched = pyqtSignal(
        int, int, str, bool
    )  # line, wayside #, trainID, authority


class CTCToTrackModel(QObject):
    requestThroughput = pyqtSignal(str)  # requests hourly


##########################################################################################
class Master(QObject):
    # Instantiate timing signals
    timingMultiplier = pyqtSignal(int)
    clockSignal = pyqtSignal(QTime)
    addTrain = pyqtSignal(str, str)  # (line, id)


# Instantiation for signals sent from Track Controller
trackControllerToCTC = TrackControllerToCTC()
trackControllerToTrackModel = TrackControllerToTrackModel()

trackModelToTrackController = TrackModelToTrackController()
trackModelToCTC = TrackModelToCTC()
trackModelToTrainModel = TrackModelToTrainModel()

# Instantiation for signals sent from Train Model
trainModelToTrackModel = TrainModelToTrackModel()
trainModelToTrainController = TrainModelToTrainController()

# Instantiation for signals sent from Train Controller (SW)
trainControllerSWToTrainModel = TrainControllerSWToTrainModel()

# Instantiation for signals sent from CTC
ctcToTrackController = CTCTrackController()
ctcToTrackModel = CTCToTrackModel()

# Instantiation of signals shared by multiple classes
masterSignals = Master()
