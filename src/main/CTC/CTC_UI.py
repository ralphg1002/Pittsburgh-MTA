# importing libraries
from multiprocessing import managers
from re import L
from sched import scheduler
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

# initalizing switches
switches = {
    # normal, alt, state
    44: [[43, 42, 41, 40, 39],[67, 68, 69, 70, 71], [0]],
    38: [[39, 40, 41, 42, 43],[71, 70, 69, 68, 67], [0]],
    33: [[32, 31, 30, 29, 28],[72, 73, 74, 75, 76], [0]],
    27: [[28, 29, 30, 31, 32],[76, 75, 74, 73, 72], [0]]
}

lights_greenLine = {
    0: [0, 63],
    1: [0, 13],
    12: [0, 11],
    13: [1, 12],
    29: [1, 30],
    30: [0, 31],
    57: [1, 0],
    58: [0, 59],
    62: [0, 63],
    63: [0, 64],
    76: [0, 77],
    77: [1, 101],
    85: [1, 86],
    86: [0, 87],
    100: [0, 85]
    }

lights_redLine = {
    0: [0, 9],
    1: [0, 16]
    # STILL NEED TO FILL OUT THE REST OF THIS LIST
}

globalSelectLine = None

dispatchTrainsList = []

# Global variable declaration
global_block_occupancy = {}

train_routes = {}  # Class attribute for train routes


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
        self.scheduler = Scheduler(self)
        self.mode_handler = ModeHandler(self, self.scheduler)
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
        self.testbenchButton.clicked.connect(self.openTestBench)

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
        self.schedule_header.setGeometry(30, 690, 100, 100)
        self.schedule_table = QTableWidget(self)
        self.schedule_table.setColumnCount(5)
        self.schedule_table.setHorizontalHeaderLabels(
            ["Train ID", "Departing From", "Stops", "Departure Time", "Arrival Time"]
        )
        self.schedule_table.setStyleSheet("background-color: white;")
        self.schedule_table.setGeometry(35, 750, 890, 180)
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
        self.occupancy_table.setColumnWidth(0, 120)
        self.occupancy_table.setColumnWidth(1, 120)
        self.occupancy_table.setGeometry(360, 510, 273, 200)

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
        self.sendTrain.setEnabled(False)
        self.sendTrain.clicked.connect(self.scheduler.sendTrainClicked)
        self.sendTrain.setEnabled(False)

        # Set schedule
        self.setSchedule = QPushButton("Set Schedule", self)
        self.setSchedule.setGeometry(650, 685, 275, 50)
        self.setSchedule.setFont(QFont(self.fontStyle, self.textFontSize + 4))
        self.setSchedule.setStyleSheet(
            "background-color: " + self.colorLightRed + "; color: " + self.colorBlack
        )
        self.setSchedule.clicked.connect(self.scheduler.setScheduleClicked)
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
        self.repairBlockButton.setEnabled(False)
        self.blockDropDown.currentIndexChanged.connect(self.updateRepairButtonStatus)
        self.repairBlockButton.clicked.connect(self.handleRepairBlockButton)

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
        self.closeBlockButton.setEnabled(False)
        self.blockDropDown.currentIndexChanged.connect(self.updateCloseButtonStatus)
        self.closeBlockButton.clicked.connect(self.handleCloseBlockButton)

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
        
        #self.scheduler = Scheduler(self)
        self.selectLine.currentIndexChanged.connect(self.update_global_select_line)
        self.blockDropDown.currentIndexChanged.connect(self.handleBlockStatus)

        # Create a refresh button
        self.refreshButton = QPushButton(self)
        self.refreshButton.setIcon(QIcon("src/main/CTC/change.svg"))  # Set the path to your icon image
        self.refreshButton.setGeometry(525, 170, 50, 50)  # Adjust the position and size as needed
        self.refreshButton.setStyleSheet("border: 2px solid white;")  # Set border color to white
        self.refreshButton.clicked.connect(self.ticketRequest)

        # auto schedule button
        """self.autoSchedule = QPushButton("Auto Schedule",self)
        self.autoSchedule.setFont(QFont(self.fontStyle, self.textFontSize))
        self.autoSchedule.setGeometry(50, 560, 100, 50)
        self.autoSchedule.setStyleSheet("background-color: white; color: " + self.colorDarkBlue + "; border: 1px solid black")"""

    def openTestBench(self):
        self.testBenchWindow = TestBench()
        self.testBenchWindow.show()

    def update_global_select_line(self):
        global globalSelectLine
        globalSelectLine = self.selectLine.currentText()
    
    def handleRepairBlockButton(self):
        Block.repairBlock(self)

    def handleCloseBlockButton(self):
        Block.closeBlock(self)

    def updateRepairButtonStatus(self):
        # Check if both line and block are selected
        line_selected = self.selectLine.currentText() not in ["", "Select Line"]
        block_selected = self.blockDropDown.currentText() not in ["", "Select Block"]

        # Enable button only if both line and block are selected
        self.repairBlockButton.setEnabled(line_selected and block_selected)
    
    def updateCloseButtonStatus(self):
        # Check if both line and block are selected
        line_selected = self.selectLine.currentText() not in ["", "Select Line"]
        block_selected = self.blockDropDown.currentText() not in ["", "Select Block"]

        # Enable button only if both line and block are selected
        self.closeBlockButton.setEnabled(line_selected and block_selected)
    
    def statusHandler(self):
        Block.updateStatusLabel(self)

    def ticketRequest(self):
        beforeLine = self.selectLine.currentText()
        if beforeLine != "Select a Line":
            if beforeLine == "Green Line":
                requestLine = "Green"
            else:
                requestLine = "Red"

            ctcToTrackModel.requestThroughput.emit(requestLine)

    def updateTickets(self, throughput):
        throughput_text = f"Throughput: {throughput}"
        self.throughput_label.setText(throughput_text)

    def handleBlockStatus(self):
        Block.updateStatusLabel(self)

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

