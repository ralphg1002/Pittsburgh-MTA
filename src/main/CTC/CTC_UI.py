# importing libraries
import sys
import math
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import csv
from datetime import datetime, timedelta

from numpy import block

sys.path.append("../../main")
from signals import masterSignals
from signals import ctcToTrackController
from signals import trackControllerToCTC
from signals import ctcToTrackModel
from signals import trackModelToCTC

# Global variables for the block numbers associated with each wayside
WAYSIDE_1G_BLOCKS = [
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13,
    14,
    15,
    16,
    17,
    18,
    19,
    20,
    21,
    22,
    23,
    24,
    25,
    26,
    27,
    28,
    29,
    30,
    31,
    32,
    33,
    34,
    35,
    36,
    37,
    38,
    39,
    40,
    41,
    42,
    43,
    44,
    45,
    46,
    47,
    48,
    49,
    50,
    51,
    52,
    53,
    54,
    55,
    56,
    57,
    58,
    102,
    103,
    104,
    105,
    106,
    107,
    108,
    109,
    110,
    111,
    112,
    113,
    114,
    115,
    116,
    117,
    118,
    119,
    120,
    121,
    122,
    123,
    124,
    125,
    126,
    127,
    128,
    129,
    130,
    131,
    132,
    133,
    134,
    135,
    136,
    137,
    138,
    139,
    140,
    141,
    142,
    143,
    144,
    145,
    146,
    147,
    148,
    149,
    150,
]
WAYSIDE_2G_BLOCKS = [
    0,
    59,
    60,
    61,
    62,
    63,
    64,
    65,
    66,
    67,
    68,
    69,
    70,
    71,
    72,
    73,
    74,
    75,
    76,
    77,
    78,
    79,
    80,
    81,
    82,
    83,
    84,
    85,
    86,
    87,
    88,
    89,
    90,
    91,
    92,
    93,
    94,
    95,
    96,
    97,
    98,
    99,
    100,
    101,
]

# Global variable declaration
global_block_occupancy = {}


