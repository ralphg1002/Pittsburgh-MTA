import sys
import re
import load_track
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


# DONE :)
class FailureWindow:
    selectedBlock = None
    selectedFailures = []

    def __init__(self):
        self.failureWindow = QDialog()
        self.setup_failure_popup()

    def setup_failure_popup(self):
        self.failureWindow.setWindowTitle("Change Failures")
        self.failureWindow.setGeometry(1550, 500, 250, 300)
        self.failureWindow.setStyleSheet("background-color: #ff4747;")

        self.failure_title()
        self.change_background()
        self.add_block_selection()
        self.add_failure_selection()
        self.add_set_button()

    def failure_title(self):
        title = QLabel("Failure Configuration:", self.failureWindow)
        title.setGeometry(10, 10, 230, 30)
        title.setStyleSheet("font-weight: bold; font-size: 18px")

        # Horizontal divider line
        thickness = 5
        hline = QFrame(self.failureWindow)
        hline.setFrameShape(QFrame.HLine)
        hline.setGeometry(0, 40, 250, thickness)
        hline.setLineWidth(thickness)

    def change_background(self):
        background = QWidget(self.failureWindow)
        background.setGeometry(0, 45, 250, 300)
        background.setStyleSheet("background-color: #ffd6d6;")

    def add_block_selection(self):
        selectBlock = QLabel("Select Block #:", self.failureWindow)
        selectBlock.setGeometry(10, 50, 230, 30)
        selectBlock.setStyleSheet(
            "font-weight: bold; font-size: 18px; background-color: #ffd6d6;"
        )

        # Add a dropdown selection
        self.blockDropdown = QComboBox(self.failureWindow)
        self.blockDropdown.setGeometry(10, 80, 115, 30)
        self.blockDropdown.setStyleSheet("background-color: white;")
        for i in range(1, 16):
            self.blockDropdown.addItem("Block " + str(i))

        self.blockDropdown.currentIndexChanged.connect(self.update_exit_button_state)

    def add_failure_selection(self):
        setFailure = QLabel("Set Failure Type:", self.failureWindow)
        setFailure.setGeometry(10, 120, 230, 30)
        setFailure.setStyleSheet(
            "font-weight: bold; font-size: 18px; background-color: #ffd6d6"
        )

        self.failureCheckboxes = []
        failures = ["Track Circuit Failure", "Power Failure", "Broken Rail"]
        yOffset = 150
        for failure in failures:
            option = QCheckBox(failure, self.failureWindow)
            option.setGeometry(10, yOffset, 230, 30)
            option.setStyleSheet("background-color: #ffd6d6")
            self.failureCheckboxes.append(option)
            yOffset += 30

    def update_exit_button_state(self):
        # Enable the button to "Set Failure Configuration" if a drop down item from the menu is selected
        isBlockSelected = self.blockDropdown.currentIndex() != -1
        self.button.setEnabled(isBlockSelected)

    def add_set_button(self):
        self.button = QPushButton("Set Failure Configuration", self.failureWindow)
        self.button.setGeometry(50, 250, 150, 30)
        self.button.setStyleSheet("background-color: #39E75F;")
        self.button.clicked.connect(self.update_failure)
        self.button.setEnabled(False)  # Button is set as disabled to begin with

    def update_failure(self):
        selectedBlockIndex = self.blockDropdown.currentIndex()
        selectedBlock = self.blockDropdown.itemText(selectedBlockIndex)

        self.selectedFailures.clear()
        for checkbox in self.failureCheckboxes:
            if checkbox.isChecked():
                self.selectedFailures.append(checkbox.text())
        self.selectedBlock = selectedBlock

        self.failureWindow.close()

    def get_selected_block(self):
        if self.selectedBlock != None:
            # Pull block int from string
            pattern = r"\d+"
            searchInt = re.search(pattern, self.selectedBlock)
            if searchInt:
                blockNum = int(searchInt.group())
                return blockNum

    def get_selected_failures(self):
        if self.selectedFailures == []:
            return "None"
        return self.selectedFailures


