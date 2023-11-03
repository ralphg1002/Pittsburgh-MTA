# importing libraries
import sys
import math
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from .tcsw_functions import *
# from tcsw_time import *
from .tcsw_train_attributes import *


class TestWindow(QMainWindow):
    # font variables
    textFontSize = 10
    labelFontSize = 12
    headerFontSize = 16
    titleFontSize = 22
    fontStyle = "Product Sans"

    # color variables
    colorDarkBlue = "#085394"
    colorDarkRed = "#CF2A27"
    colorDarkGreen = "#2E5339"
    colorLightGrey = "#CCCCCC"
    colorMediumGrey = "#DDDDDD"
    colorDarkGrey = "#666666"

    # dimensions
    w = 770
    h = 420

    # variables
    tcObject = TCFunctions()
    testbenchVariables = {"trainID": "", "speedLimit": 0, "authority": 0}

    def __init__(self):
        super().__init__()

        # setting title
        self.setWindowTitle("Test Bench")

        # setting geometry
        self.setGeometry(50, 50, self.w, self.h)

        """test window template layout"""
        self.headerBlock = QLabel(self)
        self.box_label(self.headerBlock, 770, 73)
        self.headerBlock.setStyleSheet(
            "background-color: " + self.colorDarkBlue + ";border: 0px"
        )

        self.testBenchLabel = QLabel("Test Bench", self)
        self.header_label(self.testBenchLabel)
        self.testBenchLabel.setStyleSheet("color: white")
        self.set_relative_below_right(self.testBenchLabel, self.headerBlock, 20)

        self.trainBox = QLabel(self)
        self.box_label(self.trainBox, 230, 432 - self.headerBlock.height() - 40)
        self.set_relative_below_right(self.trainBox, self.headerBlock, 20)
        self.trainBox.move(
            self.trainBox.x(), self.headerBlock.y() + self.headerBlock.height() + 10
        )

        self.editBox = QLabel(self)
        self.box_label(self.editBox, 230, 432 - self.headerBlock.height() - 40)
        self.set_relative_below_right(self.editBox, self.headerBlock, 20)
        self.set_relative_right(self.editBox, self.trainBox, 20)

        self.buttonBox = QLabel(self)
        self.box_label(self.buttonBox, 230, 432 - self.headerBlock.height() - 40)
        self.set_relative_right(self.buttonBox, self.editBox, 20)

        self.selectTrainLabel = QLabel("Select a Train", self)
        self.text_label(self.selectTrainLabel)
        self.set_relative_below_right(self.selectTrainLabel, self.trainBox, 10)

        self.trainCombo = QComboBox(self)
        self.text_label(self.trainCombo)
        self.set_relative_right(self.trainCombo, self.selectTrainLabel, 10)
        self.set_relative_before_right_end(self.trainCombo, self.trainBox, 10)

        self.addTrainLabel = QLabel("Add Train", self)
        self.text_label(self.addTrainLabel)
        self.set_relative_below(self.addTrainLabel, self.selectTrainLabel, 20)

        self.sendLabel = QPushButton(self)
        self.png_button(self.sendLabel, QtGui.QPixmap("TrainControllerSW/PNGs/send.svg").scaled(32, 32))
        self.sendLabel.adjustSize()
        self.set_relative_below(self.sendLabel, self.addTrainLabel, 10)
        self.set_relative_before_right_end(self.sendLabel, self.trainBox, 10)

        self.addTrainEdit = QLineEdit(self)
        self.text_label(self.addTrainEdit)
        self.set_relative_below(self.addTrainEdit, self.addTrainLabel, 10)
        self.addTrainEdit.setFixedWidth(self.sendLabel.x() - self.addTrainEdit.x() - 10)

        self.speedLimitLabel = QLabel("Speed Limit", self)
        self.text_label(self.speedLimitLabel)
        self.set_relative_below_right(self.speedLimitLabel, self.editBox, 10)

        self.speedLimitVal = QSpinBox(self)
        self.text_label(self.speedLimitVal)
        self.set_relative_right(self.speedLimitVal, self.speedLimitLabel, 10)
        self.speedLimitVal.setFixedWidth(60)
        self.set_relative_before_right_end(self.speedLimitVal, self.editBox, 10)

        self.authorityLabel = QLabel("Authority", self)
        self.text_label(self.authorityLabel)
        self.set_relative_below(self.authorityLabel, self.speedLimitLabel, 10)

        self.authorityVal = QSpinBox(self)
        self.text_label(self.authorityVal)
        self.set_relative_right(self.authorityVal, self.authorityLabel, 10)
        self.authorityVal.setFixedWidth(60)
        self.set_relative_before_right_end(self.authorityVal, self.editBox, 10)

        self.commandedSpeedLabel = QLabel("Commanded Speed", self)
        self.text_label(self.commandedSpeedLabel)
        self.set_relative_below(self.commandedSpeedLabel, self.authorityLabel, 10)

        self.commandedSpeedVal = QSpinBox(self)
        self.text_label(self.commandedSpeedVal)
        self.set_relative_right(self.commandedSpeedVal, self.commandedSpeedLabel, 10)
        self.commandedSpeedVal.setFixedWidth(60)
        self.set_relative_before_right_end(self.commandedSpeedVal, self.editBox, 10)

        self.currentSpeedLabel = QLabel("Current Speed", self)
        self.text_label(self.currentSpeedLabel)
        self.set_relative_below(self.currentSpeedLabel, self.commandedSpeedLabel, 10)

        self.currentSpeedVal = QSpinBox(self)
        self.text_label(self.currentSpeedVal)
        self.set_relative_right(self.currentSpeedVal, self.currentSpeedLabel, 10)
        self.currentSpeedVal.setFixedWidth(60)
        self.set_relative_before_right_end(self.currentSpeedVal, self.editBox, 10)

        self.currentTempLabel = QLabel("Current Temp", self)
        self.text_label(self.currentTempLabel)
        self.set_relative_below(self.currentTempLabel, self.currentSpeedLabel, 10)

        self.currentTempVal = QSpinBox(self)
        self.text_label(self.currentTempVal)
        self.set_relative_right(self.currentTempVal, self.currentTempLabel, 10)
        self.currentTempVal.setFixedWidth(60)
        self.set_relative_before_right_end(self.currentTempVal, self.editBox, 10)

        self.prevStopLabel = QLabel("Next Stop 0:", self)
        self.text_label(self.prevStopLabel)
        self.set_relative_below_right(self.prevStopLabel, self.buttonBox, 10)

        self.prevStopVal = QLineEdit(self)
        self.text_label(self.prevStopVal)
        self.set_relative_right(self.prevStopVal, self.prevStopLabel, 10)
        self.prevStopVal.setFixedWidth(60)
        self.set_relative_before_right_end(self.prevStopVal, self.buttonBox, 10)

        self.nextStopLabel = QLabel("Next Stop 1:", self)
        self.text_label(self.nextStopLabel)
        self.set_relative_below(self.nextStopLabel, self.prevStopLabel, 10)

        self.nextStopVal = QLineEdit(self)
        self.text_label(self.nextStopVal)
        self.set_relative_right(self.nextStopVal, self.nextStopLabel, 10)
        self.nextStopVal.setFixedWidth(60)
        self.set_relative_before_right_end(self.nextStopVal, self.buttonBox, 10)

        self.currStopLabel = QLabel("Current Stop:", self)
        self.text_label(self.currStopLabel)
        self.set_relative_below(self.currStopLabel, self.nextStopLabel, 10)

        self.currStopVal = QLineEdit(self)
        self.text_label(self.currStopVal)
        self.set_relative_right(self.currStopVal, self.currStopLabel, 10)
        self.currStopVal.setFixedWidth(60)
        self.set_relative_before_right_end(self.currStopVal, self.buttonBox, 10)

        self.isStationButton = QPushButton("Station", self)
        self.text_label(self.isStationButton)
        self.set_relative_below(self.isStationButton, self.currStopLabel, 10)
        self.isStationButton.setCheckable(True)

        self.engineFailButton = QPushButton("Engine Failure", self)
        self.text_label(self.engineFailButton)
        self.engineFailButton.setCheckable(True)
        self.set_relative_below(self.engineFailButton, self.currentTempLabel, 10)

        self.brakeFailButton = QPushButton("Brake Failure", self)
        self.text_label(self.brakeFailButton)
        self.brakeFailButton.setCheckable(True)
        self.set_relative_below(self.brakeFailButton, self.engineFailButton, 10)

        self.signalFailButton = QPushButton("Signal Failure", self)
        self.text_label(self.signalFailButton)
        self.signalFailButton.setCheckable(True)
        self.set_relative_below(self.signalFailButton, self.brakeFailButton, 10)

        self.passengerBrakeButton = QPushButton("Passenger E-brake", self)
        self.text_label(self.passengerBrakeButton)
        self.passengerBrakeButton.setStyleSheet("color: " + self.colorDarkRed)
        self.passengerBrakeButton.setCheckable(True)
        self.set_relative_below(self.passengerBrakeButton, self.signalFailButton, 10)

        self.tunnelButton = QPushButton("Tunnel", self)
        self.text_label(self.tunnelButton)
        self.tunnelButton.setCheckable(True)
        self.set_relative_below(self.tunnelButton, self.isStationButton, 10)

        self.stationSideLabel = QLabel("Station Side", self)
        self.text_label(self.stationSideLabel)
        self.set_relative_below(self.stationSideLabel, self.tunnelButton, 10)

        self.leftSideButton = QPushButton("Left", self)
        self.text_label(self.leftSideButton)
        self.leftSideButton.setCheckable(True)
        self.set_relative_below(self.leftSideButton, self.stationSideLabel, 10)

        self.rightSideButton = QPushButton("Right", self)
        self.text_label(self.rightSideButton)
        self.rightSideButton.setCheckable(True)
        self.set_relative_right(self.rightSideButton, self.leftSideButton, 20)

        self.beaconButton = QPushButton("Send Beacon Data", self)
        self.text_label(self.beaconButton)
        self.beaconButton.setStyleSheet("color: " + self.colorDarkGreen)
        self.set_relative_below(self.beaconButton, self.leftSideButton, 20)

        # signals
        self.testbenchVariables["trainID"] = self.trainCombo.currentText()
        self.sendLabel.clicked.connect(lambda: self.add_train())
        self.trainCombo.currentTextChanged.connect(lambda: self.select_train())
        self.speedLimitVal.valueChanged.connect(lambda: self.speed_limit())
        self.authorityVal.valueChanged.connect(lambda: self.authority_val())
        self.commandedSpeedVal.valueChanged.connect(lambda: self.commanded_speed())
        self.currentSpeedVal.valueChanged.connect(lambda: self.current_speed())
        self.currentTempVal.valueChanged.connect(lambda: self.current_temp())
        self.engineFailButton.clicked.connect(lambda: self.engine_failure())
        self.signalFailButton.clicked.connect(lambda: self.signal_failure())
        self.brakeFailButton.clicked.connect(lambda: self.brake_failure())
        self.beaconButton.clicked.connect(lambda: self.send_beacon())

    def send_beacon(self):
        for train in self.tcObject.trainList:
            if train.get_trainID() == self.testbenchVariables["trainID"]:
                train.beacon["nextStop"][0] = self.prevStopVal.text()
                train.beacon["nextStop"][1] = self.nextStopVal.text()
                train.beacon["isStation"] = self.isStationButton.isChecked()
                train.beacon["isTunnel"] = self.tunnelButton.isChecked()
                train.beacon["leftStation"] = self.leftSideButton.isChecked()
                train.beacon["rightStation"] = self.rightSideButton.isChecked()
                train.beacon["currStop"] = self.currStopVal.text()

    def brake_failure(self):
        for train in self.tcObject.trainList:
            if train.get_trainID() == self.testbenchVariables["trainID"]:
                train.set_brakeFailure(self.brakeFailButton.isChecked())

    def signal_failure(self):
        for train in self.tcObject.trainList:
            if train.get_trainID() == self.testbenchVariables["trainID"]:
                train.set_signalFailure(self.signalFailButton.isChecked())

    def engine_failure(self):
        for train in self.tcObject.trainList:
            if train.get_trainID() == self.testbenchVariables["trainID"]:
                train.set_engineFailure(self.engineFailButton.isChecked())

    def current_temp(self):
        for train in self.tcObject.trainList:
            if train.get_trainID() == self.testbenchVariables["trainID"]:
                train.set_currentTemp(self.currentTempVal.value())

    def current_speed(self):
        for train in self.tcObject.trainList:
            if train.get_trainID() == self.testbenchVariables["trainID"]:
                train.set_currentSpeed(self.currentSpeedVal.value())

    def commanded_speed(self):
        for train in self.tcObject.trainList:
            if train.get_trainID() == self.testbenchVariables["trainID"]:
                train.set_commandedSpeed(self.commandedSpeedVal.value())

    def authority_val(self):
        for train in self.tcObject.trainList:
            if train.get_trainID() == self.testbenchVariables["trainID"]:
                train.set_authority(self.authorityVal.value())

    def speed_limit(self):
        for train in self.tcObject.trainList:
            if train.get_trainID() == self.testbenchVariables["trainID"]:
                train.set_speedLimit(self.speedLimitVal.value())

    def add_train(self):
        self.trainCombo.addItem(self.addTrainEdit.text())
        self.tcObject.add_train(Train(self.addTrainEdit.text()))

    def select_train(self):
        self.testbenchVariables["trainID"] = self.trainCombo.currentText()

    def text_label(self, label):
        label.setFont(QFont(self.fontStyle, self.textFontSize))
        label.adjustSize()
        label.setStyleSheet("color:" + self.colorDarkBlue)

    def regular_label(self, label):
        label.setFont(QFont(self.fontStyle, self.labelFontSize))
        label.adjustSize()
        label.setStyleSheet("color:" + self.colorDarkBlue)

    def header_label(self, label):
        label.setFont(QFont(self.fontStyle, self.headerFontSize))
        label.adjustSize()
        label.setStyleSheet("color:" + self.colorDarkBlue)

    def title_label(self, label):
        label.setFont(QFont(self.fontStyle, self.titleFontSize))
        label.adjustSize()
        label.setStyleSheet("color:" + self.colorDarkBlue)

    def png_label(self, label, pixmap):
        label.setPixmap(pixmap)

    def png_button(self, button, pixmap):
        button.setIcon(QtGui.QIcon(pixmap))

    def line_label(self, label, orientation, value):
        # if true, horizontal
        if orientation:
            label.setGeometry(0, 0, value, 1)
        # vertical
        else:
            label.setGeometry(0, 0, 1, value)
        label.setStyleSheet("border: 1px solid" + self.colorLightGrey)

    def box_label(self, label, width, height):
        label.setGeometry(0, 0, width, height)
        label.setStyleSheet("border: 1px solid " + self.colorLightGrey)

    def set_relative_below(self, child, parent, pad):
        child.move(parent.x(), parent.y() + parent.height() + pad)

    def set_relative_right(self, child, parent, pad):
        child.move(
            parent.x() + parent.width() + pad,
            parent.y() + math.floor((parent.height() - child.height()) / 2.0),
        )

    def set_relative_left(self, child, parent, pad):
        child.move(
            parent.x() - child.width() - pad,
            parent.y() + math.floor((parent.height() - child.height()) / 2.0),
        )

    def set_relative_below_right(self, child, parent, pad):
        child.move(parent.x() + pad, parent.y() + pad)

    def set_relative_below_left(self, child, parent, pad):
        child.move(parent.x() - pad, parent.y() + parent.height() + pad)

    def set_relative_below_center(self, child, parent, pad):
        child.move(
            parent.x() + math.floor(parent.width() / 2) - math.floor(child.width() / 2),
            parent.y() + parent.height() + pad,
        )

    def set_relative_before_right_end(self, child, parent, pad):
        child.move(parent.x() + parent.width() - child.width() - pad, child.y())


testWindow = None


def showTest():
    # create window instance
    global testWindow

    if testWindow is None:
        testWindow = TestWindow()

    testWindow.show()