class CTCWindow(QMainWindow):
    # font variables
    textFontSize = 9
    labelFontSize = 12
    headerFontSize = 16
    titleFontSize = 22
    fontStyle = "Product Sans"
    # color variables
    colorDarkBlue = "#085394"
    colorLightRed = "#EA9999"
    colorLightBlue = "#9FC5F8"
    colorLightGrey = "#CCCCCC"
    colorMediumGrey = "#DDDDDD"
    colorDarkGrey = "#666666"
    colorBlack = "#000000"
    # dimensions
    w = 960
    h = 960
    moduleName = "CTC"

    def __init__(self):
        super().__init__()
        self.mode_handler = ModeHandler(self)
        self.scheduler = Scheduler(self)
        # setting title
        self.setWindowTitle(self.moduleName)

        # setting geometry
        self.setGeometry(50, 50, self.w, self.h)

        """main window template layout"""
        # body block
        self.bodyBlock = QLabel(self)
        self.bodyBlock.setGeometry(20, 20, 920, 920)
        self.bodyBlock.setStyleSheet(
            "background-color: white;" "border: 1px solid black"
        )

        # header block
        self.headerBlock = QLabel(self)
        self.headerBlock.setGeometry(20, 20, 920, 70)
        self.headerBlock.setStyleSheet(
            "background-color:" + self.colorDarkBlue + ";" "border: 1px solid black"
        )

        # title
        self.titleLabel = QLabel(
            "Pittsburgh Metropolitan Transportation Authority", self
        )
        self.titleLabel.setFont(QFont(self.fontStyle, self.titleFontSize))
        self.titleLabel.setAlignment(Qt.AlignCenter)
        self.titleLabel.setGeometry(120, 35, 400, 400)
        self.titleLabel.adjustSize()
        self.titleLabel.setStyleSheet("color: white")

        # logo
        self.pixmapMTALogo = QtGui.QPixmap("src/main/CTC/MTA_NYC_logo.svg.png")
        self.pixmapMTALogo = self.pixmapMTALogo.scaled(70, 70)
        self.logo = QLabel(self)
        self.logo.setPixmap(self.pixmapMTALogo)
        self.logo.move(20, 20)
        self.logo.adjustSize()

        # module
        self.moduleLabel = QLabel("Centralized Traffic Control", self)
        self.moduleLabel.setFont(QFont(self.fontStyle, self.headerFontSize))
        self.moduleLabel.setAlignment(Qt.AlignCenter)
        self.moduleLabel.move(30, 100)
        self.moduleLabel.adjustSize()
        self.moduleLabel.setStyleSheet("color:" + self.colorDarkBlue)

        # test bench icon
        self.pixmapGear = QtGui.QPixmap("src/main/CTC/gear_icon.png")
        self.pixmapGear = self.pixmapGear.scaled(25, 25)
        self.testbenchIcon = QLabel(self)
        self.testbenchIcon.setPixmap(self.pixmapGear)
        self.testbenchIcon.setGeometry(30, 140, 32, 32)

        # test bench button
        self.testbenchButton = QPushButton("Test Bench", self)
        self.testbenchButton.setFont(QFont(self.fontStyle, self.textFontSize))
        self.testbenchButton.setGeometry(60, 140, 100, 32)
        self.testbenchButton.setStyleSheet(
            "color:" + self.colorDarkBlue + ";border: 1px solid white"
        )

        # system time input
        self.systemTimeInput = QLabel("00:00:00", self)
        self.systemTimeInput.setFont(QFont(self.fontStyle, self.headerFontSize))
        self.systemTimeInput.setGeometry(820, 67, 150, 100)
        self.systemTimeInput.setStyleSheet("color:" + self.colorDarkBlue)

        # system time label
        self.systemTimeLabel = QLabel("System Time:", self)
        self.systemTimeLabel.setFont(QFont(self.fontStyle, self.headerFontSize))
        self.systemTimeLabel.adjustSize()
        self.systemTimeLabel.setGeometry(650, 65, 200, 100)
        self.systemTimeLabel.setStyleSheet("color:" + self.colorDarkBlue)

        # system speed label
        self.systemSpeedLabel = QLabel("System Speed:", self)
        self.systemSpeedLabel.setFont(QFont(self.fontStyle, self.textFontSize))
        self.systemSpeedLabel.setGeometry(700, 140, 100, 100)
        self.systemSpeedLabel.adjustSize()
        self.systemSpeedLabel.setStyleSheet("color:" + self.colorDarkBlue)

        # system speed input
        self.systemSpeedInput = QLabel("x1.000", self)
        self.systemSpeedInput.setFont(QFont(self.fontStyle, self.textFontSize))
        self.systemSpeedInput.setGeometry(850, 140, 50, 50)
        self.systemSpeedInput.adjustSize()
        self.systemSpeedInput.setStyleSheet("color:" + self.colorDarkBlue)

        # increase system speed button
        self.pixmapFastForward = QtGui.QPixmap("src/main/CTC/forward.svg")
        self.pixmapFastForward = self.pixmapFastForward.scaled(20, 20)
        self.speedUpButton = QPushButton(self)
        self.speedUpButton.setIcon(QtGui.QIcon(self.pixmapFastForward))
        self.speedUpButton.setGeometry(910, 140, 20, 20)
        self.speedUpButton.setStyleSheet(
            "color:" + self.colorDarkBlue + ";border: 1px solid white"
        )

        # decrease system speed button
        self.pixmapRewind = QtGui.QPixmap("src/main/CTC/backward.svg")
        self.pixmapRewind = self.pixmapRewind.scaled(20, 20)
        self.slowDownButton = QPushButton(self)
        self.slowDownButton.setIcon(QtGui.QIcon(self.pixmapRewind))
        self.slowDownButton.setGeometry(820, 140, 20, 20)
        self.slowDownButton.setStyleSheet(
            "color:" + self.colorDarkBlue + ";border: 1px solid white"
        )

        self.speedUpButton.clicked.connect(self.increase_speed)
        self.slowDownButton.clicked.connect(self.decrease_speed)

        self.current_time = QDateTime.currentDateTime()
        self.current_time.setTime(QTime(0, 0, 0))
        self.system_speed = 1.0
        self.timer_interval = 1000

        self.systemTimeInput.setText(self.current_time.toString("hh:mm:ss"))
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(self.timer_interval)

        ################################# MODE BUTTONS #############################################################################
        self.last_clicked_button = None
        # Add an "Automatic Mode" button
        self.automatic = QPushButton("Automatic Mode", self)
        self.automatic.setGeometry(
            30, 180, 130, 30
        )  # Set the button's position and size
        self.automatic.setFont(QFont(self.fontStyle, self.textFontSize))
        self.automatic.setStyleSheet(
            "background-color: "
            + self.colorLightGrey
            + "; color: "
            + self.colorDarkBlue
            + "; border: 1px solid black"
        )
        self.automatic.clicked.connect(self.mode_handler.automaticButtonClicked)

        # Manual Button
        self.manual = QPushButton("Manual Mode", self)
        self.manual.setGeometry(165, 180, 130, 30)  # Set the button's position and size
        self.manual.setFont(QFont(self.fontStyle, self.textFontSize))
        self.manual.setStyleSheet(
            "background-color: white; color:"
            + self.colorBlack
            + "; border: 1px solid black"
        )
        self.manual.clicked.connect(self.mode_handler.manualButtonClicked)

        # Maintenance Button
        """self.maintenance = QPushButton("Maintenance Mode", self)
        self.maintenance.setGeometry(300, 180, 130, 30)  # Set the button's position and size
        self.maintenance.setFont(QFont(self.fontStyle, self.textFontSize))
        self.maintenance.setStyleSheet('background-color: white; color:' +
                                        self.colorBlack + '; border: 1px solid black')
        self.maintenance.clicked.connect(self.mode_handler.maintenanceButtonClicked) """

        # Select a Line
        self.selectLine = QComboBox(self)
        self.selectLine.setGeometry(30, 220, 130, 30)
        self.selectLine.addItem("Select a Line")
        self.selectLine.addItem("Blue Line")
        self.selectLine.addItem("Green Line")
        self.selectLine.addItem("Red Line")
        self.selectLine.setFont(QFont(self.fontStyle, self.textFontSize))
        self.selectLine.currentIndexChanged.connect(self.scheduler.getSelectedLine)

        # CSV File Button
        self.inputSchedule = QPushButton("Import Schedule", self)
        self.inputSchedule.setGeometry(
            165, 220, 130, 30
        )  # Set the button's position and size
        self.inputSchedule.setFont(QFont(self.fontStyle, self.textFontSize))
        self.inputSchedule.setStyleSheet(
            "background-color: white; color:"
            + self.colorBlack
            + "; border: 1px solid black"
        )
        self.inputSchedule.setEnabled(True)
        self.inputSchedule.clicked.connect(self.scheduler.load_file)

        ################################# Automatic ###################################################################
        # Error text
        self.error_label = QLabel("", self)
        self.error_label.setFont(QFont(self.fontStyle, self.textFontSize))
        self.error_label.setStyleSheet("color: red")
        self.error_label.setGeometry(170, 245, 125, 30)

        # Schedule Table
        self.schedule_header = QLabel("Schedule:", self)
        self.schedule_header.setFont(QFont(self.fontStyle, self.textFontSize))
        self.schedule_header.setGeometry(30, 610, 100, 100)
        self.schedule_table = QTableWidget(self)
        self.schedule_table.setColumnCount(5)
        self.schedule_table.setHorizontalHeaderLabels(
            ["Train ID", "Departing From", "Stops", "Departure Time", "Arrival Time"]
        )
        self.schedule_table.setStyleSheet("background-color: white;")
        self.schedule_table.setGeometry(35, 680, 890, 240)
        self.schedule_table.setColumnWidth(0, 150)
        self.schedule_table.setColumnWidth(1, 150)
        self.schedule_table.setColumnWidth(2, 250)
        self.schedule_table.setColumnWidth(3, 130)
        self.schedule_table.setColumnWidth(4, 130)
        self.schedule_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # Occupancy Table
        self.occupancy_header = QLabel("Occupied Blocks:", self)
        self.occupancy_header.setFont(QFont(self.fontStyle, self.textFontSize))
        self.occupancy_header.setGeometry(360, 460, 110, 80)
        self.occupancy_table = QTableWidget(self)
        self.occupancy_table.setColumnCount(2)
        self.occupancy_table.setHorizontalHeaderLabels(["Block", "Line"])
        self.occupancy_table.setStyleSheet("background-color: white;")
        self.occupancy_table.setGeometry(360, 510, 252, 100)

        # Throughput per line
        self.throughput_label = QLabel("Throughput: ", self)
        self.throughput_label.setFont(QFont(self.fontStyle, self.textFontSize + 5))
        self.throughput_label.setGeometry(350, 170, 400, 50)

        ############################################## MANUAL MODE #################################################################
        # Departing Station
        self.departingStation = QComboBox(self)
        self.departingStation.setGeometry(650, 175, 200, 55)
        self.departingStation.addItem("Select a Departing Station")
        self.selectLine.currentIndexChanged.connect(
            self.scheduler.updateDepartingStations
        )
        self.departingStation.setFont(QFont(self.fontStyle, 9))
        self.departingStation.setEnabled(False)
        self.departingStation.setStyleSheet(
            "background-color: "
            + self.colorLightGrey
            + "; color: "
            + self.colorDarkGrey
        )

        # Next Station
        """self.arrivalStation = QComboBox(self)
        self.arrivalStation.setVisible(False)
        self.arrivalStation.setGeometry(50, 350, 200, 55)
        self.arrivalStation.addItem("Select Arrival Station")
        self.selectLine.currentIndexChanged.connect(self.scheduler.updateArrivalStation)
        self.arrivalStation.setFont(QFont(self.fontStyle, 9))  """

        # Send Train Button
        self.sendTrain = QPushButton("Add Train to Schedule", self)
        self.sendTrain.setGeometry(650, 625, 275, 50)
        self.sendTrain.setFont(QFont(self.fontStyle, self.textFontSize + 4))
        self.sendTrain.setStyleSheet(
            "background-color: " + self.colorLightGrey + "; color: " + self.colorBlack
        )
        self.sendTrain.clicked.connect(self.scheduler.sendTrainClicked)
        self.sendTrain.setEnabled(False)

        # Set schedule
        self.setSchedule = QPushButton("Set Schedule", self)
        self.setSchedule.setGeometry(350, 625, 275, 50)
        self.setSchedule.setFont(QFont(self.fontStyle, self.textFontSize + 4))
        self.setSchedule.setStyleSheet(
            "background-color: " + self.colorLightRed + "; color: " + self.colorBlack
        )
        # self.setSchedule.clicked.connect(self.scheduler.sendTrainClicked)
        self.setSchedule.setEnabled(True)

        # Input an arrival time
        self.arrivalTime = QLineEdit(self)
        self.arrivalTime.setPlaceholderText("0000 (Military Time) - Optional")
        self.arrivalHeader = QLabel("Input an Arrival Time:", self)
        self.arrivalHeader.setFont(QFont(self.fontStyle, self.textFontSize))
        self.arrivalHeader.setGeometry(650, 270, 200, 100)
        self.arrivalTime.setGeometry(650, 335, 200, 50)
        self.arrivalTime.setEnabled(False)
        self.arrivalTime.setStyleSheet(
            "background-color: "
            + self.colorLightGrey
            + "; color: "
            + self.colorDarkGrey
        )

        # Input a train ID
        self.trainIDInput = QLineEdit(self)
        self.trainIDInput.setPlaceholderText("Optional")
        self.trainIDHeader = QLabel("Input a Train ID:", self)
        self.trainIDHeader.setFont(QFont(self.fontStyle, self.textFontSize))
        self.trainIDHeader.setGeometry(650, 190, 200, 100)
        self.trainIDInput.setGeometry(650, 255, 100, 50)
        self.trainIDInput.setEnabled(False)
        self.trainIDInput.setStyleSheet(
            "background-color: "
            + self.colorLightGrey
            + "; color: "
            + self.colorDarkGrey
        )

        # Input a suggested speed
        self.suggSpeedInput = QLineEdit(self)
        self.suggSpeedInput.setPlaceholderText("mph - Optional")
        self.suggSpeedHeader = QLabel("Suggested speed:", self)
        self.suggSpeedHeader.setFont(QFont(self.fontStyle, self.textFontSize))
        self.suggSpeedHeader.setGeometry(785, 190, 200, 100)
        self.suggSpeedInput.setGeometry(785, 255, 100, 50)
        self.suggSpeedInput.setEnabled(False)
        self.suggSpeedInput.setStyleSheet(
            "background-color: "
            + self.colorLightGrey
            + "; color: "
            + self.colorDarkGrey
        )

        # Add Stop Button
        self.addStopButton = QPushButton("Add Stop", self)
        self.addStopButton.setFont(QFont(self.fontStyle, self.textFontSize))
        self.addStopButton.setGeometry(825, 395, 100, 50)
        self.addStopButton.setStyleSheet(
            "background-color: white; color: "
            + self.colorDarkBlue
            + "; border: 1px solid black"
        )
        self.addStopButton.clicked.connect(self.scheduler.addStopPressed)
        self.current_departing_station = None
        self.addStopButton.setEnabled(False)
        self.addStopButton.setStyleSheet(
            "background-color: "
            + self.colorLightGrey
            + "; color: "
            + self.colorDarkGrey
        )

        # Add Stop Dropdown
        self.addStopDropdown = QComboBox(self)
        self.addStopDropdown.setGeometry(650, 395, 165, 50)
        self.addStopDropdown.setEnabled(False)
        self.addStopDropdown.setStyleSheet(
            "background-color: "
            + self.colorLightGrey
            + "; color: "
            + self.colorDarkGrey
        )
        self.stops = []
        self.current_stop_index = 0
        self.update_timer = QTimer(self)

        self.selectLine.currentIndexChanged.connect(
            self.scheduler.updateStopDropDown
        )  # Connect the signal to update the dropdown
        self.max_block = None

        # Selected Stops Table
        self.stopsQueueHeader = QLabel("Selected Stops:", self)
        self.stopsQueueHeader.setFont(QFont(self.fontStyle, self.textFontSize))
        self.stopsQueueHeader.setGeometry(650, 410, 120, 100)
        self.stopsTable = QTableWidget(self)
        self.stopsTable.setColumnCount(2)
        self.stopsTable.setHorizontalHeaderLabels(["Station", "Dwell Time"])
        self.stopsTable.setStyleSheet("background-color: white;")
        self.stopsTable.setGeometry(650, 470, 275, 150)
        self.stopsTable.setStyleSheet(
            "background-color: "
            + self.colorLightGrey
            + "; color: "
            + self.colorDarkGrey
        )

        # select block numbers
        self.blockDropDown = QComboBox(self)
        self.blockDropDown.setGeometry(35, 500, 100, 50)
        self.selectLine.currentIndexChanged.connect(self.updateInfoBlock)

        # repair block button
        self.repairBlockButton = QPushButton("Repair Block", self)
        # self.repairBlockButton.setVisible(False)
        self.repairBlockButton.setFont(QFont(self.fontStyle, self.textFontSize))
        self.repairBlockButton.setGeometry(35, 560, 100, 50)
        self.repairBlockButton.setStyleSheet(
            "background-color: white; color: "
            + self.colorDarkBlue
            + "; border: 1px solid black"
        )
        # self.repairBlockButton.clicked.connect(self.scheduler.repairBlockButton)

        # close block button
        self.closeBlockButton = QPushButton("Close Block", self)
        # self.closeBlockButton.setVisible(False)
        self.closeBlockButton.setFont(QFont(self.fontStyle, self.textFontSize))
        self.closeBlockButton.setGeometry(150, 560, 100, 50)
        self.closeBlockButton.setStyleSheet(
            "background-color: white; color: "
            + self.colorDarkBlue
            + "; border: 1px solid black"
        )
        # self.closeBlockButton.clicked.connect(Block.closeBlockButton)

        # Displaying the occupancy status
        self.status_label = QLabel("Status: ", self)
        self.status_label.setGeometry(150, 475, 300, 100)
        self.status_label.setStyleSheet("font-size: 16px; color: black;")
        self.status_label.setVisible(True)

        """self.blockStatus = QLabel("Occupied", self)
        self.blockStatus.setGeometry(220, 475, 100, 100)
        self.blockStatus.setStyleSheet("font-size: 16px; color: green;")
        self.blockStatus.setVisible(True)"""
        # self.status_label.block.showBlockStatus(self.status_label)  # Pass the status_label as an argument

        # Dispatched Trains Table
        self.dispatchHeader = QLabel("Dispatched Trains:", self)
        self.dispatchHeader.setFont(QFont(self.fontStyle, self.textFontSize))
        self.dispatchHeader.setGeometry(35, 220, 120, 100)
        self.dispatchTable = QTableWidget(self)
        self.dispatchTable.setColumnCount(5)
        self.dispatchTable.setHorizontalHeaderLabels(
            ["Train ID", "Location", "Next Stop", "Suggested Speed (mph)", "Authority"]
        )
        # Set the width of each column
        self.dispatchTable.setColumnWidth(0, 100)  # Width for "Train ID"
        self.dispatchTable.setColumnWidth(1, 100)  # Width for "Location"
        self.dispatchTable.setColumnWidth(2, 150)  # Width for "Next Stop"
        self.dispatchTable.setColumnWidth(3, 180)  # Width for "Suggested Speed (mph)"
        self.dispatchTable.setColumnWidth(4, 100)

        self.dispatchTable.setStyleSheet("background-color: white;")
        self.dispatchTable.setGeometry(35, 280, 600, 200)

        self.selectLine.currentIndexChanged.connect(self.ticketRequest)
        trackModelToCTC.throughput.connect(self.updateTickets)

        self.blockDropDown.currentIndexChanged.connect(self.blockHandler)
        self.blockDropDown.currentIndexChanged.connect(self.statusHandler)
        # self.show()
        # self.blockDropDown.currentIndexChanged.connect(self.statusHandler)  # Connect the signal to update the dropdown

    def statusHandler(self):
        Block.updateStatusLabel(self)

    def ticketRequest(self):
        beforeLine = self.selectLine.currentText()
        if beforeLine == "Green Line":
            requestLine = "Green"
        else:
            requestLine = "Red"

        ctcToTrackModel.requestThroughput.emit(requestLine)

    def updateTickets(self, throughput):
        throughput_text = f"Throughput: {throughput}"
        self.throughput_label.setText(throughput_text)

    def blockHandler(self):
        Block.setSelectedBlock(self)

    def updateInfoBlock(self):
        Block.updateBlockDropDown(self)

    def update_time(self):
        self.current_time = self.current_time.addSecs(1)  # Update the time by 1 second
        self.systemTimeInput.setText(self.current_time.toString("hh:mm:ss"))
        masterSignals.timingMultiplier.emit(self.timer_interval)
        masterSignals.clockSignal.emit(self.current_time.time())

    def increase_speed(self):
        # Convert system_speed to an interval in milliseconds
        self.timer_interval = int(self.timer_interval / 10)
        if self.timer_interval == 0:
            self.timer_interval = 1
        self.timer.setInterval(self.timer_interval)

        self.systemSpeedInput.setText(
            "x" + format(1 / (self.timer_interval / 1000), ".3f")
        )

    def decrease_speed(self):
        # Convert system_speed to an interval in milliseconds
        self.timer_interval = int(self.timer_interval * 10)
        if self.timer_interval >= 10000:
            self.timer_interval = 10000
        self.timer.setInterval(self.timer_interval)

        self.systemSpeedInput.setText(
            "x" + format(1 / (self.timer_interval / 1000), ".3f")
        )


