# this is the file that will contain the code for the main window which gives block information
import sys
import ast
import os
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *  # QPainter, QPen, QColor, QFont, QPixmap, QLine
from PyQt5.QtCore import Qt, pyqtSignal, QTimer, QDateTime
from PyQt5.uic import loadUi
from .testbench import UiMainWindow

app = QApplication(sys.argv)

modeChanged = pyqtSignal(bool)  # Custom signal to indicate mode change
switchCrossChanged = pyqtSignal(
    bool
)  # Custom signal to indicate change of switch or crossing state done manually
lightChanged = pyqtSignal(
    str
)  # Custom signal to indicate change of light state done manually


####################################################################################################
def create_text_label(text, x, y, fontSize):
    label = QLabel(text)
    font = QFont("Segoe UI", fontSize)  # Use the Segoe UI font with the specified size
    label.setFont(font)
    label.setGeometry(
        x, y, int(len(text) * 10 * (fontSize / 10)), fontSize * 2
    )  # Adjust the width based on the text length and font size
    return label


########################################### UI Classes  ############################################
####################################################################################################


class SimulationSpeed(QWidget):
    def __init__(self):
        super().__init__()
        self.simulationSpeed = 1.0

    def set_simulationspeed_controls(self, parentWindow):
        simulationspeedText = QLabel("Simulation Speed:", parentWindow)
        simulationspeedText.setGeometry(900 - 160, 890, 170, 30)
        simulationspeedText.setStyleSheet("font-weight: bold; font-size: 18px")

        self.speedText = QLabel("1.0x", parentWindow)
        self.speedText.setGeometry(1110 - 160, 890, 40, 30)
        self.speedText.setAlignment(Qt.AlignCenter)
        self.speedText.setStyleSheet("font-weight: bold; font-size: 18px")

        decreaseSpeed = QPushButton("<<", parentWindow)
        decreaseSpeed.setGeometry(1070 - 160, 895, 30, 20)
        decreaseSpeed.clicked.connect(self.decrease_simulationspeed)

        increaseSpeed = QPushButton(">>", parentWindow)
        increaseSpeed.setGeometry(1160 - 160, 895, 30, 20)
        increaseSpeed.clicked.connect(self.increase_simulationspeed)

    def decrease_simulationspeed(self):
        # Speed cannot go below 0.5
        if self.simulationSpeed > 0.5:
            self.simulationSpeed -= 0.5
            self.speedText.setText(f"{self.simulationSpeed}x")

    def increase_simulationspeed(self):
        if self.simulationSpeed < 5.0:
            self.simulationSpeed += 0.5
            self.speedText.setText(f"{self.simulationSpeed}x")


class MainBox(QWidget):
    def __init__(self):
        super().__init__()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Define the rectangle's properties
        rectX = 0
        rectY = 0
        rectWidth = 600
        rectHeight = 675
        rectColor = QColor(255, 255, 255)  # White

        # Draw the rectangle
        painter.setBrush(rectColor)
        painter.drawRect(rectX, rectY, rectWidth, rectHeight)


class OccupancyBox(QWidget):
    def __init__(self):
        super().__init__()

        # Create a table widget with 3 columns
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(["Block #", "Block Type", "Failure"])
        self.tableWidget.setGeometry(
            0, 50, 265, 625
        )  # Adjust the size and position as needed
        self.tableWidget.setParent(self)
        # Hide the vertical header (row numbers) and horiz header (column)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setVisible(False)
        # Customize the column widths
        self.tableWidget.setColumnWidth(
            0, 100
        )  # Set the width of the first column to 100 pixels
        self.tableWidget.setColumnWidth(
            1, 100
        )  # Set the width of the second column to 150 pixels
        self.tableWidget.setColumnWidth(
            2, 65
        )  # Set the width of the third column to 100 pixels
        # Enable sorting based on the first column (Block #)
        self.tableWidget.setSortingEnabled(True)

    def populate_table(self, data):
        # Set the number of rows in the table
        self.tableWidget.setRowCount(len(data))

        # Populate the table with data
        for rowIndex, rowData in enumerate(data):
            for colIndex, colData in enumerate(rowData):
                item = QTableWidgetItem(str(colData))

                # Make the item read-only
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)

                self.tableWidget.setItem(rowIndex, colIndex, item)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Define the rectangle's properties
        rectX = 0
        rectY = 0
        rectWidth = 265
        rectHeight = 600
        rectColor = QColor(255, 255, 255)  #
        # Draw the rectangle
        painter.setBrush(rectColor)
        painter.drawRect(rectX, rectY, rectWidth, rectHeight)
        # horizontal line
        painter.drawLine(0, 50, 265, 50)
        # vertical line 1
        painter.drawLine(100, 0, 100, 600)
        # vertical line 2
        painter.drawLine(200, 0, 200, 600)

    def add_item(self, blockNumber, blockType, failure):
        rowCount = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowCount)

        itemData = [blockNumber, blockType, failure]
        for colIndex, colData in enumerate(itemData):
            item = QTableWidgetItem(str(colData))
            item.setFlags(item.flags() ^ Qt.ItemIsEditable)
            self.tableWidget.setItem(rowCount, colIndex, item)

    def remove_item_by_blocknumber(self, blockNumber):
        for rowIndex in range(self.tableWidget.rowCount()):
            item = self.tableWidget.item(
                rowIndex, 0
            )  # Assuming block number is in the first column
            rowBlockNumber = item.text()[6:]
            if int(rowBlockNumber) == blockNumber:
                self.tableWidget.removeRow(rowIndex)
                return

    def does_block_and_state_exist(self, blockNumber, blockState):
        for rowIndex in range(self.tableWidget.rowCount()):
            blockNumberItem = self.tableWidget.item(
                rowIndex, 0
            )  # Assuming block number is in the first column
            blockStateItem = self.tableWidget.item(
                rowIndex, 2
            )  # Assuming block failure state is in the second column

            blockNumberString = blockNumberItem.text()[6:]
            if blockNumberItem and blockStateItem:
                if (
                    int(blockNumberString) == blockNumber
                    and ast.literal_eval(blockStateItem.text()) == blockState
                ):
                    return True

        return False

    def does_block_exist(self, blockNumber, blockState):
        for rowIndex in range(self.tableWidget.rowCount()):
            blockNumberItem = self.tableWidget.item(
                rowIndex, 0
            )  # Assuming block number is in the first column
            blockStateItem = self.tableWidget.item(
                rowIndex, 2
            )  # Assuming block failure state is in the second column

            blockNumberString = blockNumberItem.text()[6:]
            if blockNumberItem and blockStateItem:
                if int(blockNumberString) == blockNumber:
                    return True

        return False

    def clear_table(self):
        self.tableWidget.clearContents()


