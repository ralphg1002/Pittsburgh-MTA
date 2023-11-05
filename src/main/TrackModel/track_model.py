import sys
import re
from .TrackData import TrackData
from .Station import Station
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# Qgraphicsview, Qgraphicescene, Qpainterpath

MTA_STYLING = {
    # font variables
    "textFontSize": 10,
    "labelFontSize": 12,
    "headerFontSize": 16,
    "titleFontSize": 22,
    "fontStyle": "Product Sans",
    # color variables
    "darkBlue": "#085394",
    "lightRed": "#EA9999",
    "lightBlue": "#9FC5F8",
    "lightGrey": "#CCCCCC",
    "mediumGrey": "#DDDDDD",
    "darkGrey": "#666666",
    "black": "#000000",
    "green": "#00FF00",
    "red": "#FF0000",
    # dimensions
    "w": 960,
    "h": 960,
    # "moduleName": 'CTC'
}

# # DONE :)
# class FailureWindow:
#     selectedBlock = None
#     selectedFailures = []

#     def __init__(self):
#         self.failureWindow = QDialog()
#         self.setup_failure_popup()

#     def setup_failure_popup(self):
#         self.failureWindow.setWindowTitle("Change Failures")
#         self.failureWindow.setGeometry(1550, 500, 250, 300)
#         self.failureWindow.setStyleSheet("background-color: #ff4747;")

#         self.failure_title()
#         self.change_background()
#         self.add_block_selection()
#         self.add_failure_selection()
#         self.add_set_button()

#     def failure_title(self):
#         title = QLabel("Failure Configuration:", self.failureWindow)
#         title.setGeometry(10, 10, 230, 30)
#         title.setStyleSheet("font-weight: bold; font-size: 18px")

#         # Horizontal divider line
#         thickness = 5
#         hline = QFrame(self.failureWindow)
#         hline.setFrameShape(QFrame.HLine)
#         hline.setGeometry(0, 40, 250, thickness)
#         hline.setLineWidth(thickness)

#     def change_background(self):
#         background = QWidget(self.failureWindow)
#         background.setGeometry(0, 45, 250, 300)
#         background.setStyleSheet("background-color: #ffd6d6;")

#     def add_block_selection(self):
#         selectBlock = QLabel("Select Block #:", self.failureWindow)
#         selectBlock.setGeometry(10, 50, 230, 30)
#         selectBlock.setStyleSheet(
#             "font-weight: bold; font-size: 18px; background-color: #ffd6d6;"
#         )

#         # Add a dropdown selection
#         self.blockDropdown = QComboBox(self.failureWindow)
#         self.blockDropdown.setGeometry(10, 80, 115, 30)
#         self.blockDropdown.setStyleSheet("background-color: white;")
#         for i in range(1, 16):
#             self.blockDropdown.addItem("Block " + str(i))

#         self.blockDropdown.currentIndexChanged.connect(self.update_exit_button_state)

#     def add_failure_selection(self):
#         setFailure = QLabel("Set Failure Type:", self.failureWindow)
#         setFailure.setGeometry(10, 120, 230, 30)
#         setFailure.setStyleSheet(
#             "font-weight: bold; font-size: 18px; background-color: #ffd6d6"
#         )

#         self.failureCheckboxes = []
#         failures = ["Track Circuit Failure", "Power Failure", "Broken Rail"]
#         yOffset = 150
#         for failure in failures:
#             option = QCheckBox(failure, self.failureWindow)
#             option.setGeometry(10, yOffset, 230, 30)
#             option.setStyleSheet("background-color: #ffd6d6")
#             self.failureCheckboxes.append(option)
#             yOffset += 30

#     def update_exit_button_state(self):
#         # Enable the button to "Set Failure Configuration" if a drop down item from the menu is selected
#         isBlockSelected = self.blockDropdown.currentIndex() != -1
#         self.button.setEnabled(isBlockSelected)

#     def add_set_button(self):
#         self.button = QPushButton("Set Failure Configuration", self.failureWindow)
#         self.button.setGeometry(50, 250, 150, 30)
#         self.button.setStyleSheet("background-color: #39E75F;")
#         self.button.clicked.connect(self.update_failure)
#         self.button.setEnabled(False)  # Button is set as disabled to begin with

#     def update_failure(self):
#         selectedBlockIndex = self.blockDropdown.currentIndex()
#         selectedBlock = self.blockDropdown.itemText(selectedBlockIndex)

#         self.selectedFailures.clear()
#         for checkbox in self.failureCheckboxes:
#             if checkbox.isChecked():
#                 self.selectedFailures.append(checkbox.text())
#         self.selectedBlock = selectedBlock

#         self.failureWindow.close()

#     def get_selected_block(self):
#         if self.selectedBlock != None:
#             # Pull block int from string
#             pattern = r"\d+"
#             searchInt = re.search(pattern, self.selectedBlock)
#             if searchInt:
#                 blockNum = int(searchInt.group())
#                 return blockNum

#     def get_selected_failures(self):
#         if self.selectedFailures == []:
#             return "None"
#         return self.selectedFailures


class TrackView(QGraphicsView):
    def __init__(self, parent):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.layout_number = 1  # Initialize the layout to the first one
        # self.drawGreenLine()  # Call the initial layout function

    def drawGreenLine(self):
        # Create a horizontal dash track block
        path1 = QPainterPath()
        path1.moveTo(0, 0)
        path1.lineTo(20, 0)
        track_block1 = self.createTrackBlock(path1, "Horizontal Dash")
        self.scene.addItem(track_block1)

        # Create a vertical line track block
        path2 = QPainterPath()
        path2.moveTo(-20, 20)
        path2.lineTo(-20, 40)
        track_block2 = self.createTrackBlock(path2, "Vertical Line")
        self.scene.addItem(track_block2)

        path3 = QPainterPath()
        path3.moveTo(0, 0)
        path3.cubicTo(-10, 0, -20, 0, -20, 20)
        track_block3 = self.createTrackBlock(path3, "Curved Line")
        self.scene.addItem(track_block3)

    def drawRedLine(self):
        path1 = QPainterPath()
        path1.moveTo(0, 0)
        path1.lineTo(20, 0)
        track_block1 = self.createTrackBlock(path1, "Block F")
        self.scene.addItem(track_block1)

        path2 = QPainterPath()
        path2.moveTo(-20, 20)
        path2.lineTo(-20, 160)
        track_block2 = self.createTrackBlock(path2, "Block H")
        self.scene.addItem(track_block2)

        path3 = QPainterPath()
        path3.moveTo(-10, 0)
        path3.cubicTo(-10, 0, -20, 0, -20, 10)
        track_block3 = self.createTrackBlock(path3, "Block G")
        self.scene.addItem(track_block3)

        path4 = QPainterPath()
        path4.moveTo(30, 0)
        path4.lineTo(50, 0)
        track_block4 = self.createTrackBlock(path4, "Block E")
        self.scene.addItem(track_block4)

        path5 = QPainterPath()
        path5.moveTo(60, 0)
        path5.cubicTo(60, 0, 80, 0, 80, -10)
        track_block5 = self.createTrackBlock(path5, "Block D")
        self.scene.addItem(track_block5)

        path6 = QPainterPath()
        path6.moveTo(80, -20)
        path6.cubicTo(80, -20, 80, -30, 70, -30)
        track_block6 = self.createTrackBlock(path6, "Block C")
        self.scene.addItem(track_block6)

        path7 = QPainterPath()
        path7.moveTo(60, -30)
        path7.cubicTo(60, -30, 50, -30, 50, -20)
        track_block7 = self.createTrackBlock(path7, "Block B")
        self.scene.addItem(track_block7)

        path8 = QPainterPath()
        path8.moveTo(48, -16)
        path8.cubicTo(48, -16, 40, -10, 20, -2)
        track_block8 = self.createTrackBlock(path8, "Block A")
        self.scene.addItem(track_block8)

        path9 = QPainterPath()
        path9.moveTo(-30, 30)
        path9.cubicTo(-30, 30, -40, 30, -40, 40)
        track_block9 = self.createTrackBlock(path9, "Block T")
        self.scene.addItem(track_block9)

        path10 = QPainterPath()
        path10.moveTo(-40, 50)
        path10.lineTo(-40, 60)
        track_block10 = self.createTrackBlock(path10, "Block S")
        self.scene.addItem(track_block10)

        path11 = QPainterPath()
        path11.moveTo(-40, 70)
        path11.cubicTo(-40, 70, -40, 80, -30, 80)
        track_block11 = self.createTrackBlock(path11, "Block R")
        self.scene.addItem(track_block11)

        path12 = QPainterPath()
        path12.moveTo(-30, 110)
        path12.cubicTo(-30, 110, -40, 110, -40, 120)
        track_block12 = self.createTrackBlock(path12, "Block Q")
        self.scene.addItem(track_block12)

        path13 = QPainterPath()
        path13.moveTo(-40, 130)
        path13.lineTo(-40, 140)
        track_block13 = self.createTrackBlock(path13, "Block P")
        self.scene.addItem(track_block13)

        path14 = QPainterPath()
        path14.moveTo(-40, 150)
        path14.cubicTo(-40, 150, -40, 160, -30, 160)
        track_block14 = self.createTrackBlock(path14, "Block O")
        self.scene.addItem(track_block14)

        path15 = QPainterPath()
        path15.moveTo(-20, 170)
        path15.cubicTo(-20, 170, -20, 190, -40, 190)
        track_block15 = self.createTrackBlock(path15, "Block I")
        self.scene.addItem(track_block15)

        path16 = QPainterPath()
        path16.moveTo(-50, 190)
        path16.lineTo(-80, 190)
        track_block16 = self.createTrackBlock(path16, "Block J")
        self.scene.addItem(track_block16)

        path17 = QPainterPath()
        path17.moveTo(-90, 190)
        path17.cubicTo(-90, 190, -110, 190, -110, 175)
        track_block17 = self.createTrackBlock(path17, "Block K")
        self.scene.addItem(track_block17)

        path18 = QPainterPath()
        path18.moveTo(-110, 165)
        path18.cubicTo(-110, 165, -110, 155, -100, 155)
        track_block18 = self.createTrackBlock(path18, "Block L")
        self.scene.addItem(track_block18)

        path19 = QPainterPath()
        path19.moveTo(-90, 155)
        path19.cubicTo(-90, 155, -85, 155, -85, 170)
        track_block19 = self.createTrackBlock(path19, "Block M")
        self.scene.addItem(track_block19)

        path20 = QPainterPath()
        path20.moveTo(-84, 175)
        path20.cubicTo(-84, 175, -83, 180, -70, 188)
        track_block20 = self.createTrackBlock(path20, "Block N")
        self.scene.addItem(track_block20)

    def createTrackBlock(self, path, number):
        track_block = TrackBlock(path, number)
        return track_block

    def showGreenLineLayout(self):
        self.scene.clear()
        self.drawGreenLine()

    def showRedLineLayout(self):
        self.scene.clear()
        self.drawRedLine()