class ModeHandler:
    def __init__(self, main_window):
        self.main_window = main_window

    # function for if automatic button is pressed
    def automaticButtonClicked(self):
        main_window = self.main_window

        # Unhighlight the last clicked button, if any
        if main_window.last_clicked_button:
            main_window.last_clicked_button.setStyleSheet("")

        main_window.last_clicked_button = main_window.automatic
        main_window.automatic.setStyleSheet(
            "background-color: "
            + main_window.colorLightGrey
            + "; color: "
            + main_window.colorDarkBlue
            + "; border: 1px solid black"
        )

        main_window.throughput_label.setVisible(True)
        main_window.occupancy_header.setVisible(True)
        main_window.occupancy_table.setVisible(True)
        main_window.schedule_table.setVisible(True)
        # main_window.schedule_table.setGeometry(35,625,890,300)
        main_window.schedule_header.setVisible(True)
        # main_window.schedule_header.setGeometry(30,560,100,100)
        main_window.selectLine.setVisible(True)
        main_window.inputSchedule.setVisible(True)
        main_window.departingStation.setStyleSheet(
            "background-color: "
            + main_window.colorLightGrey
            + "; color: "
            + main_window.colorDarkGrey
        )
        main_window.sendTrain.setEnabled(True)
        main_window.arrivalHeader.setVisible(True)
        main_window.arrivalTime.setVisible(True)
        main_window.arrivalTime.setEnabled(False)
        main_window.arrivalTime.setStyleSheet(
            "background-color: "
            + main_window.colorLightGrey
            + "; color: "
            + main_window.colorDarkGrey
        )
        main_window.addStopButton.setEnabled(False)
        main_window.addStopButton.setStyleSheet(
            "background-color: "
            + main_window.colorLightGrey
            + "; color: "
            + main_window.colorDarkGrey
        )
        main_window.addStopDropdown.setEnabled(False)
        main_window.addStopDropdown.setStyleSheet(
            "background-color: "
            + main_window.colorLightGrey
            + "; color: "
            + main_window.colorDarkGrey
        )
        main_window.stopsQueueHeader.setVisible(False)
        main_window.stopsTable.setStyleSheet(
            "background-color: "
            + main_window.colorLightGrey
            + "; color: "
            + main_window.colorDarkGrey
        )
        main_window.trainIDInput.setEnabled(False)
        main_window.trainIDInput.setStyleSheet(
            "background-color: "
            + main_window.colorLightGrey
            + "; color: "
            + main_window.colorDarkGrey
        )
        main_window.suggSpeedInput.setEnabled(False)
        main_window.suggSpeedInput.setStyleSheet(
            "background-color: "
            + main_window.colorLightGrey
            + "; color: "
            + main_window.colorDarkGrey
        )
        main_window.sendTrain.setStyleSheet(
            "background-color: "
            + main_window.colorLightGrey
            + "; color: "
            + main_window.colorBlack
        )
        main_window.sendTrain.setEnabled(False)
        main_window.setSchedule.setStyleSheet(
            "background-color: "
            + main_window.colorLightRed
            + "; color: "
            + main_window.colorBlack
        )

    # function for if manual button is pressed
    def manualButtonClicked(self):
        main_window = self.main_window

        main_window.automatic.setStyleSheet(
            "background-color: white; color:"
            + main_window.colorBlack
            + "; border: 1px solid black"
        )
        # Unhighlight the last clicked button, if any
        if main_window.last_clicked_button:
            main_window.last_clicked_button.setStyleSheet("")

        main_window.last_clicked_button = main_window.manual
        main_window.manual.setStyleSheet(
            "background-color: "
            + main_window.colorLightGrey
            + "; color: "
            + main_window.colorDarkBlue
            + "; border: 1px solid black"
        )

        # Hide the elements
        """main_window.throughput_label.setVisible(False)
        main_window.speed_label.setVisible(False)
        main_window.authority_label.setVisible(False)
        main_window.occupancy_header.setVisible(False)
        main_window.occupancy_table.setVisible(False)"""
        main_window.schedule_table.setVisible(True)
        main_window.schedule_table.setRowCount(0)
        main_window.schedule_table.setGeometry(35, 680, 890, 240)
        main_window.schedule_header.setVisible(True)
        main_window.schedule_header.setGeometry(30, 610, 100, 100)
        main_window.selectLine.setVisible(True)
        # main_window.selectLine.setCurrentIndex(0)
        main_window.inputSchedule.setVisible(True)
        main_window.departingStation.setEnabled(True)
        main_window.departingStation.setStyleSheet("background-color: white")
        main_window.sendTrain.setEnabled(True)
        main_window.arrivalHeader.setVisible(True)
        main_window.arrivalTime.setVisible(True)
        main_window.arrivalTime.setEnabled(True)
        main_window.arrivalTime.setStyleSheet("background-color: white;")
        main_window.addStopButton.setEnabled(True)
        main_window.addStopButton.setStyleSheet("background-color: white;")
        main_window.addStopDropdown.setEnabled(True)
        main_window.addStopDropdown.setStyleSheet("background-color: white;")
        main_window.stopsQueueHeader.setVisible(True)
        main_window.stopsTable.setStyleSheet("background-color: white;")
        main_window.trainIDInput.setEnabled(True)
        main_window.trainIDInput.setStyleSheet("background-color: white")
        main_window.suggSpeedInput.setEnabled(True)
        main_window.suggSpeedInput.setStyleSheet("background-color: white")
        main_window.sendTrain.setStyleSheet(
            "background-color: "
            + main_window.colorLightRed
            + "; color: "
            + main_window.colorBlack
        )
        main_window.sendTrain.setEnabled(True)
        main_window.setSchedule.setEnabled(False)
        main_window.setSchedule.setStyleSheet(
            "background-color: "
            + main_window.colorLightGrey
            + "; color: "
            + main_window.colorDarkGrey
        )

    # function for if maintenance button is pressed
    def maintenanceButtonClicked(self):
        main_window = self.main_window

        main_window.automatic.setStyleSheet(
            "background-color: white; color:"
            + main_window.colorBlack
            + "; border: 1px solid black"
        )
        # Unhighlight the last clicked button, if any
        if main_window.last_clicked_button:
            main_window.last_clicked_button.setStyleSheet("")

        main_window.last_clicked_button = main_window.self.maintenance
        main_window.maintenance.setStyleSheet(
            "background-color: "
            + main_window.colorLightGrey
            + "; color: "
            + main_window.colorDarkBlue
            + "; border: 1px solid black"
        )

        main_window.throughput_label.setVisible(False)
        main_window.speed_label.setVisible(False)
        main_window.authority_label.setVisible(False)
        main_window.occupancy_header.setVisible(False)
        main_window.occupancy_table.setVisible(False)
        main_window.schedule_table.setVisible(False)
        main_window.schedule_header.setVisible(False)
        main_window.selectLine.setVisible(False)
        main_window.inputSchedule.setVisible(False)
        main_window.departingStation.setVisible(False)
        # main_window.arrivalStation.setVisible(False)
        main_window.sendTrain.setVisible(False)
        main_window.arrivalHeader.setVisible(False)
        main_window.arrivalTime.setVisible(False)
        main_window.addStopButton.setVisible(False)
        main_window.addStopDropdown.setVisible(False)
        main_window.stopsQueueHeader.setVisible(False)
        main_window.stopsTable.setVisible(False)