class ModeButton(QPushButton):
    modeChanged = pyqtSignal(bool)  # Custom signal to indicate mode change

    def __init__(self):
        super().__init__()
        self.clicked.connect(self.on_button_click)
        self.defaultText = "Automatic Mode"
        self.mode = True
        self.defaultColor = QColor(0, 255, 0)  # Green
        self.clickedColor = QColor(255, 0, 0)  # Red
        self.change_button_style()
        self.setText(self.defaultText)

    def get_mode(self):
        return self.mode

    def on_button_click(self):
        if self.text() == self.defaultText:
            self.setText("Manual Mode")
            self.change_button_style(clicked=True)
            self.mode = False
        else:
            self.setText(self.defaultText)
            self.change_button_style(clicked=False)
            self.mode = True

        self.modeChanged.emit(self.mode)

    def change_button_style(self, clicked=False):
        if clicked:
            self.setStyleSheet(
                f"background-color: {self.clickedColor.name()}; color: white;"
            )
            self.setFont(QFont("Segoe UI", 15, QFont.Bold))
        else:
            self.setStyleSheet(
                f"background-color: {self.defaultColor.name()}; color: black;"
            )
            self.setFont(QFont("Segoe UI", 15, QFont.Bold))

    def set_button_style(self, newMode):
        if newMode == True:
            self.setText(self.defaultText)
            self.setStyleSheet(
                f"background-color: {self.defaultColor.name()}; color: black;"
            )
            self.setFont(QFont("Segoe UI", 15, QFont.Bold))
        else:
            self.setText("Manual Mode")
            self.setStyleSheet(
                f"background-color: {self.clickedColor.name()}; color: white;"
            )
            self.setFont(QFont("Segoe UI", 15, QFont.Bold))


class MapButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.clicked.connect(self.on_button_click)
        self.defaultColor = QColor(255, 255, 255)  # White
        self.setText("Open Map")
        self.setFont(QFont("Segoe UI", 15, QFont.Bold))
        self.setStyleSheet(
            f"background-color: {self.defaultColor.name()}; color: black;"
        )
        self.mapWindow = None  # initialize map window attribute

    def on_button_click(self, line):
        if self.mapWindow is None:
            self.mapWindow = MapWindow()
            self.mapWindow.setWindowFlags(
                self.mapWindow.windowFlags() | Qt.WindowStaysOnTopHint
            )
            self.mapWindow.set_map(line)

        self.mapWindow.show()


class MapWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Map Window")
        self.setGeometry(200, 50, 500, 300)

        # Create a QLabel to display the map image
        self.mapLabel = QLabel()
        pixmapGreenLine = QPixmap("src/main/TrackController/images/green_map.png")
        self.scaledPixmapGreenLine = pixmapGreenLine.scaled(900, 200)

        pixmapGreenLine = QPixmap("src/main/TrackController/images/red_map.png")
        self.scaledPixmapRedLine = pixmapGreenLine.scaled(900, 200)

        # Add the QLabel to the main window's central widget
        centralWidget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.mapLabel)
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

    def set_map(self, line):
        if line == 1:
            self.mapLabel.setPixmap(self.scaledPixmapGreenLine)
        else:
            self.mapLabel.setPixmap(self.scaledPixmapRedLine)


class Clock(QWidget):
    def set_clock(self, parentWindow):
        self.clock = QLabel("System Clock: 00:00:00", parentWindow)
        self.clock.setGeometry(760, 920, 220, 30)
        self.clock.setStyleSheet("font-weight: bold; font-size: 18px")
        self.currentTime = "00:00:00"
        self.update_clock()

        # Update clock in real time while window is open
        timer = QTimer(parentWindow)
        timer.timeout.connect(self.update_clock)
        # Update every 1 second
        timer.start(1000)

    def update_clock(self):
        # Increment the time by 1 second
        hours, minutes, seconds = map(int, self.currentTime.split(":"))
        seconds += 1
        if seconds == 60:
            seconds = 0
            minutes += 1
            if minutes == 60:
                minutes = 0
                hours += 1
                if hours == 24:
                    hours = 0

        # Format the time as HH:mm:ss
        self.currentTime = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        self.clock.setText("System Clock: " + self.currentTime)


class DeviceBox(QWidget):
    def __init__(self):
        super().__init__()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # Define the rectangle's properties
        startX = 75  # Starting X-coordinate
        startY = 300  # Starting Y-coordinate
        rectWidth = 500  # Width of the rectangle
        rectHeight = 400  # Height of the rectangle
        rectColor = QColor(255, 255, 255)  # Whitw color
        # Draw the rectangle
        painter.setBrush(rectColor)
        painter.drawRect(startX, startY, rectWidth, rectHeight)


class BlockStatus(QWidget):
    def __init__(self):
        super().__init__()

        self.status = "Unoccupied"  # Default status is "Unoccupied"
        self.statusColors = {
            "Occupied": QColor(255, 102, 102),  # Light red
            "Unoccupied": QColor(102, 255, 102),  # Green
            "Maintenance": QColor(255, 0, 0),  # Red
        }

        self.init_ui()

    def init_ui(self):
        self.setGeometry(280, 725, 245, 55)  # Extend width to 300
        self.setWindowTitle("Block Status")

        # Create a frame for the rectangles
        self.frame = QFrame(self)
        self.frame.setGeometry(0, 0, self.width(), self.height())
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setStyleSheet("QFrame { border: 2px solid black; }")

        # Create labels
        self.labelStatus = QLabel("Block Status:", self.frame)
        self.labelStatus.setGeometry(0, 0, 175, 55)  # Extend width to 100
        self.labelStatus.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.labelStatus.setFont(QFont("Segoe UI", 10, QFont.Bold))
        self.labelStatus.setStyleSheet("QLabel { color: black; }")

        self.label = QLabel(self.frame)
        self.label.setGeometry(120, 0, 125, 55)  # Extend width to 165
        self.label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        self.label.setAlignment(Qt.AlignCenter)
        self.update_status()

    def paintEvent(self, event):
        # Draw black borders around the frame
        painter = QPainter(self)
        painter.setPen(Qt.black)
        painter.drawRect(self.frame.rect())

    def update_status(self):
        self.label.setText(self.status)
        self.label.setStyleSheet(
            f"QLabel {{ background-color : {self.statusColors[self.status].name()}; }}"
        )

    def set_status(self, newStatus):
        if newStatus in self.statusColors:
            self.status = newStatus
            self.update_status()

    def get_status(self):
        return self.status