class TrackBlock(QGraphicsPathItem):
    def __init__(self, path, number):
        super().__init__(path)
        self.number = number
        self.original_pen = QPen(QColor(0, 0, 0))
        self.original_pen.setWidth(10)
        self.hover_pen = QPen(QColor(255, 255, 0))
        self.hover_pen.setWidth(10)
        self.setPen(self.original_pen)
        self.setAcceptHoverEvents(True)

    def mousePressEvent(self, event):
        print(f"Clicked on {self.number}")

    def hoverEnterEvent(self, event):
        self.setPen(self.hover_pen)

    def hoverLeaveEvent(self, event):
        self.setPen(self.original_pen)


class TrackModel:
    moduleName = "Track Model"
    simulationSpeed = 1.0
    selectedLine = "Red"
    temperature = 65
    allowableDirections = "EAST/WEST"
    blockTrackHeater = "OFF"
    failures = []
    maintenance = 0
    occupied = 0
    beacon = "---"
    ticketSales = 0
    waiting = 0

    def __init__(self):
        self.block = TrackData()
        self.station = Station()
        self.load_data()
        self.setup_selection_window()

    def setup_selection_window(self):
        # app = QApplication(sys.argv) #Don't need for main.py
        self.mainWindow = QMainWindow()
        self.mainWindow.setGeometry(960, 35, 960, 1045)
        self.mainWindow.setWindowTitle(self.moduleName)
        self.mainWindow.setStyleSheet("background-color: white")
        # app.setWindowIcon(QIcon("src/main/TrackModel/pngs/MTA_logo.png"))

        # General layout
        self.set_clock()
        self.set_simulation_speed_controls()
        # self.add_vline(mainWindow)
        # self.add_hline(mainWindow)
        self.add_header()
        self.add_mta_logo()
        # self.add_tabbar(mainWindow)
        self.add_module_name()
        self.add_testbench_button()

        # Map
        # self.add_line_panel(mainWindow)
        self.control_temperature()
        self.add_import_button()
        # The following are hidden initially and are shown upon an excel file import
        # self.display_file_path(mainWindow)
        # self.add_track_map(mainWindow)
        # self.add_map_zoom(mainWindow)
        # self.add_map_pngs(mainWindow)

        # self.add_block_info_display(mainWindow)
        # self.add_station_info(mainWindow)

        # Block Info Selection
        self.add_input_section()
        self.show_block_data()  # NEWWW
        self.add_failure_selection()  # NEWW
        # self.add_selectable_block_info(mainWindow)
        # self.add_change_failures_button(mainWindow)

        # NEW
        self.setup_content_widget()
        self.map_toggle()

        # Hide by default
        # self.mainWindow.show()
        # sys.exit(app.exec_())

    def load_data(self):
        # Preload track data
        self.redTrackData = self.block.read_track_data(
            "src\main\TrackModel\Track Layout & Vehicle Data vF2.xlsx", "Red Line"
        )
        self.greenTrackData = self.block.read_track_data(
            "src\main\TrackModel\Track Layout & Vehicle Data vF2.xlsx", "Green Line"
        )

    # def add_vline(self, parentWindow):
    #     thickness = 5

    #     line = QFrame(parentWindow)
    #     line.setFrameShape(QFrame.VLine)
    #     line.setGeometry(950, 100, thickness, 700)
    #     line.setLineWidth(thickness)

    # def add_hline(self, parentWindow):
    #     thickness = 5

    #     line = QFrame(parentWindow)
    #     line.setFrameShape(QFrame.HLine)
    #     line.setGeometry(0, 100, 1200, thickness)
    #     line.setLineWidth(thickness)

    def add_header(self):
        headerBackground = QLabel(self.mainWindow)
        headerBackground.setGeometry(0, 0, 960, 80)
        headerBackground.setStyleSheet(f'background-color: {MTA_STYLING["darkBlue"]}')

        # Title
        windowWidth = self.mainWindow.width()
        labelWidth = 900
        titlePosition = int((windowWidth - labelWidth) / 2)

        titleLabel = QLabel(
            "Pittsburgh Metropolitan Transportation Authority", self.mainWindow
        )
        titleLabel.setGeometry(titlePosition, 20, labelWidth, 50)
        titleLabel.setAlignment(Qt.AlignCenter)
        titleFont = QFont(MTA_STYLING["fontStyle"], MTA_STYLING["titleFontSize"])
        titleLabel.setStyleSheet(
            f'color: white; background-color: {MTA_STYLING["darkBlue"]}'
        )
        titleLabel.setFont(titleFont)

    def add_mta_logo(self):
        mtaPng = QPixmap("src/main/TrackModel/pngs/mta_logo.png")
        mtaPng = mtaPng.scaledToWidth(70)
        mtaLogo = QLabel(self.mainWindow)
        mtaLogo.setPixmap(mtaPng)
        mtaLogo.setGeometry(0, 0, mtaPng.width(), mtaPng.height())
        mtaLogo.setStyleSheet(f'background-color: {MTA_STYLING["darkBlue"]}')

    def add_module_name(self):
        moduleLabel = QLabel(self.moduleName, self.mainWindow)
        moduleFont = QFont(MTA_STYLING["fontStyle"], MTA_STYLING["headerFontSize"])
        moduleLabel.setFont(moduleFont)
        moduleLabel.setGeometry(30, 80, 150, 60)
        moduleLabel.setStyleSheet(f'color: {MTA_STYLING["darkBlue"]}')

    def add_testbench_button(self):
        # icon
        gearPng = QPixmap("src/main/TrackModel/pngs/MTA_logo.png")
        gearPng = gearPng.scaledToWidth(25, 25)
        testbenchIcon = QLabel(self.mainWindow)
        testbenchIcon.setPixmap(gearPng)
        testbenchIcon.setGeometry(30, 130, gearPng.width(), gearPng.height())

        # button
        testbenchButton = QPushButton("Test Bench", self.mainWindow)
        testbenchFont = QFont(MTA_STYLING["fontStyle"], MTA_STYLING["textFontSize"])
        testbenchButton.setFont(testbenchFont)
        testbenchButton.setGeometry(60, 130, 100, 30)
        testbenchButton.setStyleSheet(
            f'color: {MTA_STYLING["darkBlue"]}; border: 1px solid white'
        )

        testbenchButton.clicked.connect(self.show_testbench)

    def control_temperature(self):
        setTemperature = QLabel("Set Temperature:", self.mainWindow)
        setTemperatureFont = QFont(
            MTA_STYLING["fontStyle"], MTA_STYLING["headerFontSize"]
        )
        setTemperature.setFont(setTemperatureFont)
        setTemperature.setGeometry(330, 80, 210, 60)
        setTemperature.setStyleSheet(f'color: {MTA_STYLING["darkBlue"]}')

        self.temperatureInput = QLineEdit(self.mainWindow)
        temperatureInputFont = QFont(
            MTA_STYLING["fontStyle"], MTA_STYLING["textFontSize"]
        )
        self.temperatureInput.setFont(temperatureInputFont)
        self.temperatureInput.setGeometry(365, 130, 40, 30)
        self.temperatureInput.setAlignment(Qt.AlignCenter)
        self.temperatureInput.setPlaceholderText("65")
        self.temperatureInput.setStyleSheet(
            f'color: {MTA_STYLING["darkBlue"]}; border: 1px solid {MTA_STYLING["darkBlue"]};'
        )

        fahrenheitUnit = QLabel("°F", self.mainWindow)
        fahrenheitFont = QFont(MTA_STYLING["fontStyle"], MTA_STYLING["headerFontSize"])
        fahrenheitUnit.setFont(fahrenheitFont)
        fahrenheitUnit.setGeometry(405, 130, 30, 30)
        fahrenheitUnit.setStyleSheet(f'color: {MTA_STYLING["darkBlue"]}')

        setTemperatureButton = QPushButton("Set", self.mainWindow)
        setTemperatureButtonFont = QFont(
            MTA_STYLING["fontStyle"], MTA_STYLING["textFontSize"]
        )
        setTemperatureButton.setFont(setTemperatureButtonFont)
        setTemperatureButton.setGeometry(440, 130, 60, 30)
        setTemperatureButton.setStyleSheet(
            f'background-color: {MTA_STYLING["darkBlue"]}; color: white'
        )
        setTemperatureButton.clicked.connect(self.set_temperature)

    def set_temperature(self):
        tempInput = self.temperatureInput.text()
        if tempInput != "":
            self.temperature = self.temperatureInput.text()
            # If temperature is greater than 45 degrees F, then track heater will remain OFF
            if int(tempInput) > 45:
                self.blockTrackHeater = "OFF"
            else:
                self.blockTrackHeater = "ON"
        self.set_trackheater()
        self.temperatureInput.setPlaceholderText(str(self.temperature))
        print(self.temperature)

    def set_clock(self):
        # system time input
        systemTimeFont = QFont(MTA_STYLING["fontStyle"], MTA_STYLING["headerFontSize"])

        clockLabel = QLabel("System Time:", self.mainWindow)
        clockLabel.setFont(systemTimeFont)
        clockLabel.setGeometry(650, 80, 170, 60)
        clockLabel.setStyleSheet(f'color: {MTA_STYLING["darkBlue"]}')

        self.clock = QLabel("00:00:00", self.mainWindow)
        self.clock.setFont(systemTimeFont)
        self.clock.setGeometry(830, 80, 150, 60)
        self.clock.setStyleSheet(f'color: {MTA_STYLING["darkBlue"]}')
        self.update_clock()

        # Update clock in real time while window is open
        timer = QTimer(self.mainWindow)
        timer.timeout.connect(self.update_clock)
        # Update every 1 second
        timer.start(1000)

    def update_clock(self):
        currentDatetime = QDateTime.currentDateTime()
        formattedTime = currentDatetime.toString("HH:mm:ss")
        self.clock.setText(formattedTime)

    def set_simulation_speed_controls(self):
        systemSpeedFont = QFont(MTA_STYLING["fontStyle"], MTA_STYLING["textFontSize"])

        systemSpeedLabel = QLabel("System Speed:", self.mainWindow)
        systemSpeedLabel.setFont(systemSpeedFont)
        systemSpeedLabel.setGeometry(700, 130, 150, 30)
        systemSpeedLabel.setStyleSheet(f'color: {MTA_STYLING["darkBlue"]}')
        self.speedText = QLabel("x1.0", self.mainWindow)
        self.speedText.setFont(systemSpeedFont)
        self.speedText.setGeometry(850, 130, 50, 30)
        self.speedText.setStyleSheet(f'color: {MTA_STYLING["darkBlue"]}')

        decreaseSpeed = QPushButton("<<", self.mainWindow)
        decreaseSpeed.setGeometry(820, 130, 20, 30)
        decreaseSpeed.setStyleSheet(
            f'color: {MTA_STYLING["darkBlue"]}; border: 1px solid white; font-weight: bold'
        )
        decreaseSpeed.clicked.connect(self.decrease_simulation_speed)
        increaseSpeed = QPushButton(">>", self.mainWindow)
        increaseSpeed.setGeometry(890, 130, 20, 30)
        increaseSpeed.setStyleSheet(
            f'color: {MTA_STYLING["darkBlue"]}; border: 1px solid white; font-weight: bold'
        )
        increaseSpeed.clicked.connect(self.increase_simulation_speed)

    def decrease_simulation_speed(self):
        # Speed cannot go below 0.5
        if self.simulationSpeed > 0.5:
            self.simulationSpeed -= 0.5
            self.speedText.setText(f"{self.simulationSpeed}x")

    def increase_simulation_speed(self):
        if self.simulationSpeed < 5.0:
            self.simulationSpeed += 0.5
            self.speedText.setText(f"{self.simulationSpeed}x")

    def setup_content_widget(self):
        mapWidget = QWidget(self.mainWindow)
        mapWidget.setGeometry(30, 300, 500, 700)
        mapWidget.setStyleSheet(f'border: 20px solid {MTA_STYLING["darkBlue"]}')
        self.trackView = TrackView(mapWidget)
        self.trackView.setGeometry(0, 0, mapWidget.width(), mapWidget.height())

    def map_toggle(self):
        selectLine = QLabel("Select Line:", self.mainWindow)
        selectLineFont = QFont(MTA_STYLING["fontStyle"], MTA_STYLING["headerFontSize"])
        selectLine.setFont(selectLineFont)
        selectLine.setGeometry(210, 260, 135, 30)
        selectLine.setStyleSheet(f'color: {MTA_STYLING["darkBlue"]}')

        buttonStyle = f'background-color: white; color: {MTA_STYLING["darkBlue"]}; border: 1px solid {MTA_STYLING["darkBlue"]}; border-radius: 10px;'

        self.greenLineButton = QPushButton("Green Line", self.mainWindow)
        greenLineButtonFont = QFont(
            MTA_STYLING["fontStyle"], MTA_STYLING["textFontSize"]
        )
        self.greenLineButton.setFont(greenLineButtonFont)
        self.greenLineButton.setGeometry(350, 260, 90, 30)
        self.greenLineButton.setStyleSheet(buttonStyle)
        self.greenLineButton.clicked.connect(self.toggle_green_data)

        self.redLineButton = QPushButton("Red Line", self.mainWindow)
        redLineButtonFont = QFont(MTA_STYLING["fontStyle"], MTA_STYLING["textFontSize"])
        self.redLineButton.setFont(redLineButtonFont)
        self.redLineButton.setGeometry(440, 260, 90, 30)
        self.redLineButton.setStyleSheet(buttonStyle)
        self.redLineButton.clicked.connect(self.toggle_red_data)

        # Set Base Line to Red
        self.change_button_color(MTA_STYLING["red"])
        self.toggle_red_data()

        # Connect button click events to change the background color when selected
        self.greenLineButton.clicked.connect(
            lambda: self.change_button_color(MTA_STYLING["green"])
        )
        self.redLineButton.clicked.connect(
            lambda: self.change_button_color(MTA_STYLING["red"])
        )

    def toggle_green_data(self):
        self.trackView.showGreenLineLayout()
        self.trackData = self.greenTrackData
        self.selectedLine = "Green"
        # self.update_blockinfo()

    def toggle_red_data(self):
        self.trackView.showRedLineLayout()
        self.trackData = self.redTrackData
        self.selectedLine = "Red"
        # self.update_blockinfo()

    def change_button_color(self, color):
        buttonStyle = f'background-color: white; color: {MTA_STYLING["darkBlue"]}; border: 1px solid {MTA_STYLING["darkBlue"]}; border-radius: 10px;'
        if color == MTA_STYLING["green"]:
            self.redLineButton.setStyleSheet(buttonStyle)
            self.greenLineButton.setStyleSheet(
                f"background-color: {color}; color: white; border: 1px solid {color}; border-radius: 10px;"
            )
        else:
            self.greenLineButton.setStyleSheet(buttonStyle)
            self.redLineButton.setStyleSheet(
                f"background-color: {color}; color: white; border: 1px solid {color}; border-radius: 10px;"
            )

    def toggle_content(self):
        self.trackView.toggleLayout()  # Call the toggleLayout method in TrackView

    # def add_line_panel(self, parentWindow):
    #     selectLine = QLabel("Select Line:", parentWindow)
    #     selectLine.setGeometry(90, 130, 110, 30)
    #     selectLine.setStyleSheet("font-weight: bold; font-size: 18px")

    #     self.bluePanel = QLabel("Blue Line", parentWindow)
    #     self.greenPanel = QLabel("Green Line", parentWindow)
    #     self.redPanel = QLabel("Red Line", parentWindow)

    #     self.bluePanel.setGeometry(20, 160, 80, 30)
    #     self.greenPanel.setGeometry(100, 160, 80, 30)
    #     self.redPanel.setGeometry(180, 160, 80, 30)

    #     # Initially greyed out as none are selected
    #     unselected = "background-color: grey; color: white; border: 1px solid black; border-radius: 5px; padding: 5px;"
    #     self.bluePanel.setStyleSheet(unselected)
    #     self.greenPanel.setStyleSheet(unselected)
    #     self.redPanel.setStyleSheet(unselected)

    #     # Handlers that call the select_line method
    #     self.bluePanel.mousePressEvent = (
    #         lambda event, line="Blue Line": self.select_line(line)
    #     )
    #     self.greenPanel.mousePressEvent = (
    #         lambda event, line="Green Line": self.select_line(line)
    #     )
    #     self.redPanel.mousePressEvent = lambda event, line="Red Line": self.select_line(
    #         line
    #     )

    # def select_line(self, selectedLine):
    #     unselected = "background-color: grey; color: white; border: 1px solid black; border-radius: 5px; padding: 5px;"
    #     if selectedLine != self.selectedLine:
    #         if selectedLine == "Blue Line":
    #             self.bluePanel.setStyleSheet(
    #                 "background-color: blue; color: white; border: 1px solid black; border-radius: 5px; padding: 5px;"
    #             )
    #             self.greenPanel.setStyleSheet(unselected)
    #             self.redPanel.setStyleSheet(unselected)
    #         elif selectedLine == "Green Line":
    #             self.bluePanel.setStyleSheet(unselected)
    #             self.greenPanel.setStyleSheet(
    #                 "background-color: green; color: white; border: 1px solid black; border-radius: 5px; padding: 5px;"
    #             )
    #             self.redPanel.setStyleSheet(unselected)
    #         elif selectedLine == "Red Line":
    #             self.bluePanel.setStyleSheet(unselected)
    #             self.greenPanel.setStyleSheet(unselected)
    #             self.redPanel.setStyleSheet(
    #                 "background-color: red; color: white; border: 1px solid black; border-radius: 5px; padding: 5px;"
    #             )

    #         self.selectedLine = selectedLine

    # def add_map_pngs(self, parentWindow):
    #     self.switchPng = QLabel(parentWindow)
    #     self.switchPng.setGeometry(450, 420, 30, 30)
    #     self.switchPng.setPixmap(
    #         QPixmap("src/main/TrackModel/pngs/train_track.png").scaled(25, 25)
    #     )
    #     self.switchPng.hide()

    #     # Temp
    #     self.occ1Png = QLabel(parentWindow)
    #     self.occ1Png.setGeometry(80, 422, 80, 60)
    #     self.occ1Png.setPixmap(QPixmap("src/main/TrackModel/pngs/occ1.png"))
    #     self.occ1Png.hide()

    #     self.occ10Png = QLabel(parentWindow)
    #     self.occ10Png.setGeometry(707, 213, 80, 70)
    #     self.occ10Png.setPixmap(QPixmap("src/main/TrackModel/pngs/occ10.png"))
    #     self.occ10Png.mousePressEvent = self.update_station_display
    #     self.occ10Png.hide()
    #     # Add rest later

    # def add_track_map(self, parentWindow):
    #     self.mapPng = QPixmap("src/main/TrackModel/pngs/blue_line.png")
    #     self.ogWidth, self.ogHeight = 950, 550
    #     self.mapWidth, self.mapHeight = self.ogWidth, self.ogHeight
    #     self.mapPng = self.mapPng.scaled(self.mapWidth, self.mapHeight)

    #     self.trackMap = QLabel(parentWindow)
    #     self.trackMap.setPixmap(self.mapPng)
    #     self.trackMap.setGeometry(0, 200, self.mapWidth, self.mapHeight)
    #     self.trackMap.hide()

    # def add_map_zoom(self, parentWindow):
    #     self.zoomInButton = QPushButton("+", parentWindow)
    #     self.zoomInButton.setGeometry(910, 210, 30, 30)
    #     self.zoomInButton.clicked.connect(self.zoom_in)
    #     self.zoomInButton.hide()

    #     self.zoomOutButton = QPushButton("-", parentWindow)
    #     self.zoomOutButton.setGeometry(910, 240, 30, 30)
    #     self.zoomOutButton.clicked.connect(self.zoom_out)
    #     self.zoomOutButton.hide()

    # def zoom_in(self):
    #     self.mapWidth += 50
    #     self.mapHeight += 50
    #     self.mapPng = self.mapPng.scaled(self.mapWidth, self.mapHeight)
    #     self.trackMap.setPixmap(self.mapPng)

    # def zoom_out(self):
    #     self.mapWidth -= 50
    #     self.mapHeight -= 50
    #     # Cannot zoom out past original size map
    #     self.mapWidth = max(self.mapWidth, self.ogWidth)
    #     self.mapHeight = max(self.mapHeight, self.ogHeight)
    #     self.mapPng = self.mapPng.scaled(self.mapWidth, self.mapHeight)
    #     self.trackMap.setPixmap(self.mapPng)

    # def display_file_path(self, parentWindow):
    #     # Originally, nothing is shown
    #     self.filePath = QLabel("", parentWindow)
    #     self.filePath.setGeometry(740, 130, 200, 30)
    #     self.filePath.setAlignment(Qt.AlignRight)
    #     self.filePath.setStyleSheet("color: #008000; font-size: 9px;")

    # def update_file_path(self, filePath):
    #     # When file is selected, its path is shown
    #     self.filePath.setText("Selected File:\n" + filePath)

    def add_import_button(self):
        importButton = QPushButton("Import Track Data", self.mainWindow)
        importButtonFont = QFont(MTA_STYLING["fontStyle"], MTA_STYLING["textFontSize"])
        importButton.setFont(importButtonFont)
        importButton.setGeometry(30, 260, 150, 30)
        importButton.setStyleSheet(
            f'background-color: {MTA_STYLING["darkBlue"]}; color: white'
        )
        # Need to call lambda as parent_window is not accessible otherwise
        importButton.clicked.connect(lambda: self.import_track_data())

    # def update_gui(self, filePath):
    #     self.update_file_path(filePath)
    #     self.select_line("Blue Line")  # Sets label to blue as that is the only line
    #     self.trackMap.show()
    #     self.zoomInButton.show()
    #     self.zoomOutButton.show()
    #     self.zoomInButton.setDisabled(True)
    #     self.zoomOutButton.setDisabled(True)
    #     self.changeFailuresButton.setEnabled(True)
    #     self.goButton.setEnabled(True)
    #     for checkbox in self.trackInfoCheckboxes.values():
    #         checkbox.setDisabled(False)

    def import_track_data(self):
        options = QFileDialog.Options() | QFileDialog.ReadOnly
        # Opens file explorer in new customized window
        filePath, _ = QFileDialog.getOpenFileName(
            self.mainWindow,
            "Import Track Data",
            "",
            "Excel Files (*.xlsx *.xls)",
            options=options,
        )

        if filePath:
            # Update Gui
            # self.update_gui(filePath)

            self.trackData = self.block.read_track_data(filePath, "Red Line")
            print(self.trackData)

    def add_input_section(self):
        entryFieldLabel = QLabel("Enter Block #:", self.mainWindow)
        entryFieldLabelFont = QFont(
            MTA_STYLING["fontStyle"], MTA_STYLING["headerFontSize"]
        )
        entryFieldLabel.setFont(entryFieldLabelFont)
        entryFieldLabel.setGeometry(570, 260, 170, 30)
        entryFieldLabel.setStyleSheet(f'color: {MTA_STYLING["darkBlue"]}')

        self.entryField = QLineEdit(self.mainWindow)
        entryFieldFont = QFont(MTA_STYLING["fontStyle"], MTA_STYLING["textFontSize"])
        self.entryField.setFont(entryFieldFont)
        self.entryField.setGeometry(750, 260, 120, 30)
        self.entryField.setPlaceholderText("Enter Block #")
        self.entryField.setStyleSheet(
            f'color: {MTA_STYLING["darkBlue"]}; border: 1px solid {MTA_STYLING["darkBlue"]};'
        )

        self.goButton = QPushButton("Go", self.mainWindow)
        goButtonFont = QFont(MTA_STYLING["fontStyle"], MTA_STYLING["textFontSize"])
        self.goButton.setFont(goButtonFont)
        self.goButton.setGeometry(880, 260, 60, 30)
        self.goButton.setStyleSheet(
            f'background-color: {MTA_STYLING["darkBlue"]}; color: white'
        )
        # Connect the button to the update_block_info_display method
        # self.goButton.clicked.connect(self.update_block_info_display)
        self.goButton.clicked.connect(self.update_blockinfo)
        # self.goButton.setEnabled(True)  # The button is disabled initially

        self.errorLabel = QLabel("", self.mainWindow)
        errorLabelFont = QFont(MTA_STYLING["fontStyle"], MTA_STYLING["textFontSize"])
        self.errorLabel.setFont(errorLabelFont)
        self.errorLabel.setGeometry(720, 290, 210, 30)
        self.errorLabel.setStyleSheet(f'color: {MTA_STYLING["red"]}; font-size: 14px')

        blockInfoLabel = QLabel("Block Information:", self.mainWindow)
        blockInfoFont = QFont(MTA_STYLING["fontStyle"], MTA_STYLING["headerFontSize"])
        blockInfoLabel.setFont(blockInfoFont)
        blockInfoLabel.setGeometry(645, 350, 220, 30)
        blockInfoLabel.setStyleSheet(f'color: {MTA_STYLING["darkBlue"]}')

    def show_block_data(self):
        infoFont = QFont(MTA_STYLING["fontStyle"], MTA_STYLING["labelFontSize"])
        infoStyle = f'color: {MTA_STYLING["darkBlue"]}'
        # firstColumn = 650, 400, 60, 20

        self.add_blockinfo_labels(infoStyle, infoFont)
        self.add_blockinfo(infoStyle, infoFont)

    def add_blockinfo_labels(self, style, font):
        lengthLabel = QLabel("Length:", self.mainWindow)
        lengthLabel.setFont(font)
        lengthLabel.setGeometry(600, 400, 140, 25)
        lengthLabel.setStyleSheet(style)

        speedLimitLabel = QLabel("Speed Limit:", self.mainWindow)
        speedLimitLabel.setFont(font)
        speedLimitLabel.setGeometry(600, 435, 140, 25)
        speedLimitLabel.setStyleSheet(style)

        gradeLabel = QLabel("Grade:", self.mainWindow)
        gradeLabel.setFont(font)
        gradeLabel.setGeometry(600, 470, 140, 25)
        gradeLabel.setStyleSheet(style)

        elevationLabel = QLabel("Elevation:", self.mainWindow)
        elevationLabel.setFont(font)
        elevationLabel.setGeometry(600, 505, 140, 25)
        elevationLabel.setStyleSheet(style)

        cumElevationLabel = QLabel("Cum. Elevation:", self.mainWindow)
        cumElevationLabel.setFont(font)
        cumElevationLabel.setGeometry(600, 540, 140, 25)
        cumElevationLabel.setStyleSheet(style)

        trackHeaterLabel = QLabel("Track Heater:", self.mainWindow)
        trackHeaterLabel.setFont(font)
        trackHeaterLabel.setGeometry(600, 575, 140, 25)
        trackHeaterLabel.setStyleSheet(style)

    def add_blockinfo(self, style, font):
        self.blockLengthLabel = QLabel(self.mainWindow)
        self.blockLengthLabel.setFont(font)
        self.blockLengthLabel.setStyleSheet(style)
        self.blockLengthLabel.setGeometry(750, 400, 110, 25)

        self.speedLimitLabel = QLabel(self.mainWindow)
        self.speedLimitLabel.setFont(font)
        self.speedLimitLabel.setStyleSheet(style)
        self.speedLimitLabel.setGeometry(750, 435, 110, 25)

        self.gradeLabel = QLabel(self.mainWindow)
        self.gradeLabel.setFont(font)
        self.gradeLabel.setStyleSheet(style)
        self.gradeLabel.setGeometry(750, 470, 110, 25)

        self.elevationLabel = QLabel(self.mainWindow)
        self.elevationLabel.setFont(font)
        self.elevationLabel.setStyleSheet(style)
        self.elevationLabel.setGeometry(750, 505, 110, 25)

        self.cumElevationLabel = QLabel(self.mainWindow)
        self.cumElevationLabel.setFont(font)
        self.cumElevationLabel.setStyleSheet(style)
        self.cumElevationLabel.setGeometry(750, 540, 110, 25)

        self.trackHeaterLabel = QLabel(self.mainWindow)
        self.trackHeaterLabel.setFont(font)
        self.trackHeaterLabel.setStyleSheet(style)
        self.trackHeaterLabel.setGeometry(750, 575, 110, 25)

    def update_blockinfo(self):
        self.parse_block_info()
        self.set_blocklength()
        self.set_speedlimit()
        self.set_grade()
        self.set_elevation()
        self.set_cumelevation()
        self.set_trackheater()

    def set_blocklength(self):
        self.blockLengthLabel.setText(f"{self.blockLength} m")

    def set_speedlimit(self):
        self.speedLimitLabel.setText(f"{self.blockSpeedLimit} Km/Hr")

    def set_grade(self):
        self.gradeLabel.setText(f"{self.blockGrade} %")

    def set_elevation(self):
        self.elevationLabel.setText(f"{self.blockElevation} M")

    def set_cumelevation(self):
        # Accept only up to certain numbers after decimal
        self.cumElevationLabel.setText(f"{self.blockCumElevation} M")

    def set_trackheater(self):
        self.trackHeaterLabel.setText(f"{self.blockTrackHeater}")

    def parse_block_info(self):
        # Obtain block number provided
        blockNumber = self.entryField.text()
        # Update the block info based on the block selected
        for data in self.trackData:
            if data["Block Number"] == int(blockNumber):
                self.blockLength = str(data["Block Length (m)"])
                self.blockSpeedLimit = str(data["Speed Limit (Km/Hr)"])
                self.blockGrade = str(data["Block Grade (%)"])
                self.blockElevation = str(data["ELEVATION (M)"])
                self.blockCumElevation = str(data["CUMALTIVE ELEVATION (M)"])

                self.failures = data[
                    "Failures"
                ]  # Store new blocks data in self.failures
                print(self.failures)
                self.check_failures()

    def check_failures(self):
        if "Track Circuit Failure" in self.failures:
            self.circuitSelection.show()
        else:
            self.circuitSelection.hide()
        if "Power Failure" in self.failures:
            self.powerSelection.show()
        else:
            self.powerSelection.hide()
        if "Broken Rail" in self.failures:
            self.brokenSelection.show()
        else:
            self.brokenSelection.hide()

    def add_failure_selection(self):
        failuresLabel = QLabel("Set Failures:", self.mainWindow)
        failuresLabelFont = QFont(
            MTA_STYLING["fontStyle"], MTA_STYLING["headerFontSize"]
        )
        failuresLabel.setFont(failuresLabelFont)
        failuresLabel.setGeometry(670, 630, 150, 30)
        failuresLabel.setStyleSheet(f'color: {MTA_STYLING["darkBlue"]}')

        circuitFailureLabel = QLabel("Circuit", self.mainWindow)
        circuitFailureLabelFont = QFont(
            MTA_STYLING["fontStyle"], MTA_STYLING["textFontSize"]
        )
        circuitFailureLabel.setFont(circuitFailureLabelFont)
        circuitFailureLabel.setGeometry(615, 665, 50, 30)
        circuitFailureLabel.setStyleSheet(f'color: {MTA_STYLING["darkBlue"]}')

        powerFailureLabel = QLabel("Power", self.mainWindow)
        powerFailureLabelFont = QFont(
            MTA_STYLING["fontStyle"], MTA_STYLING["textFontSize"]
        )
        powerFailureLabel.setFont(powerFailureLabelFont)
        powerFailureLabel.setGeometry(715, 665, 50, 30)
        powerFailureLabel.setStyleSheet(f'color: {MTA_STYLING["darkBlue"]}')

        brokenFailureLabel = QLabel("Broken", self.mainWindow)
        brokenFailureLabelFont = QFont(
            MTA_STYLING["fontStyle"], MTA_STYLING["textFontSize"]
        )
        brokenFailureLabel.setFont(brokenFailureLabelFont)
        brokenFailureLabel.setGeometry(815, 665, 50, 30)
        brokenFailureLabel.setStyleSheet(f'color: {MTA_STYLING["darkBlue"]}')

        circuitFailureSelector = QLabel(self.mainWindow)
        circuitFailureSelector.setGeometry(630, 695, 20, 20)
        circuitFailureSelector.setPixmap(
            QPixmap("src/main/TrackModel/pngs/circle_outline.png").scaled(20, 20)
        )
        circuitFailureSelector.mousePressEvent = self.set_circuit_failure

        powerFailureSelector = QLabel(self.mainWindow)
        powerFailureSelector.setGeometry(730, 695, 20, 20)
        powerFailureSelector.setPixmap(
            QPixmap("src/main/TrackModel/pngs/circle_outline.png").scaled(20, 20)
        )
        powerFailureSelector.mousePressEvent = self.set_power_failure

        brokenFailureSelector = QLabel(self.mainWindow)
        brokenFailureSelector.setGeometry(830, 695, 20, 20)
        brokenFailureSelector.setPixmap(
            QPixmap("src/main/TrackModel/pngs/circle_outline.png").scaled(20, 20)
        )
        brokenFailureSelector.mousePressEvent = self.set_broken_failure

        self.circuitSelection = QLabel(self.mainWindow)
        self.circuitSelection.setGeometry(630, 695, 20, 20)
        self.circuitSelection.setPixmap(
            QPixmap("src/main/TrackModel/pngs/red_circle.png").scaled(20, 20)
        )
        self.circuitSelection.hide()
        self.circuitSelection.mousePressEvent = self.set_circuit_failure

        self.powerSelection = QLabel(self.mainWindow)
        self.powerSelection.setGeometry(730, 695, 20, 20)
        self.powerSelection.setPixmap(
            QPixmap("src/main/TrackModel/pngs/red_circle.png").scaled(20, 20)
        )
        self.powerSelection.hide()
        self.powerSelection.mousePressEvent = self.set_power_failure

        self.brokenSelection = QLabel(self.mainWindow)
        self.brokenSelection.setGeometry(830, 695, 20, 20)
        self.brokenSelection.setPixmap(
            QPixmap("src/main/TrackModel/pngs/red_circle.png").scaled(20, 20)
        )
        self.brokenSelection.hide()
        self.brokenSelection.mousePressEvent = self.set_broken_failure

    def set_circuit_failure(self, event):
        # Obtain block number provided
        blockNumber = self.entryField.text()
        # Update the block info based on the block selected
        for data in self.trackData:
            if data["Block Number"] == int(blockNumber):
                if self.circuitSelection.isHidden():
                    self.circuitSelection.show()
                    self.failures.append("Track Circuit Failure")
                    data[
                        "Failures"
                    ] = self.failures  # Should append failure to this block
                    self.send_failure_alert(blockNumber)
                else:
                    self.circuitSelection.hide()
                    self.failures.remove("Track Circuit Failure")
                    data[
                        "Failures"
                    ] = self.failures  # Should remove failure to this block
        self.block.set_data(self.selectedLine, self.trackData)

    def set_power_failure(self, event):
        # Obtain block number provided
        blockNumber = self.entryField.text()
        # Update the block info based on the block selected
        for data in self.trackData:
            if data["Block Number"] == int(blockNumber):
                if self.powerSelection.isHidden():
                    self.powerSelection.show()
                    self.failures.append("Power Failure")
                    data[
                        "Failures"
                    ] = self.failures  # Should append failure to this block
                    self.send_failure_alert(blockNumber)
                else:
                    self.powerSelection.hide()
                    self.failures.remove("Power Failure")
                    data[
                        "Failures"
                    ] = self.failures  # Should remove failure to this block
        self.block.set_data(self.selectedLine, self.trackData)
        self.update_signal()  ###temp###

    def set_broken_failure(self, event):
        # Obtain block number provided
        blockNumber = self.entryField.text()
        # Update the block info based on the block selected
        for data in self.trackData:
            if data["Block Number"] == int(blockNumber):
                if self.brokenSelection.isHidden():
                    self.brokenSelection.show()
                    self.failures.append("Broken Rail")
                    data[
                        "Failures"
                    ] = self.failures  # Should append failure to this block
                    self.send_failure_alert(blockNumber)
                else:
                    self.brokenSelection.hide()
                    self.failures.remove("Broken Rail")
                    data[
                        "Failures"
                    ] = self.failures  # Should remove failure to this block
        self.block.set_data(self.selectedLine, self.trackData)

    # Toggle occupancy
    def toggle_occupied(self):
        # Obtain block number provided
        blockNumber = self.entryField.text()
        # Update the block info based on the block selected
        for data in self.trackData:
            if data["Block Number"] == int(blockNumber):
                if self.occupied == 0:
                    self.occupied == 1
                    data["Occupancy"] = self.occupied
                else:
                    self.occupied == 0
                    data["Occupancy"] = self.occupied
        self.block.set_data(self.selectedLine, self.trackData)

    ############################################################################################
    # Update signal state, includes turning off upon failure
    def update_signal(self):
        return

    # Send failure alert to Track Controller
    def send_failure_alert(self, blockNumber):
        return 1, blockNumber

    # Recieve maintenance from TrackData
    def update_block_state(self):
        blockNumber, self.maintenance = self.block.get_maintenance()
        for data in self.trackData:
            if data["Block Number"] == blockNumber:
                data["Maintenance"] = self.maintenance

    # Updates station information for specified block
    def update_station_info(self):
        self.trackData = self.block.get_data(self.selectedLine)

    # Show station data when station is selected
    def show_station(self):
        self.update_station_info()
        # update ui display for each station

    def show_occupancy(self):
        self.trackData = self.block.get_data(self.selectedLine)
        # show on ui (update blocks as they become occupied)

    # def add_block_info_display(self, parentWindow):
    #     self.blockInfoDisplay = QTextEdit(parentWindow)
    #     self.blockInfoDisplay.setGeometry(10, 550, 400, 160)
    #     self.blockInfoDisplay.setStyleSheet("background-color: white; font-size: 14px")
    #     self.blockInfoDisplay.setReadOnly(True)
    #     self.blockInfoDisplay.hide()

    # def add_selectable_block_info(self, parentWindow):
    #     label = QLabel("Block Information:", parentWindow)
    #     label.setGeometry(970, 210, 200, 30)
    #     label.setStyleSheet("font-weight: bold; font-size: 18px")

    #     self.blockInfoCheckboxes = {}
    #     blockInfo = [
    #         "Block Length",
    #         "Speed Limit",
    #         "Elevation",
    #         "Cumulative Elevation",
    #         "Block Grade",
    #         "Allowed Directions of Travel",
    #         "Track Heater",
    #         "Failures",
    #         "Beacon",
    #     ]
    #     yOffset = 240
    #     for info in blockInfo:
    #         checkbox = QCheckBox(info, parentWindow)
    #         checkbox.setGeometry(980, yOffset, 200, 30)
    #         self.blockInfoCheckboxes[info] = checkbox
    #         yOffset += 30
    #         checkbox.setDisabled(True)
    #         checkbox.stateChanged.connect(self.update_block_info_display)

    #     self.trackInfoCheckboxes = {}
    #     trackInfo = [
    #         "Show Occupied Blocks",
    #         "Show Switches",
    #         "Show Light Signals",
    #         "Show Railway Crossings",
    #     ]
    #     yOffset += 20
    #     for info in trackInfo:
    #         checkbox = QCheckBox(info, parentWindow)
    #         checkbox.setGeometry(970, yOffset, 160, 30)
    #         self.trackInfoCheckboxes[info] = checkbox
    #         checkbox.setDisabled(True)
    #         if "Switch" in info:
    #             switchPng = QLabel(parentWindow)
    #             switchPng.setGeometry(1080, yOffset, 30, 30)
    #             switchPng.setPixmap(
    #                 QPixmap("src/main/TrackModel/pngs/train_track.png").scaled(25, 25)
    #             )
    #         if "Light Signal" in info:
    #             lightSignalPng = QLabel(parentWindow)
    #             lightSignalPng.setGeometry(1100, yOffset, 30, 30)
    #             lightSignalPng.setPixmap(
    #                 QPixmap("src/main/TrackModel/pngs/traffic_light.png").scaled(25, 25)
    #             )
    #         if "Railway Crossing" in info:
    #             railwayCrossingPng = QLabel(parentWindow)
    #             railwayCrossingPng.setGeometry(1130, yOffset, 30, 30)
    #             railwayCrossingPng.setPixmap(
    #                 QPixmap("src/main/TrackModel/pngs/railway_crossing.png").scaled(
    #                     25, 25
    #                 )
    #             )

    #         yOffset += 30

    #     # Checkbox events
    #     showSwitchesCheckbox = self.trackInfoCheckboxes["Show Switches"]
    #     showSwitchesCheckbox.stateChanged.connect(self.change_switches_img)
    #     showSwitchesCheckbox = self.trackInfoCheckboxes["Show Occupied Blocks"]
    #     showSwitchesCheckbox.stateChanged.connect(self.change_occupied_img)

    # def add_station_info(self, parentWindow):
    #     self.stationInfo = QTextEdit("", parentWindow)
    #     self.stationInfo.setGeometry(760, 300, 160, 70)
    #     self.stationInfo.setAlignment(Qt.AlignCenter)
    #     self.stationInfo.setStyleSheet(
    #         "background-color: #d0efff; color: black; font-size: 14px"
    #     )
    #     self.stationInfo.hide()

    # def update_station_display(self, event):
    #     if self.stationInfo.isHidden():
    #         self.stationInfo.setText(
    #             f"<b>Blue Line</b>"
    #             f"<br>Ticket Sales/Hr: {self.ticketSales}</br>"
    #             f"<br>Waiting @ Station B: {self.waiting}</br>"
    #         )
    #         self.stationInfo.show()
    #     else:
    #         self.stationInfo.hide()

    # def change_switches_img(self, state):
    #     if state == Qt.Checked:
    #         self.switchPng.show()
    #     else:
    #         self.switchPng.hide()

    # def change_occupied_img(self, state):
    #     if state == Qt.Checked:
    #         self.occ1Png.show()
    #         self.occ10Png.show()
    #     else:
    #         self.occ1Png.hide()
    #         self.occ10Png.hide()

    # def update_block_info_display(self):
    #     # Always display the block number
    #     blockNumber = self.entryField.text()
    #     blockInfo = [f"Block Number: {blockNumber}"]

    #     # Check possible errors in block entry value
    #     if blockNumber.isdigit() and blockNumber:
    #         if blockNumber:
    #             blockCheck = self.check_block_exist(blockNumber)
    #             if blockCheck:
    #                 # Enable checkboxes if block # entry is valid
    #                 for checkbox in self.blockInfoCheckboxes.values():
    #                     checkbox.setDisabled(False)

    #                 self.blockInfoDisplay.setPlainText("\n".join(blockInfo))
    #                 self.blockInfoDisplay.show()
    #                 self.errorLabel.clear()
    #             else:
    #                 # Disable checkboxes if block # entry is not valid
    #                 for checkbox in self.blockInfoCheckboxes.values():
    #                     checkbox.setDisabled(True)

    #                 self.blockInfoDisplay.clear()
    #                 self.blockInfoDisplay.hide()
    #                 self.errorLabel.setText(f"Block {blockNumber} not found.")
    #     else:
    #         # Disable checkboxes if block # entry is not valid
    #         for checkbox in self.blockInfoCheckboxes.values():
    #             checkbox.setDisabled(True)

    #         self.blockInfoDisplay.clear()
    #         self.blockInfoDisplay.hide()
    #         self.errorLabel.setText("Please enter a valid block number.")

    #     # Check for checkbox selection
    #     for info, checkbox in self.blockInfoCheckboxes.items():
    #         if checkbox.isChecked():
    #             if info == "Block Length":
    #                 for data in self.trackData:
    #                     if data["Block Number"] == int(blockNumber):
    #                         blockInfo.append(
    #                             f"Block Length: {data['Block Length (m)']} m"
    #                         )
    #             if info == "Speed Limit":
    #                 for data in self.trackData:
    #                     if data["Block Number"] == int(blockNumber):
    #                         blockInfo.append(
    #                             f"Speed Limit: {data['Speed Limit (Km/Hr)']} Km/Hr"
    #                         )
    #             if info == "Elevation":
    #                 for data in self.trackData:
    #                     if data["Block Number"] == int(blockNumber):
    #                         blockInfo.append(f"Elevation: {data['ELEVATION (M)']} m")
    #             if info == "Cumulative Elevation":
    #                 for data in self.trackData:
    #                     if data["Block Number"] == int(blockNumber):
    #                         blockInfo.append(
    #                             f"Cumulative Elevation: {data['CUMALTIVE ELEVATION (M)']} m"
    #                         )
    #             if info == "Block Grade":
    #                 for data in self.trackData:
    #                     if data["Block Number"] == int(blockNumber):
    #                         blockInfo.append(f"Block Grade: {data['Block Grade (%)']}%")
    #             if info == "Allowed Directions of Travel":
    #                 for data in self.trackData:
    #                     if data["Block Number"] == int(blockNumber):
    #                         blockInfo.append(
    #                             f"Allowed Directions of Travel: {self.allowableDirections}"
    #                         )
    #             if info == "Track Heater":
    #                 for data in self.trackData:
    #                     if data["Block Number"] == int(blockNumber):
    #                         blockInfo.append(f"Track Heater: {self.trackHeater}")
    #             if info == "Failures":
    #                 for data in self.trackData:
    #                     if data["Block Number"] == int(blockNumber):
    #                         blockInfo.append(f"Failures: {data['Failures']}")
    #             if info == "Beacon":
    #                 for data in self.trackData:
    #                     if data["Block Number"] == int(blockNumber):
    #                         blockInfo.append(f"Beacon: {self.beacon}\n")
    #     # Then append to display is info is selected
    #     self.blockInfoDisplay.setPlainText("\n".join(blockInfo))

    # def check_block_exist(self, blockNumber):
    #     if self.trackData:
    #         for data in self.trackData:
    #             if data["Block Number"] == int(blockNumber):
    #                 return True
    #     return False

    # def add_change_failures_button(self, parentWindow):
    #     self.changeFailuresButton = QPushButton("Change Failures ->", parentWindow)
    #     self.changeFailuresButton.setStyleSheet("background-color: red; color: white")
    #     buttonWidth = 200
    #     buttonHeight = 30
    #     buttonX = int(950 + (parentWindow.width() - 950 - buttonWidth) / 2)
    #     buttonY = parentWindow.height() - 50
    #     self.changeFailuresButton.setGeometry(
    #         buttonX, buttonY, buttonWidth, buttonHeight
    #     )
    #     self.changeFailuresButton.setEnabled(True)

    #     self.changeFailuresButton.clicked.connect(self.show_failure_popup)

    # def add_tabbar(self, parentWindow):
    #     changeFailuresButton = QPushButton("Home", parentWindow)
    #     changeFailuresButton.setStyleSheet(
    #         "background-color: black; color: white; font-weight: bold; border: 2px solid white; border-bottom: none;"
    #     )
    #     changeFailuresButton.setGeometry(100, 70, 100, 30)

    #     testbenchTab = QPushButton("TestBench", parentWindow)
    #     testbenchTab.setStyleSheet(
    #         "background-color: black; color: white; font-weight: bold; border: 2px solid white; border-bottom: none;"
    #     )
    #     testbenchTab.setGeometry(200, 70, 100, 30)

    #     testbenchTab.clicked.connect(self.show_testbench)

    # def show_failure_popup(self):
    #     failurePopup = FailureWindow()
    #     failurePopup.failureWindow.exec()
    #     selectedBlock = failurePopup.get_selected_block()
    #     self.failures = failurePopup.get_selected_failures()

    #     # Update the track_data with failures
    #     for block in self.trackData:
    #         if block["Block Number"] == selectedBlock:
    #             # Convert to a string for the use of the display, but kept a list privately
    #             failuresStr = ", ".join(self.failures)
    #             if self.failures == "None":
    #                 failuresStr = "None"
    #             block["Failures"] = failuresStr
    #     self.update_block_info_display

    def show_testbench(self):
        testbenchWindow = TestbenchWindow()
        testbenchWindow.testbench.exec()


