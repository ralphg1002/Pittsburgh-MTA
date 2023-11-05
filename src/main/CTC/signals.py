from PyQt5.QtCore import QObject, pyqtSignal


class CTCSignals(QObject):
    sendOccupancyCTC = pyqtSignal(int, int, bool)  # line, block number, state
    sendFailureStateCTC = pyqtSignal(int, int, bool)  # line, block number, state
    sendSwitchStateCTC = pyqtSignal(int, int, bool)  # line, block number, state
    sendLightStateCTC = pyqtSignal(int, int, str)  # line, block number, state
    sendTicketSalesCTC = pyqtSignal(int, int)  # line, ticket sales


class CTCTrackController(QObject):
    sendAuthority = pyqtSignal(
        int, int, int, int
    )  # line (1 for green, 2 for red), block number, authority
    sendSuggestedSpeed = pyqtSignal(
        int, int, int, int
    )  # line, block number, suggested speed
    sendMaintenance = pyqtSignal(
        int, int, int, bool
    )  # line, block number, 1 if disabled, 0 if enabled


# list of lists, bloc, aut, speed


class TrackModelSignals(QObject):
    sendSwitchStateTrackModel = pyqtSignal(
        int, int, int, bool
    )  # line, block number, state
    sendLightStateTrackModel = pyqtSignal(
        int, int, int, str
    )  # line, block number, state
    sendCrossingStateTrackModel = pyqtSignal(
        int, int, int, bool
    )  # line, block number, state


CTCtoTrackController = CTCTrackController()
TrackControllerToCTC = CTCSignals()
TrackControllerTrackModel = TrackModelSignals()
