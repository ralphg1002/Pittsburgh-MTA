import cProfile
from decimal import DivisionByZero
from doctest import master
from email import header
from operator import length_hint
import pstats
from re import T
import sys
import os
import threading
from turtle import Turtle, update
from PyQt5 import QtGui
from PyQt5.QtCore import QCoreApplication, QRect, QSize, Qt, QTimer, QTime, QDateTime
from PyQt5.QtGui import QCursor, QFont, QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QFrame,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QComboBox,
    QCheckBox,
)
from line_profiler import LineProfiler
from numpy import block
from qtwidgets import AnimatedToggle
from TrainModel_Functions import *
from TrainModel_Calculations import *

current_path = os.path.dirname(os.path.abspath(__file__))
main_path = os.path.join(current_path, "../../main")
sys.path.append(main_path)

from signals import (
    trainControllerSWToTrainModel,
    trackModelToTrainModel,
    trainModelToTrainController,
    trainModelToTrackModel,
    masterSignals,
)


class TrainModel(QMainWindow):
    # Font variables
    textFontSize = 10
    labelFontSize = 12
    headerFontSize = 16
    titleFontSize = 22
    fontStyle = "Product Sans"

    # Color variables
    colorDarkBlue = "#085394"
    colorLightRed = "#EA9999"
    colorLightBlue = "#9FC5F8"
    colorLightGrey = "#CCCCCC"
    colorMediumGrey = "#DDDDDD"
    colorDarkGrey = "#666666"
    colorBlack = "#000000"

    # Dimensions
    w = 960
    h = 960
    moduleName = "Train Model"

    def __init__(self):
        super().__init__()
        self.trainsList = []
        self.functionsInstance = Calculations()

        self.time_interval = 1
        self.timer = QTimer(self)
        self.timer.timeout.connect(
            self.update
        )  # Connect the timer to the update_text function
        self.timer.start(
            self.time_interval
        )  # Update the text every 1000 milliseconds (1 second)

        self.sysTime = QDateTime.currentDateTime()
        self.sysTime.setTime(QTime(0, 0, 0))

        """ Header Template """

        # Setting title
        self.setWindowTitle(self.moduleName)

        # Setting geometry
        self.setGeometry(50, 50, self.w, self.h)

        # Body block
        self.bodyBlock = QLabel(self)
        self.bodyBlock.setGeometry(20, 20, 920, 920)
        self.bodyBlock.setStyleSheet(
            "background-color: white;" "border: 1px solid black"
        )

        # Header block
        self.headerBlock = QLabel(self)
        self.headerBlock.setGeometry(20, 20, 920, 70)
        self.headerBlock.setStyleSheet(
            "background-color:" + self.colorDarkBlue + ";" "border: 1px solid black"
        )

        # Title
        self.titleLabel = QLabel("Train Model", self)
        self.titleLabel.setFont(QFont(self.fontStyle, self.titleFontSize))
        self.titleLabel.setAlignment(Qt.AlignCenter)
        title_width = 400
        title_height = 50
        title_x = (self.width() - title_width) // 2
        title_y = 35
        self.titleLabel.setGeometry(title_x, title_y, title_width, title_height)
        self.titleLabel.setStyleSheet("color: white")

        # MTA Logo
        self.pixmapMTALogo = QtGui.QPixmap("src/main/TrainModel/MTA_Logo.png")
        self.pixmapMTALogo = self.pixmapMTALogo.scaled(70, 70)
        self.logo = QLabel(self)
        self.logo.setPixmap(self.pixmapMTALogo)
        self.logo.move(20, 20)
        self.logo.adjustSize()

        # Module
        self.moduleLabel = QLabel("Train Model", self)
        self.moduleLabel.setFont(QFont(self.fontStyle, self.headerFontSize))
        self.moduleLabel.setAlignment(Qt.AlignCenter)
        self.moduleLabel.move(30, 100)
        self.moduleLabel.adjustSize()
        self.moduleLabel.setStyleSheet("color:" + self.colorDarkBlue)

        # Test bench icon
        self.pixmapGear = QtGui.QPixmap("src/main/TrainModel/gear_icon.png")
        self.pixmapGear = self.pixmapGear.scaled(25, 25)
        self.testbenchIcon = QLabel(self)
        self.testbenchIcon.setPixmap(self.pixmapGear)
        self.testbenchIcon.setGeometry(30, 140, 32, 32)

        # Connect the search icon to the vehicle class
        self.testbenchIcon.mousePressEvent = self.open_test_window

        # Test bench button
        self.testbenchButton = QPushButton("Test Bench", self)
        self.testbenchButton.setFont(QFont(self.fontStyle, self.textFontSize))
        self.testbenchButton.setGeometry(60, 140, 100, 32)
        self.testbenchButton.setStyleSheet(
            "color:" + self.colorDarkBlue + ";border: 1px solid white"
        )

        # System time input
        self.systemTimeInput = QLabel("00:00:00", self)
        self.systemTimeInput.setFont(QFont(self.fontStyle, self.headerFontSize))
        self.systemTimeInput.setGeometry(820, 67, 150, 100)
        self.systemTimeInput.setStyleSheet("color:" + self.colorDarkBlue)

        # System time label
        self.systemTimeLabel = QLabel("System Time:", self)
        self.systemTimeLabel.setFont(QFont(self.fontStyle, self.headerFontSize))
        self.systemTimeLabel.adjustSize()
        self.systemTimeLabel.setGeometry(650, 65, 200, 100)
        self.systemTimeLabel.setStyleSheet("color:" + self.colorDarkBlue)

        # System speed label
        self.systemSpeedLabel = QLabel("System Speed:", self)
        self.systemSpeedLabel.setFont(QFont(self.fontStyle, self.textFontSize))
        self.systemSpeedLabel.setGeometry(689, 140, 200, 100)
        self.systemSpeedLabel.adjustSize()
        self.systemSpeedLabel.setStyleSheet("color:" + self.colorDarkBlue)

        # System speed input
        self.systemSpeedInput = QLabel("x1.0", self)
        self.systemSpeedInput.setFont(QFont(self.fontStyle, self.textFontSize))
        self.systemSpeedInput.setGeometry(850, 127, 50, 50)
        self.systemSpeedInput.setStyleSheet("color:" + self.colorDarkBlue)

        # Increase system speed button
        self.pixmapFastForward = QtGui.QPixmap("src/main/TrainModel/fast-forward.svg")
        self.pixmapFastForward = self.pixmapFastForward.scaled(20, 20)
        self.speedUpButton = QPushButton(self)
        self.speedUpButton.setIcon(QtGui.QIcon(self.pixmapFastForward))
        self.speedUpButton.setGeometry(890, 143, 20, 20)
        self.speedUpButton.setStyleSheet(
            "color:" + self.colorDarkBlue + ";border: 1px solid white"
        )

        # Decrease system speed button
        self.pixmapRewind = QtGui.QPixmap("src/main/TrainModel/rewind.svg")
        self.pixmapRewind = self.pixmapRewind.scaled(20, 20)
        self.slowDownButton = QPushButton(self)
        self.slowDownButton.setIcon(QtGui.QIcon(self.pixmapRewind))
        self.slowDownButton.setGeometry(819, 143, 20, 20)
        self.slowDownButton.setStyleSheet(
            "color:" + self.colorDarkBlue + ";border: 1px solid white"
        )

        """ Drop-down Menu """

        # Calculate the position of the QComboBox
        drop_down_width = 500
        drop_down_height = 40
        drop_down_x = int((self.w - drop_down_width) // 2)
        drop_down_y = int((self.h / 2) + (self.h / 4) - (drop_down_height / 2))

        # Create the QComboBox
        self.comboBox = QComboBox(self.bodyBlock)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.setGeometry(
            QRect(drop_down_x, drop_down_y, drop_down_width, drop_down_height)
        )
        font1 = QFont(self.fontStyle)
        font1.setPointSize(18)
        font1.setKerning(True)
        self.comboBox.setFont(font1)

        # Create a search icon for new window
        self.search_button = QtGui.QPixmap("src/main/TrainModel/search_icon.png")
        self.search_button = self.search_button.scaled(40, 40)
        self.icon = QLabel(self)
        self.icon.setPixmap(self.search_button)
        self.icon.setGeometry(QRect(750, 720, 40, 40))
        self.icon.adjustSize()

        # Connect the search icon to the vehicle class
        self.icon.mousePressEvent = self.open_results_window

        # Insert Train Image to main window
        image_path = "src/main/TrainModel/Train_Image.jpg"
        pixmap_train = QPixmap(image_path)
        image_width = 500
        image_height = 400
        image_y = drop_down_y - image_height - 20
        pixmap_train = pixmap_train.scaled(image_width, image_height)
        train_image_label = QLabel(self.bodyBlock)
        train_image_label.setPixmap(pixmap_train)
        train_image_label.setGeometry(drop_down_x, image_y, image_width, image_height)

        self.retranslate_Ui()

        self.results_window = None

    def retranslate_Ui(self):
        self.setWindowTitle(
            QCoreApplication.translate("TrainModel", "MainWindow", None)
        )
        self.titleLabel.setText(
            QCoreApplication.translate("TrainModel", "Train Model", None)
        )
        self.logo.setText("")

    def open_results_window(self, event):
        # This function is called when the search icon is clicked
        selected_item = self.comboBox.currentText()
        self.results_window = ResultsWindow(
            selected_item, self.trainsList
        )
        self.results_window.show()

    def open_test_window(self, event):
        # This function is called when the gear icon is clicked
        selected_item = self.comboBox.currentText()
        self.test_window = TrainTest()
        self.test_window.show()

    def show_gui(self):
        self.show()

    def signal_period(self, period):
        self.time_interval = period
    
    def signal_addTrain(self, line, id):
        # Combine line and id to create the trainID
        name = line + "_" + id
        train = TrainModelAttributes(name)
        
        # Check if trainID already exists in the list
        idCheck = False
        for train in self.trainsList:
            if train.calculations["trainID"]== name:
                idCheck = True
                break
        
        # If trainID already exists, do nothing
        if idCheck:
            return
        
        # Otherwise, add the new train to the list
        self.trainsList.append(train)
        
    def update_drop_down(self):
        existing_items = [self.comboBox.itemText(i) for i in range(self.comboBox.count())]
        
        all_trainIDs = []
        for trains in self.trainsList:
            all_trainIDs.append(trains.calculations["trainID"])

        missing_trainIDs = set(all_trainIDs) - set(existing_items)
        
        for trainID in missing_trainIDs:
            self.comboBox.addItem(trainID)

        for item in existing_items:
            if item not in all_trainIDs:
                index = self.comboBox.findText(item)
                self.comboBox.removeItem(index)

    def update(self):
        # system time
        # self.sysTime = self.sysTime.addSecs(1)
        masterSignals.addTrain.emit("green", "train1")
        masterSignals.timingMultiplier.connect(self.signal_period)
        masterSignals.clockSignal.connect(self.sysTime.setTime)
        masterSignals.addTrain.connect(self.signal_addTrain)
        self.timer.setInterval(self.time_interval)

        self.systemTimeInput.setText(self.sysTime.toString("HH:mm:ss"))
        self.systemSpeedInput.setText(
            "x" + format(1 / (self.time_interval / 1000), ".3f")
        )

        self.update_drop_down()

        # Signals that connect from the train controller to the train model
        trainControllerSWToTrainModel.sendPower.connect(self.signal_power)
        trainControllerSWToTrainModel.sendDriverEmergencyBrake.connect(self.signal_emergency_brake)
        trainControllerSWToTrainModel.sendDriverServiceBrake.connect(self.signal_brake)
        trainControllerSWToTrainModel.sendAnnouncement.connect(self.signal_announcement)
        trainControllerSWToTrainModel.sendHeadlightState.connect(self.signal_headlights)
        trainControllerSWToTrainModel.sendInteriorLightState.connect(self.signal_interior_lights)
        trainControllerSWToTrainModel.sendLeftDoorState.connect(self.signal_left_door)
        trainControllerSWToTrainModel.sendRightDoorState.connect(self.signal_right_door)
        trainControllerSWToTrainModel.sendSetpointTemperature.connect(self.signal_temperature)
        trainControllerSWToTrainModel.sendAdvertisement.connect(self.signal_advertisements)

        # Signals that connect from the track model to the train model
        trackModelToTrainModel.blockInfo.connect(self.signal_blockInfo)
        trackModelToTrainModel.beacon.connect(self.signal_beacon)
        trackModelToTrainModel.newCurrentPassengers.connect(self.signal_new_passengers)

        # Send train controller information
        for trainObject in self.trainsList:
            trainObject.calculations["timeInterval"] = self.time_interval
            self.functionsInstance.TrainModelCalculations(trainObject)
            self.functionsInstance.temperature(trainObject)
            self.functionsInstance.beacon(trainObject)
            trainModelToTrainController.sendSpeedLimit.emit(trainObject.calculations["trainID"], trainObject.vehicle_status["speed_limit"])
            trainModelToTrainController.sendBlockNumber.emit(trainObject.calculations["trainID"], trainObject.vehicle_status["current_speed"])
            trainModelToTrainController.sendCommandedSpeed.emit(trainObject.calculations["trainID"], trainObject.vehicle_status["commanded_speed"])
            trainModelToTrainController.sendAuthority.emit(trainObject.calculations["trainID"], trainObject.navigation_status["authority"])
            trainModelToTrainController.sendEngineFailure.emit(trainObject.calculations["trainID"], trainObject.failure_status["engine_failure"])
            trainModelToTrainController.sendSignalPickupFailure.emit(trainObject.calculations["trainID"], trainObject.failure_status["signal_pickup_failure"])
            trainModelToTrainController.sendBrakeFailure.emit(trainObject.calculations["trainID"], trainObject.failure_status["brake_failure"])
            trainModelToTrainController.sendPassengerEmergencyBrake.emit(trainObject.calculations["trainID"], trainObject.navigation_status["passenger_emergency_brake"])
            trainModelToTrainController.sendTemperature.emit(trainObject.calculations["trainID"], trainObject.passenger_status["temperature"])
            trainModelToTrainController.sendNextStation1.emit(trainObject.calculations["trainID"], trainObject.calculations["nextStation1"])
            trainModelToTrainController.sendNextStation2.emit(trainObject.calculations["trainID"], trainObject.calculations["nextStation2"])
            trainModelToTrainController.sendCurrStation.emit(trainObject.calculations["trainID"], trainObject.calculations["currStation"])
            trainModelToTrainController.sendLeftDoor.emit(trainObject.calculations["trainID"], trainObject.passenger_status["left_door"])
            trainModelToTrainController.sendRightDoor.emit(trainObject.calculations["trainID"], trainObject.passenger_status["right_door"])
            trainModelToTrainController.sendBlockNumber.emit(trainObject.calculations["trainID"], trainObject.calculations["currBlock"])            
            if trainObject.calculations["initialized"]:
                trainModelToTrackModel.sendPolarity.emit(trainObject.calculations["line"], trainObject.calculations["currBlock"], trainObject.calculations["prevBlock"])
                trainObject.calculations["initialized"] = False
            if trainObject.calculations["distance"] == trainObject.navigation_status["block_length"]:
                trainObject.calculations["back_length"] = trainObject.calculations["distance"] - trainObject.calculations["length"]
                trainObject.calculations["distance"] = 0
                trainObject.calculations["polarity"] = not trainObject.calculations["polarity"]
                trainModelToTrackModel.sendPolarity.emit(trainObject.calculations["line"], trainObject.calculations["currBlock"], trainObject.calculations["prevBlock"])
                if trainObject.calculations["back_length"] >= trainObject.navigation_status["block_length"]:
                    # Reset distance for the back of the train
                    trainObject.calculations["back_length"] = 0
                    trainModelToTrackModel.sendPolarity.emit(trainObject.calculations["line"], trainObject.calculations["currBlock"], trainObject.calculations["prevBlock"])
            trainModelToTrainController.sendPolarity.emit(trainObject.calculations["trainID"], trainObject.calculations["polarity"])
            trainObject.calculations["prevBlock"] = trainObject.calculations["currBlock"]

    def signal_blockInfo(self, nextBlock, blockLength, blockGrade, speedLimit, suggestedSpeed, authority):
        for trainObject in self.trainsList:
            trainObject.calculations["nextBlock"] = nextBlock
            trainObject.navigation_status["block_length"] = blockLength
            trainObject.navigation_status["block_grade"] = blockGrade
            trainObject.vehicle_status["speed_limit"] = speedLimit
            trainObject.vehicle_status["commanded_speed"] = suggestedSpeed
            trainObject.navigation_status["authority"] = authority
        return

    def signal_beacon(self, beaconDict):
        for trainObject in self.trainsList:
            if trainObject.calulations["currStation"] == trainObject.navigation_status["next_station"]:
                # The train is at a station, request passengers
                trainModelToTrackModel.sendCurrentPassengers.emit(trainObject.calculations["line"], trainObject.
                                                                  calculations["currStation"], trainObject.passenger_status["passengers"])
                            
            trainObject.calculations["nextStation1"] = beaconDict["Next Station1"]
            trainObject.calculations["nextStation2"] = beaconDict["Next Station2"]
            trainObject.calculations["currStation"] = beaconDict["Current Station"]
            trainObject.calculations["doorSide"] = beaconDict["Door Side"]

            if trainObject.calculations["nextStation1"] == trainObject.navigation_status["prev_station"]:
                trainObject.navigation_status["next_station"] = trainObject.calculations["nextStation2"]
            else: 
                trainObject.navigation_status["next_station"] = trainObject.calculations["nextStation1"]
            
        return

    def signal_new_passengers(self, passengers):
        for trainObject in self.trainsList:
            trainObject.passenger_status["passengers"] = passengers

    def signal_power(self, id, power):
        for train in self.trainsList:
            if train.calculations["trainID"] == id:
                train.vehicle_status["power"] = power

    def signal_interior_lights(self, id, status):
        for train in self.trainsList:
            if train.calculations["trainID"] == id:
                train.passenger_status["lights_status"] = status

    def signal_left_door(self, id, status):
        for train in self.trainsList:
            if train.calculations["trainID"] == id:
                train.passenger_status["left_door"] = status

    def signal_right_door(self, id, status):
        for train in self.trainsList:
            if train.calculations["trainID"] == id:
                train.passenger_status["right_door"] = status

    def signal_temperature(self, id, temp):
        for train in self.trainsList:
            if train.calculations["trainID"] == id:
                train.calculations["setpoint_temp"] = temp

    def signal_advertisements(self, id, val):
        for train in self.trainsList:
            if train.calculations["trainID"] == id:
                train.passenger_status["advertisements"] = val

    def signal_headlights(self, id, status):
        for train in self.trainsList:
            if train.calculations["trainID"] == id:
                train.navigation_status["headlights"] = status

    def signal_brake(self, id, eff):
        for train in self.trainsList:
            if train.calculations["trainID"] == id:
                train.vehicle_status["brakes"] = eff

    def signal_emergency_brake(self, id, status):
        for train in self.trainsList:
            if train.calculations["trainID"] == id:
                train.failure_status["emergency_brake"] = status

    def signal_announcement(self, id, ann):
        for train in self.trainsList:
            if train.calculations["trainID"] == id:
                train.passenger_status["announcements"] = ann

class ResultsWindow(QMainWindow):
    # Font variables
    textFontSize = 10
    labelFontSize = 12
    headerFontSize = 16
    titleFontSize = 22
    fontStyle = "Product Sans"

    # Color variables
    colorDarkBlue = "#085394"
    colorLightRed = "#EA9999"
    colorLightBlue = "#9FC5F8"
    colorLightGrey = "#CCCCCC"
    colorMediumGrey = "#DDDDDD"
    colorDarkGrey = "#666666"
    colorBlack = "#000000"

    # Dimensions
    w = 960
    h = 960

    moduleName = "Results Window"

    def __init__(self, selected_text, trains):
        super().__init__()
        # Trains List
        self.trainsList = trains

        ############

        self.time_interval = 1
        self.timer = QTimer(self)
        self.timer.timeout.connect(
            self.update
        )  # Connect the timer to the update_text function
        self.timer.start(
            self.time_interval
        )  # Update the text every 1000 milliseconds (1 second)

        self.sysTime = QDateTime.currentDateTime()
        self.sysTime.setTime(QTime(0, 0, 0))

        """ Header Template """

        # Setting title
        self.setWindowTitle(self.moduleName)

        # Setting geometry
        self.setGeometry(50, 50, self.w, self.h)

        # Body block
        self.bodyBlock = QLabel(self)
        self.bodyBlock.setGeometry(20, 20, 920, 920)
        self.bodyBlock.setStyleSheet(
            "background-color: white;" "border: 1px solid black"
        )

        # Header block
        self.headerBlock = QLabel(self)
        self.headerBlock.setGeometry(20, 20, 920, 70)
        self.headerBlock.setStyleSheet(
            "background-color:" + self.colorDarkBlue + ";" "border: 1px solid black"
        )

        # Title
        self.titleLabel = QLabel("Train Model", self)
        self.titleLabel.setFont(QFont(self.fontStyle, self.titleFontSize))
        self.titleLabel.setAlignment(Qt.AlignCenter)
        title_width = 400
        title_height = 50
        title_x = (self.width() - title_width) // 2
        title_y = 35
        self.titleLabel.setGeometry(title_x, title_y, title_width, title_height)
        self.titleLabel.setStyleSheet("color: white")

        # MTA Logo
        self.pixmapMTALogo = QtGui.QPixmap("src/main/TrainModel/MTA_Logo.png")
        self.pixmapMTALogo = self.pixmapMTALogo.scaled(70, 70)
        self.logo = QLabel(self)
        self.logo.setPixmap(self.pixmapMTALogo)
        self.logo.move(20, 20)
        self.logo.adjustSize()

        # Module
        self.moduleLabel = QLabel("Train Model", self)
        self.moduleLabel.setFont(QFont(self.fontStyle, self.headerFontSize))
        self.moduleLabel.setAlignment(Qt.AlignCenter)
        self.moduleLabel.move(30, 100)
        self.moduleLabel.adjustSize()
        self.moduleLabel.setStyleSheet("color:" + self.colorDarkBlue)

        # Test bench icon
        self.pixmapGear = QtGui.QPixmap("src/main/TrainModel/gear_icon.png")
        self.pixmapGear = self.pixmapGear.scaled(25, 25)
        self.testbenchIcon = QLabel(self)
        self.testbenchIcon.setPixmap(self.pixmapGear)
        self.testbenchIcon.setGeometry(30, 140, 32, 32)

        # Test bench button
        self.testbenchButton = QPushButton("Test Bench", self)
        self.testbenchButton.setFont(QFont(self.fontStyle, self.textFontSize))
        self.testbenchButton.setGeometry(60, 140, 100, 32)
        self.testbenchButton.setStyleSheet(
            "color:" + self.colorDarkBlue + ";border: 1px solid white"
        )

        # System time input
        self.systemTimeInput = QLabel("00:00:00", self)
        self.systemTimeInput.setFont(QFont(self.fontStyle, self.headerFontSize))
        self.systemTimeInput.setGeometry(820, 67, 150, 100)
        self.systemTimeInput.setStyleSheet("color:" + self.colorDarkBlue)

        # System time label
        self.systemTimeLabel = QLabel("System Time:", self)
        self.systemTimeLabel.setFont(QFont(self.fontStyle, self.headerFontSize))
        self.systemTimeLabel.adjustSize()
        self.systemTimeLabel.setGeometry(650, 65, 200, 100)
        self.systemTimeLabel.setStyleSheet("color:" + self.colorDarkBlue)

        # System speed label
        self.systemSpeedLabel = QLabel("System Speed:", self)
        self.systemSpeedLabel.setFont(QFont(self.fontStyle, self.textFontSize))
        self.systemSpeedLabel.setGeometry(689, 140, 100, 100)
        self.systemSpeedLabel.adjustSize()
        self.systemSpeedLabel.setStyleSheet("color:" + self.colorDarkBlue)

        # System speed input
        self.systemSpeedInput = QLabel("x1.0", self)
        self.systemSpeedInput.setFont(QFont(self.fontStyle, self.textFontSize))
        self.systemSpeedInput.setGeometry(850, 127, 50, 50)
        self.systemSpeedInput.setStyleSheet("color:" + self.colorDarkBlue)

        # Increase system speed button
        self.pixmapFastForward = QtGui.QPixmap("src/main/TrainModel/fast-forward.svg")
        self.pixmapFastForward = self.pixmapFastForward.scaled(20, 20)
        self.speedUpButton = QPushButton(self)
        self.speedUpButton.setIcon(QtGui.QIcon(self.pixmapFastForward))
        self.speedUpButton.setGeometry(890, 143, 20, 20)
        self.speedUpButton.setStyleSheet(
            "color:" + self.colorDarkBlue + ";border: 1px solid white"
        )

        # Decrease system speed button
        self.pixmapRewind = QtGui.QPixmap("src/main/TrainModel/rewind.svg")
        self.pixmapRewind = self.pixmapRewind.scaled(20, 20)
        self.slowDownButton = QPushButton(self)
        self.slowDownButton.setIcon(QtGui.QIcon(self.pixmapRewind))
        self.slowDownButton.setGeometry(819, 143, 20, 20)
        self.slowDownButton.setStyleSheet(
            "color:" + self.colorDarkBlue + ";border: 1px solid white"
        )

        # Create a QLabel to display the drop-down text
        current_train = QLabel(self)
        current_train.setText(f"Selected Train: {selected_text}")
        current_train.setFont(QFont(self.fontStyle, 16))
        current_train.setGeometry(QRect(275, 100, 400, 50))
        current_train.setAlignment(Qt.AlignCenter)

        # Extract the selected train name from the QLabel's text
        self.selected_train_name = current_train.text().split(":")[-1].strip()

        """ Vehicle Status """

        # Create a QLabel for the vehicle status window
        self.vehicle_label = QLabel(self.bodyBlock)
        self.vehicle_label.setGeometry(QRect(75, 170, 350, 300))
        self.vehicle_label.setStyleSheet("margin: 10px; padding: 0px; border: none;")

        # Create a container widget for the blue and white backgrounds for vehicle status
        self.vehicle_background_widget = QWidget(self.vehicle_label)
        self.vehicle_background_widget.setGeometry(QRect(0, 0, 350, 50))
        self.vehicle_background_widget.setStyleSheet(
            "background-color: #007BFF; border: 2px solid #000000; border-radius: 5px;"
        )

        # Create a layout for the blue and white backgrounds for vehicle status
        self.vehicle_background_layout = QVBoxLayout(self.vehicle_background_widget)
        self.vehicle_background_layout.setContentsMargins(0, 0, 0, 0)
        self.vehicle_background_layout.setSpacing(0)

        # Create a QLabel for the white background below the blue for vehicle status
        self.vehicle_white_background_label = QLabel(self.bodyBlock)
        self.vehicle_white_background_label.setGeometry(QRect(75, 200, 350, 300))
        self.vehicle_white_background_label.setStyleSheet(
            "background-color: #FFFFFF; margin: 10px; padding: 10px; border: 2px solid #000000; border-radius: 5px;"
        )

        # Create a layout for the white background below the blue header for vehicle status
        self.vehicle_white_background_layout = QVBoxLayout(
            self.vehicle_white_background_label
        )
        self.vehicle_white_background_layout.setContentsMargins(5, 5, 5, 5)
        self.vehicle_white_background_layout.setSpacing(10)

        # Create QLabel widgets for the list of words
        self.vehicle_word_list = [
            "Speed Limit: {} mph",
            "Current Speed: {} mph",
            "Setpoint Speed: {} mph",
            "Commanded Speed: {} mph",
            "Acceleration: {} ft/s",
            "Brakes: {}",
            "Power: {} kW",
            "Power Limit: {} kW",
        ]

        # QLabel for speed limit
        self.word_label_speed_limit = QLabel(
            "Speed Limit: {} mph".format(self.trainsList[0].vehicle_status["speed_limit"]),
            self.vehicle_white_background_label
        )
        self.word_label_speed_limit.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.word_label_speed_limit.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.word_label_speed_limit.setContentsMargins(5, 5, 5, 5)
        self.word_label_speed_limit.setFont(QFont("Arial", 9))

        # QLabel for current speed
        self.word_label_current_speed = QLabel(
            "Current Speed: {} mph".format(self.trainsList[0].vehicle_status["current_speed"]),
            self.vehicle_white_background_label
        )
        self.word_label_current_speed.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.word_label_current_speed.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.word_label_current_speed.setContentsMargins(5, 5, 5, 5)
        self.word_label_current_speed.setFont(QFont("Arial", 9))

        # QLabel for Setpoint Speed
        self.word_label_setpoint_speed = QLabel(
            "Setpoint Speed: {} mph".format(self.trainsList[0].vehicle_status["setpoint_speed"]),
            self.vehicle_white_background_label
        )
        self.word_label_setpoint_speed.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.word_label_setpoint_speed.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.word_label_setpoint_speed.setContentsMargins(5, 5, 5, 5)
        self.word_label_setpoint_speed.setFont(QFont("Arial", 9))

        # QLabel for commanded speed
        self.word_label_commanded_speed = QLabel(
            "Commanded Speed: {} mph".format(self.trainsList[0].vehicle_status["commanded_speed"]),
            self.vehicle_white_background_label
        )
        self.word_label_commanded_speed.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.word_label_commanded_speed.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.word_label_commanded_speed.setContentsMargins(5, 5, 5, 5)
        self.word_label_commanded_speed.setFont(QFont("Arial", 9))

        # QLabel for acceleration
        self.word_label_acceleration = QLabel(
            "Acceleration: {} ft/s".format(self.trainsList[0].vehicle_status["acceleration"]),
            self.vehicle_white_background_label
        )
        self.word_label_acceleration.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.word_label_acceleration.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.word_label_acceleration.setContentsMargins(5, 5, 5, 5)
        self.word_label_acceleration.setFont(QFont("Arial", 9))

        # QLabel for brakes
        self.word_label_brakes = QLabel(
            "Brakes: {}".format(self.trainsList[0].vehicle_status["brakes"]),
            self.vehicle_white_background_label
        )
        self.word_label_brakes.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.word_label_brakes.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.word_label_brakes.setContentsMargins(5, 5, 5, 5)
        self.word_label_brakes.setFont(QFont("Arial", 9))

        # QLabel for power
        self.word_label_power = QLabel(
            "Power: {} kW".format(self.trainsList[0].vehicle_status["power"]),
            self.vehicle_white_background_label
        )
        self.word_label_power.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.word_label_power.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.word_label_power.setContentsMargins(5, 5, 5, 5)
        self.word_label_power.setFont(QFont("Arial", 9))

        # QLabel for power limit
        self.word_label_power_limit = QLabel(
            "Power Limit: {} kW".format(self.trainsList[0].vehicle_status["power_limit"]),
            self.vehicle_white_background_label
        )
        self.word_label_power_limit.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.word_label_power_limit.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.word_label_power_limit.setContentsMargins(5, 5, 5, 5)
        self.word_label_power_limit.setFont(QFont("Arial", 9))

        # Add QLabel widgets to layout
        self.vehicle_white_background_layout.addWidget(
            self.word_label_speed_limit, alignment=Qt.AlignTop
        )

        self.vehicle_white_background_layout.addWidget(
            self.word_label_current_speed, alignment=Qt.AlignTop
        )

        self.vehicle_white_background_layout.addWidget(
            self.word_label_setpoint_speed, alignment=Qt.AlignTop
        )

        self.vehicle_white_background_layout.addWidget(
            self.word_label_commanded_speed, alignment=Qt.AlignTop
        )

        self.vehicle_white_background_layout.addWidget(
            self.word_label_acceleration, alignment=Qt.AlignTop
        )

        self.vehicle_white_background_layout.addWidget(
            self.word_label_brakes, alignment=Qt.AlignTop
        )

        self.vehicle_white_background_layout.addWidget(
            self.word_label_power, alignment=Qt.AlignTop
        )

        self.vehicle_white_background_layout.addWidget(
            self.word_label_power_limit, alignment=Qt.AlignTop
        )

        # Add stretch
        self.vehicle_white_background_layout.addStretch(1)
        
        # self.vehicle_status = {}
        # self.vehicle_labels = []

        # # Check if the selected train exists in the trains dictionary
        # if self.selected_train_name in self.trains.trains:
        #     train_data = self.trains.trains[self.selected_train_name]
        #     self.vehicle_status = train_data.get("vehicle_status", {})

        #     # Create and add QLabel widgets for each word the layout in vehicle status
        #     for word_placeholders in self.vehicle_word_list:
        #         word_key = (
        #             word_placeholders.split(":")[0].strip().lower().replace(" ", "_")
        #         )
        #         word_value = self.vehicle_status.get(word_key, "N/A")

        #         # Create the QLabel widget
        #         if (
        #             "{}" in word_placeholders
        #             and "{}" in word_placeholders[word_placeholders.find("{}") + 2 :]
        #         ):  # Check if there are two placeholders in the string
        #             word = word_placeholders.format(
        #                 self.selected_train_name, word_value
        #             )
        #         else:
        #             word = word_placeholders.format(word_value)

        #         # Create the QLabel widget
        #         self.word_label = QLabel(word, self.vehicle_white_background_label)
        #         self.word_label.setStyleSheet(
        #             "color: #000000; background-color: transparent; border: none;"
        #         )
        #         self.word_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        #         self.word_label.setContentsMargins(5, 5, 5, 5)
        #         self.word_label.setFont(QFont("Arial", 9))

        #         self.vehicle_labels.append(self.word_label)

        #         self.vehicle_white_background_layout.addWidget(
        #             self.word_label, alignment=Qt.AlignTop
        #         )

        # self.vehicle_white_background_layout.addStretch(1)

        # Create the title label for vehicle status
        self.vehicle_title_label = QLabel("Vehicle Status:", self.vehicle_label)
        self.font = QFont()
        self.font.setPointSize(14)
        self.font.setBold(True)
        self.vehicle_title_label.setFont(self.font)
        self.vehicle_title_label.setStyleSheet(
            "color: #FFFFFF; background-color: transparent; border: none;"
        )
        self.vehicle_title_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.vehicle_title_label.setGeometry(
            QRect(
                0,
                0,
                self.vehicle_background_widget.width(),
                self.vehicle_background_widget.height(),
            )
        )

        """ Failure Status """

        # Create a QLabel for the failure rectangle
        self.failure_label = QLabel(self.bodyBlock)
        self.failure_label.setGeometry(QRect(500, 170, 350, 300))
        self.failure_label.setStyleSheet("margin: 10px; padding: 0px; border: none;")

        # Create a container widget for the red and white backgrounds for failure window
        self.failure_background_widget = QWidget(self.failure_label)
        self.failure_background_widget.setGeometry(QRect(0, 0, 350, 50))
        self.failure_background_widget.setStyleSheet(
            "background-color: #FF0000; border: 2px solid #000000; border-radius: 5px;"
        )

        # Create a layout for the red and white background widget for failure window
        self.failure_white_background_layout = QVBoxLayout(
            self.failure_background_widget
        )
        self.failure_white_background_layout.setContentsMargins(0, 0, 0, 0)
        self.failure_white_background_layout.setSpacing(0)

        # Create a QLabel for the white background below the red for failure window
        self.failure_white_background_label = QLabel(self.bodyBlock)
        self.failure_white_background_label.setGeometry(QRect(500, 200, 350, 300))
        self.failure_white_background_label.setStyleSheet(
            "background-color: #FFFFFF; margin: 10px; padding: 10px; border: 2px solid #000000; border-radius: 5px;"
        )

        # Create a layout for the white background below the red header for failure window
        self.failure_white_background_layout = QVBoxLayout(
            self.failure_white_background_label
        )
        self.failure_white_background_layout.setContentsMargins(5, 5, 5, 5)
        self.failure_white_background_layout.setSpacing(10)

        # Create QLabel widgets for the list of words
        failure_word_list = [
            "Engine Failure: {}",
            "Signal Pickup Failure: {}",
            "Brake Failure: {}",
            "Emergency Brake: {}",
        ]

        # QLabel for engine failure
        self.word_label_engine_failure = QLabel(
            "Engine Failure: {}".format(self.trainsList[0].failure_status["engine_failure"]),
            self.failure_white_background_label
        )
        self.word_label_engine_failure.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.word_label_engine_failure.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.word_label_engine_failure.setContentsMargins(0, 0, 0, 0)
        self.word_label_engine_failure.setFont(QFont("Arial", 9))

        # QLabel for signal pickup failure
        self.word_label_signal_pickup_failure = QLabel(
            "Signal Pickup Failure: {}".format(self.trainsList[0].failure_status["signal_pickup_failure"]),
            self.failure_white_background_label
        )
        self.word_label_signal_pickup_failure.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.word_label_signal_pickup_failure.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.word_label_signal_pickup_failure.setContentsMargins(0, 0, 0, 0)
        self.word_label_signal_pickup_failure.setFont(QFont("Arial", 9))

        # QLabel for brake failure
        self.word_label_brake_failure = QLabel(
            "Brake Failure: {}".format(self.trainsList[0].failure_status["brake_failure"]),
            self.failure_white_background_label
        )
        self.word_label_brake_failure.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.word_label_brake_failure.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.word_label_brake_failure.setContentsMargins(0, 0, 0, 0)
        self.word_label_brake_failure.setFont(QFont("Arial", 9))

        # QLabel for emergency brake
        self.word_label_emergency_brake = QLabel(
            "Emergency Brake: {}".format(self.trainsList[0].failure_status["emergency_brake"]),
            self.failure_white_background_label
        )
        self.word_label_emergency_brake.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.word_label_emergency_brake.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.word_label_emergency_brake.setContentsMargins(0, 0, 0, 0)
        self.word_label_emergency_brake.setFont(QFont("Arial", 9))

        # Add QLabel widgets to layout
        self.failure_white_background_layout.addWidget(
            self.word_label_engine_failure, alignment=Qt.AlignTop
        )

        # Add QLabel widgets to layout
        self.failure_white_background_layout.addWidget(
            self.word_label_signal_pickup_failure, alignment=Qt.AlignTop
        )

        # Add QLabel widgets to layout
        self.failure_white_background_layout.addWidget(
            self.word_label_brake_failure, alignment=Qt.AlignTop
        )

        # Add QLabel widgets to layout
        self.failure_white_background_layout.addWidget(
            self.word_label_emergency_brake, alignment=Qt.AlignTop
        )
        
        # failure_status = {}

        # # Check if the selected train exists in the trains dictionary
        # if self.selected_train_name in self.trains.trains:
        #     train_data = self.trains.trains[self.selected_train_name]
        #     failure_status = train_data.get("failure_status", {})

        #     # Iterate through the failure_word_list
        #     for word_placeholders in failure_word_list:
        #         word_key = (
        #             word_placeholders.split(":")[0].strip().lower().replace(" ", "_")
        #         )

        #         # Create the QLabel widget for failure name
        #         failure_label_text = word_placeholders.format("")
        #         failure_label = QLabel(
        #             failure_label_text, self.failure_white_background_label
        #         )
        #         failure_label.setStyleSheet(
        #             "color: #000000; background-color: transparent; border: none;"
        #         )
        #         failure_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        #         failure_label.setContentsMargins(10, 10, 10, 10)
        #         failure_label.setFont(QFont("Arial", 9))

        #         # Create the QCheckBox widget
        #         check = QCheckBox()

        #         # Set the checkbox state based on the value in failure_status
        #         check.setChecked(
        #             self.trains.get_value(
        #                 self.selected_train_name, "failure_status", word_key
        #             )
        #         )

        #         # Create a QHBoxLayout for each failure and add QLabel and QCheckBox to it
        #         failure_layout = QHBoxLayout()
        #         failure_layout.addWidget(failure_label)
        #         failure_layout.addWidget(check)
        #         failure_layout.setAlignment(Qt.AlignVCenter | Qt.AlignRight)
        #         failure_layout.setContentsMargins(10, 10, 10, 10)

        #         # Add the QHBoxLayout to the main layout
        #         self.failure_white_background_layout.addLayout(failure_layout)

        #         # Connect the checkbox state change to a function/slot
        #         check.stateChanged.connect(
        #             lambda state, train=self.selected_train_name, key=word_key, checkbox=check: self.update_failure_status(
        #                 train, key, checkbox.isChecked()
        #             )
        #         )

        # self.failure_white_background_layout.addStretch(1)

        # Create the title label
        self.failure_title_label = QLabel("Failures:", self.failure_label)
        self.font = QFont()
        self.font.setPointSize(14)
        self.font.setBold(True)
        self.failure_title_label.setFont(self.font)
        self.failure_title_label.setStyleSheet(
            "color: #FFFFFF; background-color: transparent;"
        )
        self.failure_title_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.failure_title_label.setGeometry(
            QRect(
                0,
                0,
                self.failure_background_widget.width(),
                self.failure_background_widget.height(),
            )
        )

        """ Passenger Status """

        # Create a QLabel for the Passenger Status
        self.passenger_label = QLabel(self.bodyBlock)
        self.passenger_label.setGeometry(QRect(75, 550, 350, 300))
        self.passenger_label.setStyleSheet("margin: 10px; padding: 0px; border: none;")

        # Create a container widget for the blue and white backgrounds for passenger status
        self.passenger_background_widget = QWidget(self.passenger_label)
        self.passenger_background_widget.setGeometry(QRect(0, 0, 350, 50))
        self.passenger_background_widget.setStyleSheet(
            "background-color: #007BFF; border: 2px solid #000000; border-radius: 5px;"
        )

        # Create a layout for the blue and white background widget for passenger status
        self.passenger_background_layout = QVBoxLayout(self.passenger_background_widget)
        self.passenger_background_layout.setContentsMargins(0, 0, 0, 0)
        self.passenger_background_layout.setSpacing(0)

        # Create a QLabel for the white background below the blue
        self.passenger_white_background_label = QLabel(self.bodyBlock)
        self.passenger_white_background_label.setGeometry(QRect(75, 580, 350, 300))
        self.passenger_white_background_label.setStyleSheet(
            "background-color: #FFFFFF; margin: 10px; padding: 10px; border: 2px solid #000000; border-radius: 5px;"
        )

        # Create a layout for the white background below the blue header for vehicle status
        self.passenger_white_background_layout = QVBoxLayout(
            self.passenger_white_background_label
        )
        self.passenger_white_background_layout.setContentsMargins(5, 5, 5, 5)
        self.passenger_white_background_layout.setSpacing(10)

        # Create QLabel widgets for the list of words
        self.passenger_word_list = [
            "Passengers: {}",
            "Passenger Limit: {}",
            "Left Door: {}",
            "Right Door: {}",
            "Lights Status: {}",
            "Announcements: {}",
            "Temperature: {}",
            "Air Conditioning: {}",
            "Advertisements: {}",
        ]

        # QLabel for passengers
        self.word_label_passengers = QLabel(
            "Passengers: {}".format(self.trainsList[0].passenger_status["passengers"]),
            self.passenger_white_background_label
            
        )
        self.word_label_passengers.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.word_label_passengers.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.word_label_passengers.setContentsMargins(5, 5, 5, 5)
        self.word_label_passengers.setFont(QFont("Arial", 9))

        # QLabel for passenger limit
        self.word_label_passenger_limit = QLabel(
            "Passenger Limit: {}".format(self.trainsList[0].passenger_status["passenger_limit"]),
            self.passenger_white_background_label
        )
        self.word_label_passenger_limit.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.word_label_passenger_limit.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.word_label_passenger_limit.setContentsMargins(5, 5, 5, 5)
        self.word_label_passenger_limit.setFont(QFont("Arial", 9))

        # QLabel for left door
        self.word_label_left_door = QLabel(
            "Left Door: {}".format(self.trainsList[0].passenger_status["left_door"]),
            self.passenger_white_background_label
        )
        self.word_label_left_door.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.word_label_left_door.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.word_label_left_door.setContentsMargins(5, 5, 5, 5)
        self.word_label_left_door.setFont(QFont("Arial", 9))

        # QLabel for right door
        self.word_label_right_door = QLabel(
            "Right Door: {}".format(self.trainsList[0].passenger_status["right_door"]),
            self.passenger_white_background_label
        )
        self.word_label_right_door.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.word_label_right_door.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.word_label_right_door.setContentsMargins(5, 5, 5, 5)
        self.word_label_right_door.setFont(QFont("Arial", 9))

        # QLabel for lights status
        self.word_label_lights_status = QLabel(
            "Lights Status: {}".format(self.trainsList[0].passenger_status["lights_status"]),
            self.passenger_white_background_label
        )
        self.word_label_lights_status.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.word_label_lights_status.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.word_label_lights_status.setContentsMargins(5, 5, 5, 5)
        self.word_label_lights_status.setFont(QFont("Arial", 9))

        # QLabel for announcements
        self.word_label_announcements = QLabel(
            "Announcements: {}".format(self.trainsList[0].passenger_status["announcements"]),
            self.passenger_white_background_label
        )
        self.word_label_announcements.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.word_label_announcements.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.word_label_announcements.setContentsMargins(5, 5, 5, 5)
        self.word_label_announcements.setFont(QFont("Arial", 9))

        # QLabel for temperature
        self.word_label_temperature = QLabel(
            "Temperature: {}".format(self.trainsList[0].passenger_status["temperature"]),
            self.passenger_white_background_label
        )
        self.word_label_temperature.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.word_label_temperature.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.word_label_temperature.setContentsMargins(5, 5, 5, 5)
        self.word_label_temperature.setFont(QFont("Arial", 9))

        # QLabel for air conditioning
        self.word_label_air_conditioning = QLabel(
            "Air Conditioning: {}".format(self.trainsList[0].passenger_status["air_conditioning"]),
            self.passenger_white_background_label
        )
        self.word_label_air_conditioning.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.word_label_air_conditioning.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.word_label_air_conditioning.setContentsMargins(5, 5, 5, 5)
        self.word_label_air_conditioning.setFont(QFont("Arial", 9))

        # QLabel for advertisements
        self.word_label_advertisements = QLabel(
            "Advertisements: {}".format(self.trainsList[0].passenger_status["advertisements"]),
            self.passenger_white_background_label
        )
        self.word_label_advertisements.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.word_label_advertisements.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.word_label_advertisements.setContentsMargins(5, 5, 5, 5)
        self.word_label_advertisements.setFont(QFont("Arial", 9))

        # Add QLabel widgets to layout
        self.passenger_white_background_layout.addWidget(
            self.word_label_passengers, alignment=Qt.AlignTop
        )

        self.passenger_white_background_layout.addWidget(
            self.word_label_passenger_limit, alignment=Qt.AlignTop
        )

        self.passenger_white_background_layout.addWidget(
            self.word_label_left_door, alignment=Qt.AlignTop
        )

        self.passenger_white_background_layout.addWidget(
            self.word_label_right_door, alignment=Qt.AlignTop
        )

        self.passenger_white_background_layout.addWidget(
            self.word_label_lights_status, alignment=Qt.AlignTop
        )

        self.passenger_white_background_layout.addWidget(
            self.word_label_announcements, alignment=Qt.AlignTop
        )

        self.passenger_white_background_layout.addWidget(
            self.word_label_temperature, alignment=Qt.AlignTop
        )

        self.passenger_white_background_layout.addWidget(
            self.word_label_air_conditioning, alignment=Qt.AlignTop
        )

        self.passenger_white_background_layout.addWidget(
            self.word_label_advertisements, alignment=Qt.AlignTop
        )

        # Add stretch
        self.passenger_white_background_layout.addStretch(1)
        
        # self.passenger_status = {}
        # self.passenger_labels = []

        # # Check if the selected train exists in the trains dictionary
        # if self.selected_train_name in self.trains.trains:
        #     train_data = self.trains.trains[self.selected_train_name]
        #     self.passenger_status = train_data.get("passenger_status", {})

        #     # Create and add QLabel widgets for each word in the layout in passenger status
        #     for word_placeholders in self.passenger_word_list:
        #         word_key = (
        #             word_placeholders.split(":")[0].strip().lower().replace(" ", "_")
        #         )
        #         word_value = self.passenger_status.get(word_key, "N/A")

        #         # Create the QLabel widget
        #         if (
        #             "{}" in word_placeholders
        #             and "{}" in word_placeholders[word_placeholders.find("{}") + 2 :]
        #         ):
        #             word = word_placeholders.format(
        #                 self.selected_train_name, word_value
        #             )
        #         else:
        #             word = word_placeholders.format(word_value)

        #         self.word_label = QLabel(word, self.passenger_white_background_label)
        #         self.word_label.setStyleSheet(
        #             "color: #000000; background-color: transparent; border: none;"
        #         )
        #         self.word_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        #         self.word_label.setContentsMargins(5, 5, 5, 5)
        #         self.word_label.setFont(QFont("Arial", 9))

        #         self.passenger_labels.append(self.word_label)

        #         self.passenger_white_background_layout.addWidget(
        #             self.word_label, alignment=Qt.AlignTop
        #         )

        # self.passenger_white_background_layout.addStretch(1)

        # Create the title label
        self.passenger_title_label = QLabel("Passenger Status:", self.passenger_label)
        self.font = QFont()
        self.font.setPointSize(14)
        self.font.setBold(True)
        self.passenger_title_label.setFont(self.font)
        self.passenger_title_label.setStyleSheet(
            "color: #FFFFFF; background-color: transparent;"
        )
        self.passenger_title_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.passenger_title_label.setGeometry(
            QRect(
                0,
                0,
                self.passenger_background_widget.width(),
                self.passenger_background_widget.height(),
            )
        )

        """ Navigation Status """

        # Create a QLabel for the Navigation status
        self.navigation_label = QLabel(self.bodyBlock)
        self.navigation_label.setGeometry(QRect(500, 550, 350, 300))
        self.navigation_label.setStyleSheet("margin: 10px; padding: 0px; border: none;")

        # Create a container widget for the blue and white backgrounds for navigation status
        self.navigation_background_widget = QWidget(self.navigation_label)
        self.navigation_background_widget.setGeometry(QRect(0, 0, 350, 50))
        self.navigation_background_widget.setStyleSheet(
            "background-color: #007BFF; border: 2px solid #000000; border-radius: 5px;"
        )

        # Create a layout for the blue and white background widget for navigation status
        self.navigation_background_layout = QVBoxLayout(
            self.navigation_background_widget
        )
        self.navigation_background_layout.setContentsMargins(0, 0, 0, 0)
        self.navigation_background_layout.setSpacing(0)

        # Create a QLabel for the white background below the blue for navigation status
        self.navigation_white_background_label = QLabel(self.bodyBlock)
        self.navigation_white_background_label.setGeometry(QRect(500, 580, 350, 300))
        self.navigation_white_background_label.setStyleSheet(
            "background-color: #FFFFFF; margin: 10px; padding: 10px; border: 2px solid #000000; border-radius: 5px;"
        )

        # Create a layout for the white background below the blue header for navigation status
        self.navigation_white_background_layout = QVBoxLayout(
            self.navigation_white_background_label
        )
        self.navigation_white_background_layout.setContentsMargins(5, 5, 5, 5)
        self.navigation_white_background_layout.setSpacing(10)

        # Create QLabel widgets for the list of words
        self.navigation_word_list = [
            "Authority: {}",
            "Beacon: {}",
            "Block Length: {}",
            "Block Grade: {}",
            "Next Station: {}",
            "Previous Station: {}",
            "Headlights: {}",
            "Passenger Emergency Brake: {}",
        ]

        # QLabel for authority
        self.word_label_authority = QLabel(
            "Authority: {}".format(self.trainsList[0].navigation_status["authority"]),
            self.navigation_white_background_label
        )
        self.word_label_authority.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.word_label_authority.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.word_label_authority.setContentsMargins(5, 5, 5, 5)
        self.word_label_authority.setFont(QFont("Arial", 9))

        # QLabel for beacon
        self.word_label_beacon = QLabel(
            "Beacon: {}".format(self.trainsList[0].navigation_status["beacon"]),
            self.navigation_white_background_label
        )
        self.word_label_beacon.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.word_label_beacon.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.word_label_beacon.setContentsMargins(5, 5, 5, 5)
        self.word_label_beacon.setFont(QFont("Arial", 9))

        # QLabel for block length
        self.word_label_block_length = QLabel(
            "Block Length: {}".format(self.trainsList[0].navigation_status["block_length"]),
            self.navigation_white_background_label
        )
        self.word_label_block_length.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.word_label_block_length.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.word_label_block_length.setContentsMargins(5, 5, 5, 5)
        self.word_label_block_length.setFont(QFont("Arial", 9))

        # QLabel for block grade
        self.word_label_block_grade = QLabel(
            "Block Grade: {}".format(self.trainsList[0].navigation_status["block_grade"]),
            self.navigation_white_background_label
        )
        self.word_label_block_grade.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.word_label_block_grade.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.word_label_block_grade.setContentsMargins(5, 5, 5, 5)
        self.word_label_block_grade.setFont(QFont("Arial", 9))

        # QLabel for next station
        self.word_label_next_station = QLabel(
            "Next Station: {}".format(self.trainsList[0].navigation_status["next_station"]),
            self.navigation_white_background_label
        )
        self.word_label_next_station.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.word_label_next_station.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.word_label_next_station.setContentsMargins(5, 5, 5, 5)
        self.word_label_next_station.setFont(QFont("Arial", 9))

        # QLabel for prev station
        self.word_label_prev_station = QLabel(
            "Previous Station: {}".format(self.trainsList[0].navigation_status["prev_station"]),
            self.navigation_white_background_label
        )
        self.word_label_prev_station.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.word_label_prev_station.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.word_label_prev_station.setContentsMargins(5, 5, 5, 5)
        self.word_label_prev_station.setFont(QFont("Arial", 9))

        # QLabel for headlights
        self.word_label_headlights = QLabel(
            "Headlights: {}".format(self.trainsList[0].navigation_status["headlights"]),
            self.navigation_white_background_label
        )
        self.word_label_headlights.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.word_label_headlights.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.word_label_headlights.setContentsMargins(5, 5, 5, 5)
        self.word_label_headlights.setFont(QFont("Arial", 9))

        # QLabel for passenger emergency brake
        self.word_label_pass_emergency_brake = QLabel(
            "Passenger Emergency Brake: {}".format(self.trainsList[0].navigation_status["passenger_emergency_brake"]),
            self.navigation_white_background_label
        )
        self.word_label_pass_emergency_brake.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.word_label_pass_emergency_brake.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.word_label_pass_emergency_brake.setContentsMargins(5, 5, 5, 5)
        self.word_label_pass_emergency_brake.setFont(QFont("Arial", 9))

        # Add QLabel widgets to layout
        self.navigation_white_background_layout.addWidget(
            self.word_label_authority, alignment=Qt.AlignTop
        )

        self.navigation_white_background_layout.addWidget(
            self.word_label_beacon, alignment=Qt.AlignTop
        )

        self.navigation_white_background_layout.addWidget(
            self.word_label_block_length, alignment=Qt.AlignTop
        )

        self.navigation_white_background_layout.addWidget(
            self.word_label_block_grade, alignment=Qt.AlignTop
        )

        self.navigation_white_background_layout.addWidget(
            self.word_label_next_station, alignment=Qt.AlignTop
        )

        self.navigation_white_background_layout.addWidget(
            self.word_label_prev_station, alignment=Qt.AlignTop
        )

        self.navigation_white_background_layout.addWidget(
            self.word_label_headlights, alignment=Qt.AlignTop
        )

        self.navigation_white_background_layout.addWidget(
            self.word_label_pass_emergency_brake, alignment=Qt.AlignTop
        )

        # Add stretch
        self.navigation_white_background_layout.addStretch(1)
        
        # self.navigation_status = {}
        # self.navigation_labels = []

        # # Check if the selected train exists in the trains dictionary
        # if self.selected_train_name in self.trains.trains:
        #     train_data = self.trains.trains[self.selected_train_name]
        #     navigation_status = train_data.get("navigation_status", {})

        #     # Create and add QLabel widgets for each word the layout in navigation status
        #     for word_placeholders in self.navigation_word_list:
        #         word_key = (
        #             word_placeholders.split(":")[0].strip().lower().replace(" ", "_")
        #         )
        #         word_value = navigation_status.get(word_key, "N/A")

        #         # Create the QLabel widget
        #         if (
        #             "{}" in word_placeholders
        #             and "{}" in word_placeholders[word_placeholders.find("{}") + 2 :]
        #         ):
        #             word = word_placeholders.format(
        #                 self.selected_train_name, word_value
        #             )
        #         else:
        #             word = word_placeholders.format(word_value)

        #         self.word_label = QLabel(word, self.navigation_white_background_label)
        #         self.word_label.setStyleSheet(
        #             "color: #000000; background-color: transparent; border: none;"
        #         )
        #         self.word_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        #         self.word_label.setContentsMargins(5, 5, 5, 5)
        #         self.word_label.setFont(QFont("Arial", 9))

        #         self.navigation_labels.append(self.word_label)

        #         self.navigation_white_background_layout.addWidget(
        #             self.word_label, alignment=Qt.AlignTop
        #         )

        # self.navigation_white_background_layout.addStretch(1)

        # Create the title label
        self.navigation_title_label = QLabel(
            "Navigation Status:", self.navigation_label
        )
        self.font = QFont()
        self.font.setPointSize(14)
        self.font.setBold(True)
        self.navigation_title_label.setFont(self.font)
        self.navigation_title_label.setStyleSheet(
            "color: #FFFFFF; background-color: transparent;"
        )
        self.navigation_title_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.navigation_title_label.setGeometry(
            QRect(
                0,
                0,
                self.navigation_background_widget.width(),
                self.navigation_background_widget.height(),
            )
        )

    def update_failure_status(self, train_name, key, state):
        # Sets the value of the dictionary value for the failure variables
        self.trains.set_value(train_name, "failure_status", key, state)

    def update_ui(self):
        word_value = {}
        if self.vehicle_word_list:
            # Update each UI element with the corresponding variable from the SharedData dictionary class
            for i, word_placeholders in enumerate(self.vehicle_word_list):
                word_key = (
                    word_placeholders.split(":")[0].strip().lower().replace(" ", "_")
                )

                label_text = word_placeholders.format(word_value)

                # Update the text of the QLabel
                self.vehicle_labels[i].setText(label_text)

        if self.passenger_word_list:
            for i, word_placeholders in enumerate(self.passenger_word_list):
                word_key = (
                    word_placeholders.split(":")[0].strip().lower().replace(" ", "_")
                )

                label_text = word_placeholders.format(word_value)

                # Update the text of the QLabel
                self.passenger_labels[i].setText(label_text)

        if self.navigation_word_list:
            for i, word_placeholders in enumerate(self.navigation_word_list):
                word_key = (
                    word_placeholders.split(":")[0].strip().lower().replace(" ", "_")
                )

                label_text = word_placeholders.format(word_value)

                # Update the text of the QLabel
                self.navigation_labels[i].setText(label_text)

    def signal_period(self, period):
        self.time_interval = period

    def update(self):
        # system time
        # self.sysTime = self.sysTime.addSecs(1)
        masterSignals.timingMultiplier.connect(self.signal_period)
        masterSignals.clockSignal.connect(self.sysTime.setTime)

        self.timer.setInterval(self.time_interval)

        self.systemTimeInput.setText(self.sysTime.toString("HH:mm:ss"))
        self.systemSpeedInput.setText(
            "x" + format(1 / (self.time_interval / 1000), ".3f")
        )

        for trainObject in self.trainsList:
            # Update QLabel widgets with new information
            self.word_label_speed_limit.setText(
                "Speed Limit: {} mph".format(trainObject.vehicle_status["speed_limit"])
            )

            self.word_label_current_speed.setText(
                "Current Speed: {} mph".format(trainObject.vehicle_status["current_speed"])
            )

            self.word_label_setpoint_speed.setText(
                "Setpoint Speed: {} mph".format(trainObject.vehicle_status["setpoint_speed"])
            )

            self.word_label_commanded_speed.setText(
                "Commanded Speed: {} mph".format(trainObject.vehicle_status["commanded_speed"])
            )
            
            self.word_label_acceleration.setText(
                "Acceleration: {} ft/s".format(trainObject.vehicle_status["acceleration"])
            )

            self.word_label_brakes.setText(
                "Brakes: {}".format(trainObject.vehicle_status["brakes"])
            )
            
            self.word_label_power.setText(
                "Power: {} kW".format(trainObject.vehicle_status["power"])
            )

            self.word_label_power_limit.setText(
                "Power Limit: {} kW".format(trainObject.vehicle_status["power_limit"])
            )

            self.word_label_engine_failure.setText(
                "Engine Failure: {}".format(self.trainsList[0].failure_status["engine_failure"])
            )

            self.word_label_signal_pickup_failure.setText(
                "Signal Pickup Failure: {}".format(self.trainsList[0].failure_status["signal_pickup_failure"])
            )

            self.word_label_brake_failure.setText(
                "Brake Failure: {}".format(self.trainsList[0].failure_status["brake_failure"])
            )

            self.word_label_emergency_brake.setText(
                "Emergency Brake: {}".format(self.trainsList[0].failure_status["emergency_brake"])
            )

            self.word_label_passengers.setText(
                "Power Limit: {} kW".format(trainObject.vehicle_status["power_limit"])
            )

            self.word_label_power_limit.setText(
                "Passenger Limit: {}".format(trainObject.passenger_status["passenger_limit"])
            )

            self.word_label_left_door.setText(
                "Left Door: {}".format(trainObject.passenger_status["left_door"])
            )

            self.word_label_right_door.setText(
                "Right Door: {}".format(trainObject.passenger_status["right_door"])
            )

            self.word_label_lights_status.setText(
                "Lights Status: {}".format(trainObject.passenger_status["lights_status"])
            )

            self.word_label_announcements.setText(
                "Announcements: {}".format(trainObject.passenger_status["announcements"])
            )

            self.word_label_temperature.setText(
                "Temperature: {}".format(trainObject.passenger_status["temperature"])
            )

            self.word_label_air_conditioning.setText(
                "Air Conditioning: {}".format(trainObject.passenger_status["air_conditioning"])
            )

            self.word_label_advertisements.setText(
                "Advertisements: {}".format(trainObject.passenger_status["advertisements"])
            )

            self.word_label_authority.setText(
                "Authority: {}".format(trainObject.navigation_status["authority"])
            )

            self.word_label_beacon.setText(
                "Beacon: {}".format(trainObject.navigation_status["beacon"])
            )

            self.word_label_block_length.setText(
                "Block Length: {}".format(trainObject.navigation_status["block_length"])
            )

            self.word_label_block_grade.setText(
                "Block Grade: {}".format(trainObject.navigation_status["block_grade"])
            )

            self.word_label_next_station.setText(
                "Next Station: {}".format(trainObject.navigation_status["next_station"])
            )

            self.word_label_prev_station.setText(
                "Previous Station: {}".format(trainObject.navigation_status["prev_station"])
            )

            self.word_label_headlights.setText(
                "Headlights: {}".format(trainObject.navigation_status["headlights"])
            )

            self.word_label_pass_emergency_brake.setText(
                "Passenger Emergency Brake: {}".format(trainObject.navigation_status["passenger_emergency_brake"])
            )





class TrainTest(QMainWindow):
    # Font variables
    textFontSize = 10
    labelFontSize = 12
    headerFontSize = 16
    titleFontSize = 22
    fontStyle = "Product Sans"

    # Color variables
    colorDarkBlue = "#085394"
    colorLightRed = "#EA9999"
    colorLightBlue = "#9FC5F8"
    colorLightGrey = "#CCCCCC"
    colorMediumGrey = "#DDDDDD"
    colorDarkGrey = "#666666"
    colorBlack = "#000000"

    # Dimensions
    w = 960
    h = 960
    moduleName = "Train Test"
    
    def __init__(self):
        super().__init__()
        self.test_train = TrainModelAttributes(trainID="Test_Train")
        
        self.time_interval = 1
        self.timer = QTimer(self)
        self.timer.timeout.connect(
            self.update
        )  # Connect the timer to the update_text function
        self.timer.start(
            self.time_interval
        )  # Update the text every 1000 milliseconds (1 second)

        self.sysTime = QDateTime.currentDateTime()
        self.sysTime.setTime(QTime(0, 0, 0))

        """ Header Template """

        # Setting title
        self.setWindowTitle(self.moduleName)

        # Setting goemetry
        self.setGeometry(50, 50, self.w, self.h)

        # Body block
        self.bodyBlock = QLabel(self)
        self.bodyBlock.setGeometry(20, 20, 920, 920)
        self.bodyBlock.setStyleSheet(
            "background-color: white;" "border: 1px solid black"
        )

        # Header block
        self.headerBlock = QLabel(self)
        self.headerBlock.setGeometry(20, 20, 920, 70)
        self.headerBlock.setStyleSheet(
            "background-color:" + self.colorDarkBlue + ";" "border: 1px solid black"
        )

        # Title
        self.titleLabel = QLabel("Train Test", self)
        self.titleLabel.setFont(QFont(self.fontStyle, self.titleFontSize))
        self.titleLabel.setAlignment(Qt.AlignCenter)
        title_width = 400
        title_height = 50
        title_x = (self.width() - title_width) // 2
        title_y = 35
        self.titleLabel.setGeometry(title_x, title_y, title_width, title_height)
        self.titleLabel.setStyleSheet("color: white")

        # MTA Logo
        self.pixmapMTALogo = QtGui.QPixmap("src/main/TrainModel/MTA_Logo.png")
        self.pixmapMTALogo = self.pixmapMTALogo.scaled(70, 70)
        self.logo = QLabel(self)
        self.logo.setPixmap(self.pixmapMTALogo)
        self.logo.move(20, 20)
        self.logo.adjustSize()

        # Module
        self.moduleLabel = QLabel("Train Test", self)
        self.moduleLabel.setFont(QFont(self.fontStyle, self.headerFontSize))
        self.moduleLabel.setAlignment(Qt.AlignCenter)
        self.moduleLabel.move(30, 100)
        self.moduleLabel.adjustSize()
        self.moduleLabel.setStyleSheet("color:" + self.colorDarkBlue)

        # Test bench icon
        self.pixmapGear = QtGui.QPixmap("src/main/TrainModel/gear_icon.png")
        self.pixmapGear = self.pixmapGear.scaled(25, 25)
        self.testbenchIcon = QLabel(self)
        self.testbenchIcon.setPixmap(self.pixmapGear)
        self.testbenchIcon.setGeometry(30, 140, 32, 32)

        # Test bench button
        self.testbenchButton = QPushButton("Test Bench", self)
        self.testbenchButton.setFont(QFont(self.fontStyle, self.textFontSize))
        self.testbenchButton.setGeometry(60, 140, 100, 32)
        self.testbenchButton.setStyleSheet(
            "color:" + self.colorDarkBlue + ";border: 1px solid white"
        )

        # System time input
        self.systemTimeInput = QLabel("00:00:00", self)
        self.systemTimeInput.setFont(QFont(self.fontStyle, self.headerFontSize))
        self.systemTimeInput.setGeometry(820, 67, 150, 100)
        self.systemTimeInput.setStyleSheet("color:" + self.colorDarkBlue)

        # System time label
        self.systemTimeLabel = QLabel("System Time:", self)
        self.systemTimeLabel.setFont(QFont(self.fontStyle, self.headerFontSize))
        self.systemTimeLabel.adjustSize()
        self.systemTimeLabel.setGeometry(650, 65, 200, 100)
        self.systemTimeLabel.setStyleSheet("color:" + self.colorDarkBlue)

        # System speed label
        self.systemSpeedLabel = QLabel("System Speed:", self)
        self.systemSpeedLabel.setFont(QFont(self.fontStyle, self.textFontSize))
        self.systemSpeedLabel.setGeometry(689, 140, 100, 100)
        self.systemSpeedLabel.adjustSize()
        self.systemSpeedLabel.setStyleSheet("color:" + self.colorDarkBlue)

        # System speed input
        self.systemSpeedInput = QLabel("x1.0", self)
        self.systemSpeedInput.setFont(QFont(self.fontStyle, self.textFontSize))
        self.systemSpeedInput.setGeometry(850, 127, 50, 50)
        self.systemSpeedInput.setStyleSheet("color:" + self.colorDarkBlue)

        # Increase system speed button
        self.pixmapFastForward = QtGui.QPixmap("src/main/TrainModel/fast-forward.svg")
        self.pixmapFastForward = self.pixmapFastForward.scaled(20, 20)
        self.speedUpButton = QPushButton(self)
        self.speedUpButton.setIcon(QtGui.QIcon(self.pixmapFastForward))
        self.speedUpButton.setGeometry(890, 143, 20, 20)
        self.speedUpButton.setStyleSheet(
            "color:" + self.colorDarkBlue + ";border: 1px solid white"
        )

        # Decrease system speed button
        self.pixmapRewind = QtGui.QPixmap("src/main/TrainModel/rewind.svg")
        self.pixmapRewind = self.pixmapRewind.scaled(20, 20)
        self.slowDownButton = QPushButton(self)
        self.slowDownButton.setIcon(QtGui.QIcon(self.pixmapRewind))
        self.slowDownButton.setGeometry(819, 143, 20, 20)
        self.slowDownButton.setStyleSheet(
            "color:" + self.colorDarkBlue + ";border: 1px solid white"
        )

        """ Drop-down Menu """

        # Calculate the position of the QComboBox
        drop_down_width = 500
        drop_down_height = 40
        drop_down_x = int((self.w - drop_down_width) // 2)
        drop_down_y = int((self.h / 2) + (self.h / 4) - (drop_down_height / 2))

        # Create the QComboBox
        self.comboBox = QComboBox(self.bodyBlock)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.setGeometry(
            QRect(drop_down_x, drop_down_y, drop_down_width, drop_down_height)
        )
        font1 = QFont(self.fontStyle)
        font1.setPointSize(18)
        font1.setKerning(True)
        self.comboBox.setFont(font1)

        # Populate the combo box with the train ID
        self.populate_train_id()

        # Connect the combo box signal to the method that handles the selection change
        self.comboBox.currentIndexChanged.connect(self.handle_train_selection)

        # Create a search icon for new window
        self.search_button = QtGui.QPixmap("src/main/TrainModel/search_icon.png")
        self.search_button = self.search_button.scaled(40, 40)
        self.icon = QLabel(self)
        self.icon.setPixmap(self.search_button)
        self.icon.setGeometry(QRect(750, 720, 40, 40))
        self.icon.adjustSize()

        # Insert Train Image to main window
        image_path = "src/main/TrainModel/Train_Image.jpg"
        pixmap_train = QPixmap(image_path)
        image_width = 500
        image_height = 400
        image_y = drop_down_y - image_height - 20
        pixmap_train = pixmap_train.scaled(image_width, image_height)
        train_image_label = QLabel(self.bodyBlock)
        train_image_label.setPixmap(pixmap_train)
        train_image_label.setGeometry(drop_down_x, image_y, image_width, image_height)

        # Create a search icon for new window
        self.search_button = QtGui.QPixmap("src/main/TrainModel/search_icon.png")
        self.search_button = self.search_button.scaled(40, 40)
        self.icon = QLabel(self)
        self.icon.setPixmap(self.search_button)
        self.icon.setGeometry(QRect(750, 720, 40, 40))
        self.icon.adjustSize()

        # Track Model Test button
        self.pushButton = QPushButton("Track Model", self.bodyBlock)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setGeometry(230, 750, 125, 100)
        self.pushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton.setAutoRepeatInterval(105)
        self.pushButton.clicked.connect(self.show_track_model_test)

        # Applying style to Track Model button
        self.pushButton.setStyleSheet("""
            QPushButton#pushButton {
                background-color: lightgray;  /* Set the background color */
                border: 2px solid black;  /* Set the border */
                border-radius: 5px;  /* Set the border radius for rounded corners */
                padding: 5px 10px;  /* Set padding for content inside the button */
            }
        """)

        # Train Controller Test button
        self.pushButton2 = QPushButton("Train Controller", self.bodyBlock)
        self.pushButton2.setObjectName("pushButton")
        self.pushButton2.setGeometry(417, 750, 125, 100)
        self.pushButton2.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton2.setAutoRepeatInterval(105)
        self.pushButton2.clicked.connect(self.show_train_controller_test)

        # Applying style to Train Controller button
        self.pushButton2.setStyleSheet("""
            QPushButton#pushButton {
                background-color: lightgray;  /* Set the background color */
                border: 2px solid black;  /* Set the border */
                border-radius: 5px;  /* Set the border radius for rounded corners */
                padding: 5px 10px;  /* Set padding for content inside the button */
            }
        """)

        # Murphy Test button
        self.pushButton3 = QPushButton("Murphy Test", self.bodyBlock)
        self.pushButton3.setObjectName("pushButton")
        self.pushButton3.setGeometry(605, 750, 125, 100)
        self.pushButton3.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton3.setAutoRepeatInterval(105)
        self.pushButton3.clicked.connect(self.show_murphy_test)

        # Applying style to Train Controller button
        self.pushButton3.setStyleSheet("""
            QPushButton#pushButton {
                background-color: lightgray;  /* Set the background color */
                border: 2px solid black;  /* Set the border */
                border-radius: 5px;  /* Set the border radius for rounded corners */
                padding: 5px 10px;  /* Set padding for content inside the button */
            }
        """)

    def show_gui(self):
        self.show()

    def populate_train_id(self):
        # Clear any exisiting items in the combo box
        self.comboBox.clear()

        # Add the single train ID to the combo box
        self.comboBox.addItem(self.test_train.calculations["trainID"])

    def handle_train_selection(self):
        selected_train_id = self.test_train.calculations["trainID"]
        selected_train_attributes = self.test_train

        # Pass the TrainModelAttributes instance to other classes as needed
        self.show_track_model_test(selected_train_attributes)
        self.show_train_controller_test(selected_train_attributes)
        self.show_murphy_test(selected_train_attributes)
    
    def show_track_model_test(self, train_attributes):
        self.track_model_test = TrackModelTestWindow(train_attributes=train_attributes)
        self.track_model_test.show()

    def show_train_controller_test(self, train_attributes):
        self.train_controller_test = TrainControllerTestWindow(train_attributes=train_attributes)
        self.train_controller_test.show()

    def show_murphy_test(self, train_attributes):
        self.murphy_test = MurphyTestWindow(train_attributes=train_attributes)
        self.murphy_test.show()


class TrackModelTestWindow(QMainWindow):
    # Font variables
    textFontSize = 10
    labelFontSize = 12
    headerFontSize = 16
    titleFontSize = 22
    fontStyle = "Product Sans"

    # Color variables
    colorDarkBlue = "#085394"
    colorLightRed = "#EA9999"
    colorLightBlue = "#9FC5F8"
    colorLightGrey = "#CCCCCC"
    colorMediumGrey = "#DDDDDD"
    colorDarkGrey = "#666666"
    colorBlack = "#000000"

    # Dimensions
    w = 960
    h = 960
    moduleName = "Track Model Test"

    def __init__(self, train_attributes):
        super().__init__()
        self.trainsList = []
        self.functionsInstance = Calculations()
        self.test_train = TrainModelAttributes(train_attributes)
        
        self.time_interval = 1
        self.timer = QTimer(self)
        self.timer.timeout.connect(
            self.update
        )  # Connect the timer to the update_text function
        self.timer.start(
            self.time_interval
        )  # Update the text every 1000 milliseconds (1 second)

        self.sysTime = QDateTime.currentDateTime()
        self.sysTime.setTime(QTime(0, 0, 0))

        """ Header Template """

        # Setting title
        self.setWindowTitle(self.moduleName)

        # Setting goemetry
        self.setGeometry(50, 50, self.w, self.h)

        # Body block
        self.bodyBlock = QLabel(self)
        self.bodyBlock.setGeometry(20, 20, 920, 920)
        self.bodyBlock.setStyleSheet(
            "background-color: white;" "border: 1px solid black"
        )

        # Header block
        self.headerBlock = QLabel(self)
        self.headerBlock.setGeometry(20, 20, 920, 70)
        self.headerBlock.setStyleSheet(
            "background-color:" + self.colorDarkBlue + ";" "border: 1px solid black"
        )

        # Title
        self.titleLabel = QLabel("Train Test", self)
        self.titleLabel.setFont(QFont(self.fontStyle, self.titleFontSize))
        self.titleLabel.setAlignment(Qt.AlignCenter)
        title_width = 400
        title_height = 50
        title_x = (self.width() - title_width) // 2
        title_y = 35
        self.titleLabel.setGeometry(title_x, title_y, title_width, title_height)
        self.titleLabel.setStyleSheet("color: white")

        # MTA Logo
        self.pixmapMTALogo = QtGui.QPixmap("src/main/TrainModel/MTA_Logo.png")
        self.pixmapMTALogo = self.pixmapMTALogo.scaled(70, 70)
        self.logo = QLabel(self)
        self.logo.setPixmap(self.pixmapMTALogo)
        self.logo.move(20, 20)
        self.logo.adjustSize()

        # Module
        self.moduleLabel = QLabel("Train Test", self)
        self.moduleLabel.setFont(QFont(self.fontStyle, self.headerFontSize))
        self.moduleLabel.setAlignment(Qt.AlignCenter)
        self.moduleLabel.move(30, 100)
        self.moduleLabel.adjustSize()
        self.moduleLabel.setStyleSheet("color:" + self.colorDarkBlue)

        # Test bench icon
        self.pixmapGear = QtGui.QPixmap("src/main/TrainModel/gear_icon.png")
        self.pixmapGear = self.pixmapGear.scaled(25, 25)
        self.testbenchIcon = QLabel(self)
        self.testbenchIcon.setPixmap(self.pixmapGear)
        self.testbenchIcon.setGeometry(30, 140, 32, 32)

        # Test bench button
        self.testbenchButton = QPushButton("Test Bench", self)
        self.testbenchButton.setFont(QFont(self.fontStyle, self.textFontSize))
        self.testbenchButton.setGeometry(60, 140, 100, 32)
        self.testbenchButton.setStyleSheet(
            "color:" + self.colorDarkBlue + ";border: 1px solid white"
        )

        # System time input
        self.systemTimeInput = QLabel("00:00:00", self)
        self.systemTimeInput.setFont(QFont(self.fontStyle, self.headerFontSize))
        self.systemTimeInput.setGeometry(820, 67, 150, 100)
        self.systemTimeInput.setStyleSheet("color:" + self.colorDarkBlue)

        # System time label
        self.systemTimeLabel = QLabel("System Time:", self)
        self.systemTimeLabel.setFont(QFont(self.fontStyle, self.headerFontSize))
        self.systemTimeLabel.adjustSize()
        self.systemTimeLabel.setGeometry(650, 65, 200, 100)
        self.systemTimeLabel.setStyleSheet("color:" + self.colorDarkBlue)

        # System speed label
        self.systemSpeedLabel = QLabel("System Speed:", self)
        self.systemSpeedLabel.setFont(QFont(self.fontStyle, self.textFontSize))
        self.systemSpeedLabel.setGeometry(689, 140, 100, 100)
        self.systemSpeedLabel.adjustSize()
        self.systemSpeedLabel.setStyleSheet("color:" + self.colorDarkBlue)

        # System speed input
        self.systemSpeedInput = QLabel("x1.0", self)
        self.systemSpeedInput.setFont(QFont(self.fontStyle, self.textFontSize))
        self.systemSpeedInput.setGeometry(850, 127, 50, 50)
        self.systemSpeedInput.setStyleSheet("color:" + self.colorDarkBlue)

        # Increase system speed button
        self.pixmapFastForward = QtGui.QPixmap("src/main/TrainModel/fast-forward.svg")
        self.pixmapFastForward = self.pixmapFastForward.scaled(20, 20)
        self.speedUpButton = QPushButton(self)
        self.speedUpButton.setIcon(QtGui.QIcon(self.pixmapFastForward))
        self.speedUpButton.setGeometry(890, 143, 20, 20)
        self.speedUpButton.setStyleSheet(
            "color:" + self.colorDarkBlue + ";border: 1px solid white"
        )

        # Decrease system speed button
        self.pixmapRewind = QtGui.QPixmap("src/main/TrainModel/rewind.svg")
        self.pixmapRewind = self.pixmapRewind.scaled(20, 20)
        self.slowDownButton = QPushButton(self)
        self.slowDownButton.setIcon(QtGui.QIcon(self.pixmapRewind))
        self.slowDownButton.setGeometry(819, 143, 20, 20)
        self.slowDownButton.setStyleSheet(
            "color:" + self.colorDarkBlue + ";border: 1px solid white"
        )

        ''' Track Model Inputs'''

        # Create a QLabel for the vehicle status window
        self.track_model_label = QLabel(self.bodyBlock)
        self.track_model_label.setGeometry(QRect(75, 170, 350, 600))
        self.track_model_label.setStyleSheet("margin: 10px; padding: 0px; border: none;")

        # Create a container widget for the blue and white backgrounds for vehicle status
        self.track_model_background_widget = QWidget(self.track_model_label)
        self.track_model_background_widget.setGeometry(QRect(0, 0, 350, 50))
        self.track_model_background_widget.setStyleSheet(
            "background-color: #007BFF; border: 2px solid #000000; border-radius: 5px;"
        )

        # Create a layout for the blue and white backgrounds for vehicle status
        self.track_model_background_layout = QVBoxLayout(self.track_model_background_widget)
        self.track_model_background_layout.setContentsMargins(0, 0, 0, 0)
        self.track_model_background_layout.setSpacing(0)

        # Create a QLabel for the white background below the blue for vehicle status
        self.track_model_white_background_label = QLabel(self.bodyBlock)
        self.track_model_white_background_label.setGeometry(QRect(75, 200, 350, 600))
        self.track_model_white_background_label.setStyleSheet(
            "background-color: #FFFFFF; margin: 10px; padding: 10px; border: 2px solid #000000; border-radius: 5px;"
        )

        # Create a layout for the white background below the blue header for vehicle status
        self.track_model_white_background_layout = QVBoxLayout(
            self.track_model_white_background_label
        )
        self.track_model_white_background_layout.setContentsMargins(5, 5, 5, 5)
        self.track_model_white_background_layout.setSpacing(0)

        # Create QLabel widgets for the list of words
        self.track_model_word_list = [
            "Speed Limit: ",
            "Authority: ",
            "Beacon: ",
            "Commanded Speed: ",
            "Passengers Entering: ",
            "Block Length: ",
            "Block Grade: ",
            "Tunnel: "
        ]

        # Create QLineEdit widgets for track model inputs
        self.track_input_line_edits = [
            QLineEdit("", self) for _ in range(len(self.track_model_word_list))
        ]
        
        # Create a list to store the horizontal layouts
        self.input_layouts = []

        for i, word in enumerate(self.track_model_word_list):
            # Create a horizontal layout for each word and its corresponding input
            input_layout = QHBoxLayout()
            input_layout.setContentsMargins(0, 0, 0, 0)
            input_layout.setSpacing(0)

            # Add QLabel for the word
            word_label = QLabel(word, self.track_model_white_background_label)
            word_label.setStyleSheet(
                "color: #000000; background-color: transparent; border: none; padding: 0; margin: 0;"
            )
            word_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            word_label.setFont(QFont("Arial", 9))

            # Add QLineEdit for the input
            line_edit = QLineEdit("", self.track_model_white_background_label)
            line_edit.setStyleSheet(
                "color: #000000; background-color: transparent; border: 2px solid #000000; border-radius: 5px; padding: 0; margin: 0;"
            )
            line_edit.setAlignment(Qt.AlignRight | Qt.AlignVCenter)  # Align the text to the right
            line_edit.setFixedHeight(word_label.height() + 10)  # Adjust the height
            line_edit.setFixedWidth(100)  # Set a fixed width (adjust as needed)
            line_edit.setFont(QFont("Arial", 9))

            # Add widgets to the horizontal layout
            input_layout.addWidget(word_label)
            input_layout.addWidget(line_edit)

            # Add the horizontal layout to the main layout
            self.track_model_white_background_layout.addLayout(input_layout)

            # Store the layout for later use if needed
            self.input_layouts.append(input_layout)

        # Create the title label for vehicle status
        self.track_model_title_label = QLabel("Track Model Test:", self.track_model_label)
        self.font = QFont()
        self.font.setPointSize(14)
        self.font.setBold(True)
        self.track_model_title_label.setFont(self.font)
        self.track_model_title_label.setStyleSheet(
            "color: #FFFFFF; background-color: transparent; border: none;"
        )
        self.track_model_title_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.track_model_title_label.setGeometry(
            QRect(
                0,
                0,
                self.track_model_background_widget.width(),
                self.track_model_background_widget.height(),
            )
        )

        ''' Train Model Outputs'''

        # Create a QLabel for the vehicle status window
        self.train_model_label = QLabel(self.bodyBlock)
        self.train_model_label.setGeometry(QRect(500, 170, 350, 600))
        self.train_model_label.setStyleSheet("margin: 10px; padding: 0px; border: none;")

        # Create a container widget for the blue and white backgrounds for vehicle status
        self.train_model_background_widget = QWidget(self.train_model_label)
        self.train_model_background_widget.setGeometry(QRect(0, 0, 350, 50))
        self.train_model_background_widget.setStyleSheet(
            "background-color: #007BFF; border: 2px solid #000000; border-radius: 5px;"
        )

        # Create a layout for the blue and white backgrounds for vehicle status
        self.train_model_background_layout = QVBoxLayout(self.train_model_background_widget)
        self.train_model_background_layout.setContentsMargins(0, 0, 0, 0)
        self.train_model_background_layout.setSpacing(0)

        # Create a QLabel for the white background below the blue for vehicle status
        self.train_model_white_background_label = QLabel(self.bodyBlock)
        self.train_model_white_background_label.setGeometry(QRect(500, 200, 350, 600))
        self.train_model_white_background_label.setStyleSheet(
            "background-color: #FFFFFF; margin: 10px; padding: 10px; border: 2px solid #000000; border-radius: 5px;"
        )

        # Create a layout for the white background below the blue header for vehicle status
        self.train_model_white_background_layout = QVBoxLayout(
            self.train_model_white_background_label
        )
        self.train_model_white_background_layout.setContentsMargins(5, 5, 5, 5)
        self.train_model_white_background_layout.setSpacing(0)

        # Create a dictionary to store QLineEdit widgets for track model inputs
        self.track_input_line_edits = {}
        
        # Create QLabel widgets for the list of words
        self.train_model_word_list = [
            "Speed Limit: {}",
            "Current Speed: {}",
            "Authority: {}",
            "Commanded Speed: {}",
            "Block Length: {}",
            "Temperature: {}",
            "Passenger Emergency Brake: {}",
            "Engine Failure: {}",
            "Signal Pickup Failure: {}",
            "Brake Failure: {}"
        ]

        # Iterate through the list of words and create corresponding widgets
        for word in self.train_model_word_list:
            # Create a QLineEdit widget
            line_edit = QLineEdit("", self.train_model_white_background_label)
            line_edit.setStyleSheet(
                "color: #000000; background-color: transparent; border: 2px solid #000000; border-radius: 5px;"
            )
            line_edit.setAlignment(Qt.AlignRight | Qt.AlignVCenter)  # Align the text to the right
            line_edit.setFixedHeight(20)  # Set the same height as the label (adjust as needed)
            line_edit.setFixedWidth(100)  # Set a fixed width (adjust as needed)
            line_edit.setFont(QFont("Arial", 9))

            # Add QLineEdit widgets to the dictionary with the corresponding word as the key
            self.track_input_line_edits[word] = line_edit
        
        
        # QLabel for speed limit
        self.train_model_label_speed_limit = QLabel(
            "Speed Limit: {}".format(self.test_train.vehicle_status["speed_limit"]),
            self.train_model_white_background_label
        )
        self.train_model_label_speed_limit.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.train_model_label_speed_limit.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.train_model_label_speed_limit.setContentsMargins(0, 0, 0, 0)
        self.train_model_label_speed_limit.setFont(QFont("Arial", 9))

        # QLabel for current speed
        self.train_model_label_current_speed = QLabel(
            "Current Speed: {}".format(self.test_train.vehicle_status["current_speed"]),
            self.train_model_white_background_label
        )
        self.train_model_label_current_speed.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.train_model_label_current_speed.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.train_model_label_current_speed.setContentsMargins(0, 0, 0, 0)
        self.train_model_label_current_speed.setFont(QFont("Arial", 9))

        # QLabel for authority
        self.train_model_label_authority = QLabel(
            "Authority: {}".format(self.test_train.navigation_status["authority"]),
            self.train_model_white_background_label
        )
        self.train_model_label_authority.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.train_model_label_authority.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.train_model_label_authority.setContentsMargins(0, 0, 0, 0)
        self.train_model_label_authority.setFont(QFont("Arial", 9))

        # QLabel for commanded speed
        self.train_model_label_commanded_speed = QLabel(
            "Commanded Speed: {}".format(self.test_train.vehicle_status["commanded_speed"]),
            self.train_model_white_background_label
        )
        self.train_model_label_commanded_speed.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.train_model_label_commanded_speed.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.train_model_label_commanded_speed.setContentsMargins(0, 0, 0, 0)
        self.train_model_label_commanded_speed.setFont(QFont("Arial", 9))

        # QLabel for block length
        self.train_model_label_block_length = QLabel(
            "Block Length: {}".format(self.test_train.navigation_status["block_length"]),
            self.train_model_white_background_label
        )
        self.train_model_label_block_length.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.train_model_label_block_length.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.train_model_label_block_length.setContentsMargins(0, 0, 0, 0)
        self.train_model_label_block_length.setFont(QFont("Arial", 9))

        # QLabel for temperature
        self.train_model_label_temperature = QLabel(
            "Temperature: {}".format(self.test_train.passenger_status["temperature"]),
            self.train_model_white_background_label
        )
        self.train_model_label_temperature.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.train_model_label_temperature.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.train_model_label_temperature.setContentsMargins(0, 0, 0, 0)
        self.train_model_label_temperature.setFont(QFont("Arial", 9))

        # QLabel for passenger emergency brake
        self.train_model_label_passenger_emergency_brake = QLabel(
            "Passenger Emergency Brake: {}".format(self.test_train.navigation_status["passenger_emergency_brake"]),
            self.train_model_white_background_label
        )
        self.train_model_label_passenger_emergency_brake.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.train_model_label_passenger_emergency_brake.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.train_model_label_passenger_emergency_brake.setContentsMargins(0, 0, 0, 0)
        self.train_model_label_passenger_emergency_brake.setFont(QFont("Arial", 9))

        # QLabel for engine failure
        self.train_model_label_engine_failure = QLabel(
            "Engine Failure: {}".format(self.test_train.failure_status["engine_failure"]),
            self.train_model_white_background_label
        )
        self.train_model_label_engine_failure.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.train_model_label_engine_failure.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.train_model_label_engine_failure.setContentsMargins(0, 0, 0, 0)
        self.train_model_label_engine_failure.setFont(QFont("Arial", 9))

        # QLabel for signal pickup failure
        self.train_model_label_signal_pickup_failure = QLabel(
            "Signal Pickup Failure: {}".format(self.test_train.failure_status["signal_pickup_failure"]),
            self.train_model_white_background_label
        )
        self.train_model_label_signal_pickup_failure.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.train_model_label_signal_pickup_failure.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.train_model_label_signal_pickup_failure.setContentsMargins(0, 0, 0, 0)
        self.train_model_label_signal_pickup_failure.setFont(QFont("Arial", 9))

        # QLabel for brake failure
        self.train_model_label_brake_failure = QLabel(
            "Brake Failure: {}".format(self.test_train.failure_status["brake_failure"]),
            self.train_model_white_background_label
        )
        self.train_model_label_brake_failure.setStyleSheet(
            "color: #000000; background-color: transparent; border: none;"
        )
        self.train_model_label_brake_failure.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.train_model_label_brake_failure.setContentsMargins(0, 0, 0, 0)
        self.train_model_label_brake_failure.setFont(QFont("Arial", 9))

        # Add QLabel widgets to layout
        self.train_model_white_background_layout.addWidget(
            self.train_model_label_speed_limit, alignment=Qt.AlignTop
        )

        # Add QLabel widgets to layout
        self.train_model_white_background_layout.addWidget(
            self.train_model_label_current_speed, alignment=Qt.AlignTop
        )

        # Add QLabel widgets to layout
        self.train_model_white_background_layout.addWidget(
            self.train_model_label_authority, alignment=Qt.AlignTop
        )

        # Add QLabel widgets to layout
        self.train_model_white_background_layout.addWidget(
            self.train_model_label_commanded_speed, alignment=Qt.AlignTop
        )

        # Add QLabel widgets to layout
        self.train_model_white_background_layout.addWidget(
            self.train_model_label_block_length, alignment=Qt.AlignTop
        )

        # Add QLabel widgets to layout
        self.train_model_white_background_layout.addWidget(
            self.train_model_label_temperature, alignment=Qt.AlignTop
        )

        # Add QLabel widgets to layout
        self.train_model_white_background_layout.addWidget(
            self.train_model_label_passenger_emergency_brake, alignment=Qt.AlignTop
        )

        # Add QLabel widgets to layout
        self.train_model_white_background_layout.addWidget(
            self.train_model_label_engine_failure, alignment=Qt.AlignTop
        )

        # Add QLabel widgets to layout
        self.train_model_white_background_layout.addWidget(
            self.train_model_label_signal_pickup_failure, alignment=Qt.AlignTop
        )

        # Add QLabel widgets to layout
        self.train_model_white_background_layout.addWidget(
            self.train_model_label_brake_failure, alignment=Qt.AlignTop
        )

        # Create and configure "Apply" button
        self.apply_button = QPushButton("Apply", self.bodyBlock)
        self.apply_button.setObjectName("Apply button")
        self.apply_button.setGeometry(800, 850, 100, 50)
        self.apply_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.apply_button.setAutoRepeatInterval(105)
        self.apply_button.clicked.connect(self.apply_changes)

        



    def map_word_to_attribute(self, word):
        # Implement a mapping function based on your naming convention
        # This is a simplified example; adjust it to your specific case
        word_mapping = {
            "Speed Limit: {}": ("vehicle_status", "speed_limit"),
            "Current Speed: {}": ("vehicle_status", "currVelocity"),
            "Authority: {}": ("navigation_status", "authority"),
            # ... add more mappings as needed
        }
        return word_mapping.get(word, (None, None))

    def apply_changes(self):
        # Iterate through the QLineEdit widgets and update the attributes
        for word, line_edit in self.track_input_line_edits.items():
            value = line_edit.text()

            # Get the attribute name and dictionary directly
            dictionary, attribute_name = self.map_word_to_attribute(word)

            # Check if the value is numeric before updating the attribute
            if dictionary and attribute_name:
                if value.isnumeric():
                    self.test_train[dictionary][attribute_name] = int(value)
                else:
                    self.test_train[dictionary][attribute_name] = value

        # Update the UI to reflect the changes
        self.update_train_model_ui()


    def update_train_model_ui(self):
        # Update QLabel widgets with the values from the dictionary
        for label, word in zip(self.train_model_labels, self.train_model_word_list):
            label.setText("{}: {}".format(word, self.test_train[word.lower()]))

    def set_calculation_attribute(self, attribute, value):
        # Ensure that attribute is a string
        if not isinstance(attribute, str):
            print("Error: 'attribute' must be a string.")
            return

        # Check if the attribute exists in calculations
        if attribute in self.calculations:
            self.test_train[attribute] = value
        else:
            print(f"Error: '{attribute}' is not a valid calculation attribute.")
            

        
    # def apply_values(self):
    #     values_wordlist_1 = {}

    #     # Iterate through the input text boxes and update values_wordlist_1
    #     for word_placeholder, value_input in self.value_inputs.items():
    #         input_value = value_input.text()
    #         if input_value:
    #             try:
    #                 # Try to convert the input to an integer
    #                 input_value = int(input_value)
    #             except ValueError:
    #                 pass  # If it's not a valid integer, keep it as a string
    #             values_wordlist_1[word_placeholder] = input_value

    #     # Update the corresponding output values based on the mappings
    #     for word_placeholder, output_key in self.mapping.items():
    #         if word_placeholder in values_wordlist_1:
    #             self.values_2[output_key] = values_wordlist_1[word_placeholder]
    #             # Update the corresponding text box in the second set
    #             self.update_wordlist2_textbox(
    #                 output_key, values_wordlist_1[word_placeholder]
    #             )

    #     return values_wordlist_1

    # def reset_values(self):
    #     default_values_wordlist_2 = {
    #         "Speed Limit": "45 mph",
    #         "Authority": "5 Blocks",
    #         "Commanded Speed": "35 mph",
    #         "Current Speed": "32 mph",
    #         "Temperature": "75 ℉",
    #         "Passengers Currently": "60",
    #         "Max Passengers": "74",
    #         "Next Station": "Block 9",
    #         "Previous Station": "Block 5",
    #         "Engine Failure": False,
    #         "Signal Pickup Failure": True,
    #         "Brake Failure": False,
    #         "Power": "80 kW",
    #         "Passenger Emergency Brake": "Off",
    #     }

    #     for i, (word_placeholder, value) in enumerate(
    #         zip(self.word_list_2, default_values_wordlist_2.values())
    #     ):
    #         label_text = f"{word_placeholder} {value}" if word_placeholder else value
    #         self.word_labels[i].setText(label_text)

    # def update_wordlist2_values(self):
    #     values_wordlist_1 = self.apply_values()

    #     for i, word_placeholder in enumerate(self.word_list_2):
    #         if word_placeholder in self.values_2:
    #             label = self.values_2[word_placeholder]

    #             # Check if there is a corresponding label in word list 1
    #             corresponding_label = self.get_corresponding_label(word_placeholder)

    #             if corresponding_label:
    #                 # Get the value from word list 1 and format the label
    #                 value = values_wordlist_1.get(corresponding_label, "")
    #                 label = f"{word_placeholder} {value}"

    #             self.word_labels[i].setText(label)

    # def get_corresponding_label(self, label_wordlist2):
    #     # Define a mapping between word list 2 labels and their corresponding word list 1 labels
    #     label_mapping = {
    #         "Speed Limit:": "Speed Limit:",
    #         "Authority:": "Authority:",
    #     }

    #     # Get the corresponding label from the mapping
    #     return label_mapping.get(label_wordlist2, "")

    # def update_clock_label(self):
    #     time_text = self.clock.elapsed_time.toString("HH:mm:ss")
    #     self.clock_label.setText(time_text)


class TrainControllerTestWindow(QMainWindow):
    def __init__(self, clock):
        super().__init__()
        self.setWindowTitle("Train Controller Test")
        self.setFixedSize(1280, 720)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.clock = clock

        # Create a label for the clock in the main window
        self.font = QFont()
        self.font.setPointSize(20)
        self.clock_label = QLabel(self.central_widget)
        self.clock_label.setObjectName("clock_label")
        self.clock_label.setFont(self.font)
        self.clock_label.setAlignment(Qt.AlignRight | Qt.AlignTop)

        # Connect the clock's timeUpdated signal to the update_clock_label method
        self.clock.timeUpdated.connect(self.update_clock_label)

        # Start a timer to update the clock label periodically
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_clock_label)
        self.timer.start(100)

        # Add the clock label to the central widget
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.addWidget(self.clock_label)
        self.layout.addStretch()

        # Title Left Line
        self.LeftLine = QFrame(self.central_widget)
        self.LeftLine.setObjectName("TitleLeftLine")
        self.LeftLine.setGeometry(QRect(0, 138, self.width() // 2, 3))
        self.LeftLine.setMaximumSize(QSize(720, 1280))
        self.LeftLine.setFrameShape(QFrame.HLine)
        self.LeftLine.setFrameShadow(QFrame.Sunken)

        # Title Right Line
        self.RightLine = QFrame(self.central_widget)
        self.RightLine.setObjectName("TitleRightLine")
        self.RightLine.setGeometry(QRect(self.width() // 2, 138, self.width() // 2, 3))
        self.RightLine.setMaximumSize(QSize(720, 1280))
        self.RightLine.setFrameShape(QFrame.HLine)
        self.RightLine.setFrameShadow(QFrame.Sunken)

        # Title
        self.Title = QLabel("Train Controller Test", self.central_widget)
        self.Title.setObjectName("Title")
        font = QFont()
        font.setFamilies(["Arial"])
        font.setPointSize(32)
        self.Title.setFont(font)
        self.Title.setText(
            QCoreApplication.translate("TrainTest", "Train Controller Test", None)
        )
        title_width = self.Title.sizeHint().width()
        title_height = self.Title.sizeHint().height()
        title_x = self.width() // 2 - title_width // 2
        title_y = (138 + 0) // 2 - title_height // 2
        self.Title.setGeometry(QRect(title_x, title_y, title_width, title_height))

        # MTA Logo
        self.mtaLogo = QLabel(self.central_widget)
        self.mtaLogo.setObjectName("mtaLogo")
        self.mtaLogo.setGeometry(QRect(0, 0, 128, 128))
        self.mtaLogo.setMaximumSize(QSize(1280, 720))
        self.mtaLogo.setPixmap(QPixmap("src/main/TrainModel/MTA_Logo.png"))
        self.mtaLogo.setScaledContents(True)

        # Create a QLabel for the first rectangle
        self.rectangle_label = QLabel(self.central_widget)
        self.rectangle_label.setGeometry(QRect(50, 170, 590, 500))
        self.rectangle_label.setStyleSheet("margin: 10px; padding: 0px;")

        # Create a container widget for the blue and white backgrounds
        self.background_widget = QWidget(self.rectangle_label)
        self.background_widget.setGeometry(QRect(0, 0, 590, 50))
        self.background_widget.setStyleSheet(
            "background-color: #007BFF; border: 2px solid #000000; border-radius: 5px;"
        )

        # Create a layout for the blue and white background widget
        self.background_layout = QVBoxLayout(self.background_widget)
        self.background_layout.setContentsMargins(0, 0, 0, 0)
        self.background_layout.setSpacing(0)

        # Create a QLabel for the white background below the blue
        self.white_background_label = QLabel(self.central_widget)
        self.white_background_label.setGeometry(QRect(50, 210, 590, 430))
        self.white_background_label.setStyleSheet(
            "background-color: #FFFFFF; margin: 10px; padding: 10px; border: 2px solid #000000; border-radius: 5px;"
        )

        # Create a layout for the white background below the blue header
        self.white_background_layout = QVBoxLayout(self.white_background_label)
        self.white_background_layout.setContentsMargins(0, 0, 0, 0)
        self.white_background_layout.setSpacing(10)

        # Create QLabel widgets for the list of words
        word_list_1 = [
            "Passenger Emergency Brake:",
            "Temperature:",
            "Power:",
            "Commanded Speed:",
            "Setpoint Command:",
            "Announcements:",
            "Internal Lights:",
            "Headlights:",
            "Left Door:",
            "Right Door:",
            "Advertisements:",
        ]

        # Create and add QLineEdit widgets for the first word list
        self.value_inputs = {}
        for word_placeholder in word_list_1:
            word_label = QLabel(word_placeholder, self.white_background_label)
            word_label.setStyleSheet(
                "color: #000000; background-color: transparent; border: none;"
            )
            word_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            word_label.setContentsMargins(10, 5, 10, 5)
            word_label.setFont(QFont("Arial", 10))

            value_input = QLineEdit(self.white_background_label)
            value_input.setStyleSheet(
                "background-color: #FFFFFF; border: 0.5px solid #000000;"
            )
            value_input.setContentsMargins(15, 15, 15, 15)

            word_layout = QHBoxLayout()
            word_layout.addWidget(word_label, alignment=Qt.AlignLeft)
            word_layout.addWidget(value_input, alignment=Qt.AlignLeft)

            self.white_background_layout.addLayout(word_layout)

            self.value_inputs[word_placeholder] = value_input

        self.white_background_layout.addStretch(1)

        # Create Apply and Reset buttons
        self.apply_button = QPushButton("Apply", self.central_widget)
        self.apply_button.setGeometry(1100, 640, 80, 30)
        self.apply_button.clicked.connect(self.apply_values)
        self.apply_button.setEnabled(True)

        self.reset_button = QPushButton("Reset", self.central_widget)
        self.reset_button.setGeometry(1190, 640, 80, 30)
        self.reset_button.clicked.connect(self.reset_values)
        self.reset_button.setEnabled(True)

        # Create the title label
        self.title_label = QLabel("Inputs:", self.rectangle_label)
        self.font = QFont()
        self.font.setPointSize(16)
        self.font.setBold(True)
        self.title_label.setFont(self.font)
        self.title_label.setStyleSheet("color: #FFFFFF; background-color: transparent;")
        self.title_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.title_label.setGeometry(
            QRect(0, 0, self.background_widget.width(), self.background_widget.height())
        )

        # Create the line separator
        self.line_separator = QFrame(self.rectangle_label)
        self.line_separator.setGeometry(QRect(10, 40, 570, 2))
        self.line_separator.setFrameShape(QFrame.HLine)
        self.line_separator.setFrameShadow(QFrame.Sunken)
        self.line_separator.setStyleSheet("background-color: #000000")

        # Create a QLabel for the second rectangle
        self.rectangle_label_2 = QLabel(self.central_widget)
        self.rectangle_label_2.setGeometry(QRect(640, 170, 590, 500))
        self.rectangle_label_2.setStyleSheet("margin: 10px; padding: 0px;")

        # Create a container widget for the red and white backgrounds
        self.background_widget_2 = QWidget(self.rectangle_label_2)
        self.background_widget_2.setGeometry(QRect(0, 0, 590, 50))
        self.background_widget_2.setStyleSheet(
            "background-color: #FF0000; border: 2px solid #000000; border-radius: 5px;"
        )

        # Create a layout for the red and white background widget
        self.white_background_layout_2 = QVBoxLayout(self.background_widget_2)
        self.white_background_layout_2.setContentsMargins(0, 0, 0, 0)
        self.white_background_layout_2.setSpacing(0)

        # Create a QLabel for the white background below the red
        self.white_background_label_2 = QLabel(self.central_widget)
        self.white_background_label_2.setGeometry(QRect(640, 210, 590, 430))
        self.white_background_label_2.setStyleSheet(
            "background-color: #FFFFFF; margin: 10px; padding: 10px; border: 2px solid #000000; border-radius: 5px;"
        )

        # Create a layout for the white background below the red header
        self.white_background_layout_2 = QVBoxLayout(self.white_background_label_2)
        self.white_background_layout_2.setContentsMargins(0, 0, 0, 0)
        self.white_background_layout_2.setSpacing(5)

        # Create QLabel widgets for the list of words
        self.word_list_2 = [
            "Speed Limit:",
            "Authority:",
            "Commanded Speed:",
            "Current Speed:",
            "Temperature:",
            "Passengers Currently:",
            "Max Passengers:",
            "Next Station:",
            "Previous Station:",
            "Engine Failure:",
            "Signal Pickup Failure:",
            "Brake Failure:",
            "Power:",
            "Passenger Emergency Brake:",
        ]

        # Defines a dictionary with actual values for second set of words
        self.values_2 = {
            "Speed Limit:": "40 mph",
            "Authority:": "6 Blocks",
            "Commanded Speed:": "37 mph",
            "Current Speed:": "35 mph",
            "Temperature:": "78 ℉",
            "Passengers Currently:": "58",
            "Max Passengers:": "72",
            "Next Station:": "Block 7",
            "Previous Station:": "Block 3",
            "Engine Failure:": True,
            "Signal Pickup Failure:": False,
            "Brake Failure:": True,
            "Power:": "83 kW",
            "Passenger Emergency Brake:": "On",
        }

        # Initialize the list at the beginning of my method
        self.word_labels = []

        for word_placeholder in self.word_list_2:
            value = self.values_2.get(word_placeholder, "")
            label_text = f"{word_placeholder} {value}"
            word_label = QLabel(label_text, self.white_background_label_2)
            word_label.setStyleSheet(
                "color: #000000; background-color: transparent; border: none;"
            )
            word_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            word_label.setContentsMargins(10, 5, 10, 5)
            word_label.setFont(QFont("Arial", 10))
            self.white_background_layout_2.addWidget(word_label, alignment=Qt.AlignTop)
            self.word_labels.append(word_label)

        # Create the title label
        self.title_label_2 = QLabel("Outputs:", self.rectangle_label_2)
        self.font = QFont()
        self.font.setPointSize(16)
        self.font.setBold(True)
        self.title_label_2.setFont(self.font)
        self.title_label_2.setStyleSheet(
            "color: #FFFFFF; background-color: transparent;"
        )
        self.title_label_2.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.title_label_2.setGeometry(
            QRect(0, 0, self.background_widget.width(), self.background_widget.height())
        )

        # Create the line separator
        self.line_separator_2 = QFrame(self.rectangle_label_2)
        self.line_separator_2 = QFrame(self.rectangle_label_2)
        self.line_separator_2.setGeometry(QRect(10, 40, 570, 2))
        self.line_separator_2.setFrameShape(QFrame.HLine)
        self.line_separator_2.setFrameShadow(QFrame.Sunken)
        self.line_separator_2.setStyleSheet("background-color: #000000")

    def apply_values(self):
        values_wordlist_1 = {}

        # Iterate through the input text boxes and update values_wordlist_1
        for word_placeholder, value_input in self.value_inputs.items():
            input_value = value_input.text()
            if input_value:
                try:
                    # Try to convert the input to an integer
                    input_value = int(input_value)
                except ValueError:
                    pass  # If it's not a valid integer, keep it as a string
                values_wordlist_1[word_placeholder] = input_value

        # Update the corresponding output values based on the mappings
        for word_placeholder, output_key in self.mapping.items():
            if word_placeholder in values_wordlist_1:
                self.values_2[output_key] = values_wordlist_1[word_placeholder]
                # Update the corresponding text box in the second set
                self.update_wordlist2_textbox(
                    output_key, values_wordlist_1[word_placeholder]
                )

        return values_wordlist_1

    def reset_values(self):
        default_values_wordlist_2 = {
            "Speed Limit": "45 mph",
            "Authority": "5 Blocks",
            "Commanded Speed": "35 mph",
            "Current Speed": "32 mph",
            "Temperature": "75 ℉",
            "Passengers Currently": "60",
            "Max Passengers": "74",
            "Next Station": "Block 9",
            "Previous Station": "Block 5",
            "Engine Failure": False,
            "Signal Pickup Failure": True,
            "Brake Failure": False,
            "Power": "80 kW",
            "Passenger Emergency Brake": "Off",
        }

        for i, (word_placeholder, value) in enumerate(
            zip(self.word_list_2, default_values_wordlist_2.values())
        ):
            label_text = f"{word_placeholder} {value}" if word_placeholder else value
            self.word_labels[i].setText(label_text)

    def update_wordlist2_values(self):
        values_wordlist_1 = self.apply_values()

        for i, word_placeholder in enumerate(self.word_list_2):
            if word_placeholder in self.values_2:
                label = self.values_2[word_placeholder]

                # Check if there is a corresponding label in word list 1
                corresponding_label = self.get_corresponding_label(word_placeholder)

                if corresponding_label:
                    # Get the value from word list 1 and format the label
                    value = values_wordlist_1.get(corresponding_label, "")
                    label = f"{word_placeholder} {value}"

                self.word_labels[i].setText(label)

    def get_corresponding_label(self, label_wordlist2):
        # Define a mapping between word list 2 labels and their corresponding word list 1 labels
        label_mapping = {"Passenger Emergency Brake:": "Passenger Emergency Brake"}

        # Get the corresponding label from the mapping
        return label_mapping.get(label_wordlist2, "")

    def update_clock_label(self):
        time_text = self.clock.elapsed_time.toString("HH:mm:ss")
        self.clock_label.setText(time_text)

    def update_current_speed(self):
        if "Commanded Speed:" in self.values_2:
            commanded_speed = self.values_2["Commanded Speed:", 0]
            if self.current_speed < commanded_speed:
                acceleration = 0.5
                change = acceleration / 10
                self.current_speed = min(commanded_speed, self.current_speed + change)
            elif self.current_speed > commanded_speed:
                change = 0.1
                self.current_speed = max(commanded_speed, self.current_speed - change)

            # Update the current speed label
            self.current_speed_label.setText(f"Current Speed: {self.current_speed}")


class MurphyTestWindow(QMainWindow):
    def __init__(self, clock):
        super().__init__()
        self.setWindowTitle("Murphy Test")
        self.setFixedSize(1280, 720)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.clock = clock

        # Create a label for the clock in the main window
        self.font = QFont()
        self.font.setPointSize(20)
        self.clock_label = QLabel(self.central_widget)
        self.clock_label.setObjectName("clock_label")
        self.clock_label.setFont(self.font)
        self.clock_label.setAlignment(Qt.AlignRight | Qt.AlignTop)

        # Connect the clock's timeUpdated signal to the update_clock_label method
        self.clock.timeUpdated.connect(self.update_clock_label)

        # Start a timer to update the clock label periodically
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_clock_label)
        self.timer.start(100)

        # Add the clock label to the central widget
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.addWidget(self.clock_label)
        self.layout.addStretch()

        # Title Left Line
        self.LeftLine = QFrame(self.central_widget)
        self.LeftLine.setObjectName("TitleLeftLine")
        self.LeftLine.setGeometry(QRect(0, 138, self.width() // 2, 3))
        self.LeftLine.setMaximumSize(QSize(720, 1280))
        self.LeftLine.setFrameShape(QFrame.HLine)
        self.LeftLine.setFrameShadow(QFrame.Sunken)

        # Title Right Line
        self.RightLine = QFrame(self.central_widget)
        self.RightLine.setObjectName("TitleRightLine")
        self.RightLine.setGeometry(QRect(self.width() // 2, 138, self.width() // 2, 3))
        self.RightLine.setMaximumSize(QSize(720, 1280))
        self.RightLine.setFrameShape(QFrame.HLine)
        self.RightLine.setFrameShadow(QFrame.Sunken)

        # Title
        self.Title = QLabel("Murphy Test", self.central_widget)
        self.Title.setObjectName("Title")
        font = QFont()
        font.setFamilies(["Arial"])
        font.setPointSize(32)
        self.Title.setFont(font)
        self.Title.setText(QCoreApplication.translate("TrainTest", "Murphy Test", None))
        title_width = self.Title.sizeHint().width()
        title_height = self.Title.sizeHint().height()
        title_x = self.width() // 2 - title_width // 2
        title_y = (138 + 0) // 2 - title_height // 2
        self.Title.setGeometry(QRect(title_x, title_y, title_width, title_height))

        # MTA Logo
        self.mtaLogo = QLabel(self.central_widget)
        self.mtaLogo.setObjectName("mtaLogo")
        self.mtaLogo.setGeometry(QRect(0, 0, 128, 128))
        self.mtaLogo.setMaximumSize(QSize(1280, 720))
        self.mtaLogo.setPixmap(QPixmap("src/main/TrainModel/MTA_Logo.png"))
        self.mtaLogo.setScaledContents(True)

        # Create a QLabel for the first rectangle
        self.rectangle_label = QLabel(self.central_widget)
        self.rectangle_label.setGeometry(QRect(50, 170, 590, 500))
        self.rectangle_label.setStyleSheet("margin: 10px; padding: 0px;")

        # Create a container widget for the blue and white backgrounds
        self.background_widget = QWidget(self.rectangle_label)
        self.background_widget.setGeometry(QRect(0, 0, 590, 50))
        self.background_widget.setStyleSheet(
            "background-color: #007BFF; border: 2px solid #000000; border-radius: 5px;"
        )

        # Create a layout for the blue and white background widget
        self.background_layout = QVBoxLayout(self.background_widget)
        self.background_layout.setContentsMargins(0, 0, 0, 0)
        self.background_layout.setSpacing(0)

        # Create a QLabel for the white background below the blue
        self.white_background_label = QLabel(self.central_widget)
        self.white_background_label.setGeometry(QRect(50, 210, 590, 430))
        self.white_background_label.setStyleSheet(
            "background-color: #FFFFFF; margin: 10px; padding: 10px; border: 2px solid #000000; border-radius: 5px;"
        )

        # Create a layout for the white background below the blue header
        self.white_background_layout = QVBoxLayout(self.white_background_label)
        self.white_background_layout.setContentsMargins(0, 0, 0, 0)
        self.white_background_layout.setSpacing(10)

        # Create QLabel widgets for the list of words
        word_list_1 = ["Engine Failure:", "Signal Pickup Failure:", "Brake Failure:"]

        values_1 = {
            "engine_failure": True,
            "signal_pickup_failure": False,
            "brake_failure": True,
        }

        # Create a vertical layout to place each pair of label and toggle switch
        vertical_layout = QVBoxLayout()

        for word_placeholder in word_list_1:
            # Create a widget that will hold the label and toggle switch vertically
            widget = QWidget()
            widget.setStyleSheet("background-color: transparent; border: none;")
            status_label = QLabel(word_placeholder, widget)
            status_label.setStyleSheet(
                "background: transparent; border: none;"
            )  # Remove background and border
            status_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            status_label.setFont(QFont("Arial", 10))

            # Check if the word_placeholder is in the values_2 dictionary and is a boolean value
            if word_placeholder.lower().replace(":", "").replace(
                " ", "_"
            ) in values_1 and isinstance(
                values_1[word_placeholder.lower().replace(":", "").replace(" ", "_")],
                bool,
            ):
                # Create a custom toggle switch for the value
                toggle_switch = AnimatedToggle(
                    checked_color="red"
                )  # You can also use 'Toggle' for a non-animated version
                toggle_switch.setChecked(
                    values_1[
                        word_placeholder.lower().replace(":", "").replace(" ", "_")
                    ]
                )
                toggle_switch.setStyleSheet(
                    "background: transparent; border: none;"
                )  # Remove background and border
                toggle_switch.setFixedSize(60, 30)  # Adjust the size as needed
                toggle_switch.setContentsMargins(
                    5, 0, 5, 0
                )  # Adjust margins to remove spacing

                # Set the layout for the widget
                layout = QHBoxLayout()
                layout.addWidget(status_label)
                layout.addWidget(toggle_switch)
                layout.setAlignment(Qt.AlignLeft)

                widget.setLayout(layout)
            else:
                # For other options, use a QLabel to display the value
                value = (
                    "On"
                    if values_1.get(
                        word_placeholder.lower().replace(":", "").replace(" ", "_"),
                        False,
                    )
                    else "Off"
                )
                value_label = QLabel(value, widget)
                value_label.setStyleSheet("background: transparent; border: none;")
                value_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                value_label.setFont(QFont("Arial", 10))

                # Set the layout for the widget
                layout = QHBoxLayout()
                layout.addWidget(status_label)
                layout.addWidget(value_label)

                widget.setLayout(layout)

            # Add the widget to the vertical layout
            vertical_layout.addWidget(widget)

        # Add the vertical layout to your main layout
        self.white_background_layout.addLayout(vertical_layout)

        # Create Apply and Reset buttons
        self.apply_button = QPushButton("Apply", self.central_widget)
        self.apply_button.setGeometry(1100, 640, 80, 30)
        self.apply_button.clicked.connect(self.apply_values)
        self.apply_button.setEnabled(True)

        self.reset_button = QPushButton("Reset", self.central_widget)
        self.reset_button.setGeometry(1190, 640, 80, 30)
        self.reset_button.clicked.connect(self.reset_values)
        self.reset_button.setEnabled(True)

        # Create the title label
        self.title_label = QLabel("Inputs:", self.rectangle_label)
        self.font = QFont()
        self.font.setPointSize(16)
        self.font.setBold(True)
        self.title_label.setFont(self.font)
        self.title_label.setStyleSheet("color: #FFFFFF; background-color: transparent;")
        self.title_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.title_label.setGeometry(
            QRect(0, 0, self.background_widget.width(), self.background_widget.height())
        )

        # Create the line separator
        self.line_separator = QFrame(self.rectangle_label)
        self.line_separator.setGeometry(QRect(10, 40, 570, 2))
        self.line_separator.setFrameShape(QFrame.HLine)
        self.line_separator.setFrameShadow(QFrame.Sunken)
        self.line_separator.setStyleSheet("background-color: #000000")

        # Create a QLabel for the second rectangle
        self.rectangle_label_2 = QLabel(self.central_widget)
        self.rectangle_label_2.setGeometry(QRect(640, 170, 590, 500))
        self.rectangle_label_2.setStyleSheet("margin: 10px; padding: 0px;")

        # Create a container widget for the red and white backgrounds
        self.background_widget_2 = QWidget(self.rectangle_label_2)
        self.background_widget_2.setGeometry(QRect(0, 0, 590, 50))
        self.background_widget_2.setStyleSheet(
            "background-color: #FF0000; border: 2px solid #000000; border-radius: 5px;"
        )

        # Create a layout for the red and white background widget
        self.white_background_layout_2 = QVBoxLayout(self.background_widget_2)
        self.white_background_layout_2.setContentsMargins(0, 0, 0, 0)
        self.white_background_layout_2.setSpacing(0)

        # Create a QLabel for the white background below the red
        self.white_background_label_2 = QLabel(self.central_widget)
        self.white_background_label_2.setGeometry(QRect(640, 210, 590, 430))
        self.white_background_label_2.setStyleSheet(
            "background-color: #FFFFFF; margin: 10px; padding: 10px; border: 2px solid #000000; border-radius: 5px;"
        )

        # Create a layout for the white background below the red header
        self.white_background_layout_2 = QVBoxLayout(self.white_background_label_2)
        self.white_background_layout_2.setContentsMargins(0, 0, 0, 0)
        self.white_background_layout_2.setSpacing(5)

        # Create QLabel widgets for the list of words
        self.word_list_2 = [
            "Speed Limit:",
            "Authority:",
            "Commanded Speed:",
            "Current Speed:",
            "Temperature:",
            "Passengers Currently:",
            "Max Passengers:",
            "Next Station:",
            "Previous Station:",
            "Engine Failure:",
            "Signal Pickup Failure:",
            "Brake Failure:",
            "Power:",
            "Passenger Emergency Brake:",
        ]

        # Defines a dictionary with actual values for second set of words
        self.values_2 = {
            "Speed Limit:": "40 mph",
            "Authority:": "6 Blocks",
            "Commanded Speed:": "37 mph",
            "Current Speed:": "35 mph",
            "Temperature:": "78 ℉",
            "Passengers Currently:": "58",
            "Max Passengers:": "72",
            "Next Station:": "Block 7",
            "Previous Station:": "Block 3",
            "Engine Failure:": True,
            "Signal Pickup Failure:": False,
            "Brake Failure:": True,
            "Power:": "83 kW",
            "Passenger Emergency Brake:": "On",
        }

        # Initialize the list at the beginning of my method
        self.word_labels = []

        for word_placeholder in self.word_list_2:
            value = self.values_2.get(word_placeholder, "")
            label_text = f"{word_placeholder} {value}"
            word_label = QLabel(label_text, self.white_background_label_2)
            word_label.setStyleSheet(
                "color: #000000; background-color: transparent; border: none;"
            )
            word_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            word_label.setContentsMargins(10, 5, 10, 5)
            word_label.setFont(QFont("Arial", 10))
            self.white_background_layout_2.addWidget(word_label, alignment=Qt.AlignTop)
            self.word_labels.append(word_label)

        # Create the title label
        self.title_label_2 = QLabel("Outputs:", self.rectangle_label_2)
        self.font = QFont()
        self.font.setPointSize(16)
        self.font.setBold(True)
        self.title_label_2.setFont(self.font)
        self.title_label_2.setStyleSheet(
            "color: #FFFFFF; background-color: transparent;"
        )
        self.title_label_2.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.title_label_2.setGeometry(
            QRect(0, 0, self.background_widget.width(), self.background_widget.height())
        )

        # Create the line separator
        self.line_separator_2 = QFrame(self.rectangle_label_2)
        self.line_separator_2 = QFrame(self.rectangle_label_2)
        self.line_separator_2.setGeometry(QRect(10, 40, 570, 2))
        self.line_separator_2.setFrameShape(QFrame.HLine)
        self.line_separator_2.setFrameShadow(QFrame.Sunken)
        self.line_separator_2.setStyleSheet("background-color: #000000")

    def apply_values(self):
        values_wordlist_1 = {}

        # Iterate through the input text boxes and update values_wordlist_1
        for word_placeholder, value_input in self.value_inputs.items():
            input_value = value_input.text()
            if input_value:
                try:
                    # Try to convert the input to an integer
                    input_value = int(input_value)
                except ValueError:
                    pass  # If it's not a valid integer, keep it as a string
                values_wordlist_1[word_placeholder] = input_value

        # Update the corresponding output values based on the mappings
        for word_placeholder, output_key in self.mapping.items():
            if word_placeholder in values_wordlist_1:
                self.values_2[output_key] = values_wordlist_1[word_placeholder]
                # Update the corresponding text box in the second set
                self.update_wordlist2_textbox(
                    output_key, values_wordlist_1[word_placeholder]
                )

        return values_wordlist_1

    def reset_values(self):
        default_values_wordlist_2 = {
            "Speed Limit": "45 mph",
            "Authority": "5 Blocks",
            "Commanded Speed": "35 mph",
            "Current Speed": "32 mph",
            "Temperature": "75 ℉",
            "Passengers Currently": "60",
            "Max Passengers": "74",
            "Next Station": "Block 9",
            "Previous Station": "Block 5",
            "Engine Failure": False,
            "Signal Pickup Failure": True,
            "Brake Failure": False,
            "Power": "80 kW",
            "Passenger Emergency Brake": "Off",
        }

        for i, (word_placeholder, value) in enumerate(
            zip(self.word_list_2, default_values_wordlist_2.values())
        ):
            label_text = f"{word_placeholder} {value}" if word_placeholder else value
            self.word_labels[i].setText(label_text)

    def update_wordlist2_values(self, reset=False):
        values_wordlist_1 = self.apply_values()

        for i, word_placeholder in enumerate(self.word_list_2):
            if word_placeholder in self.values_2:
                label = self.values_2[word_placeholder]

                # Check if there is a corresponding label in word list 1
                corresponding_label = self.get_corresponding_label(word_placeholder)

                if corresponding_label:
                    # Get the value from word list 1 and format the label
                    value = values_wordlist_1.get(corresponding_label, "")
                    label = f"{word_placeholder} {value}"

                self.word_labels[i].setText(label)

    def get_corresponding_label(self, label_wordlist2):
        # Define a mapping between word list 2 labels and their corresponding word list 1 labels
        label_mapping = {
            "Engine Failure:": "Engine Failure:",
            "Signal Pickup Failure:": "Signal Pickup Failure",
            "Brake Failure:": "Brake Failure",
        }

        # Get the corresponding label from the mapping
        return label_mapping.get(label_wordlist2, "")

    def update_clock_label(self):
        time_text = self.clock.elapsed_time.toString("HH:mm:ss")
        self.clock_label.setText(time_text)


def main():
    app = QApplication(sys.argv)
    ui = TrainTest()
    ui.show_gui()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