class JunctionWS(QWidget):
    def __init__(self, buttonMode):
        super().__init__()

        self.buttonMode = buttonMode

        # Call the junction rectangles object
        self.junctionBlocks = JunctionRectangles()
        self.junctionBlocks.setGeometry(0, 0, 550, 600)
        self.junctionBlocks.setParent(self)

        # junction toggle button and arrows
        self.junctionToggleButton = JunctionToggle(buttonMode, self)
        self.junctionToggleButton.setParent(self)
        self.junctionToggleButton.setGeometry(250, 400, 180, 50)
        self.junctionToggleButton.raise_

        self.labelLeft = QLabel("", self)
        self.labelRight = QLabel("", self)
        self.labelUpright = QLabel("", self)

        font = QFont("Segoe UI", 10)  # Use the Segoe UI font with the specified size

        self.labelLeft.setFont(font)
        self.labelRight.setFont(font)
        self.labelUpright.setFont(font)

        self.labelUpright.setGeometry(
            380, 275, 100, 30
        )  # Adjust the width based on the text length and font size
        self.labelRight.setGeometry(
            380, 350, 100, 30
        )  # Adjust the width based on the text length and font size
        self.labelLeft.setGeometry(
            205, 350, 200, 30
        )  # Adjust the width based on the text length and font size

    def get_switch_state(self):
        return self.junctionToggleButton.get_switch_state()

    def set_switch_state(self, state):
        self.junctionToggleButton.set_switch_state(state)

    def get_signal(self):
        return self.junctionToggleButton.switchCrossChanged

    def hide_junction(self):
        self.hide()
        self.junctionToggleButton.hide_switch()

    def set_text_box(self, blockLeft, blockRight, blockUpright):
        self.labelLeft.setText("block " + str(blockLeft))
        self.labelRight.setText("block " + str(blockRight))
        self.labelUpright.setText("block " + str(blockUpright))

    # def update_button_visibility(self):
    # self.junctionToggleButton.update_button_visibility(self.buttonMode)

    def update_button_visibility(self, mode):
        self.junctionToggleButton.update_button_visibility(mode)


class JunctionRectangles(QWidget):
    def __init__(self):
        super().__init__()

    def paintEvent(self, event):
        rectangles = QPainter(self)
        rectangles.setRenderHint(QPainter.Antialiasing)
        # Define the rectangle properties
        self.rectWidth = 100  # Width of the rectangle
        self.rectHeight = 30  # Height of the rectangle
        self.rectColor = QColor(88, 159, 252)  # Blue color
        # Draw the rectangles
        rectangles.setBrush(self.rectColor)
        rectangles.drawRect(375, 275, self.rectWidth, self.rectHeight)
        rectangles.drawRect(375, 350, self.rectWidth, self.rectHeight)
        rectangles.drawRect(200, 350, self.rectWidth, self.rectHeight)


class JunctionToggle(QWidget):
    switchCrossChanged = pyqtSignal(bool)

    def __init__(self, buttonMode, parentBox):
        super().__init__()

        # Make the buttonMode accessible throughout the class
        self.buttonMode = buttonMode
        self.parentBox = parentBox

        # Initialize the switch toggle state to false by default
        self.switchToggleState = False

        # Initialize the QLabel objects for the switch arrows
        self.uparrow = QLabel()
        self.sidearrow = QLabel()

        self.toggleSwitch = QPushButton("Toggle Switch", self)
        self.toggleSwitch.clicked.connect(self.on_button_click)
        self.toggleSwitch.setFont(QFont("Segoe UI", 15, QFont.Bold))

        # Set the background color and style for the normal state
        self.toggleSwitch.setStyleSheet(
            "QPushButton {"
            "   background-color: white;"
            "   color: black;"
            "   border: 2px solid black;"
            "   border-radius: 10px;"
            "}"
        )

        # Set the background color and style for the pressed state
        self.toggleSwitch.setStyleSheet(
            "QPushButton:pressed {"
            "   background-color: gray;"
            "   color: white;"
            "   border: 2px solid black;"
            "   border-radius: 10px;"
            "}"
        )

        # Define the text and geometry of the toggle switch
        self.toggleSwitch.setText("Toggle Switch")
        self.toggleSwitch.setGeometry(0, 0, 180, 50)

        # Connect the toggle button to call the update button visibility method
        self.buttonMode.modeChanged.connect(self.update_button_visibility)

        # Update the button visibility and switch state upon initialization
        self.update_button_visibility(self.buttonMode.get_mode())
        self.update_switch_display()

    def update_button_visibility(self, mode):
        if mode:
            self.toggleSwitch.hide()
        else:
            # if self.parentBox.isVisible():
            self.toggleSwitch.show()

    def on_button_click(self):
        self.switchToggleState = not self.switchToggleState
        self.switchCrossChanged.emit(self.switchToggleState)
        self.update_switch_display()

    def update_switch_display(self):
        if self.switchToggleState:
            # If the arrow is pointing upwards...
            uparrowPixmap = QPixmap("src/main/TrackController/images/line_up.png")
            self.uparrow.setPixmap(uparrowPixmap)
            self.uparrow.setGeometry(290, 280, 100, 100)
            self.uparrow.setParent(self.parentBox)
            self.uparrow.show()
            self.sidearrow.setHidden(True)
        else:
            # if the arrow is pointing to the side...

            sidearrowPixmap = QPixmap("src/main/TrackController/images/line_side.png")
            self.sidearrow.setPixmap(sidearrowPixmap)
            self.sidearrow.setGeometry(293, 315, 100, 100)
            self.sidearrow.setParent(self.parentBox)
            self.sidearrow.show()
            self.uparrow.setHidden(True)

    def get_switch_state(self):
        return self.switchToggleState

    def set_switch_state(self, state):
        self.switchToggleState = state
        self.update_switch_display()

    def hide_switch(self):
        self.toggleSwitch.hide()


