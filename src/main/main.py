import sys
import math
import time
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtGui

from TrackController.trackcontrol import TrackControl
from TrainControllerSW.tcsw_ui import *
from TrackModel.track_model import TrackModel
from CTC.CTC_UI import *
from TrainModel.Train_Model import TrainModel
from TrainModel.Train_Model import TrainModel


class MainWindow(QMainWindow):
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

    moduleName = "Pittsburgh MTA"

    def __init__(self):
        super().__init__()

        # Initialize all the different modules
        trackControl = TrackControl()
        trackControl.ui.hide()
        self.trainControllerSW = TrainControllerUI()
        #trackModel = TrackModel()
        ctc = CTCWindow()
        #trainModel = TrainModel()
        

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
        self.titleLabel.setGeometry(90, 35, 790, 43)
        self.titleLabel.adjustSize()
        self.titleLabel.setStyleSheet("color: white")

        # logo
        self.pixmapMTALogo = QtGui.QPixmap("src/main/MTA_NYC_logo.png")
        self.pixmapMTALogo = self.pixmapMTALogo.scaled(
            math.floor(1862 * 0.25), math.floor(2046 * 0.25)
        )
        self.logo = QLabel(self)
        self.logo.setPixmap(self.pixmapMTALogo)
        self.logo.adjustSize()
        self.logo.move(
            20, math.floor(self.bodyBlock.height() / 2 - self.logo.height() / 2)
        )
        self.logo.show()

        self.box1 = QPushButton("Track Model", self)
        self.box_button(self.box1, 200, 200)
        self.set_relative_right(self.box1, self.logo, 20)
        #self.box1.clicked.connect(lambda: trackModel.mainWindow.show())

        self.box2 = QPushButton("Train Model", self)
        self.box_button(self.box2, self.box1.width(), self.box1.height())
        self.set_relative_right(self.box2, self.box1, 20)
        #self.box2.clicked.connect(lambda: trainModel.show_gui())
    

        self.box3 = QPushButton("CTC", self)
        self.box_button(self.box3, self.box1.width(), self.box1.height())
        self.set_relative_below(self.box3, self.box1, -20 - self.box1.height() * 2)
        self.box3.clicked.connect(lambda: ctc.show())

        self.box4 = QPushButton("Track Controller", self)
        self.box_button(self.box4, self.box1.width(), self.box1.height())
        self.set_relative_right(self.box4, self.box3, 20)
        self.box4.clicked.connect(lambda: trackControl.show_gui())

        self.box5 = QPushButton("Train Controller\nSW", self)
        self.box_button(self.box5, self.box1.width(), self.box1.height())
        self.set_relative_below(self.box5, self.box1, 20)
        self.box5.clicked.connect(lambda: self.trainControllerSW.show())

        self.box6 = QPushButton("Train Controller\nHW", self)
        self.box_button(self.box6, self.box1.width(), self.box1.height())
        self.set_relative_right(self.box6, self.box5, 20)

        self.show()

    def box_button(self, button, width, height):
        button.setGeometry(0, 0, width, height)
        button.setStyleSheet(
            "color: "
            + self.colorDarkBlue
            + "; background-color: "
            + self.colorLightGrey
        )

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

    def set_relative_below(self, child, parent, pad):
        child.move(parent.x(), parent.y() + parent.height() + pad)

    def set_relative_right(self, child, parent, pad):
        child.move(
            parent.x() + parent.width() + pad,
            parent.y() + math.floor((parent.height() - child.height()) / 2.0),
        )


# create app
app = QApplication(sys.argv)

# create window instance
window = MainWindow()

app.setWindowIcon(QIcon("src/main/MTA_NYC_logo.png"))

# run app
app.exec()