class Scheduler:
    def __init__(self, main_window):
        self.main_window = main_window
        self.trainList = []
        self.numTrains = 0
        self.routing = Routing(
            "src/main/CTC/GreenLine.csv", main_window
        )  # Create an instance of the Routing class
        self.trainID = None

    def load_file(self):
        selected_line = self.getSelectedLine()
        # self.main_window.selectLine.currentText()
        if selected_line == "Select a Line":
            # Set the error message text
            self.main_window.error_label.setText("Please select a line.")
            return

        self.main_window.error_label.clear()

        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(
            self.main_window,
            "Open CSV File",
            "",
            "CSV Files (*.csv);;All Files (*)",
            options=options,
        )

        if filePath:
            with open(filePath, "r") as file:
                csv_content = file.read()

            # Split the CSV content into rows
            rows = csv_content.split("\n")

            # Determine the number of rows and columns for the table
            num_rows = len(rows)
            if num_rows > 0:
                num_columns = len(rows[0].split(","))

                # Create a QTableWidget
                self.main_window.schedule_table.setRowCount(num_rows)
                self.main_window.schedule_table.setColumnCount(num_columns)

                # Populate the table with CSV data
                for i, row in enumerate(rows):
                    columns = row.split(",")
                    for j, value in enumerate(columns):
                        item = QTableWidgetItem(value)
                        self.main_window.schedule_table.setItem(i, j, item)

        # This makes the table uneditable
        for row in range(self.main_window.schedule_table.rowCount()):
            for col in range(self.main_window.schedule_table.columnCount()):
                item = self.main_window.schedule_table.item(row, col)
                if item:
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)

    def setThroughput(self, throughput_value):
        self.main_window.throughput_label.setText(
            "Throughput: " + str(throughput_value)
        )

    def getThroughput(self):
        throughput_text = self.main_window.throughput_label.text()
        # Extract the throughput value from the label's text
        throughput_value = throughput_text.replace("Throughput: ", "")
        # You may want to handle potential conversion errors if needed
        return float(throughput_value) if throughput_value != "N/A" else None

    def setAuthority(self, authority_value):
        self.main_window.authority_label.setText("Authority: " + str(authority_value))

    def getAuthority(self):
        authority_text = self.main_window.throughput_label.text()
        # Extract the throughput value from the label's text
        authority_value = authority_text.replace("Authority: ", "")
        # You may want to handle potential conversion errors if needed
        return float(authority_value) if authority_value != "N/A" else None

    def setCommandedSpeed(self, speed_value):
        self.main_window.speed_label.setText(
            "Suggested Speed (mph): " + str(speed_value)
        )

    def getCommandedSpeed(self):
        speed_text = self.main_window.speed_label.text()
        # Extract the throughput value from the label's text
        speed_value = speed_text.replace("Suggested Speed (mph): ", "")
        # You may want to handle potential conversion errors if needed
        return float(speed_value) if speed_value != "N/A" else None

    def updateDepartingStations(self):
        # Clear the existing items in the departingStation ComboBox
        self.main_window.departingStation.clear()
        self.main_window.departingStation.addItem("Yard")
        self.selected_line = self.main_window.selectLine.currentText()

    def sendTrainClicked(self):
        selected_line = self.main_window.selectLine.currentText()
        departing_station = self.main_window.departingStation.currentText()
        # arrival_station = self.main_window.arrivalStation.currentText()
        arrival_time = self.main_window.arrivalTime.text()
        # print("Arrival Time: ", {arrival_time})
        # current_time = QTime.currentTime()

        current_time = self.main_window.systemTimeInput.text()
        current_time_qtime = QTime.fromString(current_time, "hh:mm:ss")

        if current_time_qtime.second() > 0:
            current_time_qtime = current_time_qtime.addSecs(
                60 - current_time_qtime.second()
            )
        else:
            current_time_qtime = current_time_qtime.addSecs(60)

        train_id = self.main_window.trainIDInput.text()
        suggested_speed = self.main_window.suggSpeedInput.text()

        if selected_line == "Select a Line":
            QMessageBox.critical(
                self.main_window, "Invalid Selection", "Please select a line."
            )
        elif departing_station == "Select a Departing Station":
            QMessageBox.critical(
                self.main_window,
                "Invalid Selection",
                "Please select a departing station.",
            )
        elif arrival_time and (not arrival_time.isdigit() or len(arrival_time) != 4):
            QMessageBox.critical(
                self.main_window,
                "Invalid Arrival Time",
                "Please enter a valid military time (HHmm).",
            )
        elif arrival_time and int(arrival_time) > 2359:
            QMessageBox.critical(
                self.main_window,
                "Invalid Arrival Time",
                "Arrival time cannot exceed 2359.",
            )
            """
        elif arrival_time and int(arrival_time) < int(
            QTime.currentTime().toString("HHmm")
        ):
            QMessageBox.critical(
                self.main_window,
                "Invalid Arrival Time",
                "Arrival time cannot be before the current time.",
            )"""

        else:
            arrival_stations = []
            arrival_stations.extend(self.main_window.stops)
            # arrival_stations.append(arrival_station)
            station_info_list = []
            print(arrival_stations)
            for arrival_station in arrival_stations:
                if selected_line == "Red Line":
                    print("red line")
                elif selected_line == "Blue Line":
                    print("blue line")
                elif selected_line == "Green Line":
                    routing = Routing("src/main/CTC/GreenLine.csv", CTCWindow)
                    arrival_station_to_find = arrival_station
                    station_info = routing.find_station_info(arrival_station_to_find)

                    if station_info:
                        # Add station and its information as a dictionary to the list
                        station_info_list.append(
                            {"Station": arrival_station_to_find, "Info": station_info}
                        )
                    else:
                        print(f"Station '{arrival_station_to_find}' not found.")

            if station_info_list:
                departure_station_info = routing.find_station_info(departing_station)
                if departure_station_info:
                    self.path = self.routing.find_path(
                        departing_station, arrival_stations, station_info
                    )
                    print("Path: ", self.path)
                    self.travel = self.routing.find_travel_path(self.path)
                    print("Travel: ", self.travel)

            # case if no arrival time is input, needs to be calculated
            if arrival_time == "":
                travelTime = self.routing.computeTravelTime(
                    self.travel, suggested_speed
                )
                arrivalTimeBefore = self.routing.calculateArrivalTime(
                    travelTime, current_time_qtime
                )

                arrival_hours = arrivalTimeBefore.hour()
                arrival_minutes = arrivalTimeBefore.minute()

                # Format as "HHmm"
                arrivalTime = f"{arrival_hours:02d}{arrival_minutes:02d}"
                print("Arrival Time:", arrivalTime)

                current_hours = current_time_qtime.hour()
                current_minutes = current_time_qtime.minute()

                # Format as "HHmm"
                current_time_str = f"{current_hours:02d}{current_minutes:02d}"
                departureTime = current_time_str
            else:
                travelTime = self.routing.computeTravelTime(
                    self.travel, suggested_speed
                )
                arrivalTime = arrival_time
                departureTime = self.routing.calculateDepartureTime(
                    arrivalTime, travelTime
                )

            train = Train(
                self,
                self.main_window,
                self.numTrains,
                selected_line,
                arrivalTime,
                departureTime,
                arrival_stations,
                train_id,
                suggested_speed,
                self.travel
            )

            self.trainList.append(train)
            # Print the information of all trains in the trainList
            for train in self.trainList:
                print("Train ID:", train.train_id)
                print("Line:", train.trackLine)
                print("Arrival Time:", train.timeArrival)
                print("Departure Time:", train.trainDeparture)
                print("Stops:", train.trainStops)
                print("Authority:", train.authority)
                print("Suggested Speed:", train.sugg_speed)
                print("-----------")  # Add a separator between trains

            #self.assign_route_to_train(self.travel, train.train_id)

            self.update_schedule_table(
                departing_station, departureTime, arrivalTime, train.train_id
            )

            # Clear the input fields and hide them
            self.numTrains += 1
            self.main_window.departingStation.setCurrentIndex(0)
            self.main_window.arrivalTime.clear()
            self.main_window.stops.clear()
            self.updateStopDropDown()
            self.main_window.stopsTable.setRowCount(0)

    def assign_route_to_train(self, route_queue, train_id):
        # Assuming temp_route_identifier is an index or temporary ID
        self.routing.train_routes[train_id] = route_queue

    def update_schedule_table(
        self, departing_station, departure_time, arrival_time, trainID
    ):
        # Determine where to insert the new row in the schedule table
        row_position = self.main_window.schedule_table.rowCount()
        # departure_time_str = departure_time.toString("HHmm")
        # Insert a new row in the schedule table
        self.main_window.schedule_table.insertRow(row_position)
        stops_str = ", ".join(self.main_window.stops)

        # Add the train information to the table
        self.main_window.schedule_table.setItem(
            row_position, 0, QTableWidgetItem(trainID)
        )  # Train ID
        self.main_window.schedule_table.setItem(
            row_position, 1, QTableWidgetItem(departing_station)
        )  # Departing Station
        self.main_window.schedule_table.setItem(
            row_position, 2, QTableWidgetItem(stops_str)
        )  # Stops
        self.main_window.schedule_table.setItem(
            row_position, 3, QTableWidgetItem(departure_time)
        )  # Departure Time
        self.main_window.schedule_table.setItem(
            row_position, 4, QTableWidgetItem(arrival_time)
        )  # Arrival Time

    def AutomaticSchedule(self):
        self.main_window.schedule_table.clearContents()
        self.main_window.schedule_table.setRowCount(0)

    def setBlueSchedule(self):
        # Clear the existing items in the schedule table
        self.main_window.schedule_table.clearContents()
        self.main_window.schedule_table.setRowCount(0)

        blue_line_schedule = [
            ("BlueTrain1", "Yard", "Stops", "Station B", "0800", "0830"),
            ("BlueTrain2", "Yard", "Stops", "Station C", "0900", "0930"),
        ]

        # Set the number of rows in the schedule table
        self.main_window.schedule_table.setRowCount(len(blue_line_schedule))

        # Populate the schedule table with the Blue Line schedule
        for row, schedule_entry in enumerate(blue_line_schedule):
            for col, value in enumerate(schedule_entry):
                item = QTableWidgetItem(value)
                self.main_window.schedule_table.setItem(row, col, item)

    def setRedSchedule(self):
        # Clear the existing items in the schedule table
        self.main_window.schedule_table.clearContents()
        self.main_window.schedule_table.setRowCount(0)

        red_line_schedule = [
            ("RedTrain1", "Yard", "Stops", "Station B", "0800", "0830"),
            ("RedTrain2", "Yard", "Stops", "Station C", "0900", "0930"),
        ]

        # Set the number of rows in the schedule table
        self.main_window.schedule_table.setRowCount(len(red_line_schedule))

        # Populate the schedule table with the Red Line schedule
        for row, schedule_entry in enumerate(red_line_schedule):
            for col, value in enumerate(schedule_entry):
                item = QTableWidgetItem(value)
                self.main_window.schedule_table.setItem(row, col, item)

    def setGreenSchedule(self):
        # Clear the existing items in the schedule table
        self.main_window.schedule_table.clearContents()
        self.main_window.schedule_table.setRowCount(0)

        green_line_schedule = [
            ("GreenTrain1", "Yard", "Stops", "Station B", "0800", "0830"),
            ("GreenTrain2", "Yard", "Stops", "Station C", "0900", "0930"),
        ]

        # Set the number of rows in the schedule table
        self.main_window.schedule_table.setRowCount(len(green_line_schedule))

        # Populate the schedule table with the Green Line schedule
        for row, schedule_entry in enumerate(green_line_schedule):
            for col, value in enumerate(schedule_entry):
                item = QTableWidgetItem(value)
                self.main_window.schedule_table.setItem(row, col, item)

    def getSelectedLine(self):
        selected_line = self.main_window.selectLine.currentText()
        return selected_line
        # Clear the existing items in the schedule table
        """self.main_window.schedule_table.clearContents()
        self.main_window.schedule_table.setRowCount(0)
        
        # No line selected, do nothing  
        if selected_line == "Select a Line":
            return  
        elif selected_line == "Blue Line":
            self.setBlueSchedule()
        elif selected_line == "Red Line":
            self.setRedSchedule()
        elif selected_line == "Green Line":
            self.setGreenSchedule()
            self.max_block = 150"""

    def updateStopDropDown(self):
        self.main_window.addStopDropdown.clear()
        selected_line = self.main_window.selectLine.currentText()
        available_stations = []

        if selected_line == "Blue Line":
            available_stations = [
                "Select a Station to stop at",
                "Station B",
                "Station C",
            ]
        elif selected_line == "Red Line":
            available_stations = [
                "Select a Station to stop at",
                "Shadyside",
                "Herron Ave",
                "Swissville",
                "Penn Station",
                "Steel Plaza",
                "First Ave",
                "Station Square",
                "South Hills Junction",
            ]
        elif selected_line == "Green Line":
            available_stations = [
                "Select a Station to stop at",
                "Pioneer",
                "Edgebrook",
                "Whited",
                "South Bank",
                "Central",
                "IngleWood",
                "OverBrook",
                "Glenbury",
                "Dormont",
                "Mt Lebanon",
                "Poplar",
                "Castle Shannon",
            ]

        # if self.main_window.arrivalStation.currentText() == "Select an Arrival Station":
        # If arrival station is not selected, add all available stations
        # QMessageBox.warning(self, "Error", "Please select an Arrival Station first.")
        # else:
        # Filter out stations that are already in 'stops' and remove the arrival station
        available_stations = [
            station
            for station in available_stations
            if station not in self.main_window.stops
        ]
        self.main_window.addStopDropdown.addItems(available_stations)

    def addStopPressed(self):
        selected_station = self.main_window.addStopDropdown.currentText()

        if selected_station != "Select a Station to stop at":
            # Add the selected station to the 'stops' array
            self.main_window.stops.append(selected_station)

            # add stops to stop table
            dwellTime = "1 minute"
            rowPosition = self.main_window.stopsTable.rowCount()
            self.main_window.stopsTable.insertRow(rowPosition)
            self.main_window.stopsTable.setItem(
                rowPosition, 0, QTableWidgetItem(selected_station)
            )
            self.main_window.stopsTable.setItem(
                rowPosition, 1, QTableWidgetItem(dwellTime)
            )

            # Update the dropdown to exclude the newly added stop
            self.updateStopDropDown()
            # Reset the dropdown to index 0
            self.main_window.addStopDropdown.setCurrentIndex(0)
            print("Stops:", self.main_window.stops)

    def setMaxBlock(self, selected_line):
        # Set the max_block based on the selected line
        if selected_line == "Red Line":
            self.max_block = 100
        elif selected_line == "Blue Line":
            self.max_block = 150
        elif selected_line == "Green Line":
            self.max_block = 200

    def getMaxBlock(self, selected_line):
        # Check if max_block is already set, and if not, set it
        if self.max_block is None:
            self.setMaxBlock(selected_line)
        return self.max_block