class TestBench(QMainWindow):
    def __init__(self):
        super().__init__()
        self.fontStyle = 'Arial'
        self.textFontSize = 12  # Increased font size
        self.colorLightGrey = '#d3d3d3'  # Example color for the buttons
        self.colorBlack = '#000000'
        self.initUI()

    def initUI(self):
        font = QFont(self.fontStyle, self.textFontSize)

        # Update Block Occupancy Section
        self.occupancyLabel = QLabel("Update block occupancy:", self)
        self.occupancyLabel.setFont(font)
        self.occupancyLabel.move(20, 20)
        self.occupancyLabel.resize(300, 30)  # Increased width

        self.lineSelectionDropdown = QComboBox(self)
        self.lineSelectionDropdown.setFont(font)
        self.lineSelectionDropdown.addItems(["Red Line", "Green Line"])
        self.lineSelectionDropdown.move(20, 60)
        self.lineSelectionDropdown.resize(200, 30)

        self.blockNumberInput = QLineEdit(self)
        self.blockNumberInput.setFont(font)
        self.blockNumberInput.setPlaceholderText("Block Number")
        self.blockNumberInput.move(20, 100)
        self.blockNumberInput.resize(200, 30)

        self.occupancyInput = QLineEdit(self)
        self.occupancyInput.setFont(font)
        self.occupancyInput.setPlaceholderText("Occupancy (0 or 1)")
        self.occupancyInput.move(20, 140)
        self.occupancyInput.resize(200, 30)

        self.sendOccupancyButton = QPushButton("Send Occupancy", self)
        self.sendOccupancyButton.setFont(font)
        self.sendOccupancyButton.move(20, 180)
        self.sendOccupancyButton.resize(200, 40)
        self.sendOccupancyButton.setStyleSheet(
            "background-color: " + self.colorLightGrey + "; color: " + self.colorBlack
        )        
        self.sendOccupancyButton.clicked.connect(self.sendOccupancyData)

        # Set Ticket Sales Section
        self.ticketSalesLabel = QLabel("Set ticket sales:", self)
        self.ticketSalesLabel.setFont(font)
        self.ticketSalesLabel.move(20, 230)
        self.ticketSalesLabel.resize(300, 30)  # Increased width

        self.lineDropdown = QComboBox(self)
        self.lineDropdown.setFont(font)
        self.lineDropdown.addItems(["Green Line", "Red Line"])
        self.lineDropdown.move(20, 270)
        self.lineDropdown.resize(200, 30)

        self.salesInput = QLineEdit(self)
        self.salesInput.setFont(font)
        self.salesInput.setPlaceholderText("Ticket Sales")
        self.salesInput.move(20, 320)
        self.salesInput.resize(200, 30)

        self.sendSalesButton = QPushButton("Send Ticket Sales", self)
        self.sendSalesButton.setFont(font)
        self.sendSalesButton.move(20, 360)
        self.sendSalesButton.resize(200, 40)
        self.sendSalesButton.setStyleSheet(
            "background-color: " + self.colorLightGrey + "; color: " + self.colorBlack
        )        
        self.sendSalesButton.clicked.connect(self.sendTicketSales)

        # Update Switch Section
        self.updateSwitchLabel = QLabel("Update Switch:", self)
        self.updateSwitchLabel.setFont(font)
        self.updateSwitchLabel.move(250, 20)
        self.updateSwitchLabel.resize(300, 30)

        self.switchBlockDropdown = QComboBox(self)
        self.switchBlockDropdown.setFont(font)
        self.switchBlockDropdown.addItems(["Block 1", "Block 2", "Block 3"])  # Example items
        self.switchBlockDropdown.move(250, 60)
        self.switchBlockDropdown.resize(200, 30)

        self.switchStatusLabel = QLabel("Status:", self)
        self.switchStatusLabel.setFont(font)
        self.switchStatusLabel.move(250, 110)
        self.switchStatusLabel.resize(200, 30)

        self.flipSwitchButton = QPushButton("Flip Switch", self)
        self.flipSwitchButton.setFont(font)
        self.flipSwitchButton.move(250, 160)
        self.flipSwitchButton.resize(200, 40)
        self.flipSwitchButton.setStyleSheet(
            "background-color: " + self.colorLightGrey + "; color: " + self.colorBlack
        )
        self.flipSwitchButton.clicked.connect(self.flipSwitch)

        # Change Train Data Section
        self.changeTrainLabel = QLabel("Change Train Data:", self)
        self.changeTrainLabel.setFont(font)
        self.changeTrainLabel.move(250, 220)
        self.changeTrainLabel.resize(300, 30)

        self.trainDropdown = QComboBox(self)
        self.trainDropdown.setFont(font)
        self.trainDropdown.addItems(["Train 1", "Train 2", "Train 3"])  # Example items
        self.trainDropdown.move(250, 260)
        self.trainDropdown.resize(200, 30)

        self.suggestedSpeedInput = QLineEdit(self)
        self.suggestedSpeedInput.setFont(font)
        self.suggestedSpeedInput.setPlaceholderText("Suggested Speed")
        self.suggestedSpeedInput.move(250, 310)
        self.suggestedSpeedInput.resize(200, 30)

        self.authorityInput = QLineEdit(self)
        self.authorityInput.setFont(font)
        self.authorityInput.setPlaceholderText("Authority")
        self.authorityInput.move(250, 360)
        self.authorityInput.resize(200, 30)

        self.updateTrainButton = QPushButton("Update Train", self)
        self.updateTrainButton.setFont(font)
        self.updateTrainButton.move(250, 410)
        self.updateTrainButton.resize(200, 40)
        self.updateTrainButton.setStyleSheet(
            "background-color: " + self.colorLightGrey + "; color: " + self.colorBlack
        )
        self.updateTrainButton.clicked.connect(self.updateTrainData)
        
        self.setGeometry(300, 300, 500, 500)  
        self.setWindowTitle("Test Bench")

    def sendOccupancyData(self):
        # Logic to handle occupancy data
        selectedLine = self.lineSelectionDropdown.currentText()
        blockNumber = self.blockNumberInput.text()
        occupancy = self.occupancyInput.text()
        print(f"{selectedLine} Block {blockNumber} Occupancy Update: {occupancy}")

        if selectedLine == "Green Line":
            lineNum = 1
        else:
            lineNum = 2
        #occupancyState = pyqtSignal(int, int, bool)  # line, block number, state

        self.occupancyState.emit(lineNum, blockNumber, occupancy)

    def sendTicketSales(self):
        # Logic to handle ticket sales data
        line = self.lineDropdown.currentText()
        sales = self.salesInput.text()
        print(f"Ticket Sales for {line}: {sales}")

    def flipSwitch(self):
        # Logic to handle switch flipping
        selectedBlock = self.switchBlockDropdown.currentText()
        print(f"Flipping switch for {selectedBlock}")

    def updateTrainData(self):
        # Logic to handle updating train data
        selectedTrain = self.trainDropdown.currentText()
        suggestedSpeed = self.suggestedSpeedInput.text()
        authority = self.authorityInput.text()
        print(f"Updating data for {selectedTrain}: Speed {suggestedSpeed}, Authority {authority}")

    def sendOccupancyData(self):
        # Logic to handle occupancy data
        blockNumber = self.blockNumberInput.text()
        occupancy = self.occupancyInput.text()
        print(f"Block {blockNumber} Occupancy Update: {occupancy}")

    def sendTicketSales(self):
        # Logic to handle ticket sales data
        line = self.lineDropdown.currentText()
        sales = self.salesInput.text()
        print(f"Ticket Sales for {line}: {sales}")

class ModeHandler:
    def __init__(self, main_window, scheduler):
        self.main_window = main_window
        self.scheduler = scheduler
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
        main_window.setSchedule.setEnabled(True)

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
        #main_window.schedule_table.setGeometry(35, 680, 890, 240)
        main_window.schedule_header.setVisible(True)
        #main_window.schedule_header.setGeometry(30, 610, 100, 100)
        main_window.selectLine.setVisible(True)
        # main_window.selectLine.setCurrentIndex(0)
        main_window.inputSchedule.setVisible(True)
        main_window.departingStation.setEnabled(True)
        main_window.departingStation.setStyleSheet("background-color: white")
        main_window.sendTrain.setEnabled(False)
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
        main_window.setSchedule.setEnabled(False)
        main_window.setSchedule.setStyleSheet(
            "background-color: "
            + main_window.colorLightGrey
            + "; color: "
            + main_window.colorDarkGrey
        )


