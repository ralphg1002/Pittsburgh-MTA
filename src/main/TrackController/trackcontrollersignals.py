from PyQt5.QtCore import QObject, pyqtSignal


class CTCSignals(QObject):
    sendOccupancyCTC = pyqtSignal(int, int, bool)  # line, block number, state
    sendFailureStateCTC = pyqtSignal(int, int, bool)  # line, block number, state
    sendSwitchStateCTC = pyqtSignal(int, int, bool)  # line, block number, state
    sendLightStateCTC = pyqtSignal(int, int, str)  # line, block number, state
    sendTicketSalesCTC = pyqtSignal(int, int)  # line, ticket sales


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


TrackControllerToCTC = CTCSignals()
TrackControllerToTrackModel = TrackModelSignals()