class LightStates(QWidget):
    lightChanged = pyqtSignal(str)  # Declare the signal at the class level

    def __init__(self, buttonMode, initialLightState):
        super().__init__()

        self.buttonMode = buttonMode

        redLightPixmap = QPixmap("src/main/TrackController/images/light_red.png")
        self.redLight = QLabel(self)
        scaledPixmap = redLightPixmap.scaled(200, 300, Qt.KeepAspectRatio)
        self.redLight.setPixmap(scaledPixmap)
        self.redLight.hide()

        yellowLightPixmap = QPixmap("src/main/TrackController/images/light_yellow.png")
        self.yellowLight = QLabel(self)
        scaledPixmap = yellowLightPixmap.scaled(200, 300, Qt.KeepAspectRatio)
        self.yellowLight.setPixmap(scaledPixmap)
        self.yellowLight.hide()

        greenLightPixmap = QPixmap("src/main/TrackController/images/light_green.png")
        self.greenLight = QLabel(self)
        scaledPixmap = greenLightPixmap.scaled(200, 300, Qt.KeepAspectRatio)
        self.greenLight.setPixmap(scaledPixmap)
        self.greenLight.hide()

        self.currentColor = initialLightState

        self.setRedButton = QPushButton("Set Red")
        self.setYellowButton = QPushButton("Set Yellow")
        self.setGreenButton = QPushButton("Set Green")

        buttonWidth = 150
        buttonHeight = 50
        self.setRedButton.setFixedSize(buttonWidth, buttonHeight)
        self.setYellowButton.setFixedSize(buttonWidth, buttonHeight)
        self.setGreenButton.setFixedSize(buttonWidth, buttonHeight)

        self.setup_buttons()

    def setup_buttons(self):
        def set_trafficlightcolor(color):
            self.currentColor = color
            if color == "red":
                self.redLight.show()
                self.yellowLight.hide()
                self.greenLight.hide()
            elif color == "yellow":
                self.redLight.hide()
                self.yellowLight.show()
                self.greenLight.hide()
            elif color == "green":
                self.redLight.hide()
                self.yellowLight.hide()
                self.greenLight.show()

        self.settrafficlightcolor = set_trafficlightcolor

        self.setRedButton.clicked.connect(lambda: set_trafficlightcolor("red"))
        self.setYellowButton.clicked.connect(lambda: set_trafficlightcolor("yellow"))
        self.setGreenButton.clicked.connect(lambda: set_trafficlightcolor("green"))

        self.setRedButton.clicked.connect(lambda: self.lightChanged.emit("red"))
        self.setYellowButton.clicked.connect(lambda: self.lightChanged.emit("yellow"))
        self.setGreenButton.clicked.connect(lambda: self.lightChanged.emit("green"))

        self.setRedButton.setGeometry(0, 50, 150, 50)
        self.setRedButton.setParent(self)
        self.setYellowButton.setGeometry(0, 125, 150, 50)
        self.setYellowButton.setParent(self)
        self.setGreenButton.setGeometry(0, 200, 150, 50)
        self.setGreenButton.setParent(self)

        self.buttonMode.modeChanged.connect(self.update_button_visibility)
        self.update_button_visibility(self.buttonMode.get_mode())

    def update_button_visibility(self, mode):
        if mode:
            self.redLight.setGeometry(50, 0, 200, 300)
            self.yellowLight.setGeometry(50, 0, 200, 300)
            self.greenLight.setGeometry(50, 0, 200, 300)
            self.setRedButton.hide()
            self.setYellowButton.hide()
            self.setGreenButton.hide()

        else:
            self.redLight.setGeometry(125, 0, 200, 300)
            self.yellowLight.setGeometry(125, 0, 200, 300)
            self.greenLight.setGeometry(125, 0, 250, 300)
            self.setRedButton.show()
            self.setYellowButton.show()
            self.setGreenButton.show()

    def set_state(self, newState):
        self.settrafficlightcolor(newState)

    def get_state(self):
        return self.currentColor

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # Define the rectangle's properties
        startX = -15  # Starting X-coordinate
        startY = 0  # Starting Y-coordinate
        rectWidth = 350  # Width of the rectangle
        rectHeight = 300  # Height of the rectangle
        rectColor = QColor(255, 255, 255)  # Whitw color
        # Draw the rectangle
        painter.setBrush(rectColor)
        painter.drawRect(startX, startY, rectWidth, rectHeight)


class LightBox(QWidget):
    def __init__(self):
        super().__init__()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # Define the rectangle's properties
        startX = 0  # Starting X-coordinate
        startY = 0  # Starting Y-coordinate
        rectWidth = 350  # Width of the rectangle
        rectHeight = 300  # Height of the rectangle
        rectColor = QColor(255, 255, 255)  # Whitw color
        # Draw the rectangle
        painter.setBrush(rectColor)
        painter.drawRect(startX, startY, rectWidth, rectHeight)


class Crossing(QWidget):
    switchCrossChanged = pyqtSignal(bool)

    def __init__(self, buttonMode, parent):
        super().__init__()

        # Make the buttonMode accessible throughout the class
        self.buttonMode = buttonMode

        # Initailize crossing to be open by default if nothing is passed
        self.crossingToggleState = False

        # Initialize the QLabel objects for the crossing images
        self.closed = QLabel()
        self.open = QLabel()

        self.toggleCrossing = QPushButton("Toggle Crossing", self)
        self.toggleCrossing.clicked.connect(self.on_button_click)
        self.toggleCrossing.setFont(QFont("Segoe UI", 15, QFont.Bold))
        # Define the text and geometry of the toggle swit   ch
        self.toggleCrossing.setText("Toggle Crossing")
        self.toggleCrossing.setGeometry(250, 430, 200, 50)
        self.toggleCrossing.setParent(parent)
        self.toggleCrossing.hide()

        # Set the background color and style for the normal state
        self.toggleCrossing.setStyleSheet(
            "QPushButton {"
            "   background-color: white;"
            "   color: black;"
            "   border: 2px solid black;"
            "   border-radius: 10px;"
            "}"
        )

        # Set the background color and style for the pressed state
        self.toggleCrossing.setStyleSheet(
            "QPushButton:pressed {"
            "   background-color: gray;"
            "   color: white;"
            "   border: 2px solid black;"
            "   border-radius: 10px;"
            "}"
        )

        # Connect the toggle button to call the update button visibility method
        self.buttonMode.modeChanged.connect(self.update_button_visibility)

        # Update the button visibility and switch state upon initialization
        self.update_button_visibility(self.buttonMode.get_mode())
        self.update_crossing_display()

    def update_button_visibility(self, mode):
        if mode:
            self.toggleCrossing.hide()
        else:
            if self.closed.isVisible() or self.open.isVisible():
                self.toggleCrossing.show()

    def on_button_click(self):
        self.crossingToggleState = not self.crossingToggleState
        self.update_crossing_display()
        self.switchCrossChanged.emit(self.crossingToggleState)

    def update_crossing_display(self):
        if self.crossingToggleState:
            # If the crossing is closed
            closedPixmap = QPixmap("src/main/TrackController/images/cross_closed.png")
            closedPixmap = closedPixmap.scaled(
                int(450 * 0.6), int(225 * 0.6), Qt.KeepAspectRatio
            )
            self.closed.setPixmap(closedPixmap)
            self.closed.setGeometry(90, 26, 450, 225)
            self.closed.setParent(self)
            self.closed.show()
            self.open.setHidden(True)
        else:
            # if the crossing is open
            openPixmap = QPixmap("src/main/TrackController/images/cross_open.png")
            openPixmap = openPixmap.scaled(
                int(450 * 0.65), int(225 * 0.65), Qt.KeepAspectRatio
            )
            self.open.setPixmap(openPixmap)
            self.open.setGeometry(90, 3, 450, 250)
            self.open.setParent(self)
            self.open.show()
            self.closed.setHidden(True)
            pass

    def get_crossing_state(self):
        return self.crossingToggleState

    def set_crossing_state(self, state):
        self.crossingToggleState = state
        self.update_crossing_display()

    def hide_crossing(self):
        self.toggleCrossing.hide()
        self.closed.setHidden(True)
        self.open.setHidden(True)

    def show_crossing(self):
        if ModeButton == True:
            self.toggleCrossing.show()
        self.update_crossing_display()