class Scheduler:
    def __init__(self, mainWindow):
        self.main_window = mainWindow
        self.trainList = []
        self.numTrains = 0
        selected_line = globalSelectLine
        #selected_line = self.main_window.selectLine.currentText()
        #selected_line = self.getSelectedLine()
        print("SELECTED LINE IS")
        print(selected_line)
        print(globalSelectLine)
        self.routing = Routing(
               "src/main/CTC/GreenLine.csv", self.main_window
        ) 
        """if globalSelectLine == "Green Line":
            print("GREEN ROUTING")
            self.routing = Routing(
                "src/main/CTC/GreenLine.csv", self.main_window
            )  
        elif globalSelectLine == "Red Line":
            print("RED ROUTING")
            self.routing = Routing(
                "src/main/CTC/RedLine.csv", self.main_window
            )"""

        self.trainID = None

    def load_file(self):
        selected_line = self.getSelectedLine()
        # self.main_window.selectLine.currentText()
        if selected_line == "Select a Line":
            # Set the error message text
            QMessageBox.critical(
                self.main_window,
                "Error",
                "Please Select a Line.",
            )
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
            # Clear the existing items in the schedule table
            self.main_window.schedule_table.clearContents()
            self.main_window.schedule_table.setRowCount(0)

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

    def load_file(self, filePath):
        selected_line = self.getSelectedLine()
        # self.main_window.selectLine.currentText()
        if selected_line == "Select a Line":
            # Set the error message text
            QMessageBox.critical(
                self.main_window,
                "Error",
                "Please Select a Line.",
            )
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

    def setScheduleClicked(self):
        selected_line = self.main_window.selectLine.currentText()
        if selected_line == "Green Line":
            # Iterate through rows in the schedule table
            for row in range(self.main_window.schedule_table.rowCount()):
                train_id = self.main_window.schedule_table.item(row, 0).text()
                departing_station = "Yard"
                stops_item = self.main_window.schedule_table.item(row, 2)

                # If the data is not a simple string, iterate through items in the cell
                stops_text = stops_item.text() if stops_item else ""
                stops = [stop.strip() for stop in stops_text.split(',')] if stops_text else []
              
                departure_time_text = self.main_window.schedule_table.item(row, 3)
                departure_time = departure_time_text.data(Qt.DisplayRole) if departure_time_text else ""
                arrival_time_text = self.main_window.schedule_table.item(row, 4)
                arrival_time = arrival_time_text.data(Qt.DisplayRole) if arrival_time_text else ""

                arrival_stations = []
                arrival_stations.extend(stops)
                # arrival_stations.append(arrival_station)
                station_info_list = []
                print(arrival_stations)
                for arrival_station in arrival_stations:
                    if selected_line == "Red Line":
                        routing = Routing("src/main/CTC/RedLine.csv", self.main_window)
                        arrival_station_to_find = arrival_station
                        station_info = routing.find_station_info(arrival_station_to_find)
                        if station_info:
                            # Add station and its information as a dictionary to the list
                            station_info_list.append(
                                {"Station": arrival_station_to_find, "Info": station_info}
                            )
                            print(station_info_list)
                        else:
                            print(f"Station '{arrival_station_to_find}' not found.")

                    elif selected_line == "Green Line":
                        routing = Routing("src/main/CTC/GreenLine.csv", self.main_window)
                        arrival_station_to_find = arrival_station
                        print(arrival_station_to_find)
                        station_info = routing.find_station_info(arrival_station_to_find)
                        if station_info:
                            # Add station and its information as a dictionary to the list
                            station_info_list.append(
                                {"Station": arrival_station_to_find, "Info": station_info}
                            )
                            print(station_info_list)
                        else:
                            print(f"Station '{arrival_station_to_find}' not found.")

                if station_info_list:
                    self.path = routing.find_path(
                        departing_station, arrival_stations, station_info
                    )
                    print("Path: ", self.path)
                    self.travel = routing.find_travel_path(self.path)
                    print("Travel: ", self.travel)
                    self.correctStops = routing.reorderStops(self.path)
                
                suggested_speed = 43.50
                travelTime = routing.computeTravelTime(
                    self.travel, suggested_speed
                )
                self.blockInfo = routing.makeBlockInfo(self.travel, suggested_speed)

                train = Train(
                    self,
                    self.main_window,
                    self.numTrains,
                    selected_line,
                    arrival_time,
                    departure_time,
                    self.correctStops,
                    train_id,
                    suggested_speed,
                    self.travel,
                    self.correctStops,
                    self.blockInfo
                )              
                self.trainList.append(train)
                for train in self.trainList:
                    print("Train ID:", train.train_id)
                    print("Line:", train.trackLine)
                    print("Arrival Time:", train.timeArrival)
                    print("Departure Time:", train.trainDeparture)
                    print("Stops:", train.trainStops)
                    print("Authority:", train.authority)
                    print("Suggested Speed:", train.sugg_speed)
                    print("-----------")  # Add a separator between trains
                self.numTrains += 1

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
                    routing = Routing("src/main/CTC/RedLine.csv", self.main_window)
                    arrival_station_to_find = arrival_station
                    station_info = routing.find_station_info(arrival_station_to_find)
                    if station_info:
                        # Add station and its information as a dictionary to the list
                        station_info_list.append(
                            {"Station": arrival_station_to_find, "Info": station_info}
                        )
                        print(station_info_list)
                    else:
                        print(f"Station '{arrival_station_to_find}' not found.")

                elif selected_line == "Green Line":
                    routing = Routing("src/main/CTC/GreenLine.csv", self.main_window)
                    arrival_station_to_find = arrival_station
                    station_info = routing.find_station_info(arrival_station_to_find)
                    if station_info:
                        # Add station and its information as a dictionary to the list
                        station_info_list.append(
                            {"Station": arrival_station_to_find, "Info": station_info}
                        )
                        print(station_info_list)
                    else:
                        print(f"Station '{arrival_station_to_find}' not found.")

            if station_info_list:
                #departure_station_info = routing.find_station_info(departing_station)
                #print("FOUND DEPATURE INFO")
                #print(departure_station_info)
                #if departure_station_info:
                self.path = routing.find_path(
                    departing_station, arrival_stations, station_info
                )
                print("Path: ", self.path)
                self.travel = routing.find_travel_path(self.path)
                print("Travel: ", self.travel)
                self.correctStops = routing.reorderStops(self.path)

            # case if no arrival time is input, needs to be calculated
            if arrival_time == "":
                travelTime = routing.computeTravelTime(
                    self.travel, suggested_speed
                )
                arrivalTimeBefore = routing.calculateArrivalTime(
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
                self.blockInfo = routing.makeBlockInfo(self.travel, suggested_speed)

            else:
                travelTime = routing.computeTravelTime(
                    self.travel, suggested_speed
                )
                arrivalTime = arrival_time
                departureTime = routing.calculateDepartureTime(
                    arrivalTime, travelTime
                )
                self.blockInfo = routing.makeBlockInfo(self.travel, suggested_speed)

            train = Train(
                self,
                self.main_window,
                self.numTrains,
                selected_line,
                arrivalTime,
                departureTime,
                self.correctStops,
                train_id,
                suggested_speed,
                self.travel,
                self.correctStops,
                self.blockInfo
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

        selected_line = self.main_window.selectLine.currentText()
        filePath = "src/main/CTC/green_auto_for_code"
        self.load_file(filePath)
        if selected_line == "Green Line":
            # Iterate through rows in the schedule table
            for row in range(self.main_window.schedule_table.rowCount()):
                train_id = self.main_window.schedule_table.item(row, 0).text()
                departing_station = "Yard"
                stops_item = self.main_window.schedule_table.item(row, 2)

                # If the data is not a simple string, iterate through items in the cell
                stops_text = stops_item.text() if stops_item else ""
                stops = [stop.strip() for stop in stops_text.split(',')] if stops_text else []
              
                departure_time_text = self.main_window.schedule_table.item(row, 3)
                departure_time = departure_time_text.data(Qt.DisplayRole) if departure_time_text else ""
                arrival_time_text = self.main_window.schedule_table.item(row, 4)
                arrival_time = arrival_time_text.data(Qt.DisplayRole) if arrival_time_text else ""

                arrival_stations = []
                arrival_stations.extend(stops)
                # arrival_stations.append(arrival_station)
                station_info_list = []
                print(arrival_stations)
                for arrival_station in arrival_stations:
                    if selected_line == "Red Line":
                        routing = Routing("src/main/CTC/RedLine.csv", self.main_window)
                        arrival_station_to_find = arrival_station
                        station_info = routing.find_station_info(arrival_station_to_find)
                        if station_info:
                            # Add station and its information as a dictionary to the list
                            station_info_list.append(
                                {"Station": arrival_station_to_find, "Info": station_info}
                            )
                            print(station_info_list)
                        else:
                            print(f"Station '{arrival_station_to_find}' not found.")

                    elif selected_line == "Green Line":
                        routing = Routing("src/main/CTC/GreenLine.csv", self.main_window)
                        arrival_station_to_find = arrival_station
                        print(arrival_station_to_find)
                        station_info = routing.find_station_info(arrival_station_to_find)
                        if station_info:
                            # Add station and its information as a dictionary to the list
                            station_info_list.append(
                                {"Station": arrival_station_to_find, "Info": station_info}
                            )
                            print(station_info_list)
                        else:
                            print(f"Station '{arrival_station_to_find}' not found.")

                if station_info_list:
                    self.path = routing.find_path(
                        departing_station, arrival_stations, station_info
                    )
                    print("Path: ", self.path)
                    self.travel = routing.find_travel_path(self.path)
                    print("Travel: ", self.travel)
                    self.correctStops = routing.reorderStops(self.path)
                suggested_speed = 43.50
                travelTime = routing.computeTravelTime(
                    self.travel, suggested_speed
                )

                train = Train(
                    self,
                    self.main_window,
                    self.numTrains,
                    selected_line,
                    arrival_time,
                    departure_time,
                    self.correctStops,
                    train_id,
                    suggested_speed,
                    self.travel
                )              
                
                self.trainList.append(train)
                for train in self.trainList:
                    print("Train ID:", train.train_id)
                    print("Line:", train.trackLine)
                    print("Arrival Time:", train.timeArrival)
                    print("Departure Time:", train.trainDeparture)
                    print("Stops:", train.trainStops)
                    print("Authority:", train.authority)
                    print("Suggested Speed:", train.sugg_speed)
                    print("-----------")  # Add a separator between trains
                self.numTrains += 1


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
        print("IN UPDATE STOP DROPDOWN")
        selected_line = self.main_window.selectLine.currentText()
        print(selected_line)
        available_stations = []

        if selected_line == "Red Line":
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
            self.main_window.sendTrain.setEnabled(True)
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
        self.temp_routes = []  # temp dict
        trackControllerToCTC.occupancyState.connect(self.checkPosition)
        trackControllerToCTC.occupancyState.connect(lambda line, blockNum, state: self.handleBlockOccupancy(line,blockNum,state))
        ctcToTrackController.signalTrainDwelling.connect(self.leaveStation)

    def handleBlockOccupancy(self, line, blockNum, state):
        Block.update_block_occupancy(blockNum, state, self.main_window, line)

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
        arrival_station1 = (
            arrival_station.lower()
        )  # Convert the input to lowercase for case-insensitive search

        for row in self.data:
            if len(row) >= 8:
                if arrival_station1 in row[6].lower():
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
            print(arrival_station)
            arrival_station.lower()
            current_station_info = self.find_station_info(current_station)
            arrival_station_info = self.find_station_info(arrival_station)
            print("ARRIVAL STATION INFO")
            print(arrival_station_info)
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

    def reorderStops(self, path):
        max_block = 0
        #if self.main_window.selectLine.currentText() == "Green Line":
        if globalSelectLine == "Green Line":
            max_block = 150
        else:
            max_block = 76
        # Extract the block numbers and station names from the path
        block_stations = [(block, station) for station, block in path]

        self.stations_to_stop = []
        self.route_array = []

        # Categorize other stations based on their block numbers
        first_stations = []
        second_stations = []
        third_stations = []

        ordered_stations = []

        for block, station in block_stations[0:]:  
            if 62 < block < max_block:
                first_stations.append(block)
            elif 0 <= block < 58:
                second_stations.append(block)
            elif block < 150:
                third_stations.append(block)

        # Sort stations within each category by block number
        first_stations.sort()
        second_stations.sort()
        third_stations.sort()

        # Combine stations in the desired order
        self.stations_to_stop.extend(first_stations)
        self.stations_to_stop.extend(second_stations)
        self.stations_to_stop.extend(third_stations)
        for block in self.stations_to_stop:
            station_name = self.find_station_name_by_block(block)
            ordered_stations.append(station_name)

        return ordered_stations
    
    def find_travel_path(self, path):
        max_block = 0
        #if self.main_window.selectLine.currentText() == "Green Line":
        if globalSelectLine == "Green Line":
            max_block = 150
        else:
            max_block = 76
        # Extract the block numbers and station names from the path
        block_stations = [(block, station) for station, block in path]

        self.stations_to_stop = []
        self.route_array = []

        # Categorize other stations based on their block numbers
        first_stations = []
        second_stations = []
        third_stations = []

        ordered_stations = []

        for block, station in block_stations[0:]:  
            if 62 < block < max_block:
                first_stations.append(block)
            elif 0 <= block < 58:
                second_stations.append(block)
            elif block < 150:
                third_stations.append(block)

        # Sort stations within each category by block number
        first_stations.sort()
        second_stations.sort()
        third_stations.sort()

        # Combine stations in the desired order
        self.stations_to_stop.extend(first_stations)
        self.stations_to_stop.extend(second_stations)
        self.stations_to_stop.extend(third_stations)
        for block in self.stations_to_stop:
            station_name = self.find_station_name_by_block(block)
            ordered_stations.append(station_name)

        self.stations_to_stop.append(0)
        print("BLOCKS TO STOP AT")
        print(self.stations_to_stop)
        self.routeQ = []

        trainLine = globalSelectLine
        #trainLine = self.main_window.selectLine.currentText()
        #self.routeQ = [0, 53, 54, 55, 56, 57, 0]
        if trainLine == "Green Line":
            self.routeQ = self.travelGreenBlocks()
            print("ROUTEQ IS FOUND")
        else:
            self.routeQ = self.travelRedBlocks()

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
    
    def travelRedBlocks(self):
        self.routeQ = []
        # Add all blocks to a path the train will have to go through
        self.routeQ.append(0)

        # K-Q
        for blockNum in range(9, 1, -1):
            self.routeQ.append(blockNum)

        # N
        for blockNum in range(1, 16):
            self.routeQ.append(blockNum)

        # R-Z
        for blockNum in range(16, 66):
            self.routeQ.append(blockNum)

        # F-A
        for blockNum in range(66, 1, -1):
            self.routeQ.append(blockNum)

        # D-I
        for blockNum in range(1, 9):
            self.routeQ.append(blockNum)

        self.routeQ.append(0)

        return self.routeQ

    def closeBlock(self, blockNumber):
        self.blockList[blockNumber].setEnable(0)
        if globalSelectLine == "Green Line":
            waysideNum = self.find_wayside(blockNumber)
            ctcToTrackController.sendMaintenance.emit(1, waysideNum, blockNumber, 1)

    def openBlock(self, blockNumber):
        self.blockList[blockNumber].setEnable(1)
        if globalSelectLine == "Green Line":
            waysideNum = self.find_wayside(blockNumber)
            ctcToTrackController.sendMaintenance.emit(1, waysideNum, blockNumber, 0)

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
                self.block_info = (
                    self.find_block_info()
                )  # Call the function to get all block information

                block_info = next(
                    (
                        info
                        for info in self.block_info
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

    def makeBlockInfo(self, travel_path, suggested_speed):
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
                        for info in self.block_info
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
        return self.block_info_list

    """def checkPosition(self, line, blockNum, occupancy):
        for train_id, routeQ in train_routes.items():
            try:
                routeQ[0]
            except Exception as e:
                return
            try:
                print(
                    "comparing current block of "
                    + str(blockNum)
                    + " with destination at "
                    + str(routeQ[1])
                )
            except Exception as e:
                pass

            if line == 1:
                track = "Green"
            else:
                track = "Red"

            trainLine = globalSelectLine
            print("GLOBAL SELECT LINE IS")
            print(globalSelectLine)
            #trainLine = self.main_window.selectLine.currentText()
            # for train_id, routeQ in self.train_routes.items():
            print(f"{trainLine}, {track}")
            if trainLine == "Green Line":
                trainTrack = "Green"
            else:
                trainTrack = "Red"

            if occupancy == True and blockNum == routeQ[1] and trainTrack == track:
                print("inside check position")
                self.routeQ.pop(0)
                train_routes[train_id] = routeQ

                if(len(routeQ) == 1):
                    self.main_window.dispatchTable.removeRow(0)
                    print("removing row...")
                    return
                # nextBlock = self.routeQ[1]
                wayside = self.find_wayside(routeQ[0])
                print("STATIONS TO STOP:")
                print(self.stations_to_stop[0])
                print("ROUTE Q")
                print(routeQ)
                
                ########## SWITCH CHECK ##################
                # Check if switch is in next 5 and get its index within the route queue. 
                for i in range(0, 5):
                    if i < len(self.routeQ) and routeQ[i] in switches:
                        switch_index = i
                        switch = switches[i]
                        break
                    else:
                        switch_index = None
                # if the switch is in the next 5 
                if switch_index != None:
                    # Check if the train is traveling in the right direction
                    correct_direction = False
                    for i in range (0,5):
                        if i < len(routeQ) and routeQ[i] == switch[0][0]:
                            correct_direction = True
                            break
                    # if the train is  traveling in the right direction then proceed.
                    if(correct_direction):
                        # check if switch is activated
                        if switch[2] == 1:
                            if self.altRouteBool == False:
                                self.altRouteBool = True
                                # remove the normal route from the routeQ
                                routeQ.remove(switch_index+1, switch_index+1+len(switch[0]))
                                # replace it with the alternative route
                                routeQ.insert(switch_index+1, switch[1])
                        # if switch is not activated
                        else:
                            if self.altRouteBool == True:
                                self.altRouteBool = False
                                # remove the alternative route from the routeQ
                                routeQ.remove(switch_index+1, switch_index+1+len(switch[1]))
                                # replace it with the normal route
                                routeQ.insert(switch_index+1, switch[0])


                ############## OCCUPANCY CHECK ############
                # determine the index of the occupied block within the routeQ
                for i in range(0, 5):
                    if i < len(self.routeQ) and routeQ[i] in global_block_occupancy:
                        occupied_index = i
                        occupied_block = self.routeQ[i]
                        break
                    else:
                        occupied_index = None
                # If there is an occupied block within the next 6...
                if occupied_index != None:
                    if(len(routeQ) >= 5 and occupied_block == routeQ[4]):
                        suggestedSpeed = (
                        int(0.75 * self.block_info_list[routeQ[0]].speedLimit)
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
                        line, wayside, routeQ[0], suggestedSpeed
                        )
                    elif(len(routeQ) >= 4 and occupied_block == routeQ[3]):
                        suggestedSpeed = (
                        int(0.5 * self.block_info_list[routeQ[0]].speedLimit)
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
                        line, wayside, routeQ[0], suggestedSpeed
                        )
                    elif(len(routeQ) >= 3 and occupied_block == routeQ[2]):
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
                        line, wayside, routeQ[0], suggestedSpeed
                        )
                    elif(len(routeQ) >= 2 and occupied_block == routeQ[1]):
                        suggestedSpeed = 0
                        authority = 0

                        self.main_window.dispatchTable.setItem(
                            0, 3, QTableWidgetItem(str(suggestedSpeed))
                        )
                        self.main_window.dispatchTable.setItem(
                            0, 1, QTableWidgetItem(str(blockNum))
                        )
                        ctcToTrackController.sendSuggestedSpeed.emit(
                        line, wayside, routeQ[0], suggestedSpeed
                        )
                        ctcToTrackController.sendSuggestedSpeed.emit(
                        line, wayside, routeQ[0], suggestedSpeed
                        )
                        ctcToTrackController.sendAuthority.emit(
                        line, wayside, routeQ[0], authority
                        )


                ############ LIGHT CHECK ##########
                # STILL NEED TO DO THE CODE FOR THIS PART

                ######### STATION CHECK ############
                if len(routeQ) >= 4 and self.stations_to_stop[0] == routeQ[3]:
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
                    #Block.update_block_occupancy(blockNum, 1, self.main_window)

                    ctcToTrackController.sendSuggestedSpeed.emit(
                        line, wayside, routeQ[0], suggestedSpeed
                    )
                elif len(routeQ) >= 3 and self.stations_to_stop[0] == routeQ[2]:
                    suggestedSpeed = (
                        int(0.50 * self.block_info_list[routeQ[0]].speedLimit)
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
                        line, wayside, routeQ[0], suggestedSpeed
                    )
                elif len(routeQ) >= 2 and self.stations_to_stop[0] == routeQ[1]:
                    suggestedSpeed = (
                        int(0.25 * self.block_info_list[routeQ[0]].speedLimit)
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
                        line, wayside, routeQ[0], suggestedSpeed
                    )
                elif len(routeQ) >= 1 and self.stations_to_stop[0] == routeQ[0]:
                    suggestedSpeed = 0
                    station_name = self.find_station_name_by_block(self.stations_to_stop[0])

                    self.main_window.dispatchTable.setItem(
                        0, 3, QTableWidgetItem(str(suggestedSpeed))
                    )
                    self.main_window.dispatchTable.setItem(0, 4, QTableWidgetItem("0"))
                    ctcToTrackController.sendSuggestedSpeed.emit(
                        line, wayside, routeQ[0], suggestedSpeed
                    )
                    ctcToTrackController.sendAuthority.emit(line, wayside, blockNum, 0)
                    self.main_window.dispatchTable.setItem(
                        0, 1, QTableWidgetItem(str(station_name))
                    )
                    self.main_window.dispatchTable.setItem(
                        0, 2, QTableWidgetItem("Dwelling")
                    )
                    QTimer.singleShot(15000, self.leaveStop)
                

                else:
                    print(
                        "Top of route queue: ",
                        self.block_info_list[int(routeQ[0])].speedLimit,
                    )
                    print(
                        "Suggested Speed Before: ",
                        (self.block_info_list[int(routeQ[0])].speedLimit) * 0.621371,
                    )
                    #print("Block 65: ", self.block_info_list[65].speedLimit)
                    #print("Block 65: ", self.block_info_list[66].speedLimit)

                    suggestedSpeed = (
                        self.block_info_list[int(routeQ[0])].speedLimit
                    ) * 0.621371
                    suggestedSpeed = round(suggestedSpeed, 2)

                    self.main_window.dispatchTable.setItem(
                        0, 3, QTableWidgetItem(str(suggestedSpeed))
                    )
                    self.main_window.dispatchTable.setItem(
                        0, 1, QTableWidgetItem(str(blockNum))
                    )"""

    def checkPosition(self, line, blockNum, occupancy):
        for train in dispatchTrainsList:
            routeQ = train.travelPath
            stations_to_stop = train.ordered_stations
            block_info_list = train.blockList

            try:
                routeQ[0]
            except Exception as e:
                return
            
            try:
                print(
                    "comparing current block of "
                    + str(blockNum)
                    + " with destination at "
                    + str(routeQ[1])
                )
            except Exception as e:
                pass

            if line == 1:
                track = "Green"
            else:
                track = "Red"

            trainLine = globalSelectLine
            #trainLine = self.main_window.selectLine.currentText()
            # for train_id, routeQ in self.train_routes.items():
            print(f"{trainLine}, {track}")
            if trainLine == "Green Line":
                trainTrack = "Green"
            else:
                trainTrack = "Red"

            if occupancy == True and blockNum == routeQ[1] and trainTrack == track:
                print("inside check position")
                previous_block = routeQ[0]
                routeQ.pop(0)
                if globalSelectLine == "Green Line":
                    lineNum = 1
                waysideNum = self.find_wayside(blockNum)

                ctcToTrackController.nextBlock.emit(lineNum, waysideNum, routeQ[0], routeQ[1])

                #train_routes[train_id] = self.routeQ

                if(len(routeQ) == 1):
                    self.main_window.dispatchTable.removeRow(0)
                    print("removing row...")
                    return
                # nextBlock = self.routeQ[1]
                wayside = self.find_wayside(routeQ[0])
                print("STATIONS TO STOP:")
                print(stations_to_stop[0])
                print("ROUTE Q")
                print(routeQ)
                
                ########## SWITCH CHECK ##################
                # Check if switch is in next 5 and get its index within the route queue. 
                for i in range(0, 5):
                    if i < len(routeQ) and routeQ[i] in switches:
                        switch_index = i
                        switch = switches[i]
                        break
                    else:
                        switch_index = None
                # if the switch is in the next 5 
                if switch_index != None:
                    # Check if the train is traveling in the right direction
                    correct_direction = False
                    for i in range (0,5):
                        if i < len(routeQ) and routeQ[i] == switch[0][0]:
                            correct_direction = True
                            break
                    # if the train is  traveling in the right direction then proceed.
                    if(correct_direction):
                        # check if switch is activated
                        if switch[2] == 1:
                            if self.altRouteBool == False:
                                self.altRouteBool = True
                                # remove the normal route from the routeQ
                                routeQ.remove(switch_index+1, switch_index+1+len(switch[0]))
                                # replace it with the alternative route
                                routeQ.insert(switch_index+1, switch[1])
                        # if switch is not activated
                        else:
                            if self.altRouteBool == True:
                                self.altRouteBool = False
                                # remove the alternative route from the routeQ
                                routeQ.remove(switch_index+1, switch_index+1+len(switch[1]))
                                # replace it with the normal route
                                routeQ.insert(switch_index+1, switch[0])


                ############## OCCUPANCY CHECK ############
                # determine the index of the occupied block within the routeQ
                for i in range(0, 5):
                    if i < len(routeQ) and routeQ[i] in global_block_occupancy:
                        occupied_index = i
                        occupied_block = routeQ[i]
                        break
                    else:
                        occupied_index = None
                # If there is an occupied block within the next 6...
                if occupied_index != None:
                    if(len(routeQ) >= 5 and occupied_block == routeQ[4]):
                        suggestedSpeed = (
                        int(0.75 * block_info_list[routeQ[0]].speedLimit)
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
                        line, wayside, routeQ[0], suggestedSpeed
                        )
                    elif(len(routeQ) >= 4 and occupied_block == routeQ[3]):
                        suggestedSpeed = (
                        int(0.5 * block_info_list[routeQ[0]].speedLimit)
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
                        line, wayside, routeQ[0], suggestedSpeed
                        )
                    elif(len(routeQ) >= 3 and occupied_block == routeQ[2]):
                        suggestedSpeed = (
                        int(0.25 * block_info_list[routeQ[0]].speedLimit)
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
                        line, wayside, routeQ[0], suggestedSpeed
                        )
                    elif(len(routeQ) >= 2 and occupied_block == routeQ[1]):
                        suggestedSpeed = 0
                        authority = 0

                        self.main_window.dispatchTable.setItem(
                            0, 3, QTableWidgetItem(str(suggestedSpeed))
                        )
                        self.main_window.dispatchTable.setItem(
                            0, 1, QTableWidgetItem(str(blockNum))
                        )
                        ctcToTrackController.sendSuggestedSpeed.emit(
                        line, wayside, routeQ[0], suggestedSpeed
                        )
                        ctcToTrackController.sendSuggestedSpeed.emit(
                        line, wayside, routeQ[0], suggestedSpeed
                        )
                        ctcToTrackController.sendAuthority.emit(
                        line, wayside, routeQ[0], authority
                        )


                # LIGHT CHECK 
                # STILL NEED TO DO THE CODE FOR THIS PART

                #STATION CHECK
                rowNumber = dispatchTrainsList.index(train)
                if len(routeQ) >= 4 and stations_to_stop[0] == routeQ[3]:
                    suggestedSpeed = (
                        int(0.75 * block_info_list[routeQ[0]].speedLimit)
                        * 0.621371
                    )
                    suggestedSpeed = round(suggestedSpeed, 2)
                    self.main_window.dispatchTable.setItem(
                        rowNumber, 3, QTableWidgetItem(str(suggestedSpeed))
                    )
                    self.main_window.dispatchTable.setItem(
                        rowNumber, 1, QTableWidgetItem(str(blockNum))
                    )
                    #Block.update_block_occupancy(blockNum, 1, self.main_window)

                    ctcToTrackController.sendSuggestedSpeed.emit(
                        line, wayside, routeQ[0], suggestedSpeed
                    )
                elif len(routeQ) >= 3 and stations_to_stop[0] == routeQ[2]:
                    suggestedSpeed = (
                        int(0.50 * block_info_list[routeQ[0]].speedLimit)
                        * 0.621371
                    )
                    suggestedSpeed = round(suggestedSpeed, 2)
                    self.main_window.dispatchTable.setItem(
                        rowNumber, 3, QTableWidgetItem(str(suggestedSpeed))
                    )
                    self.main_window.dispatchTable.setItem(
                        rowNumber, 1, QTableWidgetItem(str(blockNum))
                    )
                    ctcToTrackController.sendSuggestedSpeed.emit(
                        line, wayside, routeQ[0], suggestedSpeed
                    )
                elif len(routeQ) >= 2 and stations_to_stop[0] == routeQ[1]:
                    suggestedSpeed = (
                        int(0.25 * block_info_list[routeQ[0]].speedLimit)
                        * 0.621371
                    )
                    suggestedSpeed = round(suggestedSpeed, 2)

                    self.main_window.dispatchTable.setItem(
                        rowNumber, 3, QTableWidgetItem(str(suggestedSpeed))
                    )
                    self.main_window.dispatchTable.setItem(
                        rowNumber, 1, QTableWidgetItem(str(blockNum))
                    )
                    ctcToTrackController.sendSuggestedSpeed.emit(
                        line, wayside, routeQ[0], suggestedSpeed
                    )
                elif len(routeQ) >= 1 and stations_to_stop[0] == routeQ[0]:
                    suggestedSpeed = 0
                    station_name = self.find_station_name_by_block(stations_to_stop[0])

                    self.main_window.dispatchTable.setItem(
                        rowNumber, 3, QTableWidgetItem(str(suggestedSpeed))
                    )
                    self.main_window.dispatchTable.setItem(rowNumber, 4, QTableWidgetItem("0"))
                    ctcToTrackController.sendSuggestedSpeed.emit(
                        line, wayside, routeQ[0], suggestedSpeed
                    )
                    ctcToTrackController.sendAuthority.emit(line, wayside, blockNum, 0)
                    self.main_window.dispatchTable.setItem(
                        rowNumber, 1, QTableWidgetItem(str(station_name))
                    )
                    self.main_window.dispatchTable.setItem(
                        rowNumber, 2, QTableWidgetItem("Dwelling")
                    )

                    #current_time = self.main_window.systemTimeInput.text()
                    #current_time_str = current_time.replace(":", "")[:4]

                    current_time_str = self.main_window.systemTimeInput.text()[:8]
                    current_time_obj = QTime.fromString(current_time_str, "HH:mm:ss")

                    target_time_obj = current_time_obj.addSecs(60) 
                    #ctcToTrackController.signalTrainDwelling.emit(target_time_obj)
                    #print("Target Time:", target_time_obj.toString("HH:mm:ss"))
                    
                    QTimer.singleShot(15000,self.leaveStop)
                    #emite when dwelling, then check itll get, once then emit another signal

                else:
                    print(
                        "Top of route queue: ",
                        block_info_list[int(routeQ[0])].speedLimit,
                    )
                    print(
                        "Suggested Speed Before: ",
                        (block_info_list[int(routeQ[0])].speedLimit) * 0.621371,
                    )

                    suggestedSpeed = (
                        block_info_list[int(routeQ[0])].speedLimit
                    ) * 0.621371
                    suggestedSpeed = round(suggestedSpeed, 2)

                    self.main_window.dispatchTable.setItem(
                        rowNumber, 3, QTableWidgetItem(str(suggestedSpeed))
                    )
                    self.main_window.dispatchTable.setItem(
                        rowNumber, 1, QTableWidgetItem(str(blockNum))
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
                nextStop = self.find_station_name_by_block(self.stations_to_stop[0])
                print("Next stop:", nextStop)
        else:
            nextStop = "Returning to Yard"
            print("List was initially empty, nextStop set to 'Returning to Yard'")

        suggestedSpeed = round((self.block_info_list[self.routeQ[0]].speedLimit) * 0.621371, 2)
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

    def leaveStation(self, targetTimeOb):
        print("CHECKING IN LEAVE STATION")
        current_time_str = self.main_window.systemTimeInput.text()[:8]
        current_time_obj = QTime.fromString(current_time_str, "HH:mm:ss")
        print("CURRENT TIME IS:")
        print(current_time_obj)
        print("TARGET TIME IS:")
        print(targetTimeOb)

        if (current_time_obj >= targetTimeOb):
            self.leaveStop()


class Train:
    red_train_count = 0
    green_train_count = 0

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
        travel,
        correct_stations,
        blockInfo
    ):
        self.scheduler = scheduler
        self.main_window = CTCwindow

        self.trackLine = line
        self.timeArrival = arrivalTime
        self.trainDeparture = departureTime
        self.trainStops = stops
        self.authority = 1
        trainNum = trainNum + 1
        self.travelPath = travel
        self.altRouteBool = False
        self.ordered_stations = correct_stations
        self.blockList = blockInfo
        #train_routes[trainID] = self.routeQ

        self.sugg_speed = int(suggested_speed) if suggested_speed else 43.50

        if trainID and line == "Green Line":
            Train.green_train_count += 1
            self.train_id = trainID
        elif trainID and line == "Red Line":
            Train.red_train_count += 1
            self.train_id = trainID
        elif line == "Green Line":
            Train.green_train_count += 1
            self.train_id = f'{"Green"}{trainNum}'
        elif line == "Red Line":
            Train.red_train_count += 1
            self.train_id = f'{"Red"}{trainNum}'

        #self.dispatchTrainsList = []
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
        print(current_time_str)
        # Iterate through your list of trains and check their departure times
        for train in self.scheduler.trainList:
            departureTime = train.trainDeparture

            if departureTime == current_time_str:
                print("DISPATCHING TRAIN")
                # Add the train to the dispatched_trains list
                dispatchTrainsList.append(train)
                if train.trackLine == "Green Line":
                    lineTrack = "green"
                else:
                    lineTrack = "red"
                masterSignals.addTrain.emit(lineTrack, train.train_id)
                next_stop = self.trainStops[0]
                # Add the train's information to the dispatched trains table
                row_position = self.main_window.dispatchTable.rowCount()
                self.main_window.dispatchTable.insertRow(row_position)
                self.main_window.sendTrain.setEnabled(False)
                # Create a non-editable QTableWidgetItem for each piece of data
                train_id_item = QTableWidgetItem(train.train_id)
                location_item = QTableWidgetItem("0")  # Assuming "0" is the initial location
                
                next_stop_item = QTableWidgetItem(next_stop)
                suggested_speed_item = QTableWidgetItem(str(train.sugg_speed))
                authority_item = QTableWidgetItem(str(train.authority))

                # Set items as non-editable
                train_id_item.setFlags(train_id_item.flags() & ~Qt.ItemIsEditable)
                location_item.setFlags(location_item.flags() & ~Qt.ItemIsEditable)
                next_stop_item.setFlags(next_stop_item.flags() & ~Qt.ItemIsEditable)
                suggested_speed_item.setFlags(suggested_speed_item.flags() & ~Qt.ItemIsEditable)
                authority_item.setFlags(authority_item.flags() & ~Qt.ItemIsEditable)

                # Add items to the table
                self.main_window.dispatchTable.setItem(row_position, 0, train_id_item)
                self.main_window.dispatchTable.setItem(row_position, 1, location_item)
                self.main_window.dispatchTable.setItem(row_position, 2, next_stop_item)
                self.main_window.dispatchTable.setItem(row_position, 3, suggested_speed_item)
                self.main_window.dispatchTable.setItem(row_position, 4, authority_item)

            
                #Block.update_block_occupancy(0, 1, self.main_window, lineTrack)

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
    def update_block_occupancy(block_num, occupancy, main_window, line):
        global global_block_occupancy

        if global_block_occupancy.get(block_num) == occupancy:
            # The block occupancy status is unchanged, no need to update the table
            return
        
        global_block_occupancy[block_num] = occupancy
        
        Block.updateStatusLabel(main_window)

        if globalSelectLine == "Green Line":
            line = "Green"
        else:
            line = "Red"

        # Check if block_num is within the valid range (1 to 150)
        if line == "Green" and not (0 <= block_num <= 150):
            return
        elif line == "Red" and not (0 <= block_num <= 76):
            return
        
        # Update the occupancy_table
        if occupancy:  # If the block is now occupied
            # Check if the block is already in the table with the same occupancy
            for row in range(main_window.occupancy_table.rowCount()):
                if main_window.occupancy_table.item(row, 0).text() == str(block_num):
                    # Block already in the table with the same occupancy, do not add it again
                    return
                
            # Add the block and line to the table
            row_count = main_window.occupancy_table.rowCount()
            main_window.occupancy_table.insertRow(row_count)

            # Create non-editable QTableWidgetItem for block number and line
            block_num_item = QTableWidgetItem(str(block_num))
            line_item = QTableWidgetItem(line)

            # Set items as non-editable
            block_num_item.setFlags(block_num_item.flags() & ~Qt.ItemIsEditable)
            line_item.setFlags(line_item.flags() & ~Qt.ItemIsEditable)

            # Add items to the table
            main_window.occupancy_table.setItem(row_count, 0, block_num_item)
            main_window.occupancy_table.setItem(row_count, 1, line_item)

        else:  # If the block is no longer occupied
            # Remove the block from the table
            for row in range(main_window.occupancy_table.rowCount()):
                if main_window.occupancy_table.item(row, 0).text() == str(block_num):
                    main_window.occupancy_table.removeRow(row)
                    break

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
                str(i) for i in range(0, 151)
            ]  # Generating block numbers 0-150
            main_window.blockDropDown.addItem(blockItem)
            main_window.blockDropDown.addItems(block_items)
        elif selected_line == "Red Line":
            blockItem = "Select Block"
            block_items = [
                str(i) for i in range(0, 77)
            ]  # Generating block numbers 0-150
            main_window.blockDropDown.addItem(blockItem)
            main_window.blockDropDown.addItems(block_items)
            
    @staticmethod
    def updateStatusLabel(main_window):
        global global_block_occupancy  # Declare the global variable

        selected_block_num_text = main_window.blockDropDown.currentText()
        block_status = "Select a block"  # Default status
        status_color = "black"  # Default color

        # Check if the selected text is a number
        if selected_block_num_text.isdigit():
            selected_block_num = int(selected_block_num_text)

            for block_num in global_block_occupancy.keys():
                if block_num == selected_block_num:
                    # Assuming you want to check the occupancy status
                    occupancy = global_block_occupancy[block_num]
                    if occupancy:
                        block_status = "Occupied"
                        status_color = "red"
                    else:
                        block_status = "Unoccupied"
                        status_color = "green"
                    break

        status_text = f"<font color='{status_color}'>Status: {block_status}</font>"
        main_window.status_label.setText(status_text)

    @staticmethod
    def repairBlock(main_window):
        blockNum = Block.setSelectedBlock(main_window)
        global global_block_occupancy

        # Check if the block number matches any entry in the first column of dispatchTable
        for row in range(main_window.dispatchTable.rowCount()):
            if main_window.dispatchTable.item(row, 1) and \
               main_window.dispatchTable.item(row, 1).text() == str(blockNum):
                QMessageBox.warning(main_window, "Error", "Cannot repair the block as it is currently occupied by a train.")
                return
    
        # Check if the block is already unoccupied
        if not global_block_occupancy.get(blockNum, False):
            QMessageBox.warning(main_window, "Error", "Cannot repair the block as it is already unoccupied.")
            return
        
        # Set the block as unoccupied or perform the repair action
        global_block_occupancy[blockNum] = False
        Block.updateStatusLabel(main_window)

        # Remove the block from the table
        for row in range(main_window.occupancy_table.rowCount()):
            if main_window.occupancy_table.item(row, 0).text() == str(blockNum):
                main_window.occupancy_table.removeRow(row)
                break

        QMessageBox.information(main_window, "Success", "Block repaired successfully.")

    @staticmethod
    def closeBlock(main_window):
        blockNum = Block.setSelectedBlock(main_window)
        global global_block_occupancy

        if globalSelectLine == "Green Line":
            line = "Green"
        elif globalSelectLine == "Red Line":
            line = "Red"

        # Check if the block number matches any entry in the first column of dispatchTable
        for row in range(main_window.dispatchTable.rowCount()):
            if main_window.dispatchTable.item(row, 1) and \
               main_window.dispatchTable.item(row, 1).text() == str(blockNum):
                QMessageBox.warning(main_window, "Error", "Cannot close the block as it is currently occupied by a train.")
                return
    
        # Check if the block is already occupied
        if global_block_occupancy.get(blockNum, True):
            QMessageBox.warning(main_window, "Error", "Cannot close the block as it is occupied.")
            return
        
        # Set the block as unoccupied or perform the repair action
        global_block_occupancy[blockNum] = True
        Block.updateStatusLabel(main_window)

        # Add the block from the table
        # Check if the block is already in the table
        for row in range(main_window.occupancy_table.rowCount()):
            if main_window.occupancy_table.item(row, 0) and \
               main_window.occupancy_table.item(row, 0).text() == str(blockNum):
                # Block already in the table, no need to add it again
                return

        # Add the block to the table
        row_count = main_window.occupancy_table.rowCount()
        main_window.occupancy_table.insertRow(row_count)

        # Create QTableWidgetItem for block number and line
        block_num_item = QTableWidgetItem(str(blockNum))
        line_item = QTableWidgetItem(line)

        # Optionally, set items as non-editable if needed
        block_num_item.setFlags(block_num_item.flags() & ~Qt.ItemIsEditable)
        line_item.setFlags(line_item.flags() & ~Qt.ItemIsEditable)

        # Add items to the table
        main_window.occupancy_table.setItem(row_count, 0, block_num_item)
        main_window.occupancy_table.setItem(row_count, 1, line_item)

        QMessageBox.information(main_window, "Success", "Block closed successfully.")

            
    @staticmethod
    def getBlockStatus(block):
        # Assuming occupancy is a boolean, you can adjust the return value based on your requirements
        return "Occupied" if block.occupancy else "Unoccupied"

    @staticmethod
    def setSelectedBlock(main_window):
        selected_block = main_window.blockDropDown.currentText()

        # Check if the "Select a Block" placeholder is selected
        if selected_block == "Select Block":
            return None
        else:
            return int(selected_block) 
        