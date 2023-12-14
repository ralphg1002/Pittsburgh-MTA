from .TrackData import TrackData
from .Station import Station
from .Track import TrackView
from .TestBench import TestbenchWindow
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from signals import masterSignals, trainModelToTrackModel, trackControllerToTrackModel, trackModelToTrackController

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
    signals = {}

    def __init__(self):
        self.block = TrackData()
        self.station = Station()
        self.load_data()

        trainModelToTrackModel.sendPolarity.connect(self.update_occupancy)
        trackControllerToTrackModel.switchState.connect(self.update_switch_state)
        trackControllerToTrackModel.lightState.connect(self.update_light_state)
        trackControllerToTrackModel.crossingState.connect(self.update_crossing_state)

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
        self.set_simulation_speed()
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
        gearPng = QPixmap("src/main/TrackModel/pngs/gear.svg")
        gearPng = gearPng.scaledToWidth(20, 20)
        testbenchIcon = QLabel(self.mainWindow)
        testbenchIcon.setPixmap(gearPng)
        testbenchIcon.setGeometry(40, 135, gearPng.width(), gearPng.height())

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

        # Timer from CTC
        self.timer = QTimer(self.mainWindow)
        self.timer.start(1000)
        self.timer.timeout.connect(self.get_CTC_timing)

        self.sysTime = QDateTime.currentDateTime()
        self.sysTime.setTime(QTime(0, 0, 0))

    def get_CTC_timing(self):
        masterSignals.timingMultiplier.connect(self.update_clock)

    def update_clock(self, period):
        time_interval = period
        masterSignals.clockSignal.connect(self.sysTime.setTime)
        self.timer.setInterval(time_interval)

        self.clock.setText(self.sysTime.toString("HH:mm:ss"))
        self.speedText.setText("x" + format(1 / (time_interval / 1000), ".3f"))

    def set_simulation_speed(self):
        systemSpeedFont = QFont(MTA_STYLING["fontStyle"], MTA_STYLING["textFontSize"])

        systemSpeedLabel = QLabel("System Speed:", self.mainWindow)
        systemSpeedLabel.setFont(systemSpeedFont)
        systemSpeedLabel.setGeometry(700, 130, 150, 30)
        systemSpeedLabel.setStyleSheet(f'color: {MTA_STYLING["darkBlue"]}')
        self.speedText = QLabel("x1.0", self.mainWindow)
        self.speedText.setFont(systemSpeedFont)
        self.speedText.setGeometry(850, 130, 50, 30)
        self.speedText.setStyleSheet(f'color: {MTA_STYLING["darkBlue"]}')

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

        # Set Base Line to Green
        self.change_button_color(MTA_STYLING["green"])
        self.toggle_green_data()  #################

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

    def toggle_red_data(self):
        self.trackView.showRedLineLayout()
        self.trackData = self.redTrackData
        self.selectedLine = "Red"

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

    def update_occupancy(self, line, curBlock, prevBlock):
        self.trackView.change_color(line, curBlock, prevBlock)
    
    def update_light_state(self, line, _, blockNum, state):
        greenLightBlocks = [0, 1, 76, 100, 150]
        redLightBlocks = [0, 32, 43, 66, 71, 76]
        if line == 1:
            if state == "green":
                if blockNum in greenLightBlocks:
                    self.trackView.greenTrack.removeItem(self.signals[blockNum])
                    del self.signals[blockNum]
                    # print(self.signals)
            elif state == "red" and (blockNum in greenLightBlocks):
                redLight = QPixmap("src/main/TrackModel/pngs/red-light.png")
                redLight = redLight.scaledToWidth(35)
                signal = QGraphicsPixmapItem(redLight)
                self.signals[blockNum] = signal
                if blockNum == 0:
                    signal.setPos(165, 291)
                if blockNum == 1:
                    signal.setPos(-15, 16)
                if blockNum == 76:
                    signal.setPos(20, 561)
                if blockNum == 100:
                    signal.setPos(-152, 501)
                if blockNum == 150:   
                    signal.setPos(-225, 161)              
                self.trackView.greenTrack.addItem(signal)
        if line == 2:
            if state == "Green":
                if blockNum in redLightBlocks:
                    self.trackView.redTrack.removeItem(self.signals[blockNum])
                    del self.signals[blockNum]
            elif state == "Red":
                redLight = QPixmap("src/main/TrackModel/pngs/red-light.png")
                redLight = redLight.scaledToWidth(35)
                signal = QGraphicsPixmapItem(redLight)
                self.signals[blockNum] = signal
                if blockNum == 0:
                    signal.setPos(118, -44)
                if blockNum == 32:
                    signal.setPos(-94, 91)
                if blockNum == 43:
                    signal.setPos(-94, 212)
                if blockNum == 66:
                    signal.setPos(-230, 271)
                if blockNum == 71:
                    signal.setPos(-128, 150)  
                if blockNum == 76:
                    signal.setPos(-128, 29)          
                self.trackView.redTrack.addItem(signal)

    def update_crossing_state(self, line, _, __, state):
        if line == 1:
            if state == 1:
                self.trackView.greenTrack.removeItem(self.signals[19.1])
                self.trackView.greenTrack.removeItem(self.signals[19.2])
                del self.signals[19.1]
                del self.signals[19.2]
                print(self.signals)
            elif state == 0:
                redLight = QPixmap("src/main/TrackModel/pngs/red-light.png")
                redLight = redLight.scaledToWidth(20)
                crossing = QGraphicsPixmapItem(redLight)
                crossing2 = QGraphicsPixmapItem(redLight)
                self.signals[19.1] = crossing
                self.signals[19.2] = crossing2
                crossing.setPos(-194, 12)
                crossing2.setPos(-175, 12)
                self.trackView.greenTrack.addItem(crossing)
                self.trackView.greenTrack.addItem(crossing2)
        if line == 2:
            if state == 1:
                self.trackView.redTrack.removeItem(self.signals[47.1])
                self.trackView.redTrack.removeItem(self.signals[47.2])
                del self.signals[47.1]
                del self.signals[47.2]
                print(self.signals)
            elif state == 0:
                redLight = QPixmap("src/main/TrackModel/pngs/red-light.png")
                redLight = redLight.scaledToWidth(20)
                crossing = QGraphicsPixmapItem(redLight)
                crossing2 = QGraphicsPixmapItem(redLight)
                self.signals[47.1] = crossing
                self.signals[47.2] = crossing2
                crossing.setPos(-104, 332)
                crossing2.setPos(-85, 332)
                self.trackView.redTrack.addItem(crossing)
                self.trackView.redTrack.addItem(crossing2)
                
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
        # self.update_file_path(filePath)
        # self.select_line("Blue Line")  # Sets label to blue as that is the only line
        # self.trackMap.show()
        # self.zoomInButton.show()
        # self.zoomOutButton.show()
        # self.zoomInButton.setDisabled(True)
        # self.zoomOutButton.setDisabled(True)
        # self.changeFailuresButton.setEnabled(True)
        # self.goButton.setEnabled(True)
        # for checkbox in self.trackInfoCheckboxes.values():
        #     checkbox.setDisabled(False)

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

            self.trackData = self.block.read_track_data(filePath, "Green Line")
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
        self.errorLabel.setGeometry(750, 290, 210, 30)
        self.errorLabel.setStyleSheet(f'color: {MTA_STYLING["red"]}; font-size: 14px')

        blockInfoLabel = QLabel("Block Information:", self.mainWindow)
        blockInfoFont = QFont(MTA_STYLING["fontStyle"], MTA_STYLING["headerFontSize"])
        blockInfoLabel.setFont(blockInfoFont)
        blockInfoLabel.setGeometry(645, 350, 220, 30)
        blockInfoLabel.setStyleSheet(f'color: {MTA_STYLING["darkBlue"]}')

    def show_block_data(self):
        infoFont = QFont(MTA_STYLING["fontStyle"], MTA_STYLING["labelFontSize"])
        infoStyle = f'color: {MTA_STYLING["darkBlue"]}'

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

        # Station Labels:
        self.stationNameLabel = QLabel(self.mainWindow)
        self.stationNameLabel.setFont(font)
        self.stationNameLabel.setStyleSheet(style)
        self.stationNameLabel.setGeometry(650, 800, 250, 25)

        self.ticketSalesLabel = QLabel(self.mainWindow)
        self.ticketSalesLabel.setFont(font)
        self.ticketSalesLabel.setStyleSheet(style)
        self.ticketSalesLabel.setText("Ticket Sales:")
        self.ticketSalesLabel.setGeometry(600, 830, 200, 25)
        self.ticketSalesLabel.hide()

        self.ticketSalesOutput = QLabel(self.mainWindow)
        self.ticketSalesOutput.setFont(font)
        self.ticketSalesOutput.setStyleSheet(style)
        self.ticketSalesOutput.setGeometry(850, 830, 200, 25)

        self.waitingLabel = QLabel(self.mainWindow)
        self.waitingLabel.setFont(font)
        self.waitingLabel.setStyleSheet(style)
        self.waitingLabel.setText("Passengers Waiting:")
        self.waitingLabel.setGeometry(600, 860, 200, 25)
        self.waitingLabel.hide()

        self.waitingOutput = QLabel(self.mainWindow)
        self.waitingOutput.setFont(font)
        self.waitingOutput.setStyleSheet(style)
        self.waitingOutput.setGeometry(850, 860, 200, 25)

        self.boardingLabel = QLabel(self.mainWindow)
        self.boardingLabel.setFont(font)
        self.boardingLabel.setStyleSheet(style)
        self.boardingLabel.setText("Passengers Boarding:")
        self.boardingLabel.setGeometry(600, 890, 200, 25)
        self.boardingLabel.hide()

        self.boardingOutput = QLabel(self.mainWindow)
        self.boardingOutput.setFont(font)
        self.boardingOutput.setStyleSheet(style)
        self.boardingOutput.setGeometry(850, 890, 200, 25)

        self.leavingLabel = QLabel(self.mainWindow)
        self.leavingLabel.setFont(font)
        self.leavingLabel.setStyleSheet(style)
        self.leavingLabel.setText("Passengers Disembarking:")
        self.leavingLabel.setGeometry(600, 920, 200, 25)
        self.leavingLabel.hide()

        self.leavingOutput = QLabel(self.mainWindow)
        self.leavingOutput.setFont(font)
        self.leavingOutput.setStyleSheet(style)
        self.leavingOutput.setGeometry(850, 920, 200, 25)

    def update_blockinfo(self):
        if self.entryField.text() == "":
            self.errorLabel.setText("Please enter a block number")
        elif self.entryField.text().isnumeric() == False:
            self.errorLabel.setText("Please enter a valid block number")
        elif ((int(self.entryField.text()) > 151 or int(self.entryField.text()) < 0) and self.selectedLine == "Green") or ((int(self.entryField.text()) > 76 or int(self.entryField.text()) < 0) and self.selectedLine == "Red"):
            self.errorLabel.setText("Block Number does not exist")
        else:
            self.errorLabel.setText("") #Clear error message
            if self.selectedLine == "Green":
                self.trackData = self.block.get_data("Green")
            elif self.selectedLine == "Red":
                self.trackData = self.block.get_data("Red")
            self.parse_block_info()
            self.set_blocklength()
            self.set_speedlimit()
            self.set_grade()
            self.set_elevation()
            self.set_cumelevation()
            self.set_trackheater()
            self.show_station_data()          

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

    def show_station_data(self):
        blockNumber = self.entryField.text()

        for data in self.trackData:
            if data["Block Number"] == int(blockNumber):
                if type(data["Infrastructure"]) == str and "STATION" in data["Infrastructure"]:
                    stationName = str(data["Infrastructure"])
                    stationName = stationName.split(";")[0]
                    print(stationName)
                    # if stationName in data["Infrastructure"]:
                    #     print(data["Infrasctructure"])#Left off here
                    self.stationNameLabel.setText(f"{stationName}")
                    self.ticketSalesLabel.show()
                    self.waitingLabel.show()
                    self.boardingLabel.show()
                    self.leavingLabel.show()
                    self.ticketSalesOutput.setText(f"{data['Ticket Sales']}")
                    self.ticketSalesOutput.show()
                    self.waitingOutput.setText(f"{data['Passengers Waiting']}")
                    self.waitingOutput.show()
                    self.boardingOutput.setText(f"{data['Passengers Boarding']}")
                    self.boardingOutput.show()
                    self.leavingOutput.setText(f"{data['Passengers Disembarking']}")
                    self.leavingOutput.show()
                else:
                    self.stationNameLabel.setText(f"")
                    self.ticketSalesOutput.hide()
                    self.waitingOutput.hide()
                    self.boardingOutput.hide()
                    self.leavingOutput.hide()
                    self.ticketSalesLabel.hide()
                    self.waitingLabel.hide()
                    self.boardingLabel.hide()
                    self.leavingLabel.hide()

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
                    data["Occupancy"] = 1
                    self.emit_occupancy(int(blockNumber), None)
                else:
                    self.circuitSelection.hide()
                    self.failures.remove("Track Circuit Failure")
                    data[
                        "Failures"
                    ] = self.failures  # Should remove failure to this block
                    data["Occupancy"] = 0
                    self.emit_occupancy(None, int(blockNumber))
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
                    data["Occupancy"] = 1
                    self.emit_occupancy(int(blockNumber), None)
                else:
                    self.powerSelection.hide()
                    self.failures.remove("Power Failure")
                    data[
                        "Failures"
                    ] = self.failures  # Should remove failure to this block
                    data["Occupancy"] = 0
                    self.emit_occupancy(None, int(blockNumber))
        self.block.set_data(self.selectedLine, self.trackData)

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
                    data["Occupancy"] = 1
                    self.emit_occupancy(int(blockNumber), None)
                else:
                    self.brokenSelection.hide()
                    self.failures.remove("Broken Rail")
                    data[
                        "Failures"
                    ] = self.failures  # Should remove failure to this block
                    data["Occupancy"] = 0
                    self.emit_occupancy(None, int(blockNumber))
        self.block.set_data(self.selectedLine, self.trackData)
    
    def emit_occupancy(self, onBlockNum, offBlockNum):
        line = self.selectedLine
        if offBlockNum == None:
            curBlock = int(onBlockNum)
            self.update_occupancy(self.selectedLine, curBlock, None)
            if line == "Green":
                line = 1
            elif line == "Red":
                line = 2
            wayside = self.get_wayside_num(curBlock, line)
            trackModelToTrackController.occupancyState.emit(line, wayside, curBlock, True)  
        elif onBlockNum == None:
            curBlock = int(offBlockNum)
            self.update_occupancy(self.selectedLine, None, curBlock)
            if line == "Green":
                line = 1
            elif line == "Red":
                line = 2
            wayside = self.get_wayside_num(curBlock, line)
            trackModelToTrackController.occupancyState.emit(line, wayside, curBlock, False) 

    def get_wayside_num(self, blockNum, line):
        if line == 1:
            blockNum = int(blockNum)
            if (blockNum >= 1 and blockNum <= 30) or (blockNum >= 102 and blockNum <= 150):
                return 1
            # return 2
        elif line == 2:
            if (blockNum >= 0 and blockNum <= 27) or (blockNum >= 72 and blockNum <= 76):
                return 1
        return 2
                

    def update_switch_state(self, line, _, blockNum, state):
        self.trackView.change_switch(line, blockNum, state)

    def show_testbench(self):
        testbenchWindow = TestbenchWindow()
        testbenchWindow.testbench.exec()


if __name__ == "__main__":
    trackmodel = TrackModel()