class Routing:
    def __init__(self, filename, main_window):
        self.filename = filename
        self.data = self.load_data()
        self.main_window = main_window
        # self.scheduler_class = Scheduler(main_window)
        self.train_routes = {}  # Dictionary to map train IDs to their routes
        self.temp_routes = []  # temp dict

        trackControllerToCTC.occupancyState.connect(self.checkPosition)

    def load_data(self):
        data = []
        with open(self.filename, "r") as file:
            csv_reader = csv.reader(file)
            for line in csv_reader:
                data.append(line)
        return data

    def find_block_info(self):
        blockList = []  # Create a list to store block information
        header = True  # Flag to skip the header row
        for row in self.data:
            if header:
                header = False  # Skip the header row
                continue

            if len(row) >= 11:
                line = row[0]
                trackSection = row[1]
                blockNumber = int(row[2])
                blockLength = float(row[3])
                speedLimit = float(row[5])
                stationName = row[6]
                seconds_to_traverse_block = float(row[10])
                # Create a Block object for each block and append it to blockList
                block = Block(
                    self,
                    blockNumber,
                    trackSection,
                    blockLength,
                    speedLimit,
                    stationName,
                    seconds_to_traverse_block,
                )
                blockList.append(block)

        Block.initialize_blocks(blockList)

        return blockList

    def find_station_info(self, arrival_station):
        station_info = []
        arrival_station = (
            arrival_station.lower()
        )  # Convert the input to lowercase for case-insensitive search

        for row in self.data:
            if len(row) >= 8:
                if arrival_station in row[6].lower():
                    Line = row[0]
                    Block_Number = int(row[2])
                    Block_Length = float(row[3])
                    Speed_Limit = float(row[5])
                    Station = row[6]
                    Station_Side = row[7]
                    self.seconds_to_traverse_block = float(row[10])

                    station_info.append(
                        {
                            "Line": Line,
                            "Block_Number": Block_Number,
                            "Block_Length": Block_Length,
                            "Speed_Limit": Speed_Limit,
                            "Station": Station,
                            "Station_Side": Station_Side,
                            "seconds_to_traverse_block": self.seconds_to_traverse_block,
                        }
                    )

        return station_info

    def find_station_name_by_block(self, block_number):
        for row in self.data:
            if (
                len(row) >= 8 and row[2].isdigit()
            ):  # Check if row has enough elements and row[2] is a digit
                if int(row[2]) == block_number:  # Check if the block number matches
                    return row[6].title()  # Return the station name in title case
        return None  # Return None if no matching station is found

    def find_path(self, departure_station, arrival_stations, stops):
        self.path = []
        added_stations = []
        current_station = departure_station

        for arrival_station in arrival_stations:
            # Find the station information for the current and arrival stations
            current_station_info = self.find_station_info(current_station)
            arrival_station_info = self.find_station_info(arrival_station)

            # If either station's information is missing, we can't continue the path
            if current_station_info is None or arrival_station_info is None:
                return None

            # Check if the arrival station has already been added
            if arrival_station not in added_stations:
                self.path.append(
                    (arrival_station, arrival_station_info[0]["Block_Number"])
                )
                added_stations.append(arrival_station)

            # Update the current station for the next iteration
            current_station = arrival_station

        return self.path

    def find_travel_path(self, path):
        max_block = 0
        if self.main_window.selectLine == "Green Line":
            max_block = 150

        # Extract the block numbers and station names from the path
        block_stations = [(block, station) for station, block in path]

        self.stations_to_stop = []
        self.route_array = []

        # Determine the first stop based on the first station in block_stations
        # Determine the first stop based on the first station in block_stations
        if block_stations:
            first_block, first_station = block_stations[0]
            first_stop = f"Stop at block {first_block}: {first_station}"
            self.stations_to_stop.append(first_block)

        # Categorize other stations based on their block numbers
        first_stations = []
        second_stations = []
        third_stations = []
        stop_blocks = []

        for block, station in block_stations[
            1:
        ]:  # Exclude the first station from categorization
            if 62 < block < max_block:
                first_stations.append(block)
                stop_blocks.append(block)
            elif 0 <= block < 58:
                second_stations.append(block)
                stop_blocks.append(block)
            elif block < 150:
                third_stations.append(block)
                stop_blocks.append(block)

        # Sort stations within each category by block number
        first_stations.sort(key=lambda x: x[0])
        second_stations.sort(key=lambda x: x[0])
        third_stations.sort(key=lambda x: x[0])
        # Combine stations in the desired order
        self.stations_to_stop.extend(first_stations)
        self.stations_to_stop.extend(second_stations)
        self.stations_to_stop.extend(third_stations)
        self.stations_to_stop.append(0)
        print("BLOCKS TO STOP AT")
        print(self.stations_to_stop)
        self.routeQ = []
        #self.routeQ = [0, 53, 54, 55, 56, 57, 0]
        if self.main_window.selectLine == "Green Line":
            self.routeQ = self.travelGreenBlocks()
            print("ROUTEQ IS FOUND")

        self.routeQ = self.travelGreenBlocks()

        # Use stop_blocks to check if the train should stop at a block
        """for i, block in enumerate(self.routeQ):
            if isinstance(block, int):
                for station_info in self.stations_to_stop:
                    stop_block, station_name = station_info[0], station_info[1]
                    if block == stop_block:
                        self.routeQ[i] = f"{block}, {station_name}"
                        """
        self.temp_routes.append(self.routeQ)
        return self.routeQ

    def travelGreenBlocks(self):
        self.routeQ = []
        # Add all blocks to a path the train will have to go through
        self.routeQ.append(0)

        # K-Q
        for blockNum in range(63, 101):
            self.routeQ.append(blockNum)

        # N
        for blockNum in range(85, 76, -1):
            self.routeQ.append(blockNum)

        # R-Z
        for blockNum in range(101, 151):
            self.routeQ.append(blockNum)

        # F-A
        for blockNum in range(29, 0, -1):
            self.routeQ.append(blockNum)

        # D-I
        for blockNum in range(13, 58):
            self.routeQ.append(blockNum)

        self.routeQ.append(0)

        return self.routeQ

    def closeBlock(self, blockNumber):
        self.blockList[blockNumber].setEnable(0)

    def openBlock(self, blockNumber):
        self.blockList[blockNumber].setEnable(1)

    def computeTravelTime(self, travel_path, suggested_speed):
        total_time = 0  # Initialize total time to zero
        lastStopTime = 0

        for block in travel_path:
            stops_excluding_last = (
                self.stations_to_stop[:-1] if self.stations_to_stop else []
            )

            if block in stops_excluding_last:
                # Add 60 seconds for the stop at this block
                total_time += 60
                lastStopTime = total_time

            elif isinstance(block, int):
                # Find the time to traverse the block using the find_block_info function
                self.block_info_list = (
                    self.find_block_info()
                )  # Call the function to get all block information

                block_info = next(
                    (
                        info
                        for info in self.block_info_list
                        if info.blockNumber == block
                    ),
                    None,
                )
                if block_info:
                    if suggested_speed == "":
                        seconds_to_traverse_block = block_info.seconds_to_traverse_block
                    else:
                        distance = block_info.length
                        sugg_speed = int(suggested_speed)
                        if sugg_speed > 0:
                            seconds_to_traverse_block = distance / (
                                sugg_speed * 0.44704
                            )
                        else:
                            seconds_to_traverse_block = 0

                    total_time += seconds_to_traverse_block
                    # print(f"Block: {block}, Seconds: {seconds_to_traverse_block}")
                else:
                    print(f"Block {block} not found in block_list.")

        print("Last stop arrival time is ")
        print(lastStopTime)
        print("Total travel time is ")
        print(total_time)
        # print(total_time)
        return lastStopTime

    def checkPosition(self, line, blockNum, occupancy):

        # initalizing switches
        switches = {
            # normal, alt
            44: [[43, 42, 41, 40, 39],[67, 68, 69, 70, 71]],
            38: [[39, 40, 41, 42, 43],[71, 70, 69, 68, 67]],
            33: [[32, 31, 30, 29, 28],[72, 73, 74, 75, 76]],
            27: [[28, 29, 30, 31, 32],[76, 75, 74, 73, 72]]
        }

        try:
            self.routeQ[0]
        except Exception as e:
            return
        try:
            print(
                "comparing current block of "
                + str(blockNum)
                + " with destination at "
                + str(self.routeQ[1])
            )
        except Exception as e:
            pass
        if line == 1:
            track = "Green"
        else:
            track = "Red"

        trainLine = self.main_window.selectLine.currentText()
        # for train_id, routeQ in self.train_routes.items():
        print(f"{trainLine}, {track}")
        if trainLine == "Green Line":
            trainTrack = "Green"
        else:
            trainTrack = "Red"
        if occupancy == True and blockNum == self.routeQ[1] and trainTrack == track:
            print("inside check position")

            self.routeQ.pop(0)

            if(len(self.routeQ) == 1):
                self.main_window.dispatchTable.removeRow(0)
                print("removing row...")
                return
            # nextBlock = self.routeQ[1]
            wayside = self.find_wayside(self.routeQ[0])
            print("STATIONS TO STOP:")
            print(self.stations_to_stop[0])
            print("ROUTE Q")
            print(self.routeQ)
            
            # Switch

            # Occupancy

            # Station Check
            if len(self.routeQ) >= 4 and self.stations_to_stop[0] == self.routeQ[3]:
                suggestedSpeed = (
                    int(0.75 * self.block_info_list[self.routeQ[0]].speedLimit)
                    * 0.621371
                )
                suggestedSpeed = round(suggestedSpeed, 2)
                self.main_window.dispatchTable.setItem(
                    0, 3, QTableWidgetItem(str(suggestedSpeed))
                )
                self.main_window.dispatchTable.setItem(
                    0, 1, QTableWidgetItem(str(blockNum))
                )
                Block.update_block_occupancy(blockNum, 1)

                ctcToTrackController.sendSuggestedSpeed.emit(
                    line, wayside, self.routeQ[0], suggestedSpeed
                )
            elif len(self.routeQ) >= 3 and self.stations_to_stop[0] == self.routeQ[2]:
                suggestedSpeed = (
                    int(0.50 * self.block_info_list[self.routeQ[0]].speedLimit)
                    * 0.621371
                )
                suggestedSpeed = round(suggestedSpeed, 2)
                self.main_window.dispatchTable.setItem(
                    0, 3, QTableWidgetItem(str(suggestedSpeed))
                )
                self.main_window.dispatchTable.setItem(
                    0, 1, QTableWidgetItem(str(blockNum))
                )
                ctcToTrackController.sendSuggestedSpeed.emit(
                    line, wayside, self.routeQ[0], suggestedSpeed
                )
            elif len(self.routeQ) >= 2 and self.stations_to_stop[0] == self.routeQ[1]:
                suggestedSpeed = (
                    int(0.25 * self.block_info_list[self.routeQ[0]].speedLimit)
                    * 0.621371
                )
                suggestedSpeed = round(suggestedSpeed, 2)

                self.main_window.dispatchTable.setItem(
                    0, 3, QTableWidgetItem(str(suggestedSpeed))
                )
                self.main_window.dispatchTable.setItem(
                    0, 1, QTableWidgetItem(str(blockNum))
                )
                ctcToTrackController.sendSuggestedSpeed.emit(
                    line, wayside, self.routeQ[0], suggestedSpeed
                )
            elif len(self.routeQ) >= 1 and self.stations_to_stop[0] == self.routeQ[0]:
                suggestedSpeed = 0
                station_name = self.find_station_name_by_block(self.stations_to_stop[0])

                self.main_window.dispatchTable.setItem(
                    0, 3, QTableWidgetItem(str(suggestedSpeed))
                )
                self.main_window.dispatchTable.setItem(0, 4, QTableWidgetItem("0"))
                ctcToTrackController.sendSuggestedSpeed.emit(
                    line, wayside, self.routeQ[0], suggestedSpeed
                )
                ctcToTrackController.sendAuthority.emit(line, wayside, blockNum, 0)
                self.main_window.dispatchTable.setItem(
                    0, 1, QTableWidgetItem(str(station_name))
                )
                self.main_window.dispatchTable.setItem(
                    0, 2, QTableWidgetItem("Dwelling")
                )
                QTimer.singleShot(60000, self.leaveStop)
            

            else:
                print(
                    "Top of route queue: ",
                    self.block_info_list[int(self.routeQ[0])].speedLimit,
                )
                print(
                    "Suggested Speed Before: ",
                    (self.block_info_list[int(self.routeQ[0])].speedLimit) * 0.621371,
                )
                print("Block 65: ", self.block_info_list[65].speedLimit)
                print("Block 65: ", self.block_info_list[66].speedLimit)

                suggestedSpeed = (
                    self.block_info_list[int(self.routeQ[0])].speedLimit
                ) * 0.621371
                suggestedSpeed = round(suggestedSpeed, 2)

                self.main_window.dispatchTable.setItem(
                    0, 3, QTableWidgetItem(str(suggestedSpeed))
                )
                self.main_window.dispatchTable.setItem(
                    0, 1, QTableWidgetItem(str(blockNum))
                )

    def leaveStop(self):
        print("In leaveStop function")
        print("Current stations to stop:", self.stations_to_stop)

        if self.stations_to_stop:
            self.stations_to_stop.pop(0)
            print("After pop(0), stations to stop:", self.stations_to_stop)

            if not self.stations_to_stop:
                self.stations_to_stop.append(0)
                nextStop = "Returning to Yard"
                print("List is empty, added 0, nextStop set to 'Returning to Yard'")
            else:
                nextStop = "Returning to Yard"
                print("Next stop:", nextStop)
        else:
            nextStop = "Returning to Yard"
            print("List was initially empty, nextStop set to 'Returning to Yard'")

        suggestedSpeed = (self.block_info_list[self.routeQ[0]].speedLimit) * 0.621371
        wayside = self.find_wayside(self.routeQ[0])

        print("Sending suggested speed and updating dispatch table")
        ctcToTrackController.sendSuggestedSpeed.emit(
            1, wayside, self.routeQ[0], suggestedSpeed
        )
        self.main_window.dispatchTable.setItem(
            0, 3, QTableWidgetItem(str(suggestedSpeed))
        )
        self.main_window.dispatchTable.setItem(0, 1, QTableWidgetItem(self.routeQ[0]))
        self.main_window.dispatchTable.setItem(0, 2, QTableWidgetItem(str(nextStop)))
        self.main_window.dispatchTable.setItem(0, 4, QTableWidgetItem("1"))

    def calculateDepartureTime(self, arrival_time, travelTime):
        arrivalTime = QTime.fromString(arrival_time, "HHmm")
        departure_time = arrivalTime.addSecs(int(-travelTime))

        depHour = departure_time.hour()
        depMin = departure_time.minute()

        # Format as "HHmm"
        current_time_str = f"{depHour:02d}{depMin:02d}"
        departureTime = current_time_str

        return departureTime

    def calculateArrivalTime(self, travelTime, current_time):
        arrival_time = current_time.addSecs(int(travelTime))
        return arrival_time

    def find_wayside(self, block_number):
        if block_number in WAYSIDE_1G_BLOCKS:
            wayside = 1
            return wayside
        elif block_number in WAYSIDE_2G_BLOCKS:
            wayside = 2
            return wayside
        else:
            return "Block number not found"


