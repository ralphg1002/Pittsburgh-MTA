# importing libraries
import sys
import math
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from .tcsw_tb import *
from .tcsw_functions import *

# from tcsw_time import *
from .tcsw_train_attributes import *

sys.path.append("../../main")
from signals import (
    trainControllerSWToTrainModel,
    trainModelToTrainController,
    masterSignals,
)


class TrainControllerUI(QMainWindow):
    """
    to be edited
    Attributes:
        textFontSize : int
        labelFontSize : int
        headerFontSize : int
        titleFontSize : int
        fontStyle : str
        colorDarkBlue : str
        colorDarkRed : str
        colorLightBlue : str
        colorLightGrey : str
        colorMediumGrey : str
        colorDarkGrey : str
        w : int
        h : int
        moduleName : str
    Operations:
        __init__(self) : void
    """

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
    w = 960
    h = 960

    moduleName = "Train Controller Module (SW)"

    def __init__(self):
        # tc function call
        self.tcFunctions = TCFunctions()

        # some variables
        self.tcVariables = {
            "samplePeriod": 1,
            "period": 1000,
            "trainID": "",
            "line": "",
            "number": "",
            "trainList": [],
            "customAnnouncement": "",
        }

        super().__init__()
        # creating test bench window
        self.testWindow = TestWindow()

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
        self.titleLabel.setGeometry(120, 35, 790, 43)
        self.titleLabel.adjustSize()
        self.titleLabel.setStyleSheet("color: white")

        # logo
        self.pixmapMTALogo = QtGui.QPixmap(
            "src/main/TrainControllerSW/PNGs/MTA_NYC_logo.svg.png"
        )
        self.pixmapMTALogo = self.pixmapMTALogo.scaled(70, 70)
        self.logo = QLabel(self)
        self.logo.setPixmap(self.pixmapMTALogo)
        self.logo.move(20, 20)
        self.logo.adjustSize()

        # module
        self.moduleLabel = QLabel(self.moduleName, self)
        self.moduleLabel.setFont(QFont(self.fontStyle, self.headerFontSize))
        self.moduleLabel.setAlignment(Qt.AlignCenter)
        self.moduleLabel.move(30, 100)
        self.moduleLabel.adjustSize()
        self.moduleLabel.setStyleSheet("color:" + self.colorDarkBlue)

        # test bench icon
        self.pixmapGear = QtGui.QPixmap("src/main/TrainControllerSW/PNGs/gear.svg")
        self.pixmapGear = self.pixmapGear.scaled(25, 25)
        self.testbenchIcon = QLabel(self)
        self.testbenchIcon.setPixmap(self.pixmapGear)
        self.testbenchIcon.setGeometry(30, 140, 32, 32)

        # test bench button
        self.testbenchButton = QPushButton("Test Bench", self)
        self.testbenchButton.setFont(QFont(self.fontStyle, self.textFontSize))
        self.testbenchButton.setGeometry(60, 145, 100, 20)
        self.testbenchButton.setStyleSheet(
            "color:" + self.colorDarkBlue + ";border: 1px solid white"
        )
        self.testbenchButton.clicked.connect(lambda: self.testWindow.show())

        # system time input
        self.systemTimeInput = QLabel("00:00:00", self)
        self.systemTimeInput.setFont(QFont(self.fontStyle, self.headerFontSize))
        self.systemTimeInput.setGeometry(820, 100, 150, 32)
        self.systemTimeInput.setStyleSheet("color:" + self.colorDarkBlue)

        # system time label
        self.systemTimeLabel = QLabel("System Time:", self)
        self.systemTimeLabel.setFont(QFont(self.fontStyle, self.headerFontSize))
        self.systemTimeLabel.setGeometry(650, 100, 200, 32)
        self.systemTimeLabel.setStyleSheet("color:" + self.colorDarkBlue)

        # system speed label
        self.systemSpeedLabel = QLabel("System Speed:", self)
        self.systemSpeedLabel.setFont(QFont(self.fontStyle, self.textFontSize))
        self.systemSpeedLabel.setGeometry(700, 145, 100, 20)
        self.systemSpeedLabel.adjustSize()
        self.systemSpeedLabel.setStyleSheet("color:" + self.colorDarkBlue)

        # system speed input
        self.systemSpeedInput = QLabel("x" + str(8.888), self)
        self.systemSpeedInput.setFont(QFont(self.fontStyle, self.textFontSize))
        self.systemSpeedInput.move(855, 145)
        self.systemSpeedInput.adjustSize()
        self.systemSpeedInput.setStyleSheet("color:" + self.colorDarkBlue)
        self.systemSpeedInput.setText("x" + str(1.000))

        # increase system speed button
        self.pixmapFastForward = QtGui.QPixmap(
            "src/main/TrainControllerSW/PNGs/forward.svg"
        )
        self.pixmapFastForward = self.pixmapFastForward.scaled(32, 32)
        self.speedUpButton = QPushButton(self)
        self.speedUpButton.setIcon(QtGui.QIcon(self.pixmapFastForward))
        self.speedUpButton.setGeometry(890, 140, 32, 32)
        self.speedUpButton.setStyleSheet(
            "color:" + self.colorDarkBlue + ";border: 1px solid white"
        )
        self.speedUpButton.clicked.connect(lambda: self.speed_up())

        # decrease system speed button
        self.pixmapRewind = QtGui.QPixmap(
            "src/main/TrainControllerSW/PNGs/backward.svg"
        )
        self.pixmapRewind = self.pixmapRewind.scaled(32, 32)
        self.slowDownButton = QPushButton(self)
        self.slowDownButton.setIcon(QtGui.QIcon(self.pixmapRewind))
        self.slowDownButton.setGeometry(820, 140, 32, 32)
        self.slowDownButton.setStyleSheet(
            "color:" + self.colorDarkBlue + ";border: 1px solid white"
        )
        self.slowDownButton.clicked.connect(lambda: self.slow_down())

        self.set_relative_right(self.speedUpButton, self.systemSpeedInput, 20)
        self.speedUpButton.move(
            self.bodyBlock.x()
            + self.bodyBlock.width()
            - self.speedUpButton.width()
            - 10,
            self.speedUpButton.y(),
        )
        self.set_relative_left(self.systemSpeedInput, self.speedUpButton, 5)
        self.set_relative_left(self.slowDownButton, self.systemSpeedInput, 5)
        self.set_relative_left(self.systemSpeedLabel, self.slowDownButton, 5)

        # divider
        self.divider1 = QLabel(self)
        self.divider1.setGeometry(20, 176, 920, 1)
        self.divider1.setStyleSheet("background-color:" + self.colorLightGrey)

        """ui layout"""
        self.pixmapCircleCheck = QtGui.QPixmap(
            "src/main/TrainControllerSW/PNGs/circle-check.svg"
        )
        self.pixmapCircleCheck = self.pixmapCircleCheck.scaled(32, 32)

        self.pixmapCircleX = QtGui.QPixmap(
            "src/main/TrainControllerSW/PNGs/circle-x.svg"
        )
        self.pixmapCircleX = self.pixmapCircleX.scaled(32, 32)

        self.pixmapForward = QtGui.QPixmap(
            "src/main/TrainControllerSW/PNGs/forward.svg"
        )
        self.pixmapForward = self.pixmapForward.scaled(32, 32)

        self.pixmapBackward = QtGui.QPixmap(
            "src/main/TrainControllerSW/PNGs/backward.svg"
        )
        self.pixmapBackward = self.pixmapBackward.scaled(32, 32)

        self.pixmapLDoorOpen = QtGui.QPixmap(
            "src/main/TrainControllerSW/PNGs/ldoor-open.png"
        )
        self.pixmapLDoorOpen = self.pixmapLDoorOpen.scaled(32, 32)

        self.pixmapLDoorClosed = QtGui.QPixmap(
            "src/main/TrainControllerSW/PNGs/ldoor-closed.png"
        )
        self.pixmapLDoorClosed = self.pixmapLDoorClosed.scaled(32, 32)

        self.pixmapRDoorOpen = QtGui.QPixmap(
            "src/main/TrainControllerSW/PNGs/rdoor-open.png"
        )
        self.pixmapRDoorOpen = self.pixmapRDoorOpen.scaled(32, 32)

        self.pixmapRDoorClosed = QtGui.QPixmap(
            "src/main/TrainControllerSW/PNGs/rdoor-closed.png"
        )
        self.pixmapRDoorClosed = self.pixmapRDoorClosed.scaled(32, 32)

        self.pixmapToggleOff = QtGui.QPixmap(
            "src/main/TrainControllerSW/PNGs/toggle-off.svg"
        )
        self.pixmapToggleOff = self.pixmapToggleOff.scaled(32, 32)

        self.pixmapToggleOn = QtGui.QPixmap(
            "src/main/TrainControllerSW/PNGs/toggle-on.svg"
        )
        self.pixmapToggleOn = self.pixmapToggleOn.scaled(32, 32)

        self.pixmapTrain = QtGui.QPixmap("src/main/TrainControllerSW/PNGs/train.png")
        self.pixmapTrain = self.pixmapTrain.scaled(
            math.floor(48 / 532 * 532), math.floor(48 / 532 * 444)
        )

        self.pixmapTrainHlt = QtGui.QPixmap(
            "src/main/TrainControllerSW/PNGs/train-hlt.png"
        )
        self.pixmapTrainHlt = self.pixmapTrainHlt.scaled(
            math.floor(48 / 532 * 532), math.floor(48 / 532 * 444)
        )

        self.pixmapTrainIlt = QtGui.QPixmap(
            "src/main/TrainControllerSW/PNGs/train-ilt.png"
        )
        self.pixmapTrainIlt = self.pixmapTrainIlt.scaled(
            math.floor(48 / 532 * 532), math.floor(48 / 532 * 444)
        )

        self.pixmapTrainLts = QtGui.QPixmap(
            "src/main/TrainControllerSW/PNGs/train-lts.png"
        )
        self.pixmapTrainLts = self.pixmapTrainLts.scaled(
            math.floor(48 / 532 * 532), math.floor(48 / 532 * 444)
        )

        self.pixmapChange = QtGui.QPixmap("src/main/TrainControllerSW/PNGs/change.svg")
        self.pixmapChange = self.pixmapChange.scaled(32, 32)

        self.pixmapSend = QtGui.QPixmap("src/main/TrainControllerSW/PNGs/send.svg")
        self.pixmapSend = self.pixmapSend.scaled(32, 32)

        self.movieMoneyAd = QMovie("src/main/TrainControllerSW/PNGs/giphy1.gif")
        self.movieMoneyAd.setScaledSize(QSize(330, 93))

        self.pixmapAd1 = QtGui.QPixmap("src/main/TrainControllerSW/PNGs/ad1.png")
        self.pixmapAd2 = QtGui.QPixmap("src/main/TrainControllerSW/PNGs/ad2.png")
        self.pixmapAd3 = QtGui.QPixmap("src/main/TrainControllerSW/PNGs/ad3.png")

        self.pixmapAnnouncement = QtGui.QPixmap(
            "src/main/TrainControllerSW/PNGs/announcement.svg"
        )
        self.pixmapAnnouncement = self.pixmapAnnouncement.scaled(32, 32)

        # Train change section
        self.trainChangeBox = QLabel("", self)
        self.box_label(self.trainChangeBox, 245, 200)
        self.set_relative_below_right(self.trainChangeBox, self.divider1, 20)

        self.trainChangeLabel = QLabel("Change Train", self)
        self.regular_label(self.trainChangeLabel)
        self.set_relative_below_right(self.trainChangeLabel, self.trainChangeBox, 10)

        self.trainLineLabel = QLabel("Line", self)
        self.text_label(self.trainLineLabel)
        self.set_relative_below(self.trainLineLabel, self.trainChangeLabel, 10)

        self.trainLineCombo = QComboBox(self)
        self.text_label(self.trainLineCombo)
        self.trainLineCombo.setStyleSheet(
            "color: "
            + self.colorDarkBlue
            + ";"
            + "border: 1px solid"
            + self.colorLightGrey
        )
        self.set_relative_right(self.trainLineCombo, self.trainLineLabel, 20)
        self.set_relative_before_right_end(self.trainLineCombo, self.trainChangeBox, 10)
        self.trainLineCombo.addItem("red")
        self.trainLineCombo.addItem("green")

        self.trainNumberLabel = QLabel("Train Name", self)
        self.text_label(self.trainNumberLabel)
        self.set_relative_below(self.trainNumberLabel, self.trainLineLabel, 20)

        self.trainNumberCombo = QComboBox(self)
        self.text_label(self.trainNumberCombo)
        self.trainNumberCombo.setStyleSheet(
            "color: "
            + self.colorDarkBlue
            + ";"
            + "border: 1px solid"
            + self.colorLightGrey
        )
        self.set_relative_right(self.trainNumberCombo, self.trainNumberLabel, 20)
        self.set_relative_before_right_end(
            self.trainNumberCombo, self.trainChangeBox, 10
        )

        self.changeButton = QPushButton(self)
        self.png_button(self.changeButton, self.pixmapChange)
        self.set_relative_below(self.changeButton, self.trainNumberCombo, 10)
        self.changeButton.move(
            math.floor(
                (
                    self.trainChangeBox.width()
                    + self.trainChangeBox.x()
                    - self.changeButton.width()
                )
                / 2
            )
            + 20,
            self.changeButton.y(),
        )

        self.trainChangeBox.setFixedHeight(
            self.changeButton.y()
            + self.changeButton.height()
            + 10
            - self.trainChangeBox.y()
        )

        # Engineer section
        self.engineerLabel = QLabel("Engineer", self)
        self.header_label(self.engineerLabel)
        self.engineerLabel.move(
            self.trainChangeBox.x() + self.trainChangeBox.width() + 20,
            self.trainChangeBox.y(),
        )

        self.engineerBox = QLabel("", self)
        self.box_label(self.engineerBox, self.trainChangeBox.width(), 100)
        self.set_relative_below(self.engineerBox, self.engineerLabel, 20)

        self.kpLabel = QLabel("Kp", self)
        self.text_label(self.kpLabel)
        self.set_relative_below_right(self.kpLabel, self.engineerBox, 10)
        self.kpLabel.move(self.kpLabel.x(), self.kpLabel.y() + 10)

        self.kpEdit = QSpinBox(self)
        self.kpEdit.setValue(0)
        self.kpEdit.setFont(QFont(self.fontStyle, self.textFontSize))
        self.set_relative_right(self.kpEdit, self.kpLabel, 20)
        self.set_relative_before_right_end(self.kpEdit, self.engineerBox, 10)

        self.kiLabel = QLabel("Ki", self)
        self.text_label(self.kiLabel)
        self.set_relative_below(self.kiLabel, self.kpLabel, 20)

        self.kiEdit = QSpinBox(self)
        self.kiEdit.setValue(0)
        self.kiEdit.setFont(QFont(self.fontStyle, self.textFontSize))
        self.set_relative_right(self.kiEdit, self.kiLabel, 20)
        self.set_relative_before_right_end(self.kiEdit, self.engineerBox, 10)

        self.engineerBox.setFixedHeight(
            self.trainChangeBox.y()
            + self.trainChangeBox.height()
            - self.engineerBox.y()
        )

        # Middle column block
        self.driverLabel = QLabel("Train Driver", self)
        self.header_label(self.driverLabel)
        self.set_relative_below(self.driverLabel, self.divider1, 20)
        self.driverLabel.move(
            self.engineerBox.x() + self.engineerBox.width() + 20, self.driverLabel.y()
        )

        self.middleBox = QLabel("", self)
        self.box_label(self.middleBox, 350, 920)
        self.set_relative_below(self.middleBox, self.driverLabel, 20)
        self.middleBox.setFixedHeight(920 - self.middleBox.y())
        self.middleBox.move(940 - self.middleBox.width() - 20, self.middleBox.y())
        self.driverLabel.move(self.middleBox.x(), self.driverLabel.y())

        # Mode section
        self.modeLabel = QLabel("Mode", self)
        self.regular_label(self.modeLabel)
        self.set_relative_below_right(self.modeLabel, self.middleBox, 10)

        self.modeCombo = QComboBox(self)
        self.regular_label(self.modeCombo)
        self.modeCombo.addItem("Automatic")
        self.modeCombo.addItem("Manual")
        self.modeCombo.adjustSize()
        self.set_relative_right(self.modeCombo, self.modeLabel, 10)
        self.set_relative_before_right_end(self.modeCombo, self.middleBox, 10)

        self.modeDivider = QLabel(self)
        self.line_label(self.modeDivider, True, self.middleBox.width())
        self.set_relative_below_left(self.modeDivider, self.modeLabel, 10)

        # Brake section
        self.brakeLabel = QLabel("Brakes", self)
        self.regular_label(self.brakeLabel)
        self.set_relative_below_right(self.brakeLabel, self.modeDivider, 10)

        self.emergencyBrakeButton = QPushButton("Emergency Brake", self)
        self.title_label(self.emergencyBrakeButton)
        self.emergencyBrakeButton.setStyleSheet("color: " + self.colorDarkRed)
        self.set_relative_below(self.emergencyBrakeButton, self.brakeLabel, 10)
        self.emergencyBrakeButton.setCheckable(True)

        self.serviceBrakeLabel = QLabel("Service Brake", self)
        self.text_label(self.serviceBrakeLabel)
        self.set_relative_below(self.serviceBrakeLabel, self.emergencyBrakeButton, 10)

        self.serviceBrakeSlider = QSlider(self)
        self.serviceBrakeSlider.setOrientation(1)
        self.serviceBrakeSlider.setRange(0, 100)
        self.serviceBrakeSlider.setValue(0)
        self.set_relative_right(self.serviceBrakeSlider, self.serviceBrakeLabel, 10)

        self.serviceBrakeValue = QLabel("         ", self)
        self.text_label(self.serviceBrakeValue)
        self.serviceBrakeValue.setText(str(self.serviceBrakeSlider.value()) + "%")
        self.set_relative_before_right_end(
            self.serviceBrakeSlider, self.middleBox, self.serviceBrakeValue.width() + 20
        )
        self.set_relative_right(self.serviceBrakeValue, self.serviceBrakeSlider, 10)
        self.serviceBrakeSlider.valueChanged.connect(
            lambda: self.serviceBrakeValue.setText(
                str(self.serviceBrakeSlider.value()) + "%"
            )
        )

        self.brakeDivider = QLabel("", self)
        self.line_label(self.brakeDivider, True, self.middleBox.width())
        self.set_relative_below(self.brakeDivider, self.serviceBrakeLabel, 10)
        self.brakeDivider.move(self.middleBox.x(), self.brakeDivider.y())

        # Setpoint speed section
        self.setpointSpeedLabel = QLabel("Setpoint Speed", self)
        self.regular_label(self.setpointSpeedLabel)
        self.set_relative_below_right(self.setpointSpeedLabel, self.brakeDivider, 10)

        self.setpointSpeedValue = QSpinBox(self)
        self.setpointSpeedValue.setRange(0, 225)
        self.setpointSpeedValue.setSuffix(" mph")
        self.regular_label(self.setpointSpeedValue)
        self.set_relative_right(self.setpointSpeedValue, self.setpointSpeedLabel, 10)
        self.set_relative_before_right_end(self.setpointSpeedValue, self.middleBox, 10)

        self.speedDivider = QLabel(self)
        self.line_label(self.speedDivider, True, self.middleBox.width())
        self.set_relative_below_left(self.speedDivider, self.setpointSpeedLabel, 10)

        # Lights section
        self.lightLabel = QLabel("Lights", self)
        self.regular_label(self.lightLabel)
        self.set_relative_below_right(self.lightLabel, self.speedDivider, 10)

        self.hltLabel = QLabel("Headlights", self)
        self.text_label(self.hltLabel)
        self.set_relative_below(self.hltLabel, self.lightLabel, 10)

        self.hltToggle = QPushButton(self)
        self.png_button(self.hltToggle, self.pixmapToggleOff)
        self.set_relative_right(self.hltToggle, self.hltLabel, 10)
        self.set_relative_before_right_end(self.hltToggle, self.middleBox, 10)
        self.hltToggle.setCheckable(True)
        self.hltToggle.clicked.connect(
            lambda: self.png_button_toggle(self.hltToggle, self.hltToggle.isChecked())
        )

        self.iltLabel = QLabel("Interior Lights", self)
        self.text_label(self.iltLabel)
        self.set_relative_below(self.iltLabel, self.hltLabel, 20)

        self.iltToggle = QPushButton(self)
        self.png_button(self.iltToggle, self.pixmapToggleOff)
        self.set_relative_right(self.iltToggle, self.iltLabel, 10)
        self.set_relative_before_right_end(self.iltToggle, self.middleBox, 10)
        self.iltToggle.setCheckable(True)
        self.iltToggle.clicked.connect(
            lambda: self.png_button_toggle(self.iltToggle, self.iltToggle.isChecked())
        )

        self.lightDivider = QLabel(self)
        self.line_label(self.lightDivider, True, self.middleBox.width())
        self.set_relative_below_left(self.lightDivider, self.iltLabel, 10)

        # Doors section
        self.doorLabel = QLabel("Doors", self)
        self.regular_label(self.doorLabel)
        self.set_relative_below_right(self.doorLabel, self.lightDivider, 10)

        self.leftDoorButton = QPushButton("Left", self)
        self.text_label(self.leftDoorButton)
        self.png_button(self.leftDoorButton, self.pixmapLDoorClosed)
        self.leftDoorButton.setCheckable(True)
        self.leftDoorButton.clicked.connect(
            lambda: self.left_door_toggle(
                self.leftDoorButton, self.leftDoorButton.isChecked()
            )
        )

        self.rightDoorButton = QPushButton("Right", self)
        self.text_label(self.rightDoorButton)
        self.png_button(self.rightDoorButton, self.pixmapRDoorClosed)
        self.rightDoorButton.setCheckable(True)
        self.set_relative_right(self.rightDoorButton, self.doorLabel, 10)
        self.set_relative_before_right_end(self.rightDoorButton, self.middleBox, 10)
        self.set_relative_left(self.leftDoorButton, self.rightDoorButton, 10)
        self.rightDoorButton.clicked.connect(
            lambda: self.right_door_toggle(
                self.rightDoorButton, self.rightDoorButton.isChecked()
            )
        )

        self.doorDivider = QLabel(self)
        self.line_label(self.doorDivider, True, self.middleBox.width())
        self.set_relative_below_left(self.doorDivider, self.doorLabel, 10)

        # Announcement section
        self.announcementLabel = QLabel("Announcement", self)
        self.text_label(self.announcementLabel)
        self.set_relative_below_right(self.announcementLabel, self.doorDivider, 10)

        self.announcementEdit = QLineEdit(self)
        self.text_label(self.announcementEdit)
        self.set_relative_below(self.announcementEdit, self.announcementLabel, 20)

        self.announcementCombo = QComboBox(self)
        self.text_label(self.announcementCombo)
        self.announcementCombo.addItem("Automatic")
        self.announcementCombo.addItem("Custom")
        self.announcementCombo.adjustSize()
        self.set_relative_right(self.announcementCombo, self.announcementLabel, 10)
        self.set_relative_before_right_end(self.announcementCombo, self.middleBox, 10)

        self.sendLabel = QPushButton(self)
        self.png_button(self.sendLabel, self.pixmapSend)
        self.sendLabel.adjustSize()
        self.set_relative_right(self.sendLabel, self.announcementEdit, 20)
        self.set_relative_before_right_end(self.sendLabel, self.middleBox, 10)
        self.announcementEdit.setFixedWidth(
            self.sendLabel.x() - self.middleBox.x() - 30
        )
        self.sendLabel.clicked.connect(lambda: self.send_announcement())

        self.announcementDivider = QLabel(self)
        self.line_label(self.announcementDivider, True, self.middleBox.width())
        self.set_relative_below_left(
            self.announcementDivider, self.announcementEdit, 10
        )

        # Setpoint temperature section
        self.setpointTempLabel = QLabel("Setpoint Temperature", self)
        self.text_label(self.setpointTempLabel)
        self.set_relative_below_right(
            self.setpointTempLabel, self.announcementDivider, 10
        )

        self.setpointTempVal = QSpinBox(self)
        self.text_label(self.setpointTempVal)
        self.setpointTempVal.setSuffix(" °F")
        self.setpointTempVal.adjustSize()
        self.set_relative_right(self.setpointTempVal, self.setpointTempLabel, 10)
        self.set_relative_before_right_end(self.setpointTempVal, self.middleBox, 10)

        self.tempDivider = QLabel(self)
        self.line_label(self.tempDivider, True, self.middleBox.width())
        self.set_relative_below_left(self.tempDivider, self.setpointTempLabel, 10)

        # AD section
        self.adLabel = QLabel("Advertisement", self)
        self.text_label(self.adLabel)
        self.set_relative_below_right(self.adLabel, self.tempDivider, 10)

        self.adCombo = QComboBox(self)
        self.text_label(self.adCombo)
        self.adCombo.addItem("Automatic")
        self.adCombo.addItem("1")
        self.adCombo.addItem("2")
        self.adCombo.addItem("3")
        self.adCombo.adjustSize()
        self.set_relative_right(self.adCombo, self.adLabel, 10)
        self.set_relative_before_right_end(self.adCombo, self.middleBox, 10)

        self.adDisplay = QLabel(self)
        self.adDisplay.setFixedWidth(self.middleBox.width() - 20)
        self.adDisplay.setFixedHeight(
            self.middleBox.y()
            + self.middleBox.height()
            - self.adLabel.y()
            - self.adLabel.height()
            - 30
        )
        self.adDisplay.setStyleSheet("border: 1px solid black")
        self.adDisplay.setMovie(self.movieMoneyAd)
        self.movieMoneyAd.start()
        self.set_relative_below(self.adDisplay, self.adLabel, 20)

        # Third Column
        # Display block
        self.displayLabel = QLabel("Display", self)
        self.header_label(self.displayLabel)
        self.set_relative_below(self.displayLabel, self.trainChangeBox, 20)

        self.displayBox = QLabel(self)
        self.box_label(self.displayBox, 348, 200)
        self.set_relative_below(self.displayBox, self.displayLabel, 35)

        self.trainIDLabel = QLabel("Train #: ", self)
        self.text_label(self.trainIDLabel)
        self.trainIDLabel.setFixedWidth(math.floor(self.displayBox.width() / 2))
        self.set_relative_below_right(self.trainIDLabel, self.displayBox, 10)

        self.currentTempLabel = QLabel(" °F", self)
        self.text_label(self.currentTempLabel)
        self.currentTempLabel.setFixedWidth(math.floor(self.displayBox.width() / 2))
        self.currentTempLabel.setAlignment(Qt.AlignRight)
        self.set_relative_right(self.currentTempLabel, self.trainIDLabel, 10)
        self.set_relative_before_right_end(self.currentTempLabel, self.displayBox, 10)

        self.prevStopLabel = QLabel("Prev Stop:\n ", self)
        self.text_label(self.prevStopLabel)
        self.prevStopLabel.setAlignment(Qt.AlignCenter)
        self.set_relative_below(self.prevStopLabel, self.trainIDLabel, 10)

        self.nextStopLabel = QLabel("Next Stop:\n ", self)
        self.text_label(self.nextStopLabel)
        self.nextStopLabel.setAlignment(Qt.AlignCenter)
        self.set_relative_right(self.nextStopLabel, self.prevStopLabel, 10)
        self.set_relative_before_right_end(self.nextStopLabel, self.displayBox, 10)

        self.originCircle = QLabel(self)
        self.originCircle.setGeometry(0, 0, 48, 48)
        self.originCircle.setStyleSheet(
            "border: 8px solid" + self.colorDarkBlue + "; border-radius: 24px"
        )
        self.set_relative_below_center(self.originCircle, self.prevStopLabel, 20)

        self.destinationCircle = QLabel(self)
        self.destinationCircle.setGeometry(0, 0, 48, 48)
        self.destinationCircle.setStyleSheet(
            "border: 8px solid" + self.colorDarkRed + "; border-radius: 24px"
        )
        self.set_relative_below_center(self.destinationCircle, self.nextStopLabel, 20)

        self.distanceLine = QLabel(self)
        self.distanceLine.setGeometry(
            0,
            0,
            self.destinationCircle.x()
            - self.originCircle.x()
            - self.originCircle.width(),
            8,
        )
        self.distanceLine.setStyleSheet("background-color:" + self.colorLightGrey)
        self.set_relative_right(self.distanceLine, self.originCircle, 0)

        self.travelledLine = QLabel(self)
        self.travelledLine.setGeometry(
            0,
            0,
            math.floor((self.destinationCircle.x() - self.originCircle.x()) * 0.5),
            8,
        )
        self.travelledLine.setStyleSheet("background-color: " + self.colorDarkBlue)
        self.set_relative_right(self.travelledLine, self.originCircle, 0)

        self.trainLabel = QLabel(self)
        self.trainLabel.setFixedSize(48, 48)
        self.png_label(self.trainLabel, self.pixmapTrain)
        self.set_relative_right(
            self.trainLabel, self.travelledLine, -1 * math.floor(48 / 532 * 532)
        )

        self.announceIcon = QLabel(self)
        self.text_label(self.announceIcon)
        self.png_label(self.announceIcon, self.pixmapAnnouncement)
        self.announceIcon.adjustSize()
        self.set_relative_below(self.announceIcon, self.originCircle, 10)

        self.announceVal = QLabel(self)
        self.text_label(self.announceVal)
        self.set_relative_right(self.announceVal, self.announceIcon, 20)

        self.displayBox.setFixedHeight(
            self.announceIcon.y()
            + self.announceIcon.height()
            + 10
            - self.displayBox.y()
        )

        # Statistic block
        self.commandedPowerBox = QLabel(self)
        self.box_label(self.commandedPowerBox, 138, 100)
        self.commandedPowerBox.move(
            self.displayBox.x() + self.displayBox.width() + 23, self.displayBox.y()
        )

        self.commandedPowerVal = QLabel(self)
        self.commandedPowerVal.setText("120000.000")
        self.regular_label(self.commandedPowerVal)
        self.commandedPowerVal.setAlignment(Qt.AlignCenter)
        self.commandedPowerVal.setText("0")
        self.set_relative_below_center(
            self.commandedPowerVal, self.commandedPowerBox, 10
        )
        self.commandedPowerVal.move(
            self.commandedPowerVal.x(), self.commandedPowerBox.y() + 10
        )

        self.wattsLabel = QLabel("Watts", self)
        self.text_label(self.wattsLabel)
        self.set_relative_below_center(self.wattsLabel, self.commandedPowerVal, 10)

        self.commandedPowerLabel = QLabel("Power\nCommand", self)
        self.regular_label(self.commandedPowerLabel)
        self.commandedPowerLabel.setAlignment(Qt.AlignCenter)
        self.set_relative_below_center(self.commandedPowerLabel, self.wattsLabel, 10)
        self.set_relative_below_center(self.commandedPowerLabel, self.wattsLabel, 10)

        self.commandedPowerBox.setFixedHeight(
            self.commandedPowerLabel.y()
            + self.commandedPowerLabel.height()
            + 10
            - self.commandedPowerBox.y()
        )

        self.currentSpeedBox = QLabel(self)
        self.box_label(self.currentSpeedBox, self.commandedPowerBox.width(), 100)
        self.set_relative_below(self.currentSpeedBox, self.commandedPowerBox, 20)

        self.currentSpeedVal = QLabel(self)
        self.currentSpeedVal.setText("8888")
        self.regular_label(self.currentSpeedVal)
        self.currentSpeedVal.setText("0")
        self.currentSpeedVal.setAlignment(Qt.AlignCenter)
        self.set_relative_below_center(self.currentSpeedVal, self.currentSpeedBox, 10)
        self.currentSpeedVal.move(
            self.currentSpeedVal.x(), self.currentSpeedBox.y() + 10
        )

        self.mphLabel = QLabel("mph", self)
        self.text_label(self.mphLabel)
        self.set_relative_below_center(self.mphLabel, self.currentSpeedVal, 10)

        self.currentSpeedLabel = QLabel("Current\nSpeed", self)
        self.regular_label(self.currentSpeedLabel)
        self.currentSpeedLabel.setAlignment(Qt.AlignCenter)
        self.set_relative_below_center(self.currentSpeedLabel, self.mphLabel, 10)

        self.suggestedSpeedLabel = QLabel("Suggested:  ", self)
        self.text_label(self.suggestedSpeedLabel)
        self.suggestedSpeedLabel.setStyleSheet("color: " + self.colorDarkGreen)
        self.set_relative_below_center(
            self.suggestedSpeedLabel, self.currentSpeedLabel, 10
        )

        self.speedLimitLabel = QLabel("Limit:  ", self)
        self.text_label(self.speedLimitLabel)
        self.speedLimitLabel.setStyleSheet("color: " + self.colorDarkRed)
        self.set_relative_below_center(
            self.speedLimitLabel, self.suggestedSpeedLabel, 10
        )

        self.currentSpeedBox.setFixedHeight(
            self.speedLimitLabel.y()
            + self.speedLimitLabel.height()
            + 10
            - self.currentSpeedBox.y()
        )

        self.authorityBox = QLabel(self)
        self.box_label(self.authorityBox, self.commandedPowerBox.width(), 100)
        self.set_relative_below(self.authorityBox, self.currentSpeedBox, 20)

        self.authorityVal = QLabel(self)
        self.authorityVal.setText("888888888")
        self.regular_label(self.authorityVal)
        self.authorityVal.setText("0")
        self.authorityVal.setAlignment(Qt.AlignCenter)
        self.set_relative_below_center(self.authorityVal, self.authorityBox, 10)
        self.authorityVal.move(self.authorityVal.x(), self.authorityBox.y() + 10)

        self.miLabel = QLabel("mi", self)
        self.text_label(self.miLabel)
        self.set_relative_below_center(self.miLabel, self.authorityVal, 10)

        self.authorityLabel = QLabel("Authority", self)
        self.regular_label(self.authorityLabel)
        self.set_relative_below_center(self.authorityLabel, self.miLabel, 10)

        self.authorityBox.setFixedHeight(
            self.authorityLabel.y()
            + self.authorityLabel.height()
            + 10
            - self.authorityBox.y()
        )
        # Failure block
        self.failLabel = QLabel("Status", self)
        self.header_label(self.failLabel)
        self.set_relative_below(self.failLabel, self.displayBox, 14)

        self.failBox = QLabel(self)
        self.box_label(self.failBox, self.displayBox.width(), 185)
        self.set_relative_below(self.failBox, self.failLabel, 20)

        self.xLabel = QLabel(self)
        self.png_label(self.xLabel, self.pixmapCircleX)
        self.xLabel.adjustSize()
        self.set_relative_below_right(self.xLabel, self.failBox, 10)

        self.nonfunctionalLabel = QLabel("= Nonfunctional", self)
        self.text_label(self.nonfunctionalLabel)
        self.set_relative_right(self.nonfunctionalLabel, self.xLabel, 10)

        self.checkLabel = QLabel(self)
        self.png_label(self.checkLabel, self.pixmapCircleCheck)
        self.checkLabel.adjustSize()
        self.set_relative_right(self.checkLabel, self.nonfunctionalLabel, 20)

        self.functionalLabel = QLabel("= Functional", self)
        self.text_label(self.functionalLabel)
        self.set_relative_right(self.functionalLabel, self.checkLabel, 10)

        self.failDivider = QLabel(self)
        self.line_label(self.failDivider, True, self.failBox.width())
        self.set_relative_below_left(self.failDivider, self.xLabel, 10)

        self.signalFailLabel = QLabel("Signal Pickup", self)
        self.regular_label(self.signalFailLabel)
        self.set_relative_below_right(self.signalFailLabel, self.failDivider, 10)
        self.signalFailLabel.move(
            self.signalFailLabel.x(), self.signalFailLabel.y() + 10
        )

        self.signalFailStatus = QLabel(self)
        self.png_label(self.signalFailStatus, self.pixmapCircleCheck)
        self.signalFailStatus.adjustSize()
        self.set_relative_right(self.signalFailStatus, self.signalFailLabel, 20)
        self.set_relative_before_right_end(self.signalFailStatus, self.failBox, 10)

        self.engineFailLabel = QLabel("Train Engine", self)
        self.regular_label(self.engineFailLabel)
        self.set_relative_below(self.engineFailLabel, self.signalFailLabel, 20)

        self.engineFailStatus = QLabel(self)
        self.png_label(self.engineFailStatus, self.pixmapCircleCheck)
        self.engineFailStatus.adjustSize()
        self.set_relative_right(self.engineFailStatus, self.engineFailLabel, 20)
        self.set_relative_before_right_end(self.engineFailStatus, self.failBox, 10)

        self.brakeFailLabel = QLabel("Brake", self)
        self.regular_label(self.brakeFailLabel)
        self.set_relative_below(self.brakeFailLabel, self.engineFailLabel, 20)

        self.brakeFailStatus = QLabel(self)
        self.png_label(self.brakeFailStatus, self.pixmapCircleCheck)
        self.brakeFailStatus.adjustSize()
        self.set_relative_right(self.brakeFailStatus, self.brakeFailLabel, 20)
        self.set_relative_before_right_end(self.brakeFailStatus, self.failBox, 10)

        self.failBox.setFixedHeight(
            self.brakeFailStatus.y() + 32 + 20 - self.failBox.y()
        )

        self.changeButton.clicked.connect(lambda: self.change_train())

        self.timer = QTimer(self)
        self.timer.timeout.connect(
            self.update
        )  # Connect the timer to the update_text function
        self.timer.start(
            self.tcVariables["samplePeriod"]
        )  # Update the text every 1000 milliseconds (1 second)

        self.sysTime = QDateTime.currentDateTime()
        self.sysTime.setTime(QTime(0, 0, 0))

    def update(self):
        # Update Train ID list
        # from test bench
        for train in self.testWindow.testbenchVariables["trainList"]:
            idCheck = False
            for i in self.tcVariables["trainList"]:
                if i == train:
                    idCheck = True
            if not idCheck:
                self.tcVariables["trainList"].append(train)

        # from CTC
        masterSignals.addTrain.connect(lambda: self.signal_addTrain)

        if self.trainLineCombo.currentText() == "red":
            self.trainNumberCombo.clear()

            for train in self.tcVariables["trainList"]:
                if isinstance(train, dict) and "red" in train:
                    self.trainNumberCombo.addItem(train["red"])

        if self.trainLineCombo.currentText() == "green":
            self.trainNumberCombo.clear()

            for train in self.tcVariables["trainList"]:
                if isinstance(train, dict) and "green" in train:
                    self.trainNumberCombo.addItem(train["green"])

        updatedTrainList = []
        for train in self.tcVariables["trainList"]:
            if isinstance(train, dict):
                for key, value in train.items():
                    updatedTrainList.append(key + "_" + value)

        self.testWindow.refresh_train_list(updatedTrainList, self.tcFunctions.trainList)

        for name in updatedTrainList:
            idCheck2 = False
            for train in self.tcFunctions.trainList:
                if train.get_trainID() == name:
                    idCheck2 = True
            if not idCheck2:
                self.tcFunctions.add_train(Train(name))

        # Update Train ID and attributes
        self.trainIDLabel.setText("Train #: " + self.tcVariables["trainID"])

        # SIGNAL INTEGRATION: TM -> TCSW
        trainModelToTrainController.sendSpeedLimit.connect(self.signal_speedLimit)
        trainModelToTrainController.sendAuthority.connect(self.signal_authority)
        trainModelToTrainController.sendLeftDoor.connect(self.signal_leftDoor)
        trainModelToTrainController.sendRightDoor.connect(self.signal_rightDoor)
        trainModelToTrainController.sendNextStation1.connect(self.signal_nextStation1)
        trainModelToTrainController.sendNextStation2.connect(self.signal_nextStation2)
        trainModelToTrainController.sendCurrStation.connect(self.signal_currStation)
        trainModelToTrainController.sendCommandedSpeed.connect(
            self.signal_commandedSpeed
        )
        trainModelToTrainController.sendCurrentSpeed.connect(self.signal_currSpeed)
        trainModelToTrainController.sendTemperature.connect(self.signal_currTemp)
        trainModelToTrainController.sendPassengerEmergencyBrake.connect(
            self.signal_paxEbrake
        )
        trainModelToTrainController.sendEngineFailure.connect(self.signal_engineFail)
        trainModelToTrainController.sendSignalPickupFailure.connect(
            self.signal_signalFail
        )
        trainModelToTrainController.sendBrakeFailure.connect(self.signal_brakeFail)
        trainModelToTrainController.sendPolarity.connect(self.signal_polarity)

        for train in self.tcFunctions.trainList:
            if train.get_trainID() == self.tcVariables["trainID"]:
                # TRAIN MODEL INPUTS
                # current temp
                self.currentTempLabel.setText(str(train.get_currentTemp()) + " °F")

                # speed limit
                self.speedLimitLabel.setText("Limit: " + str(train.get_speedLimit()))
                self.speedLimitLabel.adjustSize()

                # authority
                if not train.get_authority:
                    self.authorityVal.setText(
                        str(
                            math.floor(
                                self.tcFunctions.distance_between(
                                    self.tcFunctions.blockDict,
                                    train.block["blockNumber"],
                                    self.tcFunctions.find_block(
                                        self.tcFunctions.blockDict, train.nextStop
                                    ),
                                )
                                / 1609
                            )
                        )
                    )
                else:
                    self.authorityVal.setText(
                        str(math.floor(train.block["blockLength"] / 1609))
                    )
                self.authorityVal.setAlignment(Qt.AlignCenter)

                # commanded speed
                self.suggestedSpeedLabel.setText(
                    "Suggested: " + str(train.get_commandedSpeed())
                )
                self.suggestedSpeedLabel.adjustSize()

                # current speed
                self.currentSpeedVal.setText(str(train.get_currentSpeed()))
                self.currentSpeedVal.setAlignment(Qt.AlignCenter)

                # failures
                if train.get_engineFailure():
                    self.png_label(self.engineFailStatus, self.pixmapCircleX)
                else:
                    self.png_label(self.engineFailStatus, self.pixmapCircleCheck)

                if train.get_brakeFailure():
                    self.png_label(self.brakeFailStatus, self.pixmapCircleX)
                else:
                    self.png_label(self.brakeFailStatus, self.pixmapCircleCheck)

                if train.get_signalFailure():
                    self.png_label(self.signalFailStatus, self.pixmapCircleX)
                else:
                    self.png_label(self.signalFailStatus, self.pixmapCircleCheck)

                # passenger brake
                if train.get_paxEbrake():
                    self.emergencyBrakeButton.setChecked(True)

                # setpoint speed range
                self.setpointSpeedValue.setRange(0, train.get_speedLimit())

                # ENGINEER INPUTS
                train.set_kp(self.kpEdit.value())
                train.set_ki(self.kiEdit.value())

                # TRAIN DRIVER INPUTS
                if self.modeCombo.currentIndex() == 0:
                    train.set_auto(True)
                else:
                    train.set_auto(False)

                # automatic
                if train.get_auto():
                    # temporary re-enable
                    self.serviceBrakeSlider.setDisabled(False)
                    self.setpointSpeedValue.setDisabled(False)
                    self.hltToggle.setDisabled(False)
                    self.iltToggle.setDisabled(False)
                    self.leftDoorButton.setDisabled(False)
                    self.rightDoorButton.setDisabled(False)
                    self.announcementCombo.setDisabled(False)
                    self.setpointTempVal.setDisabled(False)
                    self.adCombo.setDisabled(False)

                    self.tcFunctions.automatic_operations(train)

                    self.announcementCombo.setCurrentIndex(0)

                    self.setpointTempVal.setValue(train.get_setpointTemp())

                    self.adCombo.setCurrentIndex(0)

                    if train.get_headlights():
                        self.hltToggle.setChecked(True)
                        self.png_button(self.hltToggle, self.pixmapToggleOn)
                    else:
                        self.hltToggle.setChecked(False)
                        self.png_button(self.hltToggle, self.pixmapToggleOff)

                    if train.get_interiorLights():
                        self.iltToggle.setChecked(True)
                        self.png_button(self.iltToggle, self.pixmapToggleOn)
                    else:
                        self.iltToggle.setChecked(False)
                        self.png_button(self.iltToggle, self.pixmapToggleOff)

                    if train.get_leftDoor():
                        self.leftDoorButton.setChecked(True)
                        self.png_button(self.leftDoorButton, self.pixmapLDoorOpen)
                    else:
                        self.leftDoorButton.setChecked(False)
                        self.png_button(self.leftDoorButton, self.pixmapLDoorClosed)

                    if train.get_rightDoor():
                        self.rightDoorButton.setChecked(True)
                        self.png_button(self.rightDoorButton, self.pixmapRDoorOpen)
                    else:
                        self.rightDoorButton.setChecked(False)
                        self.png_button(self.rightDoorButton, self.pixmapRDoorClosed)

                    # disable some stuff
                    self.serviceBrakeSlider.setDisabled(True)
                    self.setpointSpeedValue.setDisabled(True)
                    self.hltToggle.setDisabled(True)
                    self.iltToggle.setDisabled(True)
                    self.leftDoorButton.setDisabled(True)
                    self.rightDoorButton.setDisabled(True)
                    self.announcementCombo.setDisabled(True)
                    self.announcementEdit.setDisabled(True)
                    self.sendLabel.setDisabled(True)
                    self.setpointTempVal.setDisabled(True)
                    self.adCombo.setDisabled(True)

                # manual
                else:
                    self.serviceBrakeSlider.setDisabled(False)
                    self.setpointSpeedValue.setDisabled(False)
                    self.hltToggle.setDisabled(False)
                    self.iltToggle.setDisabled(False)
                    self.leftDoorButton.setDisabled(False)
                    self.rightDoorButton.setDisabled(False)
                    self.announcementCombo.setDisabled(False)
                    self.setpointTempVal.setDisabled(False)
                    self.adCombo.setDisabled(False)

                    # an individual automatic
                    if self.announcementCombo.currentIndex() == 0:
                        print(
                            f'{not train.get_authority()}, {train.block["isStation"]}, {train.get_currentSpeed() == 0}'
                        )
                        if (
                            (not train.get_authority())
                            and (train.block["isStation"])
                            and (train.get_currentSpeed() == 0)
                        ):
                            train.set_announcement(
                                "This is " + train.beacon["currStop"] + "."
                            )
                        else:
                            train.set_announcement("")

                        self.announcementEdit.setDisabled(True)
                        self.sendLabel.setDisabled(True)
                    else:
                        train.set_announcement(self.tcVariables["customAnnouncement"])
                        self.announcementEdit.setDisabled(False)
                        self.sendLabel.setDisabled(False)

                    # updating train object driver inputs
                    train.set_driverSbrake(self.serviceBrakeSlider.value() * 0.01)

                    train.set_setpointSpeed(self.setpointSpeedValue.value())

                    if self.hltToggle.isChecked():
                        train.set_headlights(True)
                    else:
                        train.set_headlights(False)

                    if self.iltToggle.isChecked():
                        train.set_interiorLights(True)
                    else:
                        train.set_interiorLights(False)

                    if self.leftDoorButton.isChecked():
                        train.set_leftDoor(True)
                    else:
                        train.set_leftDoor(False)

                    if self.rightDoorButton.isChecked():
                        train.set_rightDoor(True)
                    else:
                        train.set_rightDoor(False)

                    train.set_setpointTemp(self.setpointTempVal.value())

                    if self.adCombo.currentIndex() == 0:
                        self.tcFunctions.advertisement_rotation(train)
                    else:
                        train.set_advertisement(self.adCombo.currentIndex())

                # regardless of automatic
                self.tcFunctions.regular_operations(self.tcFunctions.blockDict, train)

                if self.emergencyBrakeButton.isChecked():
                    train.set_driverEbrake(True)
                else:
                    train.set_driverEbrake(False)

                # reset passenger ebrake
                train.set_paxEbrake(False)

                # updating display
                self.announceVal.setText(train.get_announcement())
                self.announceVal.adjustSize()
                self.announceVal.setAlignment(Qt.AlignLeft)

                self.nextStopLabel.setText("Next Stop:\n" + train.nextStop)
                self.nextStopLabel.setAlignment(Qt.AlignRight)
                self.nextStopLabel.adjustSize()

                self.prevStopLabel.setText("Prev Stop:\n" + train.prevStop)
                self.prevStopLabel.setAlignment(Qt.AlignLeft)
                self.prevStopLabel.adjustSize()

                if train.get_interiorLights() and train.get_headlights():
                    self.png_label(self.trainLabel, self.pixmapTrainLts)
                elif train.get_interiorLights():
                    self.png_label(self.trainLabel, self.pixmapTrainIlt)
                elif train.get_headlights():
                    self.png_label(self.trainLabel, self.pixmapTrainHlt)
                else:
                    self.png_label(self.trainLabel, self.pixmapTrain)

                self.commandedPowerVal.setText(str(train.get_powerCommand()))
                self.commandedPowerVal.setAlignment(Qt.AlignCenter)

                self.travelledLine.setFixedWidth(
                    math.floor(
                        (self.destinationCircle.x() - self.originCircle.x())
                        * train.distanceRatio
                    )
                )

                self.set_relative_right(
                    self.trainLabel, self.travelledLine, -1 * math.floor(48 / 532 * 532)
                )

                if self.adCombo.currentIndex() == 0:
                    self.tcFunctions.advertisement_rotation(train)

                if train.get_advertisement() == 1:
                    self.png_label(self.adDisplay, self.pixmapAd1)
                elif train.get_advertisement() == 2:
                    self.png_label(self.adDisplay, self.pixmapAd2)
                elif train.get_advertisement() == 3:
                    self.png_label(self.adDisplay, self.pixmapAd3)

                # SIGNAL INTEGRATION: TCSW -> TM
                trainControllerSWToTrainModel.sendPower.emit(
                    train.get_trainID(), train.get_powerCommand()
                )
                trainControllerSWToTrainModel.sendDriverEmergencyBrake.emit(
                    train.get_trainID(), train.get_driverEbrake()
                )
                trainControllerSWToTrainModel.sendDriverServiceBrake.emit(
                    train.get_trainID(), train.get_driverSbrake()
                )
                trainControllerSWToTrainModel.sendAnnouncement.emit(
                    train.get_trainID(), train.get_announcement()
                )
                trainControllerSWToTrainModel.sendHeadlightState.emit(
                    train.get_trainID(), train.get_headlights()
                )
                trainControllerSWToTrainModel.sendInteriorLightState.emit(
                    train.get_trainID(), train.get_interiorLights()
                )
                trainControllerSWToTrainModel.sendLeftDoorState.emit(
                    train.get_trainID(), train.get_leftDoor()
                )
                trainControllerSWToTrainModel.sendRightDoorState.emit(
                    train.get_trainID(), train.get_rightDoor()
                )
                trainControllerSWToTrainModel.sendSetpointTemperature.emit(
                    train.get_trainID(), train.get_setpointTemp()
                )
                trainControllerSWToTrainModel.sendAdvertisement.emit(
                    train.get_trainID(), train.get_advertisement()
                )

                # test emit
                trainControllerSWToTrainModel.sendPower.connect(self.test_display)

        # system time
        # self.sysTime = self.sysTime.addSecs(1)
        masterSignals.timingMultiplier.connect(self.signal_period)
        self.tcFunctions.set_samplePeriod(self.tcVariables["samplePeriod"])

        masterSignals.clockSignal.connect(self.sysTime.setTime)

        self.systemTimeInput.setText(self.sysTime.toString("HH:mm:ss"))
        self.systemSpeedInput.setText(
            "x" + format(1 / (self.tcVariables["samplePeriod"] / 1000), ".3f")
        )
        self.timer.setInterval(self.tcVariables["samplePeriod"])

        hours, minutes, seconds = map(int, self.systemTimeInput.text().split(":"))
        self.tcFunctions.time = hours * 3600 + minutes * 60 + seconds

        #print(self.sysTime.toString("HH:mm:ss"))

    def signal_addTrain(self, line, id):
        train = {line: id}
        idCheck = False
        for i in self.tcVariables["trainList"]:
            if i == train:
                idCheck = True
        if not idCheck:
            self.tcVariables["trainList"].append(train)

    def signal_period(self, period):
        self.tcVariables["samplePeriod"] = period
        return

    def signal_speedLimit(self, id, speedLimit):
        for train in self.tcVariables["trainList"]:
            if train.get_trainID() == id:
                train.set_speedLimit(speedLimit)
        return

    def signal_authority(self, id, authority):
        for train in self.tcVariables["trainList"]:
            if train.get_trainID() == id:
                train.set_authority(authority)
        return

    def signal_leftDoor(self, id, leftStation):
        for train in self.tcVariables["trainList"]:
            if train.get_trainID() == id:
                train.beacon["leftStation"] = leftStation
        return

    def signal_rightDoor(self, id, rightStation):
        for train in self.tcVariables["trainList"]:
            if train.get_trainID() == id:
                train.beacon["rightStation"] = rightStation
        return

    def signal_nextStation1(self, id, nextStation):
        for train in self.tcVariables["trainList"]:
            if train.get_trainID() == id:
                train.beacon["nextStop"][0] = nextStation
        return

    def signal_nextStation2(self, id, nextStation):
        for train in self.tcVariables["trainList"]:
            if train.get_trainID() == id:
                train.beacon["nextStop"][1] = nextStation
        return

    def signal_currStation(self, id, currStation):
        for train in self.tcVariables["trainList"]:
            if train.get_trainID() == id:
                train.beacon["currStop"] = currStation
        return

    def signal_commandedSpeed(self, id, commandedSpeed):
        for train in self.tcVariables["trainList"]:
            if train.get_trainID() == id:
                train.set_commandedSpeed(commandedSpeed)
        return

    def signal_currSpeed(self, id, currSpeed):
        for train in self.tcVariables["trainList"]:
            if train.get_trainID() == id:
                train.set_currentSpeed(currSpeed)
        return

    def signal_currTemp(self, id, currTemp):
        for train in self.tcVariables["trainList"]:
            if train.get_trainID() == id:
                train.set_currentTemp(currTemp)
        return

    def signal_paxEbrake(self, id, status):
        for train in self.tcVariables["trainList"]:
            if train.get_trainID() == id:
                train.set_paxEbrake(status)
        return

    def signal_engineFail(self, id, status):
        for train in self.tcVariables["trainList"]:
            if train.get_trainID() == id:
                train.set_engineFailure(status)
        return

    def signal_signalFail(self, id, status):
        for train in self.tcVariables["trainList"]:
            if train.get_trainID() == id:
                train.set_signalFailure(status)
        return

    def signal_brakeFail(self, id, status):
        for train in self.tcVariables["trainList"]:
            if train.get_trainID() == id:
                train.set_brakeFailure(status)
        return

    def signal_polarity(self, id, state):
        for train in self.tcVariables["trainList"]:
            if train.get_trainID() == id:
                train.polarity = state
        return

    def test_display(self, id, power):
        # print(f"ID: {id} Power: {power}")
        return

    def speed_up(self):
        self.tcVariables["samplePeriod"] = int(self.tcVariables["samplePeriod"] / 10)
        if self.tcVariables["samplePeriod"] == 0:
            self.tcVariables["samplePeriod"] = 1
        return

    def slow_down(self):
        self.tcVariables["samplePeriod"] = int(self.tcVariables["samplePeriod"] * 10)
        if self.tcVariables["samplePeriod"] >= 10000:
            self.tcVariables["samplePeriod"] = 10000
        return

    def change_train(self):
        if self.trainNumberCombo.currentText() == "":
            return
        self.tcVariables["trainID"] = (
            self.trainLineCombo.currentText()
            + "_"
            + self.trainNumberCombo.currentText()
        )

    def send_announcement(self):
        self.tcVariables["customAnnouncement"] = self.announcementEdit.text()

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

    def png_button_toggle(self, button, checked):
        if checked:
            self.png_button(button, self.pixmapToggleOn)
        else:
            self.png_button(button, self.pixmapToggleOff)

    def left_door_toggle(self, button, checked):
        if checked:
            self.png_button(button, self.pixmapLDoorOpen)
        else:
            self.png_button(button, self.pixmapLDoorClosed)

    def right_door_toggle(self, button, checked):
        if checked:
            self.png_button(button, self.pixmapRDoorOpen)
        else:
            self.png_button(button, self.pixmapRDoorClosed)
            self.png_button(button, self.pixmapRDoorClosed)