class SelectionWindow:
    simulationSpeed = 1.0
    selectedLine = None
    temperature = 65
    allowableDirections = "EAST/WEST"
    trackHeater = "OFF"
    failures = "None"
    beacon = "---"
    ticketSales = 0
    waiting = 0

    def __init__(self):
        self.setup_selection_window()

    def setup_selection_window(self):
        app = QApplication(sys.argv)
        mainWindow = QWidget()
        mainWindow.setGeometry(350, 200, 1200, 750)
        mainWindow.setWindowTitle("Track Model")
        app.setWindowIcon(QIcon("src/main/TrackModel/pngs/MTA_logo.png"))

        # General layout
        self.add_mta_logo(mainWindow)
        self.set_clock(mainWindow)
        self.set_simulation_speed_controls(mainWindow)
        self.add_vline(mainWindow)
        self.add_hline(mainWindow)
        self.add_title(mainWindow)
        self.add_tabbar(mainWindow)

        # Map
        self.add_line_panel(mainWindow)
        self.control_temperature(mainWindow)
        self.add_import_button(mainWindow)
        # The following are hidden initially and are shown upon an excel file import
        self.display_file_path(mainWindow)
        self.add_track_map(mainWindow)
        self.add_map_zoom(mainWindow)
        self.add_map_pngs(mainWindow)

        self.add_block_info_display(mainWindow)
        self.add_station_info(mainWindow)

        # Block Info Selection
        self.add_input_section(mainWindow)
        self.add_selectable_block_info(mainWindow)
        self.add_change_failures_button(mainWindow)

        mainWindow.show()
        sys.exit(app.exec_())

    def add_mta_logo(self, parentWindow):
        mtaPng = QPixmap("src/main/TrackModel/pngs/mta_logo.png")
        mtaPng = mtaPng.scaledToWidth(90)
        mtaLogo = QLabel(parentWindow)
        mtaLogo.setPixmap(mtaPng)
        mtaLogo.setGeometry(0, 0, mtaPng.width(), mtaPng.height())

    def set_clock(self, parentWindow):
        self.clock = QLabel("System Clock: 00:00:00", parentWindow)
        self.clock.setGeometry(980, 10, 220, 30)
        self.clock.setStyleSheet("font-weight: bold; font-size: 18px")
        self.update_clock()

        # Update clock in real time while window is open
        timer = QTimer(parentWindow)
        timer.timeout.connect(self.update_clock)
        # Update every 1 second
        timer.start(1000)

    def update_clock(self):
        currentDatetime = QDateTime.currentDateTime()
        formattedTime = currentDatetime.toString("HH:mm:ss")
        self.clock.setText("System Clock: " + formattedTime)

    def set_simulation_speed_controls(self, parentWindow):
        simulationSpeedText = QLabel("Simulation Speed:", parentWindow)
        simulationSpeedText.setGeometry(900, 50, 170, 30)
        simulationSpeedText.setStyleSheet("font-weight: bold; font-size: 18px")

        self.speedText = QLabel("1.0x", parentWindow)
        self.speedText.setGeometry(1110, 50, 40, 30)
        self.speedText.setAlignment(Qt.AlignCenter)
        self.speedText.setStyleSheet("font-weight: bold; font-size: 18px")

        decreaseSpeed = QPushButton("<<", parentWindow)
        decreaseSpeed.setGeometry(1070, 55, 30, 20)
        decreaseSpeed.clicked.connect(self.decrease_simulation_speed)

        increaseSpeed = QPushButton(">>", parentWindow)
        increaseSpeed.setGeometry(1160, 55, 30, 20)
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

    def add_vline(self, parentWindow):
        thickness = 5

        line = QFrame(parentWindow)
        line.setFrameShape(QFrame.VLine)
        line.setGeometry(950, 100, thickness, 700)
        line.setLineWidth(thickness)

    def add_hline(self, parentWindow):
        thickness = 5

        line = QFrame(parentWindow)
        line.setFrameShape(QFrame.HLine)
        line.setGeometry(0, 100, 1200, thickness)
        line.setLineWidth(thickness)

    def add_title(self, parentWindow):
        windowWidth = parentWindow.width()
        labelWidth = 300
        titlePosition = int((windowWidth - labelWidth) / 2)

        titleLabel = QLabel("Track Model", parentWindow)
        titleLabel.setGeometry(titlePosition, 35, labelWidth, 30)
        titleLabel.setAlignment(Qt.AlignCenter)
        titleFont = QFont("Arial", 20, QFont.Bold)
        titleLabel.setFont(titleFont)

    def add_line_panel(self, parentWindow):
        selectLine = QLabel("Select Line:", parentWindow)
        selectLine.setGeometry(90, 130, 110, 30)
        selectLine.setStyleSheet("font-weight: bold; font-size: 18px")

        self.bluePanel = QLabel("Blue Line", parentWindow)
        self.greenPanel = QLabel("Green Line", parentWindow)
        self.redPanel = QLabel("Red Line", parentWindow)

        self.bluePanel.setGeometry(20, 160, 80, 30)
        self.greenPanel.setGeometry(100, 160, 80, 30)
        self.redPanel.setGeometry(180, 160, 80, 30)

        # Initially greyed out as none are selected
        unselected = "background-color: grey; color: white; border: 1px solid black; border-radius: 5px; padding: 5px;"
        self.bluePanel.setStyleSheet(unselected)
        self.greenPanel.setStyleSheet(unselected)
        self.redPanel.setStyleSheet(unselected)

        # Handlers that call the select_line method
        self.bluePanel.mousePressEvent = (
            lambda event, line="Blue Line": self.select_line(line)
        )
        self.greenPanel.mousePressEvent = (
            lambda event, line="Green Line": self.select_line(line)
        )
        self.redPanel.mousePressEvent = lambda event, line="Red Line": self.select_line(
            line
        )

    def select_line(self, selectedLine):
        unselected = "background-color: grey; color: white; border: 1px solid black; border-radius: 5px; padding: 5px;"
        if selectedLine != self.selectedLine:
            if selectedLine == "Blue Line":
                self.bluePanel.setStyleSheet(
                    "background-color: blue; color: white; border: 1px solid black; border-radius: 5px; padding: 5px;"
                )
                self.greenPanel.setStyleSheet(unselected)
                self.redPanel.setStyleSheet(unselected)
            elif selectedLine == "Green Line":
                self.bluePanel.setStyleSheet(unselected)
                self.greenPanel.setStyleSheet(
                    "background-color: green; color: white; border: 1px solid black; border-radius: 5px; padding: 5px;"
                )
                self.redPanel.setStyleSheet(unselected)
            elif selectedLine == "Red Line":
                self.bluePanel.setStyleSheet(unselected)
                self.greenPanel.setStyleSheet(unselected)
                self.redPanel.setStyleSheet(
                    "background-color: red; color: white; border: 1px solid black; border-radius: 5px; padding: 5px;"
                )

            self.selectedLine = selectedLine

    def control_temperature(self, parentWindow):
        setTemperature = QLabel("Set Temperature:", parentWindow)
        setTemperature.setGeometry(420, 130, 160, 30)
        setTemperature.setStyleSheet("font-weight: bold; font-size: 18px")

        self.temperatureInput = QLineEdit(parentWindow)
        self.temperatureInput.setGeometry(440, 160, 40, 30)
        self.temperatureInput.setAlignment(Qt.AlignCenter)
        self.temperatureInput.setPlaceholderText("65")

        fahrenheitUnit = QLabel("°F", parentWindow)
        fahrenheitUnit.setGeometry(480, 160, 30, 30)
        fahrenheitUnit.setStyleSheet("font-weight: bold; font-size: 14px")

        setTemperatureButton = QPushButton("Set", parentWindow)
        setTemperatureButton.setGeometry(500, 160, 60, 30)
        setTemperatureButton.setStyleSheet("background-color: blue; color: white")
        setTemperatureButton.clicked.connect(self.set_temperature)

    def set_temperature(self):
        if self.temperatureInput.text() != "":
            self.temperature = self.temperatureInput.text()
        self.temperatureInput.setPlaceholderText(str(self.temperature))
        print(self.temperature)

    def add_map_pngs(self, parentWindow):
        self.switchPng = QLabel(parentWindow)
        self.switchPng.setGeometry(450, 420, 30, 30)
        self.switchPng.setPixmap(
            QPixmap("src/main/TrackModel/pngs/train_track.png").scaled(25, 25)
        )
        self.switchPng.hide()

        # Temp
        self.occ1Png = QLabel(parentWindow)
        self.occ1Png.setGeometry(80, 422, 80, 60)
        self.occ1Png.setPixmap(QPixmap("src/main/TrackModel/pngs/occ1.png"))
        self.occ1Png.hide()

        self.occ10Png = QLabel(parentWindow)
        self.occ10Png.setGeometry(707, 213, 80, 70)
        self.occ10Png.setPixmap(QPixmap("src/main/TrackModel/pngs/occ10.png"))
        self.occ10Png.mousePressEvent = self.update_station_display
        self.occ10Png.hide()
        # Add rest later

    def add_track_map(self, parentWindow):
        self.mapPng = QPixmap("src/main/TrackModel/pngs/blue_line.png")
        self.ogWidth, self.ogHeight = 950, 550
        self.mapWidth, self.mapHeight = self.ogWidth, self.ogHeight
        self.mapPng = self.mapPng.scaled(self.mapWidth, self.mapHeight)

        self.trackMap = QLabel(parentWindow)
        self.trackMap.setPixmap(self.mapPng)
        self.trackMap.setGeometry(0, 200, self.mapWidth, self.mapHeight)
        self.trackMap.hide()

    def add_map_zoom(self, parentWindow):
        self.zoomInButton = QPushButton("+", parentWindow)
        self.zoomInButton.setGeometry(910, 210, 30, 30)
        self.zoomInButton.clicked.connect(self.zoom_in)
        self.zoomInButton.hide()

        self.zoomOutButton = QPushButton("-", parentWindow)
        self.zoomOutButton.setGeometry(910, 240, 30, 30)
        self.zoomOutButton.clicked.connect(self.zoom_out)
        self.zoomOutButton.hide()

    def zoom_in(self):
        self.mapWidth += 50
        self.mapHeight += 50
        self.mapPng = self.mapPng.scaled(self.mapWidth, self.mapHeight)
        self.trackMap.setPixmap(self.mapPng)

    def zoom_out(self):
        self.mapWidth -= 50
        self.mapHeight -= 50
        # Cannot zoom out past original size map
        self.mapWidth = max(self.mapWidth, self.ogWidth)
        self.mapHeight = max(self.mapHeight, self.ogHeight)
        self.mapPng = self.mapPng.scaled(self.mapWidth, self.mapHeight)
        self.trackMap.setPixmap(self.mapPng)

    def display_file_path(self, parentWindow):
        # Originally, nothing is shown
        self.filePath = QLabel("", parentWindow)
        self.filePath.setGeometry(740, 130, 200, 30)
        self.filePath.setAlignment(Qt.AlignRight)
        self.filePath.setStyleSheet("color: #008000; font-size: 9px;")

    def update_file_path(self, filePath):
        # When file is selected, its path is shown
        self.filePath.setText("Selected File:\n" + filePath)

    def add_import_button(self, parentWindow):
        importPng = QLabel(parentWindow)
        importPng.setGeometry(790, 160, 30, 30)
        importPng.setPixmap(
            QPixmap("src/main/TrackModel/pngs/import_arrow.png").scaled(30, 30)
        )

        importButton = QPushButton("Import Track Data", parentWindow)
        importButton.setGeometry(820, 160, 120, 30)
        importButton.setStyleSheet("background-color: #39E75F;")
        # Need to call lambda as parent_window is not accessible otherwise
        importButton.clicked.connect(lambda: self.import_track_data(parentWindow))

    def update_gui(self, filePath):
        self.update_file_path(filePath)
        self.select_line("Blue Line")  # Sets label to blue as that is the only line
        self.trackMap.show()
        self.zoomInButton.show()
        self.zoomOutButton.show()
        self.zoomInButton.setDisabled(True)
        self.zoomOutButton.setDisabled(True)
        self.changeFailuresButton.setEnabled(True)
        self.goButton.setEnabled(True)
        for checkbox in self.trackInfoCheckboxes.values():
            checkbox.setDisabled(False)

    def import_track_data(self, parentWindow):
        options = QFileDialog.Options() | QFileDialog.ReadOnly
        # Opens file explorer in new customized window
        filePath, _ = QFileDialog.getOpenFileName(
            parentWindow,
            "Import Track Data",
            "",
            "Excel Files (*.xlsx *.xls)",
            options=options,
        )

        if filePath:
            # Update Gui
            self.update_gui(filePath)

            self.trackData = load_track.read_track_data(filePath)
            # Add failures, set to default "None" to begin
            for block in self.trackData:
                block["Failures"] = self.failures

            print(self.trackData)

    def add_input_section(self, parentWindow):
        label = QLabel("Enter Block #:", parentWindow)
        label.setGeometry(970, 120, 150, 30)
        label.setStyleSheet("font-weight: bold; font-size: 18px")

        self.entryField = QLineEdit(parentWindow)
        self.entryField.setGeometry(970, 160, 100, 30)
        self.entryField.setPlaceholderText("Enter block #")

        self.goButton = QPushButton("Go", parentWindow)
        self.goButton.setGeometry(1080, 160, 60, 30)
        self.goButton.setStyleSheet("background-color: blue; color: white")
        # Connect the button to the update_block_info_display method
        self.goButton.clicked.connect(self.update_block_info_display)
        self.goButton.setEnabled(False)  # The button is disabled initially

        self.errorLabel = QLabel("", parentWindow)
        self.errorLabel.setGeometry(970, 185, 210, 30)
        self.errorLabel.setStyleSheet("color: red; font-size: 14px")

    def add_block_info_display(self, parentWindow):
        self.blockInfoDisplay = QTextEdit(parentWindow)
        self.blockInfoDisplay.setGeometry(10, 550, 400, 160)
        self.blockInfoDisplay.setStyleSheet("background-color: white; font-size: 14px")
        self.blockInfoDisplay.setReadOnly(True)
        self.blockInfoDisplay.hide()

    def add_selectable_block_info(self, parentWindow):
        label = QLabel("Block Information:", parentWindow)
        label.setGeometry(970, 210, 200, 30)
        label.setStyleSheet("font-weight: bold; font-size: 18px")

        self.blockInfoCheckboxes = {}
        blockInfo = [
            "Block Length",
            "Speed Limit",
            "Elevation",
            "Cumulative Elevation",
            "Block Grade",
            "Allowed Directions of Travel",
            "Track Heater",
            "Failures",
            "Beacon",
        ]
        yOffset = 240
        for info in blockInfo:
            checkbox = QCheckBox(info, parentWindow)
            checkbox.setGeometry(980, yOffset, 200, 30)
            self.blockInfoCheckboxes[info] = checkbox
            yOffset += 30
            checkbox.setDisabled(True)
            checkbox.stateChanged.connect(self.update_block_info_display)

        self.trackInfoCheckboxes = {}
        trackInfo = [
            "Show Occupied Blocks",
            "Show Switches",
            "Show Light Signals",
            "Show Railway Crossings",
        ]
        yOffset += 20
        for info in trackInfo:
            checkbox = QCheckBox(info, parentWindow)
            checkbox.setGeometry(970, yOffset, 160, 30)
            self.trackInfoCheckboxes[info] = checkbox
            checkbox.setDisabled(True)
            if "Switch" in info:
                switchPng = QLabel(parentWindow)
                switchPng.setGeometry(1080, yOffset, 30, 30)
                switchPng.setPixmap(
                    QPixmap("src/main/TrackModel/pngs/train_track.png").scaled(25, 25)
                )
            if "Light Signal" in info:
                lightSignalPng = QLabel(parentWindow)
                lightSignalPng.setGeometry(1100, yOffset, 30, 30)
                lightSignalPng.setPixmap(
                    QPixmap("src/main/TrackModel/pngs/traffic_light.png").scaled(25, 25)
                )
            if "Railway Crossing" in info:
                railwayCrossingPng = QLabel(parentWindow)
                railwayCrossingPng.setGeometry(1130, yOffset, 30, 30)
                railwayCrossingPng.setPixmap(
                    QPixmap("src/main/TrackModel/pngs/railway_crossing.png").scaled(
                        25, 25
                    )
                )

            yOffset += 30

        # Checkbox events
        showSwitchesCheckbox = self.trackInfoCheckboxes["Show Switches"]
        showSwitchesCheckbox.stateChanged.connect(self.change_switches_img)
        showSwitchesCheckbox = self.trackInfoCheckboxes["Show Occupied Blocks"]
        showSwitchesCheckbox.stateChanged.connect(self.change_occupied_img)

    def add_station_info(self, parentWindow):
        self.stationInfo = QTextEdit("", parentWindow)
        self.stationInfo.setGeometry(760, 300, 160, 70)
        self.stationInfo.setAlignment(Qt.AlignCenter)
        self.stationInfo.setStyleSheet(
            "background-color: #d0efff; color: black; font-size: 14px"
        )
        self.stationInfo.hide()

    def update_station_display(self, event):
        if self.stationInfo.isHidden():
            self.stationInfo.setText(
                f"<b>Blue Line</b>"
                f"<br>Ticket Sales/Hr: {self.ticketSales}</br>"
                f"<br>Waiting @ Station B: {self.waiting}</br>"
            )
            self.stationInfo.show()
        else:
            self.stationInfo.hide()

    def change_switches_img(self, state):
        if state == Qt.Checked:
            self.switchPng.show()
        else:
            self.switchPng.hide()

    def change_occupied_img(self, state):
        if state == Qt.Checked:
            self.occ1Png.show()
            self.occ10Png.show()
        else:
            self.occ1Png.hide()
            self.occ10Png.hide()

    def update_block_info_display(self):
        # Always display the block number
        blockNumber = self.entryField.text()
        blockInfo = [f"Block Number: {blockNumber}"]

        # Check possible errors in block entry value
        if blockNumber.isdigit() and blockNumber:
            if blockNumber:
                blockCheck = self.check_block_exist(blockNumber)
                if blockCheck:
                    # Enable checkboxes if block # entry is valid
                    for checkbox in self.blockInfoCheckboxes.values():
                        checkbox.setDisabled(False)

                    self.blockInfoDisplay.setPlainText("\n".join(blockInfo))
                    self.blockInfoDisplay.show()
                    self.errorLabel.clear()
                else:
                    # Disable checkboxes if block # entry is not valid
                    for checkbox in self.blockInfoCheckboxes.values():
                        checkbox.setDisabled(True)

                    self.blockInfoDisplay.clear()
                    self.blockInfoDisplay.hide()
                    self.errorLabel.setText(f"Block {blockNumber} not found.")
        else:
            # Disable checkboxes if block # entry is not valid
            for checkbox in self.blockInfoCheckboxes.values():
                checkbox.setDisabled(True)

            self.blockInfoDisplay.clear()
            self.blockInfoDisplay.hide()
            self.errorLabel.setText("Please enter a valid block number.")

        # Check for checkbox selection
        for info, checkbox in self.blockInfoCheckboxes.items():
            if checkbox.isChecked():
                if info == "Block Length":
                    for data in self.trackData:
                        if data["Block Number"] == int(blockNumber):
                            blockInfo.append(
                                f"Block Length: {data['Block Length (m)']} m"
                            )
                if info == "Speed Limit":
                    for data in self.trackData:
                        if data["Block Number"] == int(blockNumber):
                            blockInfo.append(
                                f"Speed Limit: {data['Speed Limit (Km/Hr)']} Km/Hr"
                            )
                if info == "Elevation":
                    for data in self.trackData:
                        if data["Block Number"] == int(blockNumber):
                            blockInfo.append(f"Elevation: {data['ELEVATION (M)']} m")
                if info == "Cumulative Elevation":
                    for data in self.trackData:
                        if data["Block Number"] == int(blockNumber):
                            blockInfo.append(
                                f"Cumulative Elevation: {data['CUMALTIVE ELEVATION (M)']} m"
                            )
                if info == "Block Grade":
                    for data in self.trackData:
                        if data["Block Number"] == int(blockNumber):
                            blockInfo.append(f"Block Grade: {data['Block Grade (%)']}%")
                if info == "Allowed Directions of Travel":
                    for data in self.trackData:
                        if data["Block Number"] == int(blockNumber):
                            blockInfo.append(
                                f"Allowed Directions of Travel: {self.allowableDirections}"
                            )
                if info == "Track Heater":
                    for data in self.trackData:
                        if data["Block Number"] == int(blockNumber):
                            blockInfo.append(f"Track Heater: {self.trackHeater}")
                if info == "Failures":
                    for data in self.trackData:
                        if data["Block Number"] == int(blockNumber):
                            blockInfo.append(f"Failures: {data['Failures']}")
                if info == "Beacon":
                    for data in self.trackData:
                        if data["Block Number"] == int(blockNumber):
                            blockInfo.append(f"Beacon: {self.beacon}\n")
        # Then append to display is info is selected
        self.blockInfoDisplay.setPlainText("\n".join(blockInfo))

    def check_block_exist(self, blockNumber):
        if self.trackData:
            for data in self.trackData:
                if data["Block Number"] == int(blockNumber):
                    return True
        return False

    def add_change_failures_button(self, parentWindow):
        self.changeFailuresButton = QPushButton("Change Failures ->", parentWindow)
        self.changeFailuresButton.setStyleSheet("background-color: red; color: white")
        buttonWidth = 200
        buttonHeight = 30
        buttonX = int(950 + (parentWindow.width() - 950 - buttonWidth) / 2)
        buttonY = parentWindow.height() - 50
        self.changeFailuresButton.setGeometry(
            buttonX, buttonY, buttonWidth, buttonHeight
        )
        self.changeFailuresButton.setEnabled(False)

        self.changeFailuresButton.clicked.connect(self.show_failure_popup)

    def add_tabbar(self, parentWindow):
        changeFailuresButton = QPushButton("Home", parentWindow)
        changeFailuresButton.setStyleSheet(
            "background-color: black; color: white; font-weight: bold; border: 2px solid white; border-bottom: none;"
        )
        changeFailuresButton.setGeometry(100, 70, 100, 30)

        testbenchTab = QPushButton("TestBench", parentWindow)
        testbenchTab.setStyleSheet(
            "background-color: black; color: white; font-weight: bold; border: 2px solid white; border-bottom: none;"
        )
        testbenchTab.setGeometry(200, 70, 100, 30)

        testbenchTab.clicked.connect(self.show_testbench)

    def show_failure_popup(self):
        failurePopup = FailureWindow()
        failurePopup.failureWindow.exec()

        selectedBlock = failurePopup.get_selected_block()
        self.failures = failurePopup.get_selected_failures()

        # Update the track_data with failures
        for block in self.trackData:
            if block["Block Number"] == selectedBlock:
                # Convert to a string for the use of the display, but kept a list privately
                failuresStr = ", ".join(self.failures)
                if self.failures == "None":
                    failuresStr = "None"
                block["Failures"] = failuresStr
        self.update_block_info_display

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
    selectionWindow = SelectionWindow()