class Train:
    train_count = 0

    def __init__(
        self,
        scheduler,
        CTCwindow,
        trainNum,
        line,
        arrivalTime,
        departureTime,
        stops,
        trainID,
        suggested_speed,
        travel
    ):
        self.scheduler = scheduler
        self.main_window = CTCwindow

        Train.train_count += 1
        self.trackLine = line
        self.timeArrival = arrivalTime
        self.trainDeparture = departureTime
        self.trainStops = stops
        self.authority = 1
        trainNum = trainNum + 1
        self.routeQ = travel
        self.altRouteBool = False

        self.sugg_speed = int(suggested_speed) if suggested_speed else 43.50

        if trainID:
            self.train_id = trainID
        elif line == "Green Line":
            self.train_id = f'{"Green"}{trainNum}'

        self.dispatchTrainsList = []
        # self.signals.occupancy.connect(self.routing.checkPosition)

        self.departure_timer = QTimer()
        self.departure_timer.timeout.connect(self.checkDepartureTime)
        self.departure_timer.start(1000)

    def getTrainID(self):
        return self.trainID

    def getDestination(self):
        return self.destination

    def getTrackLine(self):
        return self.trackLine

    def getArrivalTime(self):
        return self.timeArrival

    def getDepartureTime(self):
        return self.trainDeparture

    def getStops(self):
        return self.trainStops

    def getSuggestedSpeed(self):
        return self.suggestedSpeed

    def getAuthoriy(self):
        return self.authority

    def setAuthority(self, trainAuthority):
        self.authority = trainAuthority

    def setArrivalTime(self, arrivalTime):
        self.timeArrival = arrivalTime

    def setSuggestedSpeed(self, trainSpeed):
        self.suggestedSpeed = trainSpeed

    def setTrainID(self, train_id):
        self.trainID = train_id

    def checkDepartureTime(self):
        current_time = self.main_window.systemTimeInput.text()
        current_time_str = current_time.replace(":", "")[:4]

        # Iterate through your list of trains and check their departure times
        for train in self.scheduler.trainList:
            departureTime = train.trainDeparture
            if departureTime == current_time_str:
                # Add the train to the dispatched_trains list
                self.dispatchTrainsList.append(train)
                if train.trackLine == "Green Line":
                    lineTrack = "green"
                else:
                    lineTrack = "red"
                masterSignals.addTrain.emit(lineTrack, train.train_id)

                next_stop = self.trainStops[0]
                # Add the train's information to the dispatched trains table
                row_position = self.main_window.dispatchTable.rowCount()
                self.main_window.dispatchTable.insertRow(row_position)
                self.main_window.dispatchTable.setItem(
                    row_position, 0, QTableWidgetItem(train.train_id)
                )
                self.main_window.dispatchTable.setItem(
                    row_position, 1, QTableWidgetItem("0")
                )
                self.main_window.dispatchTable.setItem(
                    row_position, 2, QTableWidgetItem(next_stop)
                )
                self.main_window.dispatchTable.setItem(
                    row_position, 3, QTableWidgetItem(str(train.sugg_speed))
                )
                self.main_window.dispatchTable.setItem(
                    row_position, 4, QTableWidgetItem(str(train.authority))
                )

                if train.trackLine == "Green Line":
                    trainLine = 1
                else:
                    trainLine = 2

                ctcToTrackController.sendTrainDispatched.emit(
                    trainLine, 2, train.train_id, train.authority
                )

                self.scheduler.trainList.remove(train)

                # Get the number of rows in the schedule_table
                num_rows = self.main_window.schedule_table.rowCount()

                # Loop through the rows and search for the departure time
                for row_index in range(num_rows):
                    departure_time_item = self.main_window.schedule_table.item(
                        row_index, 3
                    )

                    if departure_time_item.text() == departureTime:
                        self.main_window.schedule_table.removeRow(row_index)
                        break
                        """else:
                            self.main_window.schedule_table.removeRow(row_index)
                            break  # Stop searching once the row is removed"""

    # def leaveStation()