class Station(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize QLabel for the station image
        self.station = QLabel()
        stationPixmap = QPixmap("src/main/TrackController/images/station.png")
        stationPixmap = stationPixmap.scaled(350, 350, Qt.KeepAspectRatio)
        self.station.setPixmap(stationPixmap)
        self.station.setGeometry(160, 280, 350, 350)
        self.station.setParent(self)
        self.station.show()

        self.label = QLabel()
        self.fontSize = 25
        font = QFont(
            "Segoe UI", self.fontSize
        )  # Use the Segoe UI font with the specified size
        self.label.setFont(font)
        self.label.setParent(self)
        self.label.raise_

    def set_station_name(self, text):
        self.label.setText(text)
        self.label.setGeometry(
            245 - int(int(len(text))),
            630,
            int(len(text) * 12 * (self.fontSize / 10)),
            self.fontSize * 2,
        )  # Adjust the width based on the text length and font size

    def hide_station(self):
        self.station.hide()
        # self.deviceBlock.hide()
        self.label.hide()

    def show_station(self):
        self.station.show()
        self.label.show()
        # self.deviceBlock.show()


class TestWindow(QMainWindow, UiMainWindow):
    # Here are the initializations of the input signals
    setSwitchState = pyqtSignal(int, int, int, bool)
    setLightState = pyqtSignal(int, int, int, str)
    setFailureState = pyqtSignal(int, int, int, bool)
    setMaintenanceState = pyqtSignal(int, int, int, bool)
    setOccupancyState = pyqtSignal(int, int, int, bool)
    setAuthority = pyqtSignal(int, int, int, int)
    setSpeed = pyqtSignal(int, int, int, float)
    setDirection = pyqtSignal(int, int, int, int)

    # Here are the initializations of the output signal requests
    requestViewSwitchState = pyqtSignal(int, int, int)
    requestViewLightState = pyqtSignal(int, int, int)
    requestViewFailureState = pyqtSignal(int, int, int)
    requestViewMaintenanceState = pyqtSignal(int, int, int)
    requestViewOccupancyState = pyqtSignal(int, int, int)
    requestViewAuthority = pyqtSignal(int, int, int)
    requestViewSpeed = pyqtSignal(int, int, int)
    requestViewDirection = pyqtSignal(int, int, int)

    # Here are the initializations of the "received" signals that are sent back after the output
    returnViewSwitchState = pyqtSignal(int, int, str)
    returnViewLightState = pyqtSignal(int, int, str)
    returnViewFailureState = pyqtSignal(int, int, str)
    returnViewMaintenanceState = pyqtSignal(int, int, str)
    returnViewOccupancyState = pyqtSignal(int, int, str)
    returnViewAuthority = pyqtSignal(int, int, str)
    returnViewSpeed = pyqtSignal(int, int, str)
    returnViewDirection = pyqtSignal(int, int, str)

    # This is the refresh signal which checks to update states if they are changed
    refreshed = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        # call the set up ui function from the UiMainWindow
        self.setup_ui(self)
        self.setGeometry(0, 0, 1100, 960)
        self.setWindowTitle("Track Controller Test Bench")
        # set the background colors of the following texts to transparent
        self.testBenchTitle.setStyleSheet(
            "QTextEdit { background-color: rgba(0, 0, 0, 0); }"
        )
        self.inputHeader.setStyleSheet(
            "QTextEdit { background-color: rgba(0, 0, 0, 0); }"
        )
        self.outputHeader.setStyleSheet(
            "QTextEdit { background-color: rgba(0, 0, 0, 0); }"
        )

        # Create links between input combo box actions for when the state value is changed
        self.setSwitchSelectState.currentIndexChanged.connect(
            self.handle_selection_set_switch
        )
        self.setLightSelectState.currentIndexChanged.connect(
            self.handle_selection_set_light
        )
        self.setBlockFailureSelectState.currentIndexChanged.connect(
            self.handle_selection_set_block_failure
        )
        self.setMaintenanceSelectState.currentIndexChanged.connect(
            self.handle_selection_set_maintenance
        )
        self.setOccupancySelectState.currentIndexChanged.connect(
            self.handle_selection_set_occupancy
        )
        self.setAuthoritySetState.valueChanged.connect(
            self.handle_selection_set_authority
        )
        self.setSpeedSetState.textChanged.connect(self.handle_selection_set_speed)
        self.setDirectionSelectState.currentIndexChanged.connect(
            self.handle_selection_set_direction
        )

        # Create links between output combo box actions for when the state value is changed
        self.viewSwitchSelectBlock.currentIndexChanged.connect(
            self.handle_selection_view_switch
        )
        self.viewLightSelectBlock.currentIndexChanged.connect(
            self.handle_selection_view_light
        )
        self.viewBlockFailureSelectBlock.currentIndexChanged.connect(
            self.handle_selection_view_block_failure
        )
        self.viewMaintenanceSelectBlock.currentIndexChanged.connect(
            self.handle_selection_view_maintenance
        )
        self.viewAuthoritySelectBlock.currentIndexChanged.connect(
            self.handle_selection_view_authority
        )
        self.viewOccupancySelectBlock.currentIndexChanged.connect(
            self.handle_selection_view_occupancy
        )
        self.viewSpeedSelectBlock.currentIndexChanged.connect(
            self.handle_selection_view_speed
        )
        self.viewDirectionSelectBlock.currentIndexChanged.connect(
            self.handle_selection_view_direction
        )

        # Link signals between the UI and the output display boxes
        self.returnViewSwitchState.connect(self.viewSwitchState.setText)
        self.returnViewLightState.connect(self.viewLightState.setText)
        self.returnViewFailureState.connect(self.viewBlockFailureState.setText)
        self.returnViewMaintenanceState.connect(self.viewMaintenanceState.setText)
        self.returnViewOccupancyState.connect(self.viewOccupancyState.setText)
        self.returnViewAuthority.connect(self.viewAuthorityState.setText)
        self.returnViewSpeed.connect(self.viewSpeedState.setText)
        self.returnViewDirection.connect(self.viewDirectionSelectState.setText)

        # Link signals for any refresh to check the view handlers
        self.refreshed.connect(self.handle_selection_view_switch)
        self.refreshed.connect(self.handle_selection_view_light)
        self.refreshed.connect(self.handle_selection_view_block_failure)
        self.refreshed.connect(self.handle_selection_view_maintenance)
        self.refreshed.connect(self.handle_selection_view_authority)
        self.refreshed.connect(self.handle_selection_view_occupancy)
        self.refreshed.connect(self.handle_selection_view_speed)
        self.refreshed.connect(self.handle_selection_view_direction)

    # The following methods are handlers for the drop down boxes in the test bench's input section
    def handle_selection_set_switch(self, index):
        if (
            self.setSwitchSelectBlock.currentIndex() == 0
            or self.setSwitch_selectLine.currentIndex() == 0
            or self.setSwitchSelectSection.currentIndex() == 0
            or self.setSwitchSelectState.currentIndex() == 0
        ):
            pass
        else:
            self.setSwitchState.emit(
                int(self.setSwitchSelectBlock.currentText()),
                bool(self.setSwitchSelectState.currentIndex() - 1),
            )

    def handle_selection_set_light(self, index):
        if (
            self.setLightSelectBlock.currentIndex() == 0
            or self.setLightSelectLine.currentIndex() == 0
            or self.setLightSelectSection.currentIndex() == 0
            or self.setLightSelectState.currentIndex() == 0
        ):
            pass
        else:
            self.setLightState.emit(
                int(self.setLightSelectBlock.currentText()),
                self.setLightSelectState.currentText(),
            )

    def handle_selection_set_block_failure(self, index):
        if (
            self.setBlockFailureSelectBlock.currentIndex() == 0
            or self.setBlockFailureSelectLine.currentIndex() == 0
            or self.setBlockFailureSelectSection.currentIndex() == 0
            or self.setBlockFailureSelectState.currentIndex() == 0
        ):
            pass
        else:
            self.setFailureState.emit(
                int(self.setBlockFailureSelectBlock.currentText()),
                ast.literal_eval(self.setBlockFailureSelectState.currentText()),
            )

    def handle_selection_set_maintenance(self, index):
        if (
            self.setMaintenanceSelectLine.currentIndex() == 0
            or self.setMaintenanceSelectSection.currentIndex() == 0
            or self.setMaintenanceSelectBlock.currentIndex() == 0
        ) or self.setMaintenanceSelectState.currentIndex() == 0:
            pass
        else:
            self.setMaintenanceState.emit(
                int(self.setMaintenanceSelectBlock.currentText()),
                ast.literal_eval(self.setMaintenanceSelectState.currentText()),
            )

    def handle_selection_set_occupancy(self, index):
        if (
            self.setOccupancySelectLine.currentIndex() == 0
            or self.setOccupancySelectWayside.currentIndex() == 0
            or self.setOccupancySelectBlock.currentIndex() == 0
            or self.setOccupancySelectState.currentIndex() == 0
        ):
            pass
        else:
            self.setOccupancyState.emit(
                self.setOccupancySelectLine.currentIndex(),
                self.setOccupancySelectWayside.currentIndex(),
                int(self.setOccupancySelectBlock.currentText()),
                (ast.literal_eval(self.setOccupancySelectState.currentText())),
            )

    def handle_selection_set_authority(self, index):
        if (
            self.setAuth_selectLine.currentIndex() == 0
            or self.setAuthoritySelectSection.currentIndex() == 0
            or self.setAuthoritySelectBlock.currentIndex() == 0
        ):
            pass
        else:
            self.setAuthority.emit(
                int(self.setAuthoritySelectBlock.currentText()),
                int(self.setAuthoritySetState.value()),
            )

    def handle_selection_set_speed(self, index):
        if (
            self.setSpeedSelectLine.currentIndex() == 0
            or self.setSpeedSelectSection.currentIndex() == 0
            or self.setSpeedSelectBlock.currentIndex() == 0
        ):
            pass
        else:
            self.setSpeed.emit(
                int(self.setSpeedSelectBlock.currentText()),
                float(self.setSpeedSetState.text()),
            )

    def handle_selection_set_direction(self, index):
        if (
            self.setDirectionSelectLine.currentIndex() == 0
            or self.setDirectionSelectSection.currentIndex() == 0
            or self.setDirectionSelectBlock.currentIndex() == 0
        ) or self.setDirectionSelectState.currentIndex() == 0:
            pass
        else:
            # determine the direction state depending on the index selected
            if self.setDirectionSelectState.currentIndex() == 1:
                directionState = -1
            elif self.setDirectionSelectState.currentIndex() == 2:
                directionState = 0
            elif self.setDirectionSelectState.currentIndex() == 3:
                directionState = 1

            self.setDirection.emit(
                int(self.setDirectionSelectBlock.currentText()), directionState
            )

    # The following methods are handlers for the drop down boxes in the test bench's input section
    def handle_selection_view_switch(self, index):
        if (
            self.viewSwitchSelectLine.currentIndex() == 0
            or self.viewSwitchSelectSection.currentIndex() == 0
            or self.viewSwitchSelectBlock.currentIndex() == 0
        ):
            pass
        else:
            self.requestViewSwitchState.emit(
                int(self.viewSwitchSelectBlock.currentText())
            )

    def handle_selection_view_light(self, index):
        if (
            self.viewLightSelectLine.currentIndex() == 0
            or self.viewLightSelectSection.currentIndex() == 0
            or self.viewLightSelectBlock.currentIndex() == 0
        ):
            pass
        else:
            self.requestViewLightState.emit(
                int(self.viewLightSelectBlock.currentText())
            )

    def handle_selection_view_block_failure(self, index):
        if (
            self.viewBlockFailureSelectLine.currentIndex() == 0
            or self.viewBlockFailureSelectSection.currentIndex() == 0
            or self.viewBlockFailureSelectBlock.currentIndex() == 0
        ):
            pass
        else:
            self.requestViewFailureState.emit(
                int(self.viewBlockFailureSelectBlock.currentText())
            )

    def handle_selection_view_maintenance(self, index):
        if (
            self.viewMaintenanceSelectLine.currentIndex() == 0
            or self.viewMaintenanceSelectSection.currentIndex() == 0
            or self.viewMaintenanceSelectBlock.currentIndex() == 0
        ):
            pass
        else:
            self.requestViewMaintenanceState.emit(
                int(self.viewMaintenanceSelectBlock.currentText())
            )

    def handle_selection_view_authority(self, index):
        if (
            self.viewAuthoritySelectLine.currentIndex() == 0
            or self.viewAuthoritySelectSection.currentIndex() == 0
            or self.viewAuthoritySelectBlock.currentIndex() == 0
        ):
            pass
        else:
            blockNum = int(self.viewAuthoritySelectBlock.currentText())
            self.requestViewAuthority.emit(blockNum)

    def handle_selection_view_occupancy(self, index):
        if (
            self.viewOccupancySelectLine.currentIndex() == 0
            or self.viewOccupancySelectSection.currentIndex() == 0
            or self.viewOccupancySelectBlock.currentIndex() == 0
        ):
            pass
        else:
            self.requestViewOccupancyState.emit(
                int(self.viewOccupancySelectBlock.currentText())
            )

    def handle_selection_view_speed(self, index):
        if (
            self.viewSpeedSelectLien.currentIndex() == 0
            or self.viewSpeedSelectSection.currentIndex() == 0
            or self.viewSpeedSelectBlock.currentIndex() == 0
        ):
            pass
        else:
            self.requestViewSpeed.emit(int(self.viewSpeedSelectBlock.currentText()))

    def handle_selection_view_direction(self, index):
        if (
            self.viewDirectionSelectLine.currentIndex() == 0
            or self.viewDirectionSelectSection.currentIndex() == 0
            or self.viewDirectionSelectBlock.currentIndex() == 0
        ):
            pass
        else:
            self.requestViewDirection.emit(
                int(self.viewDirectionSelectBlock.currentText())
            )


class MainUI(QMainWindow):
    # font variables
    textFontSize = 10
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
    moduleName = "Track Controller"

    def __init__(self):
        super().__init__(None)

        self.testBenchWindow = TestWindow()

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
        self.pixmapMTALogo = QtGui.QPixmap(
            "src/main/TrackController/images/MTA_NYC_logo.svg.png"
        )
        self.pixmapMTALogo = self.pixmapMTALogo.scaled(70, 70)
        self.logo = QLabel(self)
        self.logo.setPixmap(self.pixmapMTALogo)
        self.logo.move(20, 20)
        self.logo.adjustSize()

        # module
        self.moduleLabel = QLabel("Track Controller", self)
        self.moduleLabel.setFont(QFont(self.fontStyle, self.headerFontSize))
        self.moduleLabel.setAlignment(Qt.AlignCenter)
        self.moduleLabel.move(30, 100)
        self.moduleLabel.adjustSize()
        self.moduleLabel.setStyleSheet("color:" + self.colorDarkBlue)

        # test bench icon
        self.pixmapGear = QtGui.QPixmap("src/main/TrackController/images/gear_icon.png")
        self.pixmapGear = self.pixmapGear.scaled(25, 25)
        self.testbenchIcon = QLabel(self)
        self.testbenchIcon.setPixmap(self.pixmapGear)
        self.testbenchIcon.setGeometry(275, 100, 32, 32)

        # test bench button
        self.testbenchButton = QPushButton("Test Bench", self)
        self.testbenchButton.setFont(QFont(self.fontStyle, self.textFontSize))
        self.testbenchButton.setGeometry(300, 100, 100, 32)
        self.testbenchButton.setStyleSheet(
            "color:" + self.colorDarkBlue + ";border: 1px solid white"
        )
        self.testbenchButton.clicked.connect(lambda: self.testBenchWindow.show())

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
        self.systemSpeedInput = QLabel("x1.0", self)
        self.systemSpeedInput.setFont(QFont(self.fontStyle, self.textFontSize))
        self.systemSpeedInput.setGeometry(850, 127, 50, 50)
        self.systemSpeedInput.setStyleSheet("color:" + self.colorDarkBlue)

        # decrease system speed button
        self.pixmapRewind = QtGui.QPixmap("src/main/TrackController/images/rewind.svg")
        self.pixmapRewind = self.pixmapRewind.scaled(20, 20)
        self.slowDownButton = QPushButton(self)
        self.slowDownButton.setIcon(QtGui.QIcon(self.pixmapRewind))
        self.slowDownButton.setGeometry(819, 143, 20, 20)
        self.slowDownButton.setStyleSheet(
            "color:" + self.colorDarkBlue + ";border: 1px solid white"
        )

        # increase system speed button
        self.pixmapFastForward = QtGui.QPixmap(
            "src/main/TrackController/images/fast-forward.svg"
        )
        self.pixmapFastForward = self.pixmapFastForward.scaled(20, 20)
        self.speedUpButton = QPushButton(self)
        self.speedUpButton.setIcon(QtGui.QIcon(self.pixmapFastForward))
        self.speedUpButton.setGeometry(890, 143, 20, 20)
        self.speedUpButton.setStyleSheet(
            "color:" + self.colorDarkBlue + ";border: 1px solid white"
        )

        # decrease system speed button
        self.pixmapRewind = QtGui.QPixmap("src/main/TrackController/images/rewind.svg")
        self.pixmapRewind = self.pixmapRewind.scaled(20, 20)
        self.slowDownButton = QPushButton(self)
        self.slowDownButton.setIcon(QtGui.QIcon(self.pixmapRewind))
        self.slowDownButton.setGeometry(1874, 304, 20, 20)
        self.slowDownButton.setStyleSheet(
            "color:" + self.colorDarkBlue + ";border: 1px solid black"
        )

        # This is the initialization for the main box rectangle

        self.mainBox = MainBox()
        self.mainBox.setGeometry(50, 200, 600, 675)
        self.mainBox.setParent(self)

        # This is the initialization of the occupancy box
        self.occupancyBox = OccupancyBox()
        self.occupancyBox.setGeometry(700 - 45, 200, 400, 700)
        self.occupancyBox.setParent(self)
        # occupied blocks text header
        self.occupiedBlocks = create_text_label("Occupied Blocks", 750 - 50, 160, 16)
        self.occupiedBlocks.setParent(self)
        # block number label
        self.occupiedBlockNumber = create_text_label("Block", 680, 210, 12)
        self.occupiedBlockNumber.setParent(self)
        # block type label
        self.occupiedBlockType = create_text_label("Block Type", 758, 210, 12)
        self.occupiedBlockType.setParent(self)
        # block type label
        self.occupiedBlockFailure = create_text_label("Fail", 960 - 90, 210, 12)
        self.occupiedBlockFailure.setParent(self)
        # occupancyBox.hide()

        # This is the initialization for the device box
        self.deviceBlock = DeviceBox()
        self.deviceBlock.setGeometry(25, 0, 800, 800)
        self.deviceBlock.setParent(self)

        # This is the initialization for the mode button
        self.buttonMode = ModeButton()
        self.buttonMode.setGeometry(
            100, 890, 250, 50
        )  # Set the position and size of the button
        self.buttonMode.setParent(self)

        # This is the initialziation for the map button
        self.buttonMap = MapButton()
        self.buttonMap.setGeometry(400, 890, 200, 50)
        self.buttonMap.setParent(self)

        # This is the initializtion for the light states
        self.lightState = LightStates(self.buttonMode, "green")
        self.lightState.setParent(self)
        self.lightState.setGeometry(200, 500, 300, 300)
        self.lightState.hide()

        # This is the initialization for the crossing widget
        self.crossing = Crossing(self.buttonMode, self)
        self.crossing.setParent(self)
        self.crossing.setGeometry(125, 200, 450, 250)
        self.crossing.hide_crossing()

        # This is the initialization for the switch box
        self.junctionSwitch = JunctionWS(self.buttonMode)
        self.junctionSwitch.setParent(self)
        self.junctionSwitch.setGeometry(0, 0, 700, 550)
        self.junctionSwitch.hide()

        # This is the initialization for the station widget
        self.station = Station()
        self.station.setParent(self.deviceBlock)
        self.station.set_station_name("Station A")
        self.station.hide()

        # deviceBlock.hide()
        self.blockStatus = BlockStatus()
        self.blockStatus.setParent(self)
        self.blockStatus.setGeometry(
            230, 800, self.blockStatus.width(), self.blockStatus.height()
        )
        self.blockStatus.hide()

        # This is the initialization for the select line combo box
        self.comboboxLine = QComboBox(self)  # Create a QComboBox widget
        self.comboboxLine.setGeometry(
            75, 160, 200, 30
        )  # Set the position and size of the combobox
        # Set an initial placeholder text
        self.comboboxLine.addItem("Select Line")
        # Add other items to the combobox
        self.comboboxLine.addItem("Green Line")
        self.comboboxLine.addItem("Red Line")
        self.comboboxLine.setParent(self)
        self.comboboxLine.raise_()

        # This is the initialization for the select wayside combobox
        self.comboboxWayside = QComboBox(self)
        self.comboboxWayside.setGeometry(
            275, 160, 200, 30
        )  # Set the position and size of the combobox
        self.comboboxWayside.setParent(self)
        self.comboboxWayside.raise_()

        # This is the initialization for the select block type combo box
        self.comboboxBlockType = QComboBox(self)
        self.comboboxBlockType.setGeometry(
            120, 215, 160, 30
        )  # Set the position and size of the combobox
        self.comboboxBlockType.setParent(self)
        self.comboboxBlockType.raise_()

        # This is the initialization for the select block number combo box
        self.comboboxBlockNum = QComboBox(self)
        self.comboboxBlockNum.setGeometry(
            280, 215, 170, 30
        )  # Set the position and size of the combobox
        self.comboboxBlockNum.setParent(self)
        self.comboboxBlockNum.raise_()
        self.deviceBlock.hide()

        # This is the initialization for the load plc button
        self.plcImportButton = QPushButton(self)
        self.plcImportButton.setText("Import PLC")
        self.plcImportButton.setStyleSheet(
            "background-color: rgba(50,125,255,255); color: white; font-weight: bold;"
        )
        self.plcImportButton.setGeometry(500, 160, 120, 30)

        # Connect the signal (currentIndexChanged) to the slot (handle_selection)
        self.comboboxLine.currentIndexChanged.connect(self.handle_selection_line)

        # initialize select variables to 0
        self.waysideSelect = 0
        self.lineSelect = 0
        self.blockTypeSelect = " "

    # This is a method to make all of the device widgets hidden
    def hide_devices(self):
        self.lightState.hide()
        self.junctionSwitch.hide_junction()
        self.crossing.hide_crossing()
        self.station.hide_station()
        self.blockStatus.hide()
        self.deviceBlock.hide()

    # This is the method and code for the line selection combo box handler
    def handle_selection_line(self, index):
        # reset the indexes of each of the following options
        self.hide_devices()
        self.comboboxWayside.setCurrentIndex(0)
        self.comboboxBlockType.setCurrentIndex(0)
        self.comboboxBlockNum.setCurrentIndex(0)
        selectedItem = self.comboboxLine.currentText()

        # reset the wayside select so a plc file cannot be imported
        self.waysideSelect = 0

        if selectedItem == "Select Line":
            # Clear the options for the next combo boxes
            self.comboboxWayside.clear()
            self.comboboxBlockType.clear()
            self.comboboxBlockNum.clear()
            pass

        elif selectedItem == "Green Line":
            self.comboboxWayside.clear()
            self.comboboxWayside.addItem("Select Wayside Controller")
            self.comboboxWayside.addItem("Wayside 1 (A - J), (S - Z)")
            self.comboboxWayside.addItem("Wayside 2 (J - R)")
            self.lineSelect = 1
        elif selectedItem == "Red Line":
            self.comboboxWayside.clear()
            self.comboboxWayside.addItem("Select Wayside Controller")
            self.comboboxWayside.addItem("Wayside 1 (A - H), (R - T)")
            self.comboboxWayside.addItem("Wayside 2 (H - Q)")
            self.lineSelect = 2