class TestbenchWindow:
    speed = ""
    authority = ""
    railwayState = 0
    switchState = 0
    trackHeaterState = 0
    trackState = "Open"
    ticketSales = ""
    waiting = ""
    lightState = "Green"
    failures = []

    def __init__(self):
        self.testbench = QDialog()
        self.setup_testbench()

    def setup_testbench(self):
        self.testbench.setWindowTitle("Change Failures")
        self.testbench.setGeometry(450, 300, 960, 600)

        # General layout
        self.add_mta_logo()
        self.add_title()
        self.add_hline()

        # Inputs
        self.setup_inputs()
        self.setup_failure_inputs()
        self.add_set_inputs()

        # Outputs
        self.add_outputs()

    def add_mta_logo(self):
        mtaLogo = QLabel(self.testbench)
        mtaLogo.setGeometry(0, 0, 80, 80)
        mtaLogo.setPixmap(
            QPixmap("src/main/TrackModel/pngs/MTA_logo.png").scaled(80, 80)
        )

    def add_title(self):
        windowWidth = self.testbench.width()
        labelWidth = 350
        titlePosition = int((windowWidth - labelWidth) / 2)

        titleLabel = QLabel("Track Model- Testbench", self.testbench)
        titleLabel.setGeometry(titlePosition, 25, labelWidth, 40)
        titleLabel.setAlignment(Qt.AlignCenter)
        titleFont = QFont("Arial", 18, QFont.Bold)
        titleLabel.setFont(titleFont)

    def add_hline(self):
        thickness = 5
        line = QFrame(self.testbench)
        line.setFrameShape(QFrame.HLine)
        line.setGeometry(0, 80, 960, thickness)
        line.setLineWidth(thickness)

    def setup_inputs(self):
        blueBackground = QWidget(self.testbench)
        blueBackground.setGeometry(10, 120, 400, 450)
        blueBackground.setStyleSheet("background-color: #A9D0F5;")

        whiteBackground = "background-color: white"

        inputsLabel = QLabel("Change Inputs:", blueBackground)
        inputsLabel.setGeometry(0, 0, 400, 30)
        inputsLabel.setStyleSheet(
            "background-color: blue; color: white; font-weight: bold"
        )
        inputsLabel.setAlignment(Qt.AlignCenter)

        selectBlock = QLabel("Select Block #:", blueBackground)
        selectBlock.setGeometry(10, 50, 150, 30)
        self.blockInput = QSpinBox(blueBackground)
        self.blockInput.setGeometry(120, 50, 50, 30)
        self.blockInput.setStyleSheet(whiteBackground)
        self.blockInput.setMinimum(1)
        self.blockInput.setMaximum(15)
        self.blockInput.setValue(1)
        goButton = QPushButton("Go", blueBackground)
        goButton.setGeometry(220, 50, 150, 30)
        goButton.setStyleSheet("background-color: blue; color: white")
        # Connect the button to the update_block_info_display method
        goButton.clicked.connect(self.update_display)

        speedLabel = QLabel("Set Commanded Speed (mph):", blueBackground)
        speedLabel.setGeometry(10, 90, 200, 30)
        self.speedInput = QLineEdit(blueBackground)
        self.speedInput.setGeometry(220, 90, 150, 30)
        self.speedInput.setStyleSheet(whiteBackground)
        self.speedInput.setEnabled(False)

        authorityLabel = QLabel("Set Authority (blocks):", blueBackground)
        authorityLabel.setGeometry(10, 130, 200, 30)
        self.authorityInput = QLineEdit(blueBackground)
        self.authorityInput.setGeometry(220, 130, 150, 30)
        self.authorityInput.setStyleSheet(whiteBackground)
        self.authorityInput.setEnabled(False)

        railwayLabel = QLabel("Set Railway Crossing (0/1):", blueBackground)
        railwayLabel.setGeometry(10, 170, 200, 30)
        self.railwayInput = QSpinBox(blueBackground)
        self.railwayInput.setGeometry(220, 170, 150, 30)
        self.railwayInput.setStyleSheet(whiteBackground)
        self.railwayInput.setMinimum(0)
        self.railwayInput.setMaximum(1)
        self.railwayInput.setValue(0)
        self.railwayInput.setEnabled(False)

        switchLabel = QLabel("Set Switch Position (0/1):", blueBackground)
        switchLabel.setGeometry(10, 210, 200, 30)
        self.switchInput = QSpinBox(blueBackground)
        self.switchInput.setGeometry(220, 210, 150, 30)
        self.switchInput.setStyleSheet(whiteBackground)
        self.switchInput.setMinimum(0)
        self.switchInput.setMaximum(1)
        self.switchInput.setValue(0)
        self.switchInput.setEnabled(False)

        heaterLabel = QLabel("Set Track Heater (0/1):", blueBackground)
        heaterLabel.setGeometry(10, 250, 200, 30)
        self.heaterInput = QSpinBox(blueBackground)
        self.heaterInput.setGeometry(220, 250, 150, 30)
        self.heaterInput.setStyleSheet(whiteBackground)
        self.heaterInput.setMinimum(0)
        self.heaterInput.setMaximum(1)
        self.heaterInput.setValue(0)
        self.heaterInput.setEnabled(False)

        trackStateLabel = QLabel("Set Track State:", blueBackground)
        trackStateLabel.setGeometry(10, 290, 200, 30)
        self.trackOpen = QRadioButton("Open", blueBackground)
        self.trackOpen.setGeometry(120, 290, 60, 30)
        self.trackOpen.setEnabled(False)
        self.trackOccupied = QRadioButton("Occupied", blueBackground)
        self.trackOccupied.setGeometry(190, 290, 80, 30)
        self.trackOccupied.setEnabled(False)
        self.trackMaintenance = QRadioButton("Maintenance", blueBackground)
        self.trackMaintenance.setGeometry(280, 290, 100, 30)
        self.trackMaintenance.setEnabled(False)
        self.trackStateButtons = QButtonGroup()
        self.trackStateButtons.addButton(self.trackOpen)
        self.trackStateButtons.addButton(self.trackOccupied)
        self.trackStateButtons.addButton(self.trackMaintenance)

        ticketSalesLabel = QLabel("Set Ticket Sales/Hr:", blueBackground)
        ticketSalesLabel.setGeometry(10, 330, 200, 30)
        self.ticketSalesInput = QLineEdit(blueBackground)
        self.ticketSalesInput.setGeometry(220, 330, 150, 30)
        self.ticketSalesInput.setStyleSheet(whiteBackground)
        self.ticketSalesInput.setEnabled(False)

        waitingLabel = QLabel("Set Waiting @ Station:", blueBackground)
        waitingLabel.setGeometry(10, 370, 200, 30)
        self.waitingInput = QLineEdit(blueBackground)
        self.waitingInput.setGeometry(220, 370, 150, 30)
        self.waitingInput.setStyleSheet(whiteBackground)
        self.waitingInput.setEnabled(False)

        lightLabel = QLabel("Set Light Color:", blueBackground)
        lightLabel.setGeometry(10, 410, 150, 30)
        self.greenRadio = QRadioButton("Green", blueBackground)
        self.greenRadio.setGeometry(170, 410, 70, 30)
        self.greenRadio.setEnabled(False)
        self.yellowRadio = QRadioButton("Yellow", blueBackground)
        self.yellowRadio.setGeometry(250, 410, 70, 30)
        self.yellowRadio.setEnabled(False)
        self.redRadio = QRadioButton("Red", blueBackground)
        self.redRadio.setGeometry(330, 410, 70, 30)
        self.redRadio.setEnabled(False)
        self.lightStateButtons = QButtonGroup()
        self.lightStateButtons.addButton(self.greenRadio)
        self.lightStateButtons.addButton(self.yellowRadio)
        self.lightStateButtons.addButton(self.redRadio)

    def setup_failure_inputs(self):
        redBackground = QWidget(self.testbench)
        redBackground.setGeometry(500, 120, 350, 80)
        redBackground.setStyleSheet("background-color: #ffd6d6;")

        failureLabel = QLabel("Set Failure Input:", redBackground)
        failureLabel.setGeometry(0, 0, 350, 30)
        failureLabel.setStyleSheet(
            "background-color: red; color: white; font-weight: bold"
        )
        failureLabel.setAlignment(Qt.AlignCenter)

        self.failureCheckboxes = []
        failures = ["Track Circuit Failure", "Power Failure", "Broken Rail"]
        xOffset = 0
        for failure in failures:
            option = QCheckBox(failure, redBackground)
            option.setGeometry(xOffset, 40, 150, 30)
            if failure == "Broken Rail":
                option.setGeometry(xOffset - 40, 40, 150, 30)
            option.setStyleSheet("background-color: #ffd6d6")
            self.failureCheckboxes.append(option)
            xOffset += 150

    def add_set_inputs(self):
        # Create a green button
        self.setInputsbutton = QPushButton("Set Inputs", self.testbench)
        self.setInputsbutton.setGeometry(625, 210, 100, 30)
        self.setInputsbutton.setStyleSheet(
            "background-color: green; color: white; font-weight: bold"
        )
        self.setInputsbutton.setEnabled(False)
        self.setInputsbutton.clicked.connect(self.update_outputs)

    def update_display(self):
        self.selectedBlock = self.blockInput.value()
        # Disable all input fields and buttons at the beginning
        self.speedInput.setEnabled(False)
        self.authorityInput.setEnabled(False)
        self.railwayInput.setEnabled(False)
        self.switchInput.setEnabled(False)
        self.heaterInput.setEnabled(False)
        self.ticketSalesInput.setEnabled(False)
        self.waitingInput.setEnabled(False)

        # Reset the radio button state
        self.trackOpen.setEnabled(False)
        self.trackOccupied.setEnabled(False)
        self.trackMaintenance.setEnabled(False)

        # Reset the radio button state
        self.greenRadio.setEnabled(False)
        self.yellowRadio.setEnabled(False)
        self.redRadio.setEnabled(False)
        # Enable the relevant input fields and buttons based on the selected block
        if self.selectedBlock == 5:
            self.switchInput.setEnabled(True)
        if self.selectedBlock == 10 or self.selectedBlock == 15:
            self.ticketSalesInput.setEnabled(True)
            self.waitingInput.setEnabled(True)

        self.heaterInput.setEnabled(True)
        self.speedInput.setEnabled(True)
        self.authorityInput.setEnabled(True)
        # Enable the radio buttons for track state and light state
        self.trackOpen.setEnabled(True)
        self.trackOccupied.setEnabled(True)
        self.trackMaintenance.setEnabled(True)
        self.greenRadio.setEnabled(True)
        self.yellowRadio.setEnabled(True)
        self.redRadio.setEnabled(True)

        # Enable the "Set Inputs" button
        self.setInputsbutton.setEnabled(True)

    def add_outputs(self):
        self.outputs = QTextEdit(self.testbench)
        self.outputs.setGeometry(500, 250, 350, 300)
        self.outputs.setStyleSheet("background-color: white; font-size: 14px")
        self.outputs.setReadOnly(True)
        self.outputs.show()

    def update_outputs(self):
        self.outputs.clear()
        self.failures = []
        self.outputs.append(f"\nBlock Number: {self.selectedBlock}")
        if self.speedInput.text() != "":
            self.speed = int(self.speedInput.text())
            self.outputs.append(f"Commanded Speed: {self.speed}")
        if self.authorityInput.text() != "":
            self.authority = int(self.authorityInput.text())
            self.outputs.append(f"Authority: {self.authority}")
        # self.railwayState = self.railwayInput.value()
        if self.selectedBlock == 5:
            self.switchState = self.switchInput.value()
            self.outputs.append(f"Switch State: {self.switchState}")
        self.trackHeaterState = self.heaterInput.value()
        self.outputs.append(f"Track Heater State: {self.trackHeaterState}")
        if self.selectedBlock == 10 or self.selectedBlock == 15:
            if self.ticketSalesInput.text() != "":
                self.ticketSales = int(self.ticketSalesInput.text())
                self.outputs.append(f"Authority: {self.ticketSales}")
            if self.waitingInput.text() != "":
                self.waiting = int(self.waitingInput.text())
                self.outputs.append(f"Authority: {self.waiting}")
        # Check for track state input
        trackState = self.trackStateButtons.checkedButton()
        if trackState:
            self.trackState = trackState.text()
            self.outputs.append(f"Track State: {self.trackState}")
        # Check for light color input
        lightState = self.lightStateButtons.checkedButton()
        if lightState:
            self.lightState = lightState.text()
            self.outputs.append(f"Light State: {self.lightState}")
        # Failures
        for checkbox in self.failureCheckboxes:
            if checkbox.isChecked():
                self.failures.append(checkbox.text())
        self.outputs.append(f"Failures: {self.failures}")


if __name__ == "__main__":
    trackmodel = TrackModel()