class Block:
    def __init__(
        self,
        routing,
        blockNumber,
        trackSection,
        blockLength,
        speedLimit,
        stationName,
        seconds_to_traverse_block,
    ):
        self.routing = routing
        self.blockNumber = blockNumber
        self.section = trackSection
        self.length = blockLength
        self.speedLimit = speedLimit
        self.station = stationName
        self.seconds_to_traverse_block = seconds_to_traverse_block
        self.occupancy = 0
        self.enable = 1

    def initialize_blocks(blocks):
        for block in blocks:
            global_block_occupancy[block.blockNumber] = block.occupancy 

    @staticmethod
    def update_block_occupancy(block_num, occupancy):
        global global_block_occupancy
        global_block_occupancy[block_num] = occupancy

    def setEnable(self, blockEnable):
        self.enable = blockEnable

    def setOccupancy(self, occupancy):
        self.occupancy = occupancy

    @staticmethod
    def updateBlockDropDown(main_window):
        main_window.blockDropDown.clear()
        selected_line = main_window.selectLine.currentText()

        if selected_line == "Green Line":
            blockItem = "Select Block"
            block_items = [
                str(i) for i in range(1, 151)
            ]  # Generating block numbers 1-150
            main_window.blockDropDown.addItem(blockItem)
            main_window.blockDropDown.addItems(block_items)

    @staticmethod
    def updateStatusLabel(main_window):
        global global_block_occupancy  # Declare the global variable

        selected_block_num_text = main_window.blockDropDown.currentText()
        block_status = "Select a block"  # Default status

        # Check if the selected text is a number
        if selected_block_num_text.isdigit():
            selected_block_num = int(selected_block_num_text)

            for block_num in global_block_occupancy.keys():
                if block_num == selected_block_num:
                    # Assuming you want to check the occupancy status
                    occupancy = global_block_occupancy[block_num]
                    block_status = "Occupied" if occupancy else "Unoccupied"
                    break
            else:
                block_status = "Block not found"

        status_text = f"Status: {block_status}"
        main_window.status_label.setText(status_text)

    @staticmethod
    def getBlockStatus(block):
        # Assuming occupancy is a boolean, you can adjust the return value based on your requirements
        return "Occupied" if block.occupancy else "Unoccupied"

    @staticmethod
    def setSelectedBlock(main_window):
        selected_block = main_window.blockDropDown.currentText()
        return selected_block


